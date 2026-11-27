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

import os
import time
import traceback
import uuid
import xml.dom.minidom
import xml.etree.ElementTree as etree

import bpy

from .msfs_export_progress import MSFS2020_ExportProgress, format_duration


def export_blender_under_3_3(file_path, settings):
    return bpy.ops.export_scene.gltf(
        filepath=file_path,
        check_existing=True,
        export_format="GLTF_SEPARATE",
        export_copyright=settings.export_copyright,
        export_image_format=(
            "AUTO" if settings.enable_msfs_extension else settings.export_image_format
        ),
        export_texture_dir=settings.export_texture_dir,
        export_keep_originals=settings.export_keep_originals,
        export_texcoords=settings.export_texcoords,
        export_normals=settings.export_normals,
        export_draco_mesh_compression_enable=settings.export_draco_mesh_compression_enable,
        export_draco_mesh_compression_level=settings.export_draco_mesh_compression_level,
        export_draco_position_quantization=settings.export_draco_position_quantization,
        export_draco_normal_quantization=settings.export_draco_normal_quantization,
        export_draco_texcoord_quantization=settings.export_draco_texcoord_quantization,
        export_draco_color_quantization=settings.export_draco_color_quantization,
        export_draco_generic_quantization=settings.export_draco_generic_quantization,
        export_tangents=settings.export_tangents,
        export_materials=settings.export_materials,
        export_colors=settings.export_colors,
        use_mesh_edges=settings.use_mesh_edges,
        use_mesh_vertices=settings.use_mesh_vertices,
        export_cameras=settings.export_cameras,
        use_selection=settings.use_selection,
        use_visible=settings.use_visible,
        use_renderable=False,
        use_active_collection=True,
        export_yup=settings.export_yup,
        export_apply=settings.export_apply,
        export_animations=settings.export_animations,
        export_frame_range=settings.export_frame_range,
        export_frame_step=settings.export_frame_step,
        export_force_sampling=settings.export_force_sampling,
        export_def_bones=settings.export_def_bones,
        optimize_animation_size=settings.export_optimize_animation_size,
        export_current_frame=settings.export_current_frame,
        export_skins=settings.export_skins,
        export_all_influences=settings.export_all_influences,
        export_morph=settings.export_morph,
        export_morph_normal=settings.export_morph_normal,
        export_morph_tangent=settings.export_morph_tangent,
        export_lights=settings.export_lights,
        will_save_settings=settings.will_save_settings,
        export_extras=(
            False if settings.enable_msfs_extension else settings.export_extras
        ),
    )


def export_blender_3_3(file_path, settings):
    return bpy.ops.export_scene.gltf(
        filepath=file_path,
        check_existing=True,
        export_format="GLTF_SEPARATE",
        export_copyright=settings.export_copyright,
        export_image_format=(
            "AUTO" if settings.enable_msfs_extension else settings.export_image_format
        ),
        export_texture_dir=settings.export_texture_dir,
        export_keep_originals=settings.export_keep_originals,
        export_texcoords=settings.export_texcoords,
        export_normals=settings.export_normals,
        export_draco_mesh_compression_enable=settings.export_draco_mesh_compression_enable,
        export_draco_mesh_compression_level=settings.export_draco_mesh_compression_level,
        export_draco_position_quantization=settings.export_draco_position_quantization,
        export_draco_normal_quantization=settings.export_draco_normal_quantization,
        export_draco_texcoord_quantization=settings.export_draco_texcoord_quantization,
        export_draco_color_quantization=settings.export_draco_color_quantization,
        export_draco_generic_quantization=settings.export_draco_generic_quantization,
        export_tangents=settings.export_tangents,
        export_materials=settings.export_materials,
        export_original_specular=False,
        export_colors=settings.export_colors,
        use_mesh_edges=settings.use_mesh_edges,
        use_mesh_vertices=settings.use_mesh_vertices,
        export_cameras=settings.export_cameras,
        use_selection=settings.use_selection,
        use_visible=settings.use_visible,
        use_renderable=False,
        use_active_collection=False,
        use_active_scene=True,
        export_yup=settings.export_yup,
        export_apply=settings.export_apply,
        export_animations=settings.export_animations,
        export_frame_range=settings.export_frame_range,
        export_frame_step=settings.export_frame_step,
        export_force_sampling=settings.export_force_sampling,
        export_nla_strips_merged_animation_name=settings.export_nla_strips_merged_animation_name,
        export_def_bones=settings.export_def_bones,
        export_optimize_animation_size=settings.export_optimize_animation_size,
        export_anim_single_armature=settings.export_anim_single_armature,
        export_current_frame=settings.export_current_frame,
        export_skins=settings.export_skins,
        export_all_influences=settings.export_all_influences,
        export_morph=settings.export_morph,
        export_morph_normal=settings.export_morph_normal,
        export_morph_tangent=settings.export_morph_tangent,
        export_lights=settings.export_lights,
        will_save_settings=settings.will_save_settings,
        export_extras=(
            False if settings.enable_msfs_extension else settings.export_extras
        ),
    )


def export_blender_3_6(file_path, settings):
    return bpy.ops.export_scene.gltf(
        filepath=file_path,
        check_existing=True,
        export_format="GLTF_SEPARATE",
        export_copyright=settings.export_copyright,
        export_image_format=(
            "AUTO" if settings.enable_msfs_extension else settings.export_image_format
        ),
        export_jpeg_quality=(
            75 if settings.enable_msfs_extension else settings.export_jpeg_quality
        ),
        export_texture_dir=settings.export_texture_dir,
        export_keep_originals=settings.export_keep_originals,
        export_texcoords=settings.export_texcoords,
        export_normals=settings.export_normals,
        export_draco_mesh_compression_enable=settings.export_draco_mesh_compression_enable,
        export_draco_mesh_compression_level=settings.export_draco_mesh_compression_level,
        export_draco_position_quantization=settings.export_draco_position_quantization,
        export_draco_normal_quantization=settings.export_draco_normal_quantization,
        export_draco_texcoord_quantization=settings.export_draco_texcoord_quantization,
        export_draco_color_quantization=settings.export_draco_color_quantization,
        export_draco_generic_quantization=settings.export_draco_generic_quantization,
        export_tangents=settings.export_tangents,
        export_materials=settings.export_materials,
        export_original_specular=False,
        export_colors=settings.export_colors,
        export_attributes=settings.export_attributes,
        use_mesh_edges=settings.use_mesh_edges,
        use_mesh_vertices=settings.use_mesh_vertices,
        export_cameras=settings.export_cameras,
        use_selection=settings.use_selection,
        use_visible=settings.use_visible,
        use_renderable=False,
        use_active_collection=False,
        use_active_scene=True,
        export_yup=settings.export_yup,
        export_apply=settings.export_apply,
        export_animations=settings.export_animations,
        export_frame_range=settings.export_frame_range,
        export_frame_step=settings.export_frame_step,
        export_force_sampling=settings.export_force_sampling,
        export_animation_mode=settings.export_animation_mode,
        export_def_bones=settings.export_def_bones,
        export_optimize_animation_size=settings.export_optimize_animation_size,
        export_optimize_animation_keep_anim_armature=settings.export_optimize_animation_keep_anim_armature,
        export_optimize_animation_keep_anim_object=settings.export_optimize_animation_keep_anim_object,
        export_negative_frame=settings.export_negative_frame,
        export_anim_slide_to_zero=settings.export_anim_slide_to_zero,
        export_reset_pose_bones=settings.export_reset_pose_bones,
        export_bake_animation=settings.export_bake_animation,
        export_anim_single_armature=settings.export_anim_single_armature,
        export_current_frame=settings.export_current_frame,
        export_rest_position_armature=settings.export_rest_position_armature,
        export_anim_scene_split_object=settings.export_anim_scene_split_object,
        export_skins=settings.export_skins,
        export_all_influences=settings.export_all_influences,
        export_morph=settings.export_morph,
        export_morph_normal=settings.export_morph_normal,
        export_morph_tangent=settings.export_morph_tangent,
        export_morph_animation=settings.export_morph_animation,
        export_lights=settings.export_lights,
        will_save_settings=settings.will_save_settings,
        export_extras=(
            False if settings.enable_msfs_extension else settings.export_extras
        ),
    )


def export_blender_4_2(file_path, settings):
    return bpy.ops.export_scene.gltf(
        filepath=file_path,
        check_existing=True,
        export_format="GLTF_SEPARATE",
        export_copyright=settings.export_copyright,
        export_image_format=(
            "AUTO" if settings.enable_msfs_extension else settings.export_image_format
        ),
        export_jpeg_quality=(
            75 if settings.enable_msfs_extension else settings.export_jpeg_quality
        ),
        export_texture_dir=settings.export_texture_dir,
        export_keep_originals=settings.export_keep_originals,
        export_texcoords=settings.export_texcoords,
        export_normals=settings.export_normals,
        export_draco_mesh_compression_enable=settings.export_draco_mesh_compression_enable,
        export_draco_mesh_compression_level=settings.export_draco_mesh_compression_level,
        export_draco_position_quantization=settings.export_draco_position_quantization,
        export_draco_normal_quantization=settings.export_draco_normal_quantization,
        export_draco_texcoord_quantization=settings.export_draco_texcoord_quantization,
        export_draco_color_quantization=settings.export_draco_color_quantization,
        export_draco_generic_quantization=settings.export_draco_generic_quantization,
        export_tangents=settings.export_tangents,
        export_materials=settings.export_materials,
        export_original_specular=False,
        export_attributes=settings.export_attributes,
        use_mesh_edges=settings.use_mesh_edges,
        use_mesh_vertices=settings.use_mesh_vertices,
        export_cameras=settings.export_cameras,
        use_selection=settings.use_selection,
        use_visible=settings.use_visible,
        use_renderable=False,
        use_active_collection=False,
        use_active_scene=True,
        export_yup=settings.export_yup,
        export_apply=settings.export_apply,
        export_animations=settings.export_animations,
        export_frame_range=settings.export_frame_range,
        export_frame_step=settings.export_frame_step,
        export_force_sampling=settings.export_force_sampling,
        export_animation_mode=settings.export_animation_mode,
        export_def_bones=settings.export_def_bones,
        export_optimize_animation_size=settings.export_optimize_animation_size,
        export_optimize_animation_keep_anim_armature=settings.export_optimize_animation_keep_anim_armature,
        export_optimize_animation_keep_anim_object=settings.export_optimize_animation_keep_anim_object,
        export_negative_frame=settings.export_negative_frame,
        export_anim_slide_to_zero=settings.export_anim_slide_to_zero,
        export_reset_pose_bones=settings.export_reset_pose_bones,
        export_bake_animation=settings.export_bake_animation,
        export_anim_single_armature=settings.export_anim_single_armature,
        export_current_frame=settings.export_current_frame,
        export_rest_position_armature=settings.export_rest_position_armature,
        export_anim_scene_split_object=settings.export_anim_scene_split_object,
        export_skins=settings.export_skins,
        export_all_influences=(
            False if settings.enable_msfs_extension else settings.export_all_influences
        ),
        export_morph=settings.export_morph,
        export_morph_normal=settings.export_morph_normal,
        export_morph_tangent=settings.export_morph_tangent,
        export_morph_animation=settings.export_morph_animation,
        export_lights=settings.export_lights,
        will_save_settings=settings.will_save_settings,
        export_extras=(
            False if settings.enable_msfs_extension else settings.export_extras
        ),
        export_gn_mesh=(
            False if settings.enable_msfs_extension else settings.export_gn_mesh
        ),
        export_gpu_instances=(
            False if settings.enable_msfs_extension else settings.export_gpu_instances
        ),
        export_hierarchy_flatten_objs=(
            False
            if settings.enable_msfs_extension
            else settings.export_hierarchy_flatten_objs
        ),
        export_hierarchy_full_collections=(
            False
            if settings.enable_msfs_extension
            else settings.export_hierarchy_full_collections
        ),
        export_vertex_color=settings.export_vertex_color,
        export_all_vertex_colors=settings.export_all_vertex_colors,
        export_active_vertex_color_when_no_material=settings.export_active_vertex_color_when_no_material,
        export_image_add_webp=(
            False if settings.enable_msfs_extension else settings.export_image_add_webp
        ),
        export_image_webp_fallback=(
            False
            if settings.enable_msfs_extension
            else settings.export_image_webp_fallback
        ),
        export_unused_images=(
            False if settings.enable_msfs_extension else settings.export_unused_images
        ),
        export_unused_textures=(
            False if settings.enable_msfs_extension else settings.export_unused_textures
        ),
        export_try_sparse_sk=(
            False if settings.enable_msfs_extension else settings.export_try_sparse_sk
        ),
        export_try_omit_sparse_sk=(
            False
            if settings.enable_msfs_extension
            else settings.export_try_omit_sparse_sk
        ),
        export_armature_object_remove=settings.export_armature_object_remove,
        export_influence_nb=settings.export_influence_nb,
        export_import_convert_lighting_mode=(
            "SPEC"
            if settings.enable_msfs_extension
            else settings.export_import_convert_lighting_mode
        ),
        export_optimize_disable_viewport=settings.export_optimize_disable_viewport,
    )


# region Multi-export jobs

_MULTI_EXPORT_ACTIVE = False
_MULTI_EXPORT_ACTIVE_OPERATOR = None


class _MSFS2020_ExportJob:
    """One glTF file to export, with a pre-computed selection.

    The selection is captured when the export starts so that the modal step
    cannot be affected by a mouse click or a mode change between files.
    """

    __slots__ = ("path", "label", "group", "objects")

    def __init__(self, path, label, group, objects):
        self.path = path
        self.label = label
        self.group = group
        self.objects = objects

    def select(self, context):
        for obj in list(context.selected_objects):
            try:
                obj.select_set(False)
            except (ReferenceError, RuntimeError):
                pass

        for obj in self.objects:
            try:
                obj.select_set(True)
            except (ReferenceError, RuntimeError):
                pass


def _view_layer_objects(context):
    """Objects in the active view layer, with a background-mode fallback."""

    try:
        window = context.window
        if window is not None:
            return list(window.view_layer.objects)
    except Exception:
        pass

    try:
        return list(context.scene.objects)
    except Exception:
        return []


def _recursive_objects(obj, view_layer_objects, result=None):
    """Match the old ``select_recursive``: include children in the view layer."""

    if result is None:
        result = []

    if obj is None:
        return result

    if obj in view_layer_objects:
        result.append(obj)
        for child in obj.children:
            _recursive_objects(child, view_layer_objects, result)

    return result


def _lod_objects(context, lod, sort_by_collection):
    if sort_by_collection:
        collection = lod.collection
        if collection is None:
            return []
        try:
            return list(collection.all_objects)
        except ReferenceError:
            return []

    object_lod = lod.objectLOD
    if object_lod is None:
        return []
    return _recursive_objects(object_lod, _view_layer_objects(context))


def _is_lod_visible(context, lod, sort_by_collection):
    """LOD visibility with a fallback for background mode.

    ``MSFS2020_LODGroupUtility.lod_is_visible`` reads
    ``bpy.context.window.view_layer``; ``bpy.context.window`` is ``None`` in
    ``blender --background``, so the utility raises there.  Background exports
    only need the existence / hide checks, which are repeated here.
    """

    from .msfs_multi_export_objects import MSFS2020_LODGroupUtility

    try:
        return MSFS2020_LODGroupUtility.lod_is_visible(context, lod)
    except Exception:
        pass

    scene = context.scene
    show_hidden = scene.multi_exporter_show_hidden_objects

    if sort_by_collection:
        collection = lod.collection
        if collection is None or collection.name not in bpy.data.collections:
            return False
        if show_hidden:
            return True
        try:
            return not collection.hide_get()
        except Exception:
            return True

    object_lod = lod.objectLOD
    if object_lod is None or object_lod.name not in scene.objects:
        return False
    if show_hidden:
        return True
    try:
        return not object_lod.hide_get()
    except Exception:
        return True


def _generate_lod_xml(lod_group, export_folder_path, is_visible):
    """Write the ModelInfo XML for a LOD group.

    The body is unchanged from the original exporter; only the visibility
    check is passed in so this helper does not need a Blender context.
    """

    xml_path = os.path.join(export_folder_path, lod_group.group_name + ".xml")
    found_guid = None

    if os.path.exists(xml_path):
        tree = etree.parse(xml_path)
        found_guid = tree.getroot().attrib.get("guid")

    if lod_group.overwrite_guid or found_guid is None:
        root = etree.Element(
            "ModelInfo",
            guid="{" + str(uuid.uuid4()) + "}",
            version="1.1",
        )
    else:
        root = etree.Element("ModelInfo", guid=found_guid, version="1.1")

    lods = etree.SubElement(root, "LODS")

    lod_files = {}
    for lod in lod_group.lods:
        if not is_visible(lod):
            continue
        if lod.enabled:
            lod_files[lod.file_name] = lod.lod_value

    lod_files = sorted(lod_files.items())
    last_lod = list(lod_files)[-1:]

    for file_name, lod_value in lod_files:
        lod_element = etree.SubElement(lods, "LOD")

        if file_name != last_lod[0]:
            lod_element.set("minSize", str(lod_value))

        lod_element.set("ModelFile", os.path.splitext(file_name)[0] + ".gltf")

    if lod_files:
        dom = xml.dom.minidom.parseString(etree.tostring(root))
        xml_string = dom.toprettyxml(encoding="utf-8")

        with open(xml_path, "wb") as f:
            f.write(xml_string)


def build_export_jobs(context):
    """Build the list of files the current Multi-Export tab would write.

    Returns ``(jobs, errors)``.  ``errors`` are user-facing strings for
    entries that cannot be exported; valid jobs are still returned so one bad
    group does not stop the whole export.
    """

    jobs = []
    errors = []
    scene = context.scene
    tab = scene.msfs_multi_exporter_current_tab

    if tab == "OBJECTS":
        sort_by_collection = scene.multi_exporter_grouped_by_collections

        def is_visible(lod):
            return _is_lod_visible(context, lod, sort_by_collection)

        for lod_group in scene.msfs_multi_exporter_lod_groups:
            export_folder_path = lod_group.folder_path
            if export_folder_path == "//\\":
                export_folder_path = export_folder_path.rsplit("\\")[0]
            export_folder_path = bpy.path.abspath(export_folder_path)

            if lod_group.generate_xml:
                try:
                    _generate_lod_xml(lod_group, export_folder_path, is_visible)
                except Exception as exc:
                    traceback.print_exc()
                    errors.append(
                        "[EXPORT][ERROR] XML : {} could not be written: {}".format(
                            lod_group.group_name, exc
                        )
                    )

            for lod in lod_group.lods:
                if not is_visible(lod) or not lod.enabled:
                    continue

                if export_folder_path == "":
                    errors.append(
                        "[EXPORT][ERROR] Object : "
                        + lod.file_name
                        + " does not have an export path set."
                    )
                    continue

                export_path = bpy.path.ensure_ext(
                    os.path.join(
                        export_folder_path,
                        os.path.splitext(lod.file_name)[0],
                    ),
                    ".gltf",
                )

                try:
                    objects = _lod_objects(context, lod, sort_by_collection)
                except Exception as exc:
                    traceback.print_exc()
                    errors.append(
                        "[EXPORT][ERROR] Object : {} could not be selected: {}".format(
                            lod.file_name, exc
                        )
                    )
                    objects = []

                jobs.append(
                    _MSFS2020_ExportJob(
                        path=export_path,
                        label=os.path.basename(export_path),
                        group=lod_group.group_name,
                        objects=objects,
                    )
                )

    elif tab == "PRESETS":
        view_layer_objects = _view_layer_objects(context)

        for preset in scene.msfs_multi_exporter_presets:
            if not preset.enabled:
                continue

            if preset.folder_path == "":
                errors.append(
                    "[EXPORT][ERROR] Preset : "
                    + preset.name
                    + " does not have an export path set."
                )
                continue

            export_folder_path = preset.folder_path
            if export_folder_path == "//\\":
                export_folder_path = export_folder_path.rsplit("\\")[0]
            export_folder_path = bpy.path.abspath(export_folder_path)

            export_path = bpy.path.ensure_ext(
                os.path.join(export_folder_path, preset.name), ".gltf"
            )

            objects = []
            seen = set()
            for layer in preset.layers:
                if not layer.enabled or layer.collection is None:
                    continue
                try:
                    candidates = layer.collection.all_objects
                except ReferenceError:
                    continue

                for obj in candidates:
                    if obj in view_layer_objects and obj not in seen:
                        seen.add(obj)
                        objects.append(obj)

            jobs.append(
                _MSFS2020_ExportJob(
                    path=export_path,
                    label=os.path.basename(export_path),
                    group=preset.name,
                    objects=objects,
                )
            )

    return jobs, errors


# endregion


# Operators
class MSFS2020_OT_MultiExportGLTF2(bpy.types.Operator):
    bl_idname = "export_scene.multi_export_gltf"
    bl_label = "Multi-Export glTF 2.0"
    bl_description = (
        "Export every enabled LOD group / preset. "
        "Progress is shown in the viewport and the status bar"
    )
    bl_options = {"REGISTER"}

    _timer = None
    _reporter = None
    _jobs = None
    _errors = None
    _index = 0
    _pending_job = None
    _finish_at = None
    _cancelled = False

    @staticmethod
    def export(file_path):
        settings = bpy.context.scene.msfs_multi_exporter_settings
        bpy.context.scene.msfs_exporter_settings.use_unique_id = settings.use_unique_id

        if bpy.app.version < (3, 3, 0):
            result = export_blender_under_3_3(file_path, settings)
        elif bpy.app.version < (3, 6, 0):
            result = export_blender_3_3(file_path, settings)
        elif bpy.app.version < (4, 2, 0):
            result = export_blender_3_6(file_path, settings)
        else:
            result = export_blender_4_2(file_path, settings)

        if not result or "FINISHED" not in result:
            raise RuntimeError("glTF exporter returned {!r}".format(result))

    # ------------------------------------------------------------------
    # Reporting helpers
    # ------------------------------------------------------------------

    def _report_errors(self, errors):
        for message in errors:
            print("[MSFS export] {}".format(message))
            self.report({"ERROR"}, message)

    def _report_summary(self, reporter, error_count):
        duration = format_duration(reporter.final_duration)

        if error_count:
            self.report(
                {"ERROR"},
                "MSFS export finished with {} error(s) in {}. "
                "See the System Console for details.".format(error_count, duration),
            )
        else:
            self.report(
                {"INFO"},
                "MSFS export complete: {} file(s) in {}.".format(
                    reporter.total, duration
                ),
            )

    def _run_job(self, context, job):
        try:
            job.select(context)
            MSFS2020_OT_MultiExportGLTF2.export(job.path)
            return True, ""
        except Exception as exc:
            traceback.print_exc()
            return False, "{}: {}".format(job.label, exc)

    # ------------------------------------------------------------------
    # Operator lifecycle
    # ------------------------------------------------------------------

    def invoke(self, context, event):
        global _MULTI_EXPORT_ACTIVE, _MULTI_EXPORT_ACTIVE_OPERATOR

        # Scripts and background mode have no window to drive a modal timer.
        if bpy.app.background:
            return self.execute(context)

        if _MULTI_EXPORT_ACTIVE:
            active = _MULTI_EXPORT_ACTIVE_OPERATOR
            if active is not None and active._finish_at is not None:
                self.report(
                    {"WARNING"},
                    "Dismiss the previous export report (Esc or click anywhere) "
                    "before exporting again.",
                )
            else:
                self.report({"WARNING"}, "An MSFS export is already running.")
            return {"CANCELLED"}

        _MULTI_EXPORT_ACTIVE = True
        _MULTI_EXPORT_ACTIVE_OPERATOR = self

        try:
            jobs, errors = build_export_jobs(context)
        except Exception as exc:
            _MULTI_EXPORT_ACTIVE = False
            _MULTI_EXPORT_ACTIVE_OPERATOR = None
            traceback.print_exc()
            self.report({"ERROR"}, "MSFS export setup failed: {}".format(exc))
            return {"CANCELLED"}

        self._report_errors(errors)

        if not jobs:
            _MULTI_EXPORT_ACTIVE = False
            _MULTI_EXPORT_ACTIVE_OPERATOR = None
            if not errors:
                self.report(
                    {"WARNING"},
                    "Nothing to export. Enable at least one LOD group or preset.",
                )
            return {"CANCELLED"}

        return self._begin_modal(context, jobs, errors)

    def _begin_modal(self, context, jobs, errors):
        global _MULTI_EXPORT_ACTIVE, _MULTI_EXPORT_ACTIVE_OPERATOR

        self._jobs = jobs
        self._errors = list(errors)
        self._index = 0
        self._pending_job = None
        self._finish_at = None
        self._cancelled = False
        self._timer = None
        self._reporter = None

        try:
            self._reporter = MSFS2020_ExportProgress(
                context, len(jobs), "MSFS 2020 Multi-Export"
            )
            self._timer = context.window_manager.event_timer_add(
                0.05, window=context.window
            )
            context.window_manager.modal_handler_add(self)
        except Exception:
            _MULTI_EXPORT_ACTIVE = False
            if _MULTI_EXPORT_ACTIVE_OPERATOR is self:
                _MULTI_EXPORT_ACTIVE_OPERATOR = None
            if self._reporter is not None:
                self._reporter.close()
                self._reporter = None
            raise

        return {"RUNNING_MODAL"}

    def _finish_run(self, reporter):
        """Switch to the final HUD state and report the result once."""

        if self._finish_at is not None:
            return

        error_count = len(self._errors or [])
        reporter.show_complete(error_count)

        # A successful run closes itself after a moment.  A run with errors
        # stays up until the user dismisses it (Esc or a click), so nobody can
        # miss the report.
        if error_count:
            self._finish_at = float("inf")
        else:
            self._finish_at = time.monotonic() + 1.2

        self._report_summary(reporter, error_count)

    def modal(self, context, event):
        if (
            event.type == "LEFTMOUSE"
            and event.value == "PRESS"
            and self._finish_at is not None
        ):
            self._cleanup(context)
            return {"CANCELLED"} if self._cancelled else {"FINISHED"}

        if event.type == "ESC":
            # Pressing Esc during a short final hold (complete or cancelled)
            # just closes the HUD; it does not report a second time.
            if self._finish_at is not None:
                self._cleanup(context)
                return {"CANCELLED"} if self._cancelled else {"FINISHED"}

            reporter = self._reporter
            if reporter is None:
                self._cleanup(context)
                return {"CANCELLED"}

            self.report(
                {"WARNING"},
                "MSFS export cancelled after {} of {} file(s).".format(
                    self._index, len(self._jobs or [])
                ),
            )
            self._cancelled = True
            reporter.show_cancelled()
            self._finish_at = time.monotonic() + 0.8
            return {"RUNNING_MODAL"}

        if event.type != "TIMER":
            return {"PASS_THROUGH"}

        reporter = self._reporter
        if reporter is None or self._jobs is None:
            self._cleanup(context)
            return {"CANCELLED"}

        # Let the HUD draw the cancelled state for a moment.
        if self._cancelled:
            if time.monotonic() >= self._finish_at:
                self._cleanup(context)
                return {"CANCELLED"}
            reporter.tag_redraw()
            return {"RUNNING_MODAL"}

        # Hold the "Complete" HUD for a moment so the final state is visible.
        if self._index >= len(self._jobs):
            self._finish_run(reporter)

            if time.monotonic() >= self._finish_at:
                self._cleanup(context)
                return {"FINISHED"}

            # A persistent error report is static, so do not keep forcing
            # viewport redraws while it waits for the user to dismiss it.
            if self._finish_at != float("inf"):
                reporter.tag_redraw()
            return {"RUNNING_MODAL"}

        # Give the HUD one timer tick to show the file that is about to
        # block the main thread, otherwise a long single-file export would
        # only ever display "Preparing...".
        if self._pending_job is None:
            job = self._jobs[self._index]
            reporter.begin_job(job.label, job.group)
            self._pending_job = job
            reporter.tag_redraw()
            return {"RUNNING_MODAL"}

        job = self._pending_job
        self._pending_job = None
        success, message = self._run_job(context, job)
        reporter.end_job(success)

        if not success:
            self._errors.append(message)
            self.report({"ERROR"}, message)

        self._index += 1

        # Show the 100% state immediately after the last file.
        if self._index >= len(self._jobs):
            self._finish_run(reporter)

        reporter.tag_redraw()
        return {"RUNNING_MODAL"}

    def cancel(self, context):
        self._cleanup(context)

    def _cleanup(self, context):
        global _MULTI_EXPORT_ACTIVE, _MULTI_EXPORT_ACTIVE_OPERATOR

        if self._timer is not None:
            try:
                context.window_manager.event_timer_remove(self._timer)
            except Exception:
                pass
            self._timer = None

        if self._reporter is not None:
            self._reporter.close()
            self._reporter = None

        self._jobs = None
        self._errors = None
        self._index = 0
        self._pending_job = None
        self._finish_at = None
        self._cancelled = False
        _MULTI_EXPORT_ACTIVE = False
        if _MULTI_EXPORT_ACTIVE_OPERATOR is self:
            _MULTI_EXPORT_ACTIVE_OPERATOR = None

    def execute(self, context):
        global _MULTI_EXPORT_ACTIVE, _MULTI_EXPORT_ACTIVE_OPERATOR

        if _MULTI_EXPORT_ACTIVE:
            self.report({"WARNING"}, "An MSFS export is already running.")
            return {"CANCELLED"}

        _MULTI_EXPORT_ACTIVE = True
        _MULTI_EXPORT_ACTIVE_OPERATOR = self

        try:
            try:
                jobs, errors = build_export_jobs(context)
            except Exception as exc:
                traceback.print_exc()
                self.report({"ERROR"}, "MSFS export setup failed: {}".format(exc))
                return {"CANCELLED"}

            self._report_errors(errors)

            if not jobs:
                if not errors:
                    self.report(
                        {"WARNING"},
                        "Nothing to export. Enable at least one LOD group or preset.",
                    )
                return {"CANCELLED"}

            reporter = MSFS2020_ExportProgress(
                context,
                len(jobs),
                "MSFS 2020 Multi-Export",
                use_overlay=False,
            )
            failures = 0

            try:
                for job in jobs:
                    reporter.begin_job(job.label, job.group)
                    success, message = self._run_job(context, job)
                    reporter.end_job(success)
                    if not success:
                        failures += 1
                        self.report({"ERROR"}, message)

                reporter.show_complete(failures)
                self._report_summary(reporter, failures)
            finally:
                reporter.close()

            return {"FINISHED"}
        finally:
            _MULTI_EXPORT_ACTIVE = False
            if _MULTI_EXPORT_ACTIVE_OPERATOR is self:
                _MULTI_EXPORT_ACTIVE_OPERATOR = None


class MSFS2020_OT_ChangeTab(bpy.types.Operator):
    bl_idname = "msfs2020.multi_export_change_tab"
    bl_label = "Change tab"

    current_tab: bpy.props.StringProperty()

    def execute(self, context):
        context.scene.msfs_multi_exporter_current_tab = self.current_tab
        return {"FINISHED"}


# Panels
class MSFS2020_PT_MultiExporter(bpy.types.Panel):
    bl_label = "Multi-Export glTF 2.0"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Micorosoft Flight Simulator 2020 Tools"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_exporter_settings

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        current_tab = context.scene.msfs_multi_exporter_current_tab

        row = layout.row(align=True)
        row.operator(
            MSFS2020_OT_ChangeTab.bl_idname,
            text="Objects",
            depress=(current_tab == "OBJECTS"),
        ).current_tab = "OBJECTS"
        row.operator(
            MSFS2020_OT_ChangeTab.bl_idname,
            text="Presets",
            depress=(current_tab == "PRESETS"),
        ).current_tab = "PRESETS"
        row.operator(
            MSFS2020_OT_ChangeTab.bl_idname,
            text="Settings",
            depress=(current_tab == "SETTINGS"),
        ).current_tab = "SETTINGS"


def register_panel():
    # Register the panel on demand, we need to be sure to only register it once
    # This is necessary because the panel is a child of the extensions panel,
    # which may not be registered when we try to register this extension
    try:
        bpy.utils.register_class(MSFS2020_PT_MultiExporter)
    except Exception:
        pass

    # If the glTF exporter is disabled, we need to unregister the extension panel
    # Just return a function to the exporter so it can unregister the panel
    return unregister_panel


def unregister_panel():
    try:
        bpy.utils.unregister_class(MSFS2020_PT_MultiExporter)
    except Exception:
        pass


def register():
    bpy.types.Scene.msfs_multi_exporter_current_tab = bpy.props.EnumProperty(
        items=(
            ("OBJECTS", "Objects", ""),
            ("PRESETS", " Presets", ""),
            ("SETTINGS", "Settings", ""),
        )
    )


def unregister():
    try:
        del bpy.types.Scene.msfs_multi_exporter_current_tab
    except:
        pass
