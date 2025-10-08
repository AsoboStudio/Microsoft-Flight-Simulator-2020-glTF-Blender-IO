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

import re

import bpy

from .msfs_multi_export import MSFS_OT_MultiExportGLTF2


class MultiExporterLOD(bpy.types.PropertyGroup):
    objectLOD: bpy.props.PointerProperty(name="", type=bpy.types.Object)
    collection: bpy.props.PointerProperty(name="", type=bpy.types.Collection)

    enabled: bpy.props.BoolProperty(name="", default=False)
    lod_value: bpy.props.IntProperty(name="", default=0, min=0, max=999)
    file_name: bpy.props.StringProperty(name="", default="")

def update_relative_path(self, context):
    if self.folder_path == "//":
        self.folder_path = self.folder_path + "\\"
        
class MultiExporterLODGroup(bpy.types.PropertyGroup):
    group_name: bpy.props.StringProperty(
        name="",
        default=""
    )
    
    expanded: bpy.props.BoolProperty(
        name="",
        default=True
    )
    
    lods: bpy.props.CollectionProperty(
        type=MultiExporterLOD
    )
    
    folder_path: bpy.props.StringProperty(
        name="",
        default="",
        subtype="DIR_PATH",
        description="Path to the directory where you want your model to be exported",
        update=update_relative_path,
    )
    
    generate_xml: bpy.props.BoolProperty(
        name="",
        default=False
    )
    
    overwrite_guid: bpy.props.BoolProperty(
        name="",
        description=(
            "If an XML file already exists in the location"
            " to export to, the GUID will be overwritten"
        ),
        default=False,
    )


class MSFS_LODGroupUtility:
    @staticmethod
    def lod_is_visible(context, lod):
        sort_by_collection = context.scene.multi_exporter_grouped_by_collections

        if sort_by_collection:
            # Checking visibility from the collection itself won't work,
            # so we have to find the LayerCollection that contains our collection.
            collection_hidden = False
            for (
                layer_collection
            ) in bpy.context.window.view_layer.layer_collection.children:
                if layer_collection.collection == lod.collection:
                    collection_hidden = not layer_collection.visible_get()

            if (
                not context.scene.multi_exporter_show_hidden_objects
                and collection_hidden
            ) or (
                lod.collection is None
                or lod.collection not in list(bpy.data.collections)
            ):
                return False
        else:
            if (
                not context.scene.multi_exporter_show_hidden_objects
                and lod.objectLOD.hide_get()
            ) or (
                lod.objectLOD is None
                or lod.objectLOD not in list(bpy.context.window.view_layer.objects)
            ):
                return False

        return True


class MSFS_OT_ReloadLODGroups(bpy.types.Operator):
    bl_idname = "msfs.reload_lod_groups"
    bl_label = "Reload LOD groups"

    @staticmethod
    def update_grouped_by(self, context):
        context.scene.msfs_multi_exporter_lod_groups.clear()
        MSFS_OT_ReloadLODGroups.reload_lod_groups(self, context)

    @staticmethod
    def get_group_from_name(name):
        matches = re.findall("^x[0-9]_|_LOD[0-9]+", name)
        # If an object starts with xN_ or ends with _LODN, treat as an LOD
        if matches:
            # Get base object group name from object
            for match in matches:
                filtered_string = name.replace(match, "")
            return filtered_string
        else:
            # If prefix or suffix isn't found, use the object name as the group
            return name

    @staticmethod
    def get_lod_group_names(lod_groups):
        return [lod_group.group_name for lod_group in lod_groups]

    @staticmethod
    def reload_lod_groups(self, context):
        lod_groups = context.scene.msfs_multi_exporter_lod_groups
        sort_by_collection = context.scene.multi_exporter_grouped_by_collections

        # Remove deleted LODs
        for i, lod_group in enumerate(lod_groups):
            for j, lod in enumerate(lod_group.lods):
                if sort_by_collection:
                    if (
                        not lod.collection in list(bpy.data.collections)
                        or not MSFS_OT_ReloadLODGroups.get_group_from_name(
                            lod.collection.name
                        )
                        == lod_group.group_name
                    ):
                        lod_groups[i].lods.remove(j)
                        continue
                else:
                    if (
                        not lod.objectLOD in list(context.scene.objects)
                        or not MSFS_OT_ReloadLODGroups.get_group_from_name(
                            lod.objectLOD.name
                        )
                        == lod_group.group_name
                    ):
                        lod_groups[i].lods.remove(j)
                        continue

            if len(lod_group.lods) == 0:
                lod_groups.remove(i)

        # Search for new groups
        found_lod_groups = {}
        if sort_by_collection:
            for collection in bpy.data.collections:
                lod_group = MSFS_OT_ReloadLODGroups.get_group_from_name(collection.name)
                if lod_group not in found_lod_groups:
                    found_lod_groups[lod_group] = []
                found_lod_groups[lod_group].append(collection)
        else:
            for blender_object in context.scene.objects:
                if blender_object.parent is None:
                    lod_group = MSFS_OT_ReloadLODGroups.get_group_from_name(blender_object.name)
                    if lod_group not in found_lod_groups:
                        found_lod_groups[lod_group] = []
                    found_lod_groups[lod_group].append(blender_object)

        # Add to object groups
        for lod_group, blender_objects in found_lod_groups.items():
            if lod_group not in MSFS_OT_ReloadLODGroups.get_lod_group_names(lod_groups):
                # Create LOD group
                created_lod_group = lod_groups.add()
                created_lod_group.group_name = lod_group

            lod_group_index = MSFS_OT_ReloadLODGroups.get_lod_group_names(
                lod_groups
            ).index(lod_group)

            if sort_by_collection:
                for collection in blender_objects:
                    if collection not in [
                        lod.collection for lod in lod_groups[lod_group_index].lods
                    ]:
                        lod = lod_groups[lod_group_index].lods.add()
                        lod.collection = collection
                        lod.file_name = collection.name
            else:
                for obj in blender_objects:
                    if obj not in [
                        lod.objectLOD for lod in lod_groups[lod_group_index].lods
                    ]:
                        lod = lod_groups[lod_group_index].lods.add()
                        lod.objectLOD = obj
                        lod.file_name = obj.name

    def execute(self, context):
        MSFS_OT_ReloadLODGroups.reload_lod_groups(self, context)
        return {"FINISHED"}


class MSFS_PT_MultiExporterObjectsView(bpy.types.Panel):
    bl_label = ""
    bl_parent_id = "MSFS_PT_MultiExporter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Multi-Export glTF 2.0"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_multi_exporter_current_tab == "OBJECTS"

    def draw(self, context):
        layout = self.layout

        layout.operator(MSFS_OT_ReloadLODGroups.bl_idname, text="Reload LODs")
        layout.prop(context.scene, "multi_exporter_show_hidden_objects")
        layout.prop(context.scene, "multi_exporter_grouped_by_collections")

        lod_groups = context.scene.msfs_multi_exporter_lod_groups
        sort_by_collection = context.scene.multi_exporter_grouped_by_collections

        total_lods = 0
        for lod_group in lod_groups:
            for lod in lod_group.lods:
                if not MSFS_LODGroupUtility.lod_is_visible(context, lod):
                    continue

                total_lods += 1

        if total_lods == 0:
            box = layout.box()
            box.label(text="No LODs found in scene")
        else:
            for lod_group in lod_groups:
                # If we only have one LOD in the group, and it is hidden, then don't render the group
                if len(lod_group.lods) == 1:
                    if not MSFS_LODGroupUtility.lod_is_visible(
                        context, lod_group.lods[0]
                    ):
                        continue

                if len(lod_group.lods) > 0:
                    row = layout.row()

                    box = row.box()
                    box.prop(
                        lod_group,
                        "expanded",
                        text=lod_group.group_name,
                        icon="DOWNARROW_HLT" if lod_group.expanded else "RIGHTARROW",
                        icon_only=True,
                        emboss=False,
                    )
                    
                    if lod_group.expanded:
                        box.prop(lod_group, "generate_xml", text="Generate XML")
                        if lod_group.generate_xml:
                            box.prop(lod_group, "overwrite_guid", text="Overwrite GUID")

                        box.prop(lod_group, "folder_path", text="Export Path")

                        col = box.column()
                        for lod in lod_group.lods:
                            if not MSFS_LODGroupUtility.lod_is_visible(context, lod):
                                continue

                            row = col.row()
                            if sort_by_collection:
                                row.prop(lod, "enabled", text=lod.collection.name)
                            else:
                                row.prop(lod, "enabled", text=lod.objectLOD.name)
                            subrow = row.column()
                            subrow.prop(lod, "lod_value", text="LOD Value")
                            subrow.prop(lod, "file_name", text="File Name")

        row = layout.row(align=True)
        row.operator(MSFS_OT_MultiExportGLTF2.bl_idname, text="Export")


def register():
    bpy.types.Scene.msfs_multi_exporter_lod_groups = bpy.props.CollectionProperty(
        type=MultiExporterLODGroup
    )
    
    bpy.types.Scene.multi_exporter_show_hidden_objects = bpy.props.BoolProperty(
        name="Show hidden objects",
        default=True
    )
    
    bpy.types.Scene.multi_exporter_grouped_by_collections = bpy.props.BoolProperty(
        name="Grouped by collections",
        default=False,
        update=MSFS_OT_ReloadLODGroups.update_grouped_by,
    )
