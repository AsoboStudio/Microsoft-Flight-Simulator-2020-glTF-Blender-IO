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

from .msfs_gizmo import MSFS2020Gizmo
from .msfs_light import MSFS2020Light
from .msfs_material import MSFS2020Material


class Import:

    def __init__(self):
        self.properties = bpy.context.scene.msfs_importer_properties

    # Create lights
    def gather_import_light_after_hook(
        self, 
        gltf2_node, 
        blender_node, 
        blender_light, 
        import_settings
    ):
        MSFS2020Light.create(
            gltf2_node, 
            blender_node, 
            import_settings
        )

    # Create gizmos
    def gather_import_scene_before_hook(
        self, 
        gltf_scene, 
        blender_scene, 
        import_settings
    ):
        MSFS2020Gizmo.create(
            gltf_scene, 
            blender_scene, 
            import_settings
        )

    # Create Lights
    def gather_import_node_before_hook(
        self,
        vnode,
        gltf_node,
        gltf
    ):
        MSFS2020Light.create(
            vnode,
            gltf_node,
            gltf
        )

    # Set proper gizmo blender object properties
    def gather_import_node_after_hook(
        self,
        vnode,
        gltf2_node,
        blender_object,
        import_settings
    ):
        MSFS2020Gizmo.set_blender_data(gltf2_node, blender_object, import_settings)
        MSFS2020Light.removeLightObject(vnode, gltf2_node, blender_object)

    # Create materials
    def gather_import_material_after_hook(
        self,
        gltf2_material,
        vertex_color,
        blender_material,
        import_settings
    ):
        MSFS2020Material.create(gltf2_material, blender_material, import_settings)
