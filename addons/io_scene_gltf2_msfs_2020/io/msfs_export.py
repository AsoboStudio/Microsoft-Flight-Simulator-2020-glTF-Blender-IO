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
import os
import urllib

from .. import get_version_string
from .msfs_gizmo import MSFS2020Gizmo
from .msfs_light import MSFS2020Light
from .msfs_material import MSFS2020_Material_IO
from .msfs_unique_id import MSFS2020_unique_id

def get_blender_version_string() -> str:
    return (
        str(bpy.app.version[0])
        + "."
        + str(bpy.app.version[1])
        + "."
        + str(bpy.app.version[2])
    )

class Export:
    def __init__(self):
        # We need to wait until we create the gltf2UserExtension to import the gltf2 modules
        # Otherwise, it may fail because the gltf2 may not be loaded yet
        from io_scene_gltf2.io.com.gltf2_io_extensions import Extension
        self.Extension = Extension
        self.properties = bpy.context.scene.msfs_exporter_settings
        
    def gather_asset_hook(
        self,
        gltf2_asset,
        export_settings
    ):
        if not self.properties.enable_msfs_extension:
            return
        
        if gltf2_asset.extensions is None:
            gltf2_asset.extensions = {}
            
        gltf2_asset.extensions["ASOBO_normal_map_convention"] = self.Extension(
            name="ASOBO_normal_map_convention",
            extension={"tangent_space_convention": "DirectX"},
            required=False
        )

        gltf2_asset.generator += f" and Asobo Studio MSFS2020 Blender I/O v{get_version_string()}" 
        gltf2_asset.generator += f" with Blender v{get_blender_version_string()}"

    def gather_gltf_extensions_hook(
        self,
        gltf2_plan,
        export_settings
    ):
        if not self.properties.enable_msfs_extension:
            return
        
        for image in gltf2_plan.images:
            image.uri = os.path.basename(urllib.parse.unquote(image.uri))

    def gather_node_hook(
        self,
        gltf2_object,
        blender_object,
        export_settings
    ):
        if not self.properties.enable_msfs_extension:
            return
        
        if gltf2_object.extensions is None:
            gltf2_object.extensions = {}

        if self.properties.use_unique_id:
            MSFS2020_unique_id.export(gltf2_object, blender_object)

        if blender_object.type == "LIGHT":
            MSFS2020Light.export(gltf2_object, blender_object)
    
    def gather_joint_hook(
        self,
        gltf2_node,
        blender_bone,
        export_settings
    ):
        if not self.properties.enable_msfs_extension:
            return

        if gltf2_node.extensions is None:
            gltf2_node.extensions = {}

        if self.properties.use_unique_id:
            MSFS2020_unique_id.export(gltf2_node, blender_bone)

    def gather_scene_hook(
        self,
        gltf2_scene,
        blender_scene,
        export_settings
    ):
        if not self.properties.enable_msfs_extension:
            return
        
        MSFS2020Gizmo.export(
            gltf2_scene.nodes,
            blender_scene,
            export_settings
        )

    def gather_material_hook(
        self,
        gltf2_material,
        blender_material,
        export_settings
    ):
        if not self.properties.enable_msfs_extension:
            return
        
        MSFS2020_Material_IO.export(
            gltf2_material,
            blender_material,
            export_settings
        )
        
        if "KHR_materials_anisotropy" in gltf2_material.extensions:
            gltf2_material.extensions.pop("KHR_materials_anisotropy", None)
