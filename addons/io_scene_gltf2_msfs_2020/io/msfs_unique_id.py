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

import bpy
from io_scene_gltf2.io.com.gltf2_io_extensions import Extension


class MSFS_unique_id:
    bl_options = {"UNDO"}

    extension_name = "ASOBO_unique_id"

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("%s should not be instantiated" % cls)

    @staticmethod
    def create(gltf2_node, blender_node, import_settings):
        pass

    @staticmethod
    def export(gltf2_object, blender_object):
        extension = {}

        if type(blender_object) == bpy.types.PoseBone:
            blender_object = blender_object.bone
            
        uniqueID =  blender_object.name
        if blender_object.msfs_override_unique_id:
            uniqueID = blender_object.msfs_unique_id
        extension["id"] = uniqueID

        gltf2_object.extensions[MSFS_unique_id.extension_name] = Extension(
            name=MSFS_unique_id.extension_name,
            extension=extension,
            required=False
        )