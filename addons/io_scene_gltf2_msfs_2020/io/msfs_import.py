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
from .msfs_material import MSFS2020_Material_IO
from .msfs_optimized import MSFS2020OptimizedAsset


class Import:

    def __init__(self):
        self.properties = bpy.context.scene.msfs_importer_properties

        # Package Builder output marks MSFT_texture_dds as required
        from io_scene_gltf2.io.com.gltf2_io_extensions import Extension
        self.extensions = [Extension(name="MSFT_texture_dds", extension={}, required=True)]

    # Decode Package Builder (ASOBO_asset_optimized) data
    def gather_import_gltf_before_hook(self, gltf):
        MSFS2020OptimizedAsset.prepare(gltf)

    # Decode BC5 normal maps Blender can't load
    def gather_import_image_after_hook(self, img, blender_image, gltf):
        if MSFS2020OptimizedAsset.is_optimized(gltf):
            MSFS2020OptimizedAsset.load_bc5(gltf, img, blender_image)

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
        MSFS2020_Material_IO.create(gltf2_material, blender_material, import_settings)
