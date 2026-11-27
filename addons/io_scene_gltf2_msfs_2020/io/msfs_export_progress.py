# Copyright 2021-2022 The glTF-Blender-IO-MSFS-2020 authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Progress reporting for the MSFS 2020 multi-export.

The glTF exporter itself is one long, blocking operator.  The multi-export
operator therefore exports one file per timer tick and this module reports the
overall progress:

* a native progress bar in the status bar (``wm.progress_*``),
* a line of status text next to it, and
* a small heads-up display in the 3D viewport.

The HUD is drawn from a ``SpaceView3D`` draw handler, so it does not need a
popup/dialog and cannot leave a window behind if the export is interrupted.
"""

import time

import bpy


FONT_ID = 0

# Panel geometry, in unscaled Blender UI units.
_PANEL_WIDTH = 440.0
_PANEL_PAD = 14.0
_PANEL_ROW = 18.0
_PANEL_BAR_HEIGHT = 7.0

# Reporters with a live draw handler, so the add-on can be unloaded safely.
_ACTIVE_REPORTERS = set()


def format_duration(seconds):
    """Format a duration as ``mm:ss`` (or ``h:mm:ss``) for the HUD."""

    if seconds is None:
        return "--:--"

    seconds = max(0, int(round(float(seconds))))
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)

    if hours:
        return "{:d}:{:02d}:{:02d}".format(hours, minutes, secs)
    return "{:02d}:{:02d}".format(minutes, secs)


def hud_bounds(region_width, region_height, ui_scale):
    """Return ``(x, y, width, height)`` of the HUD in region pixels.

    The panel is centred in the 3D viewport rather than pinned under the
    header.  Keep the geometry here so the draw callback and any hit-testing
    cannot drift apart.
    """

    width = _PANEL_WIDTH * ui_scale
    pad = _PANEL_PAD * ui_scale
    row = _PANEL_ROW * ui_scale
    bar_height = _PANEL_BAR_HEIGHT * ui_scale

    panel_height = pad * 2.0 + row * 6.0 + bar_height + 8.0 * ui_scale
    x = max(16.0 * ui_scale, (region_width - width) * 0.5)
    y = max(16.0 * ui_scale, (region_height - panel_height) * 0.5)
    return x, y, width, panel_height


class MSFS2020_ExportProgress:
    """Track and display the progress of one multi-export run.

    One instance lives for the whole run.  ``begin_job`` / ``end_job`` are
    called around every exported file; ``show_complete`` and ``close`` finish
    the display.  All methods must be called from Blender's main thread.
    """

    def __init__(self, context, total, title="MSFS 2020 Multi-Export", use_overlay=True):
        self.wm = getattr(context, "window_manager", None)
        self.workspace = getattr(context, "workspace", None)

        self.total = max(1, int(total))
        self.done = 0
        self.title = title

        self.current_label = ""
        self.current_group = ""
        self.job_running = False

        self.start_time = time.monotonic()
        self.job_start = None
        self.job_elapsed_total = 0.0
        self.final_duration = 0.0
        self.error_count = 0

        self.state = "running"
        self._wm_progress = False
        self._draw_handle = None
        self._closed = False

        _ACTIVE_REPORTERS.add(self)

        self._begin_native_progress()

        if use_overlay and not bpy.app.background:
            try:
                self._draw_handle = bpy.types.SpaceView3D.draw_handler_add(
                    _draw_export_hud, (self,), "WINDOW", "POST_PIXEL"
                )
            except Exception as exc:  # pragma: no cover - depends on the GPU backend
                print("[MSFS export] viewport progress overlay unavailable: {}".format(exc))
                self._draw_handle = None

        self._update_status()
        self.tag_redraw()

    # ------------------------------------------------------------------
    # Native progress bar and status text
    # ------------------------------------------------------------------

    def _begin_native_progress(self):
        if self.wm is None:
            return
        try:
            self.wm.progress_begin(0, self.total)
            self.wm.progress_update(0)
            self._wm_progress = True
        except Exception:
            self._wm_progress = False

    def _update_native_progress(self):
        if self.wm is None or not self._wm_progress:
            return
        try:
            self.wm.progress_update(self.done)
        except Exception:
            self._wm_progress = False

    def _end_native_progress(self):
        if self.wm is None or not self._wm_progress:
            return
        try:
            self.wm.progress_end()
        except Exception:
            pass
        self._wm_progress = False

    def _status_text(self):
        if self.state == "running":
            current = self.current_label or "preparing"
            number = self.done + 1 if self.job_running else max(1, self.done)
            return "MSFS export {}/{}: {}".format(
                min(number, self.total), self.total, current
            )
        if self.state == "complete":
            if self.error_count:
                return "MSFS export finished with {} error(s) in {}".format(
                    self.error_count, format_duration(self.final_duration)
                )
            return "MSFS export complete: {} file(s) in {}".format(
                self.total, format_duration(self.final_duration)
            )
        if self.state == "cancelled":
            return "MSFS export cancelled after {}/{} file(s)".format(
                self.done, self.total
            )
        return "MSFS export"

    def _update_status(self):
        if self.workspace is None:
            return
        try:
            self.workspace.status_text_set(self._status_text())
        except Exception:
            pass

    def _clear_status(self):
        if self.workspace is None:
            return
        try:
            self.workspace.status_text_set(None)
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Redraw
    # ------------------------------------------------------------------

    def tag_redraw(self):
        """Ask every window to redraw; safe to call from a modal timer."""

        try:
            wm = bpy.context.window_manager
            for window in wm.windows:
                screen = window.screen
                if screen is None:
                    continue
                for area in screen.areas:
                    area.tag_redraw()
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Job lifecycle
    # ------------------------------------------------------------------

    def begin_job(self, label="", group=""):
        self.current_label = label or ""
        self.current_group = group or ""
        self.job_running = True
        self.job_start = time.monotonic()
        self.state = "running"
        self._update_status()
        self._update_native_progress()
        self.tag_redraw()

    def end_job(self, success=True):
        self.job_running = False
        now = time.monotonic()
        if self.job_start is not None:
            self.job_elapsed_total += max(0.0, now - self.job_start)
            self.job_start = None

        if not success:
            self.error_count += 1

        self.done = min(self.total, self.done + 1)
        self._update_native_progress()
        self._update_status()
        self.tag_redraw()

    def show_complete(self, error_count=0):
        self.error_count = error_count
        self.job_running = False
        self.state = "complete"
        self.done = self.total
        self.final_duration = time.monotonic() - self.start_time
        self.current_label = ""
        self.current_group = ""
        self._update_native_progress()
        self._end_native_progress()
        self._update_status()
        self.tag_redraw()

    def show_cancelled(self):
        self.job_running = False
        self.state = "cancelled"
        self.final_duration = time.monotonic() - self.start_time
        self.current_label = ""
        self.current_group = ""
        self._end_native_progress()
        self._update_status()
        self.tag_redraw()

    def close(self):
        if self._closed:
            return
        self._closed = True
        _ACTIVE_REPORTERS.discard(self)

        if self._draw_handle is not None:
            try:
                bpy.types.SpaceView3D.draw_handler_remove(self._draw_handle, "WINDOW")
            except Exception:
                pass
            self._draw_handle = None

        self._end_native_progress()
        self._clear_status()
        self.tag_redraw()

    # ------------------------------------------------------------------
    # Values used by the HUD
    # ------------------------------------------------------------------

    @property
    def elapsed(self):
        if self.state in {"complete", "cancelled"}:
            return self.final_duration
        return time.monotonic() - self.start_time

    @property
    def eta(self):
        if self.state != "running" or self.done <= 0:
            return None
        average = self.job_elapsed_total / float(self.done)
        return max(0.0, average * (self.total - self.done))

    @property
    def percent(self):
        if self.state == "complete":
            return 100.0
        return min(100.0, (self.done / float(self.total)) * 100.0)

    @property
    def accent_color(self):
        if self.state == "complete":
            if self.error_count:
                return (0.95, 0.62, 0.20, 1.0)
            return (0.28, 0.78, 0.38, 1.0)
        if self.state == "cancelled":
            return (0.90, 0.62, 0.25, 1.0)
        return (0.25, 0.56, 1.00, 1.0)


# ----------------------------------------------------------------------
# Drawing
# ----------------------------------------------------------------------

def _draw_export_hud(progress):
    """Draw handler entry point; never let a draw error break the export."""

    try:
        _draw_export_hud_impl(progress)
    except Exception:
        pass


def _draw_export_hud_impl(progress):
    import blf

    context = bpy.context
    region = context.region
    if region is None:
        return

    ui = context.preferences.system.ui_scale
    width = _PANEL_WIDTH * ui
    pad = _PANEL_PAD * ui
    row = _PANEL_ROW * ui
    bar_height = _PANEL_BAR_HEIGHT * ui

    x, bottom, width, panel_height = hud_bounds(
        region.width, region.height, ui
    )
    top = bottom + panel_height

    # Panel: a one-pixel border, a dark body and a coloured accent strip.
    _draw_rect(x - 1.0, bottom - 1.0, width + 2.0, panel_height + 2.0, (1, 1, 1, 0.16))
    _draw_rect(x, bottom, width, panel_height, (0.020, 0.020, 0.020, 0.86))
    _draw_rect(x, top - 3.0 * ui, width, 3.0 * ui, progress.accent_color)

    text_x = x + pad
    text_width = width - pad * 2.0

    # Row 1: title.
    y = top - pad - 15.0 * ui
    _draw_text(text_x, y, 15.0 * ui, (1.0, 1.0, 1.0, 0.96), progress.title)

    # Row 2: file counter.
    y -= row
    if progress.state == "running":
        number = progress.done + 1 if progress.job_running else max(1, progress.done)
        status = "{} of {}  ·  {:.0f}%".format(
            min(number, progress.total), progress.total, progress.percent
        )
    elif progress.state == "cancelled":
        status = "Cancelled after {} of {}".format(progress.done, progress.total)
    elif progress.error_count:
        status = "Finished with {} error(s)  ·  {} of {}".format(
            progress.error_count, progress.done, progress.total
        )
    else:
        status = "Complete  ·  {} of {}".format(progress.done, progress.total)
    _draw_text(text_x, y, 12.5 * ui, (0.78, 0.82, 0.90, 1.0), status)

    # Row 3: current file.
    y -= row
    if progress.state == "running":
        file_line = progress.current_label or "Preparing…"
    elif progress.state == "cancelled":
        file_line = "Stopped — files already written were kept"
    elif progress.error_count:
        file_line = "See the System Console for details"
    else:
        file_line = "All files written"
    _draw_text(
        text_x,
        y,
        12.5 * ui,
        (1.0, 1.0, 1.0, 1.0),
        _fit_text(file_line, text_width, 12.5 * ui),
    )

    # Row 4: group / preset and final duration.
    y -= row
    if progress.state == "running":
        group_line = (
            "Group: {}".format(progress.current_group) if progress.current_group else ""
        )
    elif progress.state == "cancelled":
        group_line = "Cancelled"
    elif progress.error_count:
        group_line = "Finished with errors"
    else:
        group_line = "Finished"
    _draw_text(
        text_x,
        y,
        11.0 * ui,
        (0.62, 0.66, 0.72, 1.0),
        _fit_text(group_line, text_width, 11.0 * ui),
    )

    # Progress bar.
    y -= row - 2.0 * ui
    bar_x = text_x
    bar_y = y - bar_height
    bar_width = text_width
    _draw_rect(bar_x, bar_y, bar_width, bar_height, (1, 1, 1, 0.12))
    fill = bar_width * (progress.percent / 100.0)
    if fill > 0.0:
        _draw_rect(bar_x, bar_y, fill, bar_height, progress.accent_color)

    # Row 5: elapsed / remaining.
    y = bar_y - 12.0 * ui
    if progress.state == "running":
        if progress.eta is None:
            timing = "Elapsed {}  ·  estimating remaining…".format(
                format_duration(progress.elapsed)
            )
        else:
            timing = "Elapsed {}  ·  remaining ~{}".format(
                format_duration(progress.elapsed), format_duration(progress.eta)
            )
    elif progress.state == "cancelled":
        timing = "Elapsed {}".format(format_duration(progress.final_duration))
    else:
        timing = "Total {}".format(format_duration(progress.final_duration))
    _draw_text(text_x, y, 11.0 * ui, (0.72, 0.75, 0.80, 1.0), timing)

    # Row 6: hint.
    y -= row
    if progress.state == "running":
        hint = "Esc — cancel (stops after the current file)"
    elif progress.state == "cancelled":
        hint = "Stopped"
    elif progress.error_count:
        hint = "Click anywhere or press Esc to dismiss"
    else:
        hint = "You can keep working"
    _draw_text(text_x, y, 11.0 * ui, (0.55, 0.58, 0.63, 1.0), hint)

    # Leave the font in a sensible state for any other draw callbacks.
    blf.size(FONT_ID, 11.0)
    blf.color(FONT_ID, 1.0, 1.0, 1.0, 1.0)


def _draw_rect(x, y, width, height, color):
    if width <= 0.0 or height <= 0.0:
        return

    import gpu
    from gpu_extras.batch import batch_for_shader

    shader = gpu.shader.from_builtin("UNIFORM_COLOR")
    vertices = (
        (x, y),
        (x + width, y),
        (x + width, y + height),
        (x, y),
        (x + width, y + height),
        (x, y + height),
    )
    batch = batch_for_shader(shader, "TRIS", {"pos": vertices})

    gpu.state.blend_set("ALPHA")
    try:
        shader.bind()
        shader.uniform_float("color", color)
        batch.draw(shader)
    finally:
        gpu.state.blend_set("NONE")


def _draw_text(x, y, size, color, text):
    if not text:
        return

    import blf

    blf.size(FONT_ID, size)
    # A cheap shadow keeps the text readable over bright viewport content.
    blf.color(FONT_ID, 0.0, 0.0, 0.0, 0.85 * color[3])
    blf.position(FONT_ID, x + 1.0, y - 1.0, 0)
    blf.draw(FONT_ID, text)

    blf.color(FONT_ID, *color)
    blf.position(FONT_ID, x, y, 0)
    blf.draw(FONT_ID, text)


def _fit_text(text, max_width, size):
    if not text:
        return text

    import blf

    blf.size(FONT_ID, size)
    if blf.dimensions(FONT_ID, text)[0] <= max_width:
        return text

    suffix = "…"
    shortened = text
    while shortened and blf.dimensions(FONT_ID, shortened + suffix)[0] > max_width:
        shortened = shortened[:-1]
    return (shortened + suffix) if shortened else suffix


def unregister():
    """Close any HUD left behind if the add-on is disabled mid-export."""

    for reporter in list(_ACTIVE_REPORTERS):
        try:
            reporter.close()
        except Exception:
            pass
