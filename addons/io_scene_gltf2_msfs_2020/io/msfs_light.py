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

import math
import bpy

from mathutils import Quaternion

from io_scene_gltf2.io.com.gltf2_io_extensions import Extension

class MSFS2020Light:
    bl_options = {"UNDO"}

    extension_name = "ASOBO_macro_light"

    def __new__(cls, *args, **kwargs):
        raise RuntimeError(f"{cls} should not be instantiated")

    @staticmethod
    def create(vnode, gltf_node, gltf):
        if not gltf_node.extensions:
            return

        extension = gltf_node.extensions.get(MSFS2020Light.extension_name)
        if not extension:
            return

        if extension.get("cone_angle") != 360:
            blender_light = bpy.data.lights.new(name=gltf_node.name, type="SPOT")
            blender_light.spot_size = extension.get("cone_angle")
        else:
            blender_light = bpy.data.lights.new(name=gltf_node.name, type="POINT")

        # Set Blender light properties
        blender_light.color = extension.get("color")
        blender_light.energy = extension.get("intensity")

        blender_node = bpy.data.objects.new(gltf_node.name, blender_light)

        # Set transform
        trans, rot, scale = vnode.trs()
        blender_node.location = trans
        blender_node.rotation_mode = "QUATERNION"
        blender_node.rotation_quaternion = rot
        blender_node.scale = scale

        # Set MSFS2020 light properties
        blender_node.msfs_light_has_symmetry = extension.get("has_symmetry")
        blender_node.msfs_light_flash_frequency = extension.get("flash_frequency")
        blender_node.msfs_light_flash_duration = extension.get("flash_duration")
        blender_node.msfs_light_flash_phase = extension.get("flash_phase")
        blender_node.msfs_light_rotation_speed = extension.get("rotation_speed")
        blender_node.msfs_light_day_night_cycle = extension.get("day_night_cycle")

        bpy.data.scenes[gltf.blender_scene].collection.objects.link(blender_node)

    @staticmethod
    def removeLightObject(vnode, gltf2_node, blender_node):
        if not gltf2_node.extensions:
            return
        
        extension = gltf2_node.extensions.get(MSFS2020Light.extension_name)
        if not extension:
            return
        
        bpy.data.objects.remove(blender_node)
        vnode.blender_object = bpy.data.objects[gltf2_node.name]

    @staticmethod
    def export(gltf2_object, blender_object):
        # First, clear all KHR_lights_punctual extensions from children.
        # TODO: remove children?
        for child in gltf2_object.children:
            if not isinstance(child.extensions, dict):
                continue

            if not "KHR_lights_punctual" in child.extensions:
                continue

            child.extensions.pop("KHR_lights_punctual")

        if (
            isinstance(gltf2_object.extensions, dict) 
            and "KHR_lights_punctual" in gltf2_object.extensions
        ):
            gltf2_object.extensions.pop("KHR_lights_punctual")

        angle = 360.0
        if blender_object.data.type == "SPOT":
            angle = (180.0 / math.pi) * blender_object.data.spot_size

        extension = {}

        extension["color"] = list(blender_object.data.color)
        extension["intensity"] = blender_object.data.energy
        extension["cone_angle"] = angle
        extension["has_symmetry"] = blender_object.msfs_light_has_symmetry
        extension["flash_frequency"] = blender_object.msfs_light_flash_frequency
        extension["flash_duration"] = blender_object.msfs_light_flash_duration
        extension["flash_phase"] = blender_object.msfs_light_flash_phase
        extension["rotation_speed"] = blender_object.msfs_light_rotation_speed
        extension["day_night_cycle"] = blender_object.msfs_light_day_night_cycle

        # start quick dirty fix to solve rotationn problem
        # this can be removed after blender 3.2 goes out
        currentRotationQuat = (
            Quaternion(
                (
                    gltf2_object.rotation[3],
                    gltf2_object.rotation[0],
                    gltf2_object.rotation[1],
                    gltf2_object.rotation[2],
                )
            )
            if gltf2_object.rotation
            else Quaternion()
        )
        quat_a = Quaternion(
            (1.0, 0.0, 0.0), 
            math.radians(
                90.0 
                if bpy.app.version < (3, 2, 0) 
                else 180
            )
        )
        r = currentRotationQuat @ quat_a
        gltf2_object.rotation = [r.x, r.y, r.z, r.w]
        # end quick fix

        gltf2_object.extensions[MSFS2020Light.extension_name] = Extension(
            name=MSFS2020Light.extension_name, 
            extension=extension, 
            required=False
        )
