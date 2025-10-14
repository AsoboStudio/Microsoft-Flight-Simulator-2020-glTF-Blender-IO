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

import importlib
import inspect
import pkgutil
from pathlib import Path

import bpy

bl_info = {
    "name": "Microsoft Flight Simulator 2020: glTF Extension",
    "author": "Asobo Studio",
    "description": "This toolkit prepares your 3D assets to be used for Microsoft Flight Simulator 2020",
    "blender": (3, 3, 0),
    "version": (3, 3, 0),
    "location": "File > Import-Export",
    "category": "Import-Export",
    "tracker_url": "https://github.com/AsoboStudio/glTF-Blender-IO-MSFS-2020",
}


def get_version_string():
    return (
        str(bl_info["version"][0])
        + "."
        + str(bl_info["version"][1])
        + "."
        + str(bl_info["version"][2])
    )


# region MSFS2020 Importer/Exporter Properties
class MSFS2020_ImporterProperties(bpy.types.PropertyGroup):
    enable_msfs_extension: bpy.props.BoolProperty(
        name="Microsoft Flight Simulator 2020 Extensions",
        description="Enable MSFS2020 glTF import extensions",
        default=True,
    )


class MSFS2020_ExporterProperties(bpy.types.PropertyGroup):
    def msfs_enable_msfs_extension_update(self, context):
        props = bpy.context.scene.msfs_exporter_settings
        settings = bpy.context.scene.msfs_multi_exporter_settings
        settings.enable_msfs_extension = props.enable_msfs_extension

    enable_msfs_extension: bpy.props.BoolProperty(
        name="Microsoft Flight Simulator 2020 Extensions",
        description="Enable MSFS2020 glTF export extensions",
        default=True,
        update=msfs_enable_msfs_extension_update,
    )

    use_unique_id: bpy.props.BoolProperty(
        name="Use ASOBO Unique ID",
        description="use ASOBO Unique ID extension",
        default=True,
    )


# endregion

# region MSFS2020 Importer/Exporter Panels
if bpy.app.version < (4, 2, 0):

    class GLTF_PT_MSFS2020_ImporterExtensionPanel(bpy.types.Panel):
        bl_space_type = "FILE_BROWSER"
        bl_region_type = "TOOL_PROPS"
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
            layout.label(
                text="Microsoft Flight Simulator 2020 Extensions", icon="TOOL_SETTINGS"
            )

        def draw(self, context):
            props = bpy.context.scene.msfs_importer_properties

            layout = self.layout
            layout.use_property_split = True
            layout.use_property_decorate = False  # No animation.

            layout.prop(props, "enable_msfs_extension", text="Enabled")

    class GLTF_PT_MSFS2020_ExporterExtensionPanel(bpy.types.Panel):
        bl_space_type = "FILE_BROWSER"
        bl_region_type = "TOOL_PROPS"
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
            layout.label(
                text="Microsoft Flight Simulator 2020 Extensions", icon="TOOL_SETTINGS"
            )

        def draw(self, context):
            props = bpy.context.scene.msfs_exporter_settings

            layout = self.layout
            layout.use_property_split = True
            layout.use_property_decorate = False  # No animation.

            layout.prop(props, "enable_msfs_extension", text="Enabled")
            if props.enable_msfs_extension:
                layout.prop(
                    props, 
                    "use_unique_id",
                    text="Enable ASOBO Unique ID extension"
                )

else:

    def draw_import(context, layout):
        header, body = layout.panel("GLTF_addon_example_importer", default_closed=True)
        header.use_property_split = False

        row = header.row()
        row.label(
            text="Microsoft Flight Simulator 2020 Extensions", icon="TOOL_SETTINGS"
        )
        if body is not None:
            settings = context.scene.msfs_importer_properties

            body.prop(settings, "enable_msfs_extension", text="Enabled")

    def draw_export(context, layout):
        header, body = layout.panel("GLTF_addon_example_exporter", default_closed=True)
        header.use_property_split = False

        row = header.row()
        row.label(
            text="Microsoft Flight Simulator 2020 Extensions", icon="TOOL_SETTINGS"
        )
        if body is not None:
            settings = context.scene.msfs_multi_exporter_settings
            body.prop(settings, "enable_msfs_extension", text="Enabled")


#  endregion


# region ######################### REGISTRATION #################################
modules=[]
classes = []

def recursive_module_search(path, root=""):
    for _, module_name, ispkg in pkgutil.iter_modules([str(path)]):
        if ispkg:
            yield from recursive_module_search(
                path / module_name,
                f"{root}.{module_name}"
            )
        else:
            yield root, module_name

def update_module_list():
    global modules
    for root, module_name in recursive_module_search(Path(__file__).parent):
        modules.append(
            importlib.import_module(
                f".{module_name}",
                package=f"{__package__}{root}"
            )
        )
    return modules

# Refresh the list of classes
def update_class_list():
    global modules
    global classes

    classes = []

    for module in modules:
        for obj in module.__dict__.values():
            if inspect.isclass(obj) \
                    and module.__name__ in str(obj) \
                    and "bpy" in str(inspect.getmro(obj)[1]):
                classes.append(obj)

def register():
    try:
        bpy.utils.register_class(MSFS2020_ImporterProperties)
        bpy.utils.register_class(MSFS2020_ExporterProperties)
    except (ValueError, RuntimeError):
        pass
    global modules
    global classes
    
    modules = []
    classes = []

    update_module_list()
    
    # Refresh the list of classes whenever the addon is reloaded 
    # So we can stay up to date with the files on disk.
    update_class_list()
    
    # Always register modules after classes
    # Some props have classes as types
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except (ValueError, RuntimeError):
            pass

    for module in modules:
        if hasattr(module, "register"):
            module.register()
        
    bpy.types.Scene.msfs_importer_properties = bpy.props.PointerProperty(
        type=MSFS2020_ImporterProperties
    )
    bpy.types.Scene.msfs_exporter_settings = bpy.props.PointerProperty(
        type=MSFS2020_ExporterProperties
    )

def unregister():
    try:
        bpy.utils.unregister_class(MSFS2020_ImporterProperties)
        bpy.utils.unregister_class(MSFS2020_ExporterProperties)
        
        del bpy.types.Scene.msfs_importer_properties
        del bpy.types.Scene.msfs_exporter_settings
    except RuntimeError:
        pass 
    
    global classes
    global modules
    for cls in classes:
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass

    for module in modules:
        if hasattr(module, "unregister"):
            module.unregister()

extension_panels = []
if bpy.app.version < (4, 2, 0):
    extension_panels = [
        GLTF_PT_MSFS2020_ImporterExtensionPanel,
        GLTF_PT_MSFS2020_ExporterExtensionPanel,
    ]
          
def register_panel():
    global modules
    for module in modules:
        if hasattr(module, "register_panel"):
            module.register_panel()
            
    if bpy.app.version >= (4, 2, 0):
        return
    
    for panel in extension_panels:
        try:
            bpy.utils.register_class(panel)
        except Exception:
            pass

def unregister_panel():
    global modules
    for module in modules:
        if hasattr(module, "unregister_panel"):
            module.unregister_panel()
            
    if bpy.app.version >= (4, 2, 0):
        return
    
    for panel in extension_panels:
        try:
            bpy.utils.unregister_class(panel)
        except Exception:
            pass
            
# endregion

# region Import
from .io.msfs_import import Import


class glTF2ImportUserExtension(Import):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# endregion

# region Export

from .io.msfs_export import Export


class glTF2ExportUserExtension(Export):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# endregion
