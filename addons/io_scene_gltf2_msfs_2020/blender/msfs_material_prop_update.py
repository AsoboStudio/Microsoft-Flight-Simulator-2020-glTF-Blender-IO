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

from .material.msfs_material_anisotropic import MSFS2020_Anisotropic
from .material.msfs_material_clearcoat import MSFS2020_Clearcoat
from .material.msfs_material_environment_occluder import MSFS2020_Environment_Occluder
from .material.msfs_material_fake_terrain import MSFS2020_Fake_Terrain
from .material.msfs_material_fresnel_fade import MSFS2020_Fresnel_Fade
from .material.msfs_material_geo_decal import MSFS2020_Geo_Decal
from .material.msfs_material_geo_decal_frosted import MSFS2020_Geo_Decal_Frosted
from .material.msfs_material_ghost import MSFS2020_Ghost
from .material.msfs_material_glass import MSFS2020_Glass
from .material.msfs_material_hair import MSFS2020_Hair
from .material.msfs_material_invisible import MSFS2020_Invisible
from .material.msfs_material_parallax import MSFS2020_Parallax
from .material.msfs_material_porthole import MSFS2020_Porthole
from .material.msfs_material_sss import MSFS2020_SSS
from .material.msfs_material_standard import MSFS2020_Standard
from .material.msfs_material_windshield import MSFS2020_Windshield
from .msfs_material_function import MSFS2020_Material


class MSFS2020_Material_Property_Update:

    @staticmethod
    def getMaterial(material):
        if material.msfs_material_type == "msfs_standard":
            return MSFS2020_Standard(material)
        elif material.msfs_material_type == "msfs_geo_decal":
            return MSFS2020_Geo_Decal(material)
        elif material.msfs_material_type == "msfs_geo_decal_frosted":
            return MSFS2020_Geo_Decal_Frosted(material)
        elif material.msfs_material_type == "msfs_windshield":
            return MSFS2020_Windshield(material)
        elif material.msfs_material_type == "msfs_porthole":
            return MSFS2020_Porthole(material)
        elif material.msfs_material_type == "msfs_glass":
            return MSFS2020_Glass(material)
        elif material.msfs_material_type == "msfs_clearcoat":
            return MSFS2020_Clearcoat(material)
        elif material.msfs_material_type == "msfs_parallax":
            return MSFS2020_Parallax(material)
        elif material.msfs_material_type == "msfs_anisotropic":
            return MSFS2020_Anisotropic(material)
        elif material.msfs_material_type == "msfs_hair":
            return MSFS2020_Hair(material)
        elif material.msfs_material_type == "msfs_sss":
            return MSFS2020_SSS(material)
        elif material.msfs_material_type == "msfs_invisible":
            return MSFS2020_Invisible(material)
        elif material.msfs_material_type == "msfs_fake_terrain":
            return MSFS2020_Fake_Terrain(material)
        elif material.msfs_material_type == "msfs_fresnel_fade":
            return MSFS2020_Fresnel_Fade(material)
        elif material.msfs_material_type == "msfs_environment_occluder":
            return MSFS2020_Environment_Occluder(material)
        elif material.msfs_material_type == "msfs_ghost":
            return MSFS2020_Ghost(material)

    @staticmethod
    def update_msfs_material_type(self, context):
        material = None
        if self.msfs_material_type == "msfs_standard":
            material = MSFS2020_Standard(self, buildTree=True)
            self.msfs_alpha_mode = "OPAQUE"
        elif self.msfs_material_type == "msfs_geo_decal":
            material = MSFS2020_Geo_Decal(self, buildTree=True)
            self.msfs_alpha_mode = "BLEND"
        elif self.msfs_material_type == "msfs_geo_decal_frosted":
            material = MSFS2020_Geo_Decal_Frosted(self, buildTree=True)
            self.msfs_alpha_mode = "BLEND"
        elif self.msfs_material_type == "msfs_windshield":
            material = MSFS2020_Windshield(self, buildTree=True)
            self.msfs_alpha_mode = "BLEND"
            self.msfs_metallic_factor = 0.0
        elif self.msfs_material_type == "msfs_porthole":
            material = MSFS2020_Porthole(self, buildTree=True)
            self.msfs_alpha_mode = "OPAQUE"
        elif self.msfs_material_type == "msfs_glass":
            material = MSFS2020_Glass(self, buildTree=True)
            self.msfs_alpha_mode = "BLEND"
            self.msfs_metallic_factor = 0.0
        elif self.msfs_material_type == "msfs_clearcoat":
            material = MSFS2020_Clearcoat(self, buildTree=True)
            self.msfs_alpha_mode = "OPAQUE"
        elif self.msfs_material_type == "msfs_parallax":
            material = MSFS2020_Parallax(self, buildTree=True)
            self.msfs_alpha_mode = "MASK"
        elif self.msfs_material_type == "msfs_anisotropic":
            material = MSFS2020_Anisotropic(self, buildTree=True)
            self.msfs_alpha_mode = "OPAQUE"
        elif self.msfs_material_type == "msfs_hair":
            material = MSFS2020_Hair(self, buildTree=True)
            self.msfs_alpha_mode = "OPAQUE"
        elif self.msfs_material_type == "msfs_sss":
            material = MSFS2020_SSS(self, buildTree=True)
            self.msfs_alpha_mode = "OPAQUE"
        elif self.msfs_material_type == "msfs_invisible":
            material = MSFS2020_Invisible(self, buildTree=True)
            self.msfs_no_cast_shadow = True
            self.msfs_alpha_mode = "BLEND"
        elif self.msfs_material_type == "msfs_fake_terrain":
            material = MSFS2020_Fake_Terrain(self, buildTree=True)
            self.msfs_alpha_mode = "OPAQUE"
        elif self.msfs_material_type == "msfs_fresnel_fade":
            material = MSFS2020_Fresnel_Fade(self, buildTree=True)
            self.msfs_alpha_mode = "BLEND"
        elif self.msfs_material_type == "msfs_environment_occluder":
            material = MSFS2020_Environment_Occluder(self, buildTree=True)
            self.msfs_no_cast_shadow = True
            self.msfs_alpha_mode = "BLEND"
        elif self.msfs_material_type == "msfs_ghost":
            material = MSFS2020_Ghost(self, buildTree=True)
            self.msfs_no_cast_shadow = True
            self.msfs_alpha_mode = "BLEND"
        else:
            MSFS2020_Material_Property_Update.reset_material_prop_object(self)
            material = MSFS2020_Material(self)
            material.revertToPBRShaderTree()
            self.msfs_alpha_mode = "OPAQUE"
            return
    
    @staticmethod
    def reset_material_prop_object(self):
        self.msfs_alpha_cutoff = 0.5
        self.msfs_base_color_blend_factor = 1.0
        self.msfs_base_color_factor = [1.0, 1.0, 1.0, 1.0]
        self.msfs_base_color_texture = None
        self.msfs_blend_mask_texture = None
        self.msfs_clamp_uv_x = False
        self.msfs_clamp_uv_y = False
        self.msfs_collision_material = False
        self.msfs_day_night_cycle = False
        self.msfs_detail_blend_threshold = 0.1
        self.msfs_detail_color_texture = None
        self.msfs_detail_occlusion_metallic_roughness_texture = None
        self.msfs_detail_normal_texture = None
        self.msfs_detail_uv_offset_u = 0.0
        self.msfs_detail_uv_offset_v = 0.0
        self.msfs_detail_uv_scale = 1.0
        self.msfs_dirt_texture = None
        self.msfs_disable_motion_blur = False
        self.msfs_double_sided = False
        self.msfs_draw_order_offset = 0
        self.msfs_emissive_blend_factor = 1.0
        self.msfs_emissive_factor = [0.0, 0.0, 0.0]
        self.msfs_emissive_scale = 1.0
        self.msfs_emissive_texture = None
        self.msfs_extra_slot1_texture = None
        self.msfs_fresnel_factor = 1.0
        self.msfs_fresnel_opacity_offset = 1.0
        self.msfs_ghost_bias = 1.0
        self.msfs_ghost_power = 1.0
        self.msfs_ghost_scale = 1.0
        self.msfs_glass_deformation_factor = 0.0
        self.msfs_glass_reflection_mask_factor = 0.0
        self.msfs_metallic_blend_factor = 0.0
        self.msfs_metallic_factor = 1.0
        self.msfs_no_cast_shadow = False
        self.msfs_normal_blend_factor = 1.0
        self.msfs_normal_scale = 1.0
        self.msfs_normal_texture = None
        self.msfs_occlusion_blend_factor = 1.0
        self.msfs_occlusion_metallic_roughness_texture = None
        self.msfs_opacity_texture = None
        self.msfs_parallax_corridor = False
        self.msfs_parallax_room_number_xy = 1
        self.msfs_parallax_room_size_x = 1.0
        self.msfs_parallax_room_size_y = 1.0
        self.msfs_parallax_scale = 0.0
        self.msfs_pearl_brightness = 0.0
        self.msfs_pearl_range = 0.0
        self.msfs_pearl_shift = 0.0
        self.msfs_rain_drop_scale = 1.0
        self.msfs_responsive_aa = False
        self.msfs_road_collision_material = False
        self.msfs_roughness_blend_factor = 1.0
        self.msfs_roughness_factor = 1.0
        self.msfs_sss_color = [1.0, 1.0, 1.0, 1.0]
        self.msfs_use_pearl = False
        self.msfs_uv_offset_u = 0.0
        self.msfs_uv_offset_v = 0.0
        self.msfs_uv_rotation = 0.0
        self.msfs_uv_tiling_u = 1.0
        self.msfs_uv_tiling_v = 1.0
        self.msfs_wiper_1_state = 0.0
        self.msfs_wiper_2_state = 0.0
        self.msfs_wiper_3_state = 0.0
        self.msfs_wiper_4_state = 0.0
        self.msfs_alpha_mode = "OPAQUE"
        return

    @staticmethod
    def update_base_color_texture(self, context):
        material = MSFS2020_Material_Property_Update.getMaterial(self)
        if material is not None and type(material) is not MSFS2020_Invisible:
            material.setBaseColorTex(self.msfs_base_color_texture)

    @staticmethod
    def update_comp_texture(self, context):
        material = MSFS2020_Material_Property_Update.getMaterial(self)
        if material is not None and type(material) is not MSFS2020_Invisible:
            material.setCompTex(self.msfs_occlusion_metallic_roughness_texture)

    @staticmethod
    def update_normal_texture(self, context):
        material = MSFS2020_Material_Property_Update.getMaterial(self)
        if material is not None and type(material) is not MSFS2020_Invisible:
            material.setNormalTex(self.msfs_normal_texture)

    @staticmethod
    def update_emissive_texture(self, context):
        material = MSFS2020_Material_Property_Update.getMaterial(self)
        if material is not None and type(material) is not MSFS2020_Invisible:
            material.setEmissiveTexture(self.msfs_emissive_texture)

    @staticmethod
    def update_detail_color_texture(self, context):
        material = MSFS2020_Material_Property_Update.getMaterial(self)
        if material is not None and type(material) is not MSFS2020_Invisible:
            material.setDetailColorTex(self.msfs_detail_color_texture)

    @staticmethod
    def update_detail_comp_texture(self, context):
        material = MSFS2020_Material_Property_Update.getMaterial(self)
        if material is not None and type(material) is not MSFS2020_Invisible:
            material.setDetailCompTex(self.msfs_detail_occlusion_metallic_roughness_texture)

    @staticmethod
    def update_detail_normal_texture(self, context):
        material = MSFS2020_Material_Property_Update.getMaterial(self)
        if material is not None and type(material) is not MSFS2020_Invisible:
            material.setDetailNormalTex(self.msfs_detail_normal_texture)

    @staticmethod
    def update_blend_mask_texture(self, context):
        material = MSFS2020_Material_Property_Update.getMaterial(self)
        if material is not None and type(material) is MSFS2020_Standard:
            material.setBlendMaskTex(self.msfs_blend_mask_texture)
            material.toggleVertexBlendMapMask(self.msfs_blend_mask_texture is None)

    @staticmethod
    def update_extra_slot1_texture(self, context):
        material = MSFS2020_Material_Property_Update.getMaterial(self)
        if material is not None and (type(material) is MSFS2020_Anisotropic or type(material) is MSFS2020_Hair):
            material.setAnisotropicTex(self.msfs_extra_slot1_texture)

    @staticmethod
    def update_dirt_texture(self, context):
        material = MSFS2020_Material_Property_Update.getMaterial(self)
        if material is not None and type(material) is MSFS2020_Clearcoat:
            material.setClearcoatDirtTexture(self.msfs_dirt_texture)

    @staticmethod
    def update_alpha_mode(self, context):
        material = MSFS2020_Material(self)
        material.setBlendMode(self.msfs_alpha_mode)

    # Update functions for the "tint" parameters:
    @staticmethod
    def update_base_color(self, context):
        material = MSFS2020_Material_Property_Update.getMaterial(self)
        if material is not None:
            material.setBaseColor(self.msfs_base_color_factor)

    @staticmethod
    def update_emissive_color(self, context):
        material = MSFS2020_Material_Property_Update.getMaterial(self)
        if material is not None:
            material.setEmissiveColor(self.msfs_emissive_factor)

    @staticmethod
    def update_emissive_scale(self, context):
        material = MSFS2020_Material_Property_Update.getMaterial(self)
        if material is not None:
            material.setEmissiveScale(self.msfs_emissive_scale)

    @staticmethod
    def update_metallic_scale(self, context):
        material = MSFS2020_Material_Property_Update.getMaterial(self)
        if material is not None:
            material.setMetallicScale(self.msfs_metallic_factor)

    @staticmethod
    def update_roughness_scale(self, context):
        material = MSFS2020_Material_Property_Update.getMaterial(self)
        if material is not None:
            material.setRoughnessScale(self.msfs_roughness_factor)

    @staticmethod
    def update_normal_scale(self, context):
        material = MSFS2020_Material_Property_Update.getMaterial(self)
        if material is not None:
            material.setNormalScale(self.msfs_normal_scale)

    @staticmethod
    def update_color_sss(self, context):
        material = MSFS2020_Material_Property_Update.getMaterial(self)
        if material is not None and type(material) is MSFS2020_SSS:
            material.setSSSColor(self.msfs_sss_color)

    @staticmethod
    def update_double_sided(self, context):
        self.use_backface_culling = not self.msfs_double_sided

    @staticmethod
    def update_alpha_cutoff(self, context):
        self.alpha_threshold = self.msfs_alpha_cutoff
        
    @staticmethod
    def update_detail_uv(self, context):
        material = MSFS2020_Material_Property_Update.getMaterial(self)
        if material is None:
            return
        
        material.setUV(
            self.msfs_detail_uv_scale, 
            self.msfs_detail_uv_offset_u,
            self.msfs_detail_uv_offset_v, 
            self.msfs_detail_normal_scale
        )
