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

import bpy


class MSFS2020_PT_BoneProperties(bpy.types.Panel):
    bl_label = "MSFS2020 Properties"
    bl_idname = "BONE_PT_msfs_properties"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "bone"

    def draw(self, context):
        layout = self.layout

        if context.mode == "EDIT_ARMATURE":
            return
        
        box = layout.box()
        active_bone = context.active_bone
        box.prop(active_bone, "msfs_override_unique_id")
        if active_bone.msfs_override_unique_id:
            box.prop(active_bone, "msfs_unique_id")


class MSFS2020_PT_ObjectProperties(bpy.types.Panel):
    bl_label = "MSFS2020 Properties"
    bl_idname = "OBJECT_PT_msfs_properties"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        return context.object.type

    def draw(self, context):
        layout = self.layout

        active_object = context.object

        box = layout.box()
        box.prop(active_object, "msfs_override_unique_id")
        
        if active_object.msfs_override_unique_id:
            box.prop(active_object, "msfs_unique_id")

        if active_object.type == "LIGHT":
            box = layout.box()
            box.label(text="MSFS2020 Light Parameters", icon="LIGHT")
            box.prop(active_object, "msfs_light_has_symmetry")
            box.prop(active_object, "msfs_light_flash_frequency")
            box.prop(active_object, "msfs_light_flash_duration")
            box.prop(active_object, "msfs_light_flash_phase")
            box.prop(active_object, "msfs_light_rotation_speed")
            box.prop(active_object, "msfs_light_day_night_cycle")

        elif active_object.type == "EMPTY":
            box = layout.box()
            box.label(text="MSFS2020 Collision Parameters", icon="SHADING_BBOX")
            box.prop(active_object, "msfs_gizmo_type")
            
            if active_object.msfs_gizmo_type != "NONE":
                box.prop(active_object, "msfs_collision_is_road_collider")
