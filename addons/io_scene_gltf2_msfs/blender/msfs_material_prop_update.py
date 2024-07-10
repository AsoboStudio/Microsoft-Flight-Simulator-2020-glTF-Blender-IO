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

from .material.msfs_material_anisotropic import MSFS_Anisotropic
from .material.msfs_material_clearcoat import MSFS_Clearcoat
from .material.msfs_material_environment_occluder import \
    MSFS_Environment_Occluder
from .material.msfs_material_fake_terrain import MSFS_Fake_Terrain
from .material.msfs_material_fresnel_fade import MSFS_Fresnel_Fade
from .material.msfs_material_geo_decal import MSFS_Geo_Decal
from .material.msfs_material_geo_decal_frosted import MSFS_Geo_Decal_Frosted
from .material.msfs_material_ghost import MSFS_Ghost
from .material.msfs_material_glass import MSFS_Glass
from .material.msfs_material_hair import MSFS_Hair
from .material.msfs_material_invisible import MSFS_Invisible
from .material.msfs_material_parallax import MSFS_Parallax
from .material.msfs_material_porthole import MSFS_Porthole
from .material.msfs_material_sss import MSFS_SSS
from .material.msfs_material_standard import MSFS_Standard
from .material.msfs_material_windshield import MSFS_Windshield
from .msfs_material_function import MSFS_Material


class MSFS_Material_Property_Update:

    @staticmethod
    def getMaterial(mat):
        if mat.msfs_material_type == "msfs_standard":
            return MSFS_Standard(mat)
        elif mat.msfs_material_type == "msfs_geo_decal":
            return MSFS_Geo_Decal(mat)
        elif mat.msfs_material_type == "msfs_geo_decal_frosted":
            return MSFS_Geo_Decal_Frosted(mat)
        elif mat.msfs_material_type == "msfs_windshield":
            return MSFS_Windshield(mat)
        elif mat.msfs_material_type == "msfs_porthole":
            return MSFS_Porthole(mat)
        elif mat.msfs_material_type == "msfs_glass":
            return MSFS_Glass(mat)
        elif mat.msfs_material_type == "msfs_clearcoat":
            return MSFS_Clearcoat(mat)
        elif mat.msfs_material_type == "msfs_parallax":
            return MSFS_Parallax(mat)
        elif mat.msfs_material_type == "msfs_anisotropic":
            return MSFS_Anisotropic(mat)
        elif mat.msfs_material_type == "msfs_hair":
            return MSFS_Hair(mat)
        elif mat.msfs_material_type == "msfs_sss":
            return MSFS_SSS(mat)
        elif mat.msfs_material_type == "msfs_invisible":
            return MSFS_Invisible(mat)
        elif mat.msfs_material_type == "msfs_fake_terrain":
            return MSFS_Fake_Terrain(mat)
        elif mat.msfs_material_type == "msfs_fresnel_fade":
            return MSFS_Fresnel_Fade(mat)
        elif mat.msfs_material_type == "msfs_environment_occluder":
            return MSFS_Environment_Occluder(mat)
        elif mat.msfs_material_type == "msfs_ghost":
            return MSFS_Ghost(mat)

    @staticmethod
    def update_msfs_material_type(self, context):
        msfs_mat = None
        if self.msfs_material_type == "msfs_standard":
            msfs_mat = MSFS_Standard(self, buildTree=True)
            self.msfs_alpha_mode = "OPAQUE"
        elif self.msfs_material_type == "msfs_geo_decal":
            msfs_mat = MSFS_Geo_Decal(self, buildTree=True)
            self.msfs_alpha_mode = "BLEND"
        elif self.msfs_material_type == "msfs_geo_decal_frosted":
            msfs_mat = MSFS_Geo_Decal_Frosted(self, buildTree=True)
            self.msfs_alpha_mode = "BLEND"
        elif self.msfs_material_type == "msfs_windshield":
            msfs_mat = MSFS_Windshield(self, buildTree=True)
            self.msfs_alpha_mode = "BLEND"
            self.msfs_metallic_factor = 0.0
            self.msfs_roughness_factor = 0.1
            self.msfs_base_color_factor = [1.0, 1.0, 1.0, 0.1]
        elif self.msfs_material_type == "msfs_porthole":
            msfs_mat = MSFS_Porthole(self, buildTree=True)
            self.msfs_alpha_mode = "OPAQUE"
        elif self.msfs_material_type == "msfs_glass":
            msfs_mat = MSFS_Glass(self, buildTree=True)
            self.msfs_alpha_mode = "BLEND"
            self.msfs_metallic_factor = 0.0
            self.msfs_roughness_factor = 0.1
            self.msfs_base_color_factor = [1.0, 1.0, 1.0, 0.1]
        elif self.msfs_material_type == "msfs_clearcoat":
            msfs_mat = MSFS_Clearcoat(self, buildTree=True)
            self.msfs_alpha_mode = "OPAQUE"
        elif self.msfs_material_type == "msfs_parallax":
            msfs_mat = MSFS_Parallax(self, buildTree=True)
            self.msfs_alpha_mode = "MASK"
        elif self.msfs_material_type == "msfs_anisotropic":
            msfs_mat = MSFS_Anisotropic(self, buildTree=True)
            self.msfs_alpha_mode = "OPAQUE"
        elif self.msfs_material_type == "msfs_hair":
            msfs_mat = MSFS_Hair(self, buildTree=True)
            self.msfs_alpha_mode = "OPAQUE"
        elif self.msfs_material_type == "msfs_sss":
            msfs_mat = MSFS_SSS(self, buildTree=True)
            self.msfs_alpha_mode = "OPAQUE"
        elif self.msfs_material_type == "msfs_invisible":
            msfs_mat = MSFS_Invisible(self, buildTree=True)
            self.msfs_no_cast_shadow = True
            self.msfs_alpha_mode = "BLEND"
            self.msfs_base_color_factor = [0.8, 0.0, 0.0, 0.1]
            self.msfs_emissive_factor = [0.8, 0.0, 0.0]
        elif self.msfs_material_type == "msfs_fake_terrain":
            msfs_mat = MSFS_Fake_Terrain(self, buildTree=True)
            self.msfs_alpha_mode = "OPAQUE"
        elif self.msfs_material_type == "msfs_fresnel_fade":
            msfs_mat = MSFS_Fresnel_Fade(self, buildTree=True)
            self.msfs_alpha_mode = "BLEND"
        elif self.msfs_material_type == "msfs_environment_occluder":
            msfs_mat = MSFS_Environment_Occluder(self, buildTree=True)
            self.msfs_no_cast_shadow = True
            self.msfs_alpha_mode = "BLEND"
            self.msfs_base_color_factor = [0.0, 0.8, 0.0, 0.1]
            self.msfs_emissive_factor = [0.0, 0.8, 0.0]
        elif self.msfs_material_type == "msfs_ghost":
            msfs_mat = MSFS_Ghost(self, buildTree=True)
            self.msfs_no_cast_shadow = True
            self.msfs_alpha_mode = "BLEND"
        else:
            MSFS_Material_Property_Update.reset_material_prop_object(self)
            msfs_mat = MSFS_Material(self)
            msfs_mat.revertToPBRShaderTree()
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
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is not None and type(msfs) is not MSFS_Invisible:
            msfs.setBaseColorTex(self.msfs_base_color_texture)

    @staticmethod
    def update_comp_texture(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is not None and type(msfs) is not MSFS_Invisible:
            msfs.setCompTex(self.msfs_occlusion_metallic_roughness_texture)

    @staticmethod
    def update_normal_texture(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is not None and type(msfs) is not MSFS_Invisible:
            msfs.setNormalTex(self.msfs_normal_texture)

    @staticmethod
    def update_emissive_texture(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is not None and type(msfs) is not MSFS_Invisible:
            msfs.setEmissiveTexture(self.msfs_emissive_texture)

    @staticmethod
    def update_detail_color_texture(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is not None and type(msfs) is not MSFS_Invisible:
            msfs.setDetailColorTex(self.msfs_detail_color_texture)

    @staticmethod
    def update_detail_comp_texture(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is not None and type(msfs) is not MSFS_Invisible:
            msfs.setDetailCompTex(self.msfs_detail_occlusion_metallic_roughness_texture)

    @staticmethod
    def update_detail_normal_texture(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is not None and type(msfs) is not MSFS_Invisible:
            msfs.setDetailNormalTex(self.msfs_detail_normal_texture)

    @staticmethod
    def update_blend_mask_texture(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is not None and type(msfs) is MSFS_Standard:
            msfs.setBlendMaskTex(self.msfs_blend_mask_texture)
            msfs.toggleVertexBlendMapMask(self.msfs_blend_mask_texture is None)

    @staticmethod
    def update_extra_slot1_texture(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is not None and (type(msfs) is MSFS_Anisotropic or type(msfs) is MSFS_Hair):
            msfs.setAnisotropicTex(self.msfs_extra_slot1_texture)

    @staticmethod
    def update_dirt_texture(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is not None and type(msfs) is MSFS_Clearcoat:
            msfs.setClearcoatDirtTexture(self.msfs_dirt_texture)

    @staticmethod
    def update_alpha_mode(self, context):
        msfs_mat = MSFS_Material(self)
        msfs_mat.setBlendMode(self.msfs_alpha_mode)

    # Update functions for the "tint" parameters:
    @staticmethod
    def update_base_color(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is not None:
            msfs.setBaseColor(self.msfs_base_color_factor)

    @staticmethod
    def update_emissive_color(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is not None:
            msfs.setEmissiveColor(self.msfs_emissive_factor)

    @staticmethod
    def update_emissive_scale(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is not None:
            if type(msfs) is MSFS_Windshield or type(msfs) is MSFS_Glass:
                msfs.setEmissiveScale(0.1)
            else:
                msfs.setEmissiveScale(self.msfs_emissive_scale)

    @staticmethod
    def update_metallic_scale(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is not None:
            msfs.setMetallicScale(self.msfs_metallic_factor)

    @staticmethod
    def update_roughness_scale(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is not None:
            msfs.setRoughnessScale(self.msfs_roughness_factor)

    @staticmethod
    def update_normal_scale(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is not None:
            msfs.setNormalScale(self.msfs_normal_scale)

    @staticmethod
    def update_color_sss(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is not None and type(msfs) is MSFS_SSS:
            msfs.setSSSColor(self.msfs_sss_color)

    @staticmethod
    def update_double_sided(self, context):
        self.use_backface_culling = not self.msfs_double_sided

    @staticmethod
    def update_alpha_cutoff(self, context):
        self.alpha_threshold = self.msfs_alpha_cutoff
        
    @staticmethod
    def update_detail_uv(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is not None:
            msfs.setUV(self.msfs_detail_uv_scale, self.msfs_detail_uv_offset_u, self.msfs_detail_uv_offset_v, self.msfs_detail_normal_scale)
