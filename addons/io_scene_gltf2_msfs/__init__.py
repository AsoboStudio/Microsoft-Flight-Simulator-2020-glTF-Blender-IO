# Copyright 2021-2022 The glTF-Blender-IO-MSFS authors.
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

import importlib
import inspect
import pkgutil
from pathlib import Path

import bpy

bl_info = {
    "name": "Microsoft Flight Simulator glTF Extension",
    "author": "Luca Pierabella, Yasmine Khodja, Wing42, pepperoni505, ronh991, and others",
    "description": "This toolkit prepares your 3D assets to be used for Microsoft Flight Simulator",
    "blender": (3, 3, 0),
    "version": (1, 3, 3, 1),
    "location": "File > Import-Export",
    "category": "Import-Export",
    "tracker_url": "https://github.com/AsoboStudio/glTF-Blender-IO-MSFS"
}

def get_version_string():
    return str(bl_info['version'][0]) + '.' + str(bl_info['version'][1]) + '.' + str(bl_info['version'][2])

class MSFS_ImporterProperties(bpy.types.PropertyGroup):
    enable_msfs_extension: bpy.props.BoolProperty(
        name='Microsoft Flight Simulator Extensions',
        description='Enable MSFS glTF import extensions',
        default=True
    )

class MSFS_ExporterProperties(bpy.types.PropertyGroup):
    def msfs_enable_msfs_extension_update(self, context):
        props = bpy.context.scene.msfs_exporter_settings
        settings = bpy.context.scene.msfs_multi_exporter_settings
        settings.enable_msfs_extension = props.enable_msfs_extension

    enable_msfs_extension: bpy.props.BoolProperty(
        name='Microsoft Flight Simulator Extensions',
        description='Enable MSFS glTF export extensions',
        default=True,
        update=msfs_enable_msfs_extension_update
    )

    use_unique_id: bpy.props.BoolProperty(
        name='Use ASOBO Unique ID',
        description='use ASOBO Unique ID extension',
        default=True,
    )
    

class GLTF_PT_MSFSImporterExtensionPanel(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = ""
    bl_parent_id = "GLTF_PT_import_user_extensions"
    bl_location = "File > Import > glTF 2.0"

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == "IMPORT_SCENE_OT_gltf"

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="MSFS Extensions", icon='TOOL_SETTINGS')

    def draw(self, context):
        props = bpy.context.scene.msfs_importer_properties

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.prop(props, 'enable_msfs_extension', text="Enabled")

class GLTF_PT_MSFSExporterExtensionPanel(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = ""
    bl_parent_id = "GLTF_PT_export_user_extensions"
    bl_location = "File > Export > glTF 2.0"

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == "EXPORT_SCENE_OT_gltf"

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="Microsoft Flight Simulator Extensions", icon='TOOL_SETTINGS')

    def draw(self, context):
        props = bpy.context.scene.msfs_exporter_settings

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.prop(props, 'enable_msfs_extension', text="Enabled")
        if props.enable_msfs_extension:
            layout.prop(props, 'use_unique_id', text="Enable ASOBO Unique ID extension")

def recursive_module_search(path, root=""):
    for _, name, ispkg in pkgutil.iter_modules([str(path)]):
        if ispkg:
            yield from recursive_module_search(path / name, f"{root}.{name}")
        else:
            yield root, name


def modules():
    for root, name in recursive_module_search(Path(__file__).parent):
        if name in locals():
            yield importlib.reload(locals()[name])
        else:
            yield importlib.import_module(f".{name}", package=f"{__package__}{root}")


classes = []
extension_classes = [MSFS_ImporterProperties, MSFS_ExporterProperties]
extension_panels = [GLTF_PT_MSFSImporterExtensionPanel, GLTF_PT_MSFSExporterExtensionPanel]

# Refresh the list of classes
def update_class_list():
    global classes

    classes = []

    for module in modules():
        for obj in module.__dict__.values():
            if inspect.isclass(obj) \
                    and module.__name__ in str(obj) \
                    and "bpy" in str(inspect.getmro(obj)[1]):
                classes.append(obj)


def register():
    # Refresh the list of classes whenever the addon is reloaded so we can stay up to date with the files on disk.
    update_class_list()

    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            pass

    for module in modules():
        if hasattr(module, "register"):
            module.register()

    for cls in extension_classes:
        try:
            bpy.utils.register_class(cls)
        except Exception:
            pass

    bpy.types.Scene.msfs_importer_properties = bpy.props.PointerProperty(type=MSFS_ImporterProperties)
    bpy.types.Scene.msfs_exporter_settings = bpy.props.PointerProperty(type=MSFS_ExporterProperties)


def register_panel():
    # Register the panel on demand, we need to be sure to only register it once
    # This is necessary because the panel is a child of the extensions panel,
    # which may not be registered when we try to register this extension
    for panel in extension_panels:
        try:
            bpy.utils.register_class(panel)
        except Exception:
            pass

    for module in modules():
        if hasattr(module, "register_panel"):
            module.register_panel()

    # If the glTF exporter is disabled, we need to unregister the extension panel
    # Just return a function to the exporter so it can unregister the panel
    return unregister_panel


def unregister():
    for cls in classes:
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass

    for module in modules():
        if hasattr(module, "unregister"):
            module.unregister()

    for cls in extension_classes:
        bpy.utils.unregister_class(cls)

def unregister_panel():
    for panel in extension_panels:
        try:
            bpy.utils.unregister_class(panel)
        except Exception:
            pass

    for module in modules():
        if hasattr(module, "unregister_panel"):
            module.unregister_panel()


##################################################################################
from .io.msfs_import import Import


class glTF2ImportUserExtension(Import):
    def __init__(self):
        self.properties = bpy.context.scene.msfs_importer_properties


##################################################################################
from .io.msfs_export import Export


class glTF2ExportUserExtension(Export):
    def __init__(self):
        # We need to wait until we create the gltf2UserExtension to import the gltf2 modules
        # Otherwise, it may fail because the gltf2 may not be loaded yet
        from io_scene_gltf2.io.com.gltf2_io_extensions import Extension
        self.Extension = Extension
        self.properties = bpy.context.scene.msfs_exporter_settings
