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

if bpy.app.version >= (4, 2, 0):
    from io_scene_gltf2.blender.exp.material.gltf2_blender_search_node_tree import (
        NodeSocket
    )

if bpy.app.version >= (3, 6, 0):
    from io_scene_gltf2.blender.exp.material.gltf2_blender_gather_texture_info import (
        gather_material_normal_texture_info_class,
        gather_texture_info
    )
else:
    from io_scene_gltf2.blender.exp.gltf2_blender_gather_texture_info import (
        gather_material_normal_texture_info_class,
        gather_texture_info
    )
    
from io_scene_gltf2.blender.imp.gltf2_blender_image import BlenderImage

from ..com import msfs_material_props as MSFS2020_MaterialExtensions


class MSFS2020_Material_IO:
    bl_options = {"UNDO"}

    extensions = [
        MSFS2020_MaterialExtensions.AsoboMaterialCommon,
        MSFS2020_MaterialExtensions.AsoboMaterialGeometryDecal,
        MSFS2020_MaterialExtensions.AsoboMaterialGhostEffect,
        MSFS2020_MaterialExtensions.AsoboMaterialDrawOrder,
        MSFS2020_MaterialExtensions.AsoboDayNightCycle,
        MSFS2020_MaterialExtensions.AsoboDisableMotionBlur,
        MSFS2020_MaterialExtensions.AsoboPearlescent,
        MSFS2020_MaterialExtensions.AsoboAlphaModeDither,
        MSFS2020_MaterialExtensions.AsoboMaterialInvisible,
        MSFS2020_MaterialExtensions.AsoboMaterialEnvironmentOccluder,
        MSFS2020_MaterialExtensions.AsoboMaterialUVOptions,
        MSFS2020_MaterialExtensions.AsoboMaterialShadowOptions,
        MSFS2020_MaterialExtensions.AsoboMaterialResponsiveAAOptions,
        MSFS2020_MaterialExtensions.AsoboMaterialDetail,
        MSFS2020_MaterialExtensions.AsoboMaterialFakeTerrain,
        MSFS2020_MaterialExtensions.AsoboMaterialFresnelFade,
        MSFS2020_MaterialExtensions.AsoboSSS,
        MSFS2020_MaterialExtensions.AsoboAnisotropic,
        MSFS2020_MaterialExtensions.AsoboWindshield,
        MSFS2020_MaterialExtensions.AsoboClearCoat,
        MSFS2020_MaterialExtensions.AsoboParallaxWindow,
        MSFS2020_MaterialExtensions.AsoboGlass,
        MSFS2020_MaterialExtensions.AsoboTags,
        MSFS2020_MaterialExtensions.AsoboMaterialCode,
    ]

    def __new__(cls, *args, **kwargs):
        raise RuntimeError(f"{cls} should not be instantiated")

    @staticmethod
    def create_image(index, import_settings):
        pytexture = import_settings.data.textures[index]
        BlenderImage.create(import_settings, pytexture.source)
        pyimg = import_settings.data.images[pytexture.source]

        # Find image created
        blender_image_name = pyimg.blender_image_name
        if blender_image_name:
            return bpy.data.images[blender_image_name]

    @staticmethod
    def export_image(blender_material, blender_image, image_type, export_settings):
        nodes = blender_material.node_tree.nodes
        links = blender_material.node_tree.links

        # Create a fake texture node temporarily (unfortunately this is the only solid way of doing this)
        texture_node = nodes.new("ShaderNodeTexImage")
        texture_node.name = "Texture Output"
        texture_node.image = blender_image

        # Save image path before converting it to an absolute path
        saved_image_path = blender_image.filepath

        # Make sure that the path of the image is absolute
        texture_node.image.filepath = bpy.path.abspath(texture_node.image.filepath)
        texture_node.image.filepath = os.path.realpath(texture_node.image.filepath)

        # Create shader to plug texture into
        principled_bsdf_node = nodes.new("ShaderNodeBsdfPrincipled")
        principled_bsdf_node.name = "Principled BSDF Temp Node"

        texture_info = None

        # region Gather texture info
        if image_type == "DEFAULT":
            node_link = links.new(
                texture_node.outputs[0],
                principled_bsdf_node.inputs["Base Color"]
            )

            if bpy.app.version >= (4, 2, 0):
                node_socket = NodeSocket(
                    principled_bsdf_node.inputs["Base Color"],
                    [blender_material.node_tree]
                )

                texture_info = gather_texture_info(
                    node_socket,
                    (node_socket,),
                    export_settings
                )
            else:
                texture_info = gather_texture_info(
                    principled_bsdf_node.inputs["Base Color"],
                    (principled_bsdf_node.inputs["Base Color"],),
                    export_settings
                )

        elif image_type == "NORMAL":
            normal_node = nodes.new("ShaderNodeNormalMap")
            normal_node.name = "Normal Texture Output"

            links.new(
                texture_node.outputs[0],
                normal_node.inputs["Color"]
            )

            links.new(
                normal_node.outputs[0],
                principled_bsdf_node.inputs["Normal"]
            )

            if bpy.app.version >= (4, 2, 0):
                node_socket = NodeSocket(
                    principled_bsdf_node.inputs["Normal"],
                    [blender_material.node_tree]
                )

                texture_info = gather_material_normal_texture_info_class(
                    node_socket,
                    (node_socket,),
                    export_settings
                )
            else:
                texture_info = gather_material_normal_texture_info_class(
                    principled_bsdf_node.inputs["Normal"],
                    (principled_bsdf_node.inputs["Normal"],),
                    export_settings
                )

        # endregion

        # Restore saved image file path
        blender_image.filepath = saved_image_path

        if texture_info is None:
            return None

        # Some versions of the Khronos exporter have gather_texture_info return a tuple
        if isinstance(texture_info, tuple):
            texture_info = texture_info[0]

        if hasattr(texture_info, "tex_coord"):
            texture_info.tex_coord = None
            
        # region Delete temp nodes
        nodes.remove(principled_bsdf_node)
        nodes.remove(texture_node)
        
        if image_type == "NORMAL":
            nodes.remove(normal_node)
        # endregion
        
        return texture_info

    @staticmethod
    def create(gltf2_material, blender_material, import_settings):
        for extension in MSFS2020_Material_IO.extensions:
            extension.from_dict(blender_material, gltf2_material, import_settings)

    @staticmethod
    def export(gltf2_material, blender_material, export_settings):
        for extension in MSFS2020_Material_IO.extensions:
            extension.to_extension(blender_material, gltf2_material, export_settings)
