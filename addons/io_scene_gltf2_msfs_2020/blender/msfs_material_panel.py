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

from .msfs_material_prop_update import MSFS2020_Material_Property_Update

# TODO: Remove eventually
class MSFS2020_OT_MigrateMaterialData(bpy.types.Operator): 
    """
    This addon changes some of the internal property names. 
    This current material has older properties, and is able to be migrated.\n
    WARNING: This removes all the old properties from the material
    """

    bl_idname = "msfs2020.migrate_material_data"
    bl_label = "Migrate Material Data"

    old_property_to_new_mapping = {
        "msfs_color_sss": "msfs_sss_color",
        "msfs_use_pearl_effect ": "msfs_use_pearl",
        "msfs_decal_color_blend_factor": "msfs_base_color_blend_factor",
        "msfs_decal_metal_blend_factor": "msfs_metallic_blend_factor",
        "msfs_decal_normal_blend_factor": "msfs_normal_blend_factor",
        "msfs_decal_roughness_blend_factor": "msfs_roughness_blend_factor",
        "msfs_decal_occlusion_blend_factor": "msfs_occlusion_blend_factor",
        "msfs_decal_emissive_blend_factor": "msfs_emissive_blend_factor",
        "msfs_fresnel_opacity_bias": "msfs_fresnel_opacity_offset",
        "msfs_parallax_room_number": "msfs_parallax_room_number_xy",
        "msfs_geo_decal_blend_factor_color": "msfs_base_color_blend_factor",
        "msfs_geo_decal_blend_factor_metal": "msfs_metallic_blend_factor",
        "msfs_geo_decal_blend_factor_normal": "msfs_normal_blend_factor",
        "msfs_geo_decal_blend_factor_roughness": "msfs_roughness_blend_factor",
        "msfs_geo_decal_blend_factor_blast_sys": "msfs_occlusion_blend_factor",
        "msfs_geo_decal_blend_factor_melt_sys": "msfs_emissive_blend_factor",
        "msfs_draw_order": "msfs_draw_order_offset",
        "msfs_road_material": "msfs_road_collision_material",
        "msfs_uv_clamp_x": "msfs_clamp_uv_x",
        "msfs_uv_clamp_y": "msfs_clamp_uv_y",
        "msfs_uv_clamp_z": "msfs_clamp_uv_z",
        "msfs_roughness_scale": "msfs_roughness_factor",
        "msfs_metallic_scale": "msfs_metallic_factor",
        "msfs_detail_uv_offset_x": "msfs_detail_uv_offset_u",
        "msfs_detail_uv_offset_y": "msfs_detail_uv_offset_v",
        "msfs_blend_threshold": "msfs_detail_blend_threshold",
        "msfs_albedo_texture": "msfs_base_color_texture",
        "msfs_metallic_texture": "msfs_occlusion_metallic_roughness_texture",
        "msfs_detail_albedo_texture": "msfs_detail_color_texture",
        "msfs_detail_metallic_texture": "msfs_detail_occlusion_metallic_roughness_texture",
        "msfs_anisotropic_direction_texture": "msfs_extra_slot1_texture",
        "msfs_clearcoat_texture": "msfs_dirt_texture",
        "msfs_behind_glass_texture": "msfs_detail_color_texture",
    }

    @staticmethod
    def old_properties_present(active_material):
        # Don't unnecessarily loop if we have no properties on the material
        if len(active_material.keys()) <= 0: 
            return False
        
        for old_property in MSFS2020_OT_MigrateMaterialData.old_property_to_new_mapping:
            if active_material.get(old_property) is not None:
                return True
            
        return False

    def execute(self, context):
        active_material = context.active_object.active_material
        for (
            old_property,
            new_property,
        ) in MSFS2020_OT_MigrateMaterialData.old_property_to_new_mapping.items():
            if active_material.get(old_property) is None:
                continue
            
            # msfs_behind_glass_texture and msfs_detail_albedo_texture 
            # are special cases as they are they write to the same property
            if (
                active_material.get("msfs_material_mode") == "msfs_windshield" 
                and old_property == "msfs_behind_glass_texture"
            ):
                continue
            
            if (
                active_material.get("msfs_material_mode") == "msfs_parallax" 
                and old_property == "msfs_detail_albedo_texture"
            ):
                continue
            active_material[new_property] = active_material[old_property]

            del active_material[old_property]

        # Base color is a special case - can only have 3 values, we need 4
        base_color = [1,1,1,1]
        alpha = 1
        if active_material.get("msfs_color_alpha_mix"):
            alpha = active_material.get("msfs_color_alpha_mix")
            base_color[3] = alpha
            
        if active_material.get("msfs_color_albedo_mix"):
            base_color = list(active_material.get("msfs_color_albedo_mix"))
            if len(base_color) == 3:
                base_color.append(alpha)
                
        active_material.msfs_base_color_factor = base_color

        # Emissive factor is also a special case - old material system had 4 floats, we only need 3
        if active_material.get("msfs_color_emissive_mix"):
            active_material.msfs_emissive_factor = active_material.get("msfs_color_emissive_mix")[0:3]

        # Do our enums manually as only their index of the value are stored - not the string
        if active_material.get("msfs_blend_mode"):
            old_alpha_order = [
                "OPAQUE",
                "MASK",  # Changed from old version - matches new name
                "BLEND",
                "DITHER",
            ]
            active_material.msfs_alpha_mode = old_alpha_order[active_material["msfs_blend_mode"]]

            del active_material["msfs_blend_mode"]

        if active_material.get("msfs_material_mode"):
            # Assuming the user uninstalled the old plugin, the index of the 
            # value will be stored instead of the name of the current material. 
            # Replicate the order here
            old_material_older = [
                "NONE",
                "msfs_standard",
                "msfs_anisotropic",
                "msfs_sss",
                "msfs_glass",
                "msfs_geo_decal",  # Changed from old version - matches new name
                "msfs_clearcoat",
                "msfs_environment_occluder",  # Changed from old version - matches new name
                "msfs_fake_terrain",
                "msfs_fresnel_fade",  # Changed from old version - matches new name
                "msfs_windshield",
                "msfs_porthole",
                "msfs_parallax",
                "msfs_geo_decal_frosted",  # Changed from old version - matches new name
                "msfs_hair",
                "msfs_invisible",
            ]
            active_material.msfs_material_type = old_material_older[active_material["msfs_material_mode"]]

            del active_material["msfs_material_mode"]

        MSFS2020_Material_Property_Update.update_msfs_material_type(active_material, context)

        return {"FINISHED"}


class MSFS2020_PT_Material(bpy.types.Panel):
    bl_label = "MSFS2020 Material Params"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return context.active_object.active_material is not None

    def draw_prop(
        self,
        layout,
        mat,
        prop,
        enabled=True,
        visible=True,
        text="",
    ):
        if not visible:
            return
        
        column = layout.column()
        if text:
            column.prop(mat, prop, text=text)
        else:
            column.prop(mat, prop)

        column.enabled = enabled

    def draw_texture_prop(
        self,
        layout,
        mat,
        prop,
        enabled=True,
        visible=True,
        text="",
    ):
        if not visible:
            return
        
        column = layout.column()
        if text:
            column.label(text=text)

        column.template_ID(mat, prop, new="image.new", open="image.open")
        column.enabled = enabled

    def draw(self, context):
        layout = self.layout
        # Disabled animation UI until material animations are properly implemented
        # layout.use_property_split = True
        # layout.use_property_decorate = True

        active_material = context.active_object.active_material

        if not active_material:
            return
        
        if MSFS2020_OT_MigrateMaterialData.old_properties_present(active_material):
            layout.operator(MSFS2020_OT_MigrateMaterialData.bl_idname)

        self.draw_prop(layout, active_material, "msfs_material_type")

        if active_material.msfs_material_type != "NONE":
            self.draw_prop(layout, active_material, "msfs_base_color_factor")
            self.draw_prop(
                layout,
                active_material,
                "msfs_emissive_factor",
                enabled=(
                    active_material.msfs_material_type
                    not in ["msfs_invisible", "msfs_environment_occluder"]
                ),
            )

            # Alpha mode
            box = layout.box()
            box.label(text="Alpha Mode")
            box.enabled = active_material.msfs_material_type in [
                "msfs_standard",
                "msfs_anisotropic",
                "msfs_hair",
                "msfs_sss",
                "msfs_fresnel_fade",
                "msfs_clearcoat",
            ]
            self.draw_prop(box, active_material, "msfs_alpha_mode")

            # Render params
            box = layout.box()
            box.label(text="Render Parameters")
            box.enabled = active_material.msfs_material_type not in [
                "msfs_invisible",
                "msfs_environment_occluder",
            ]
            self.draw_prop(box, active_material, "msfs_draw_order_offset")
            self.draw_prop(
                box,
                active_material,
                "msfs_no_cast_shadow",
                enabled=(active_material.msfs_material_type != "msfs_ghost"),
            )
            self.draw_prop(box, active_material, "msfs_double_sided")
            self.draw_prop(
                box,
                active_material,
                "msfs_day_night_cycle",
                enabled=(active_material.msfs_material_type == "msfs_standard"),
            )
            self.draw_prop(box, active_material, "msfs_disable_motion_blur")

            # Gameplay params
            box = layout.box()
            box.label(text="Gameplay Parameters")
            box.enabled = active_material.msfs_material_type != "msfs_environment_occluder"
            self.draw_prop(box, active_material, "msfs_collision_material")
            self.draw_prop(box, active_material, "msfs_road_collision_material")

            # UV options
            box = layout.box()
            box.label(text="UV Options")
            box.enabled = active_material.msfs_material_type not in [
                "msfs_invisible",
                "msfs_environment_occluder",
            ]
            self.draw_prop(box, active_material, "msfs_uv_offset_u")
            self.draw_prop(box, active_material, "msfs_uv_offset_v")
            self.draw_prop(box, active_material, "msfs_uv_tiling_u")
            self.draw_prop(box, active_material, "msfs_uv_tiling_v")
            self.draw_prop(box, active_material, "msfs_uv_rotation")

            # UV clamp
            box = layout.box()
            box.label(text="UV Clamp")
            box.enabled = active_material.msfs_material_type != "msfs_environment_occluder"
            self.draw_prop(box, active_material, "msfs_clamp_uv_x")
            self.draw_prop(box, active_material, "msfs_clamp_uv_y")

            # General params
            box = layout.box()
            box.label(text="General Parameters")
            box.enabled = active_material.msfs_material_type not in [
                "msfs_invisible",
                "msfs_environment_occluder",
            ]
            self.draw_prop(box, active_material, "msfs_metallic_factor")
            self.draw_prop(box, active_material, "msfs_roughness_factor")
            self.draw_prop(box, active_material, "msfs_normal_scale")
            self.draw_prop(
                box,
                active_material,
                "msfs_alpha_cutoff",
                enabled=(
                    active_material.msfs_material_type
                    in [
                        "msfs_standard",
                        "msfs_anisotropic",
                        "msfs_hair",
                        "msfs_sss",
                        "msfs_fresnel_fade",
                        "msfs_clearcoat",
                    ]
                    and active_material.msfs_alpha_mode == "MASK"
                ),
            )
            self.draw_prop(
                box,
                active_material,
                "msfs_detail_uv_scale",
                enabled=(
                    active_material.msfs_material_type
                    not in ["msfs_parallax", "msfs_fresnel_fade", "msfs_sss"]
                ),
            )
            self.draw_prop(
                box,
                active_material,
                "msfs_detail_uv_offset_u",
                enabled=(
                    active_material.msfs_material_type
                    not in ["msfs_parallax", "msfs_fresnel_fade", "msfs_sss"]
                ),
            )
            self.draw_prop(
                box,
                active_material,
                "msfs_detail_uv_offset_v",
                enabled=(
                    active_material.msfs_material_type
                    not in ["msfs_parallax", "msfs_fresnel_fade", "msfs_sss"]
                ),
            )
            self.draw_prop(
                box,
                active_material,
                "msfs_detail_normal_scale",
                enabled=(
                    active_material.msfs_material_type
                    not in ["msfs_parallax", "msfs_fresnel_fade", "msfs_sss"]
                ),
            )
            self.draw_prop(
                box,
                active_material,
                "msfs_detail_blend_threshold",
                enabled=(
                    active_material.msfs_material_type not in ["msfs_fresnel_fade", "msfs_sss"]
                    and active_material.msfs_blend_mask_texture is not None
                ),
            )
            self.draw_prop(
                box,
                active_material,
                "msfs_emissive_scale",
                enabled=(
                    active_material.msfs_material_type
                    not in ["msfs_invisible", "msfs_environment_occluder"]
                ),
            )

            # Decal params
            if active_material.msfs_material_type in [
                "msfs_geo_decal",
                "msfs_geo_decal_frosted",
            ]:
                box = layout.box()
                box.label(text="Decal Blend Factors")
                box.enabled = active_material.msfs_material_type in [
                    "msfs_geo_decal",
                    "msfs_geo_decal_frosted",
                ]
                self.draw_prop(box, active_material, "msfs_base_color_blend_factor")
                self.draw_prop(box, active_material, "msfs_roughness_blend_factor")
                self.draw_prop(box, active_material, "msfs_metallic_blend_factor")
                self.draw_prop(
                    box,
                    active_material,
                    "msfs_occlusion_blend_factor",
                    text="Blast Sys Blend Factor"
                    if active_material.msfs_material_type == "msfs_geo_decal_frosted"
                    else "",
                )
                self.draw_prop(box, active_material, "msfs_normal_blend_factor")
                self.draw_prop(
                    box,
                    active_material,
                    "msfs_emissive_blend_factor",
                    text="Melt Sys Blend Factor"
                    if active_material.msfs_material_type == "msfs_geo_decal_frosted"
                    else "",
                )

            # SSS params - enabled
            if active_material.msfs_material_type in ["msfs_sss", "msfs_hair"]:
                box = layout.box()
                box.label(text="SSS Parameters")
                box.enabled = active_material.msfs_material_type  == "msfs_sss" or active_material.msfs_material_type == "msfs_hair"
                self.draw_prop(
                    box, 
                    active_material,
                    "msfs_sss_color",
                    enabled=True
                )

            # Glass params
            if active_material.msfs_material_type == "msfs_glass":
                box = layout.box()
                box.label(text="Glass Parameters")
                box.enabled = active_material.msfs_material_type == "msfs_glass"
                self.draw_prop(box, active_material, "msfs_glass_reflection_mask_factor")
                self.draw_prop(box, active_material, "msfs_glass_deformation_factor")

            # Parallax params
            if active_material.msfs_material_type == "msfs_parallax":
                box = layout.box()
                box.label(text="Parallax Parameters")
                box.enabled = active_material.msfs_material_type == "msfs_parallax"
                self.draw_prop(box, active_material, "msfs_parallax_scale")
                self.draw_prop(box, active_material, "msfs_parallax_room_size_x")
                self.draw_prop(box, active_material, "msfs_parallax_room_size_y")
                self.draw_prop(box, active_material, "msfs_parallax_room_number_xy")
                self.draw_prop(box, active_material, "msfs_parallax_corridor")

            # Fresnel params
            if active_material.msfs_material_type == "msfs_fresnel_fade":
                box = layout.box()
                box.label(text="Fresnel Parameters")
                box.enabled = active_material.msfs_material_type == "msfs_fresnel_fade"
                self.draw_prop(box, active_material, "msfs_fresnel_factor")
                self.draw_prop(box, active_material, "msfs_fresnel_opacity_offset")

            # Ghost params
            if active_material.msfs_material_type == "msfs_ghost":
                box = layout.box()
                box.label(text="Ghost Parameters")
                box.enabled = active_material.msfs_material_type == "msfs_ghost"
                self.draw_prop(box, active_material, "msfs_ghost_bias")
                self.draw_prop(box, active_material, "msfs_ghost_power")
                self.draw_prop(box, active_material, "msfs_ghost_scale")

            # Windshield params
            if active_material.msfs_material_type == "msfs_windshield":
                box = layout.box()
                box.label(text="Windshield Parameters")
                box.enabled = active_material.msfs_material_type == "msfs_windshield"
                self.draw_prop(box, active_material, "msfs_rain_drop_scale")
                self.draw_prop(box, active_material, "msfs_wiper_1_state")
                self.draw_prop(box, active_material, "msfs_wiper_2_state")
                self.draw_prop(box, active_material, "msfs_wiper_3_state", visible=False)
                self.draw_prop(box, active_material, "msfs_wiper_4_state", visible=False)

            # Pearl params
            if active_material.msfs_material_type == "msfs_standard":
                box = layout.box()
                box.label(text="Pearl Parameters")
                box.enabled = active_material.msfs_material_type == "msfs_standard"
                self.draw_prop(box, active_material, "msfs_use_pearl")
                self.draw_prop(box, active_material, "msfs_pearl_shift")
                self.draw_prop(box, active_material, "msfs_pearl_range")
                self.draw_prop(box, active_material, "msfs_pearl_brightness")

            # Textures
            if active_material.msfs_material_type in ("msfs_invisible", "msfs_environment_occluder"):
                return
            
            box = layout.box()
            box.label(text="Textures")

            # In the 3DS Max exporter, the textures have different display 
            # names depending on material type and other properties used. 
            # We replicate that process here
            base_color_tex_name = "Base Color"
            occlusion_metallic_roughness_texture_name = "Occlusion (R), Roughness (G), Metallic (B)"
            normal_texture_name = "Normal"
            blend_mask_texture_name = "Blend Mask"
            dirt_texture_name = "Clearcoat amount (R), Clearcoat rough (G)"
            extra_slot1_texture = "Extra Slot 1"
            emissive_texture_name = "Emissive"
            detail_color_texture_name = "Secondary Color (RGB), Alpha (A)"
            detail_occlusion_metallic_roughness_texture_name = "Secondary Occ (R), Rough (G), Metal (B)"
            detail_normal_texture_name = "Secondary Normal"

            if active_material.msfs_blend_mask_texture is None:
                detail_color_texture_name = "Detail Color (RGB), Alpha (A)"
                detail_normal_texture_name = "Detail Normal"
                detail_occlusion_metallic_roughness_texture_name = "Detail Occlusion (R), Roughness (G), Metallic (B)"

            if active_material.msfs_material_type == "msfs_windshield":
                emissive_texture_name = "Secondary Details(A)"
                extra_slot1_texture = "Wiper Mask (RG)"
                detail_color_texture_name = "Details Scratch(R), Icing Mask(G), Fingerprints(B)"
                detail_normal_texture_name = "Icing Normal (use DetailMap UV)"
                
            elif active_material.msfs_material_type == "msfs_geo_decal_frosted":
                detail_occlusion_metallic_roughness_texture_name = "Melt pattern (R), Roughness (G), Metallic (B)"
                
            elif active_material.msfs_material_type == "msfs_parallax":
                base_color_tex_name = "Front Glass Color"
                normal_texture_name = "Front Glass Normal"
                detail_color_texture_name = "Behind Glass Color (RGB), Alpha (A)"
                emissive_texture_name = "Emissive Ins Window (RGB), offset Time (A)"
                
            elif active_material.msfs_material_type in ["msfs_anisotropic", "msfs_hair"]:
                extra_slot1_texture = "Anisotropic direction (RG)"

            self.draw_texture_prop(
                box, 
                active_material, 
                "msfs_base_color_texture", 
                text=base_color_tex_name
            )
            self.draw_texture_prop(
                box,
                active_material,
                "msfs_occlusion_metallic_roughness_texture",
                text=occlusion_metallic_roughness_texture_name,
            )
            self.draw_texture_prop(
                box, 
                active_material,
                "msfs_normal_texture",
                text=normal_texture_name
            )
            self.draw_texture_prop(
                box,
                active_material,
                "msfs_emissive_texture",
                text=emissive_texture_name
            )

            if (
                active_material.msfs_material_type not in (
                    "msfs_hair",
                    "msfs_sss",
                    "msfs_fresnel_fade",
                )
            ):
                self.draw_texture_prop(
                    box,
                    active_material,
                    "msfs_detail_color_texture",
                    text=detail_color_texture_name,
                )
                
            if (
                active_material.msfs_material_type not in (
                    "msfs_parallax",
                    "msfs_hair",
                    "msfs_sss",
                    "msfs_fresnel_fade",
                )
            ):
                self.draw_texture_prop(
                    box,
                    active_material,
                    "msfs_detail_normal_texture",
                    text=detail_normal_texture_name,
                )
                
                self.draw_texture_prop(
                    box,
                    active_material,
                    "msfs_detail_occlusion_metallic_roughness_texture",
                    text=detail_occlusion_metallic_roughness_texture_name,
                )
                
            if (
                active_material.msfs_material_type not in (
                    "msfs_geo_decal_frosted",
                    "msfs_parallax",
                    "msfs_hair",
                    "msfs_sss",
                    "msfs_fresnel_fade",
                    "msfs_ghost",
                )
            ):
                self.draw_texture_prop(
                    box,
                    active_material,
                    "msfs_blend_mask_texture",
                    text=blend_mask_texture_name,
                )
                
            if (
                active_material.msfs_material_type in (
                    "msfs_winshield",
                    "msfs_anisotropic",
                    "msfs_hair",
                )
            ):
                self.draw_texture_prop(
                    box,
                    active_material,
                    "msfs_extra_slot1_texture",
                    text=extra_slot1_texture,
                )
                
            if active_material.msfs_material_type == "msfs_clearcoat":
                self.draw_texture_prop(
                    box,
                    active_material,
                    "msfs_dirt_texture",
                    text=dirt_texture_name
                )
