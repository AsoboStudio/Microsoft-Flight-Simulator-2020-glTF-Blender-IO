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

import os
import uuid
import xml.dom.minidom
import xml.etree.ElementTree as etree

import bpy


def export_blender_under_3_3(file_path, settings):
    return bpy.ops.export_scene.gltf(
        filepath=file_path,
        check_existing=True,
        export_format="GLTF_SEPARATE",
        export_copyright=settings.export_copyright,
        export_image_format=settings.export_image_format,
        export_texture_dir=settings.export_texture_dir,
        export_keep_originals=settings.export_keep_originals,
        export_texcoords=settings.export_texcoords,
        export_normals=settings.export_normals,
        export_draco_mesh_compression_enable=settings.export_draco_mesh_compression_enable,
        export_draco_mesh_compression_level=settings.export_draco_mesh_compression_level,
        export_draco_position_quantization=settings.export_draco_position_quantization,
        export_draco_normal_quantization=settings.export_draco_normal_quantization,
        export_draco_texcoord_quantization=settings.export_draco_texcoord_quantization,
        export_draco_color_quantization=settings.export_draco_color_quantization,
        export_draco_generic_quantization=settings.export_draco_generic_quantization,
        export_tangents=settings.export_tangents,
        export_materials=settings.export_materials,
        export_colors=settings.export_colors,
        use_mesh_edges=settings.use_mesh_edges,
        use_mesh_vertices=settings.use_mesh_vertices,
        export_cameras=settings.export_cameras,
        use_selection=settings.use_selection,
        use_visible=settings.use_visible,
        use_renderable=settings.use_renderable,
        use_active_collection=settings.use_active_collection,
        export_yup=settings.export_yup,
        export_apply=settings.export_apply,
        export_animations=settings.export_animations,
        export_frame_range=settings.export_frame_range,
        export_frame_step=settings.export_frame_step,
        export_force_sampling=settings.export_force_sampling,
        export_def_bones=settings.export_def_bones,
        optimize_animation_size=settings.export_optimize_animation_size,
        export_current_frame=settings.export_current_frame,
        export_skins=settings.export_skins,
        export_all_influences=settings.export_all_influences,
        export_morph=settings.export_morph,
        export_morph_normal=settings.export_morph_normal,
        export_morph_tangent=settings.export_morph_tangent,
        export_lights=settings.export_lights,
        will_save_settings=settings.will_save_settings,
        export_displacement=settings.export_displacement,
    )


def export_blender_3_3(file_path, settings):
    return bpy.ops.export_scene.gltf(
        filepath=file_path,
        check_existing=True,
        export_format="GLTF_SEPARATE",
        export_copyright=settings.export_copyright,
        export_image_format=settings.export_image_format,
        export_texture_dir=settings.export_texture_dir,
        export_keep_originals=settings.export_keep_originals,
        export_texcoords=settings.export_texcoords,
        export_normals=settings.export_normals,
        export_draco_mesh_compression_enable=settings.export_draco_mesh_compression_enable,
        export_draco_mesh_compression_level=settings.export_draco_mesh_compression_level,
        export_draco_position_quantization=settings.export_draco_position_quantization,
        export_draco_normal_quantization=settings.export_draco_normal_quantization,
        export_draco_texcoord_quantization=settings.export_draco_texcoord_quantization,
        export_draco_color_quantization=settings.export_draco_color_quantization,
        export_draco_generic_quantization=settings.export_draco_generic_quantization,
        export_tangents=settings.export_tangents,
        export_materials=settings.export_materials,
        export_original_specular=False,
        export_colors=settings.export_colors,
        use_mesh_edges=settings.use_mesh_edges,
        use_mesh_vertices=settings.use_mesh_vertices,
        export_cameras=settings.export_cameras,
        use_selection=settings.use_selection,
        use_visible=settings.use_visible,
        use_renderable=settings.use_renderable,
        use_active_collection=settings.use_active_collection,
        use_active_scene=settings.use_active_scene,
        export_yup=settings.export_yup,
        export_apply=settings.export_apply,
        export_animations=settings.export_animations,
        export_frame_range=settings.export_frame_range,
        export_frame_step=settings.export_frame_step,
        export_force_sampling=settings.export_force_sampling,
        export_nla_strips_merged_animation_name=settings.export_nla_strips_merged_animation_name,
        export_def_bones=settings.export_def_bones,
        export_optimize_animation_size=settings.export_optimize_animation_size,
        export_anim_single_armature=settings.export_anim_single_armature,
        export_current_frame=settings.export_current_frame,
        export_skins=settings.export_skins,
        export_all_influences=settings.export_all_influences,
        export_morph=settings.export_morph,
        export_morph_normal=settings.export_morph_normal,
        export_morph_tangent=settings.export_morph_tangent,
        export_lights=settings.export_lights,
        will_save_settings=settings.will_save_settings,
    )


def export_blender_3_6(file_path, settings):
    return bpy.ops.export_scene.gltf(
        filepath=file_path,
        check_existing=True,
        export_format="GLTF_SEPARATE",
        export_copyright=settings.export_copyright,
        export_image_format=settings.export_image_format,
        export_texture_dir=settings.export_texture_dir,
        export_jpeg_quality=settings.export_jpeg_quality,
        export_keep_originals=settings.export_keep_originals,
        export_texcoords=settings.export_texcoords,
        export_normals=settings.export_normals,
        export_draco_mesh_compression_enable=settings.export_draco_mesh_compression_enable,
        export_draco_mesh_compression_level=settings.export_draco_mesh_compression_level,
        export_draco_position_quantization=settings.export_draco_position_quantization,
        export_draco_normal_quantization=settings.export_draco_normal_quantization,
        export_draco_texcoord_quantization=settings.export_draco_texcoord_quantization,
        export_draco_color_quantization=settings.export_draco_color_quantization,
        export_draco_generic_quantization=settings.export_draco_generic_quantization,
        export_tangents=settings.export_tangents,
        export_materials=settings.export_materials,
        export_original_specular=False,
        export_colors=settings.export_colors,
        export_attributes=settings.export_attributes,
        use_mesh_edges=settings.use_mesh_edges,
        use_mesh_vertices=settings.use_mesh_vertices,
        export_cameras=settings.export_cameras,
        use_selection=settings.use_selection,
        use_visible=settings.use_visible,
        use_renderable=settings.use_renderable,
        use_active_collection=settings.use_active_collection,
        use_active_scene=settings.use_active_scene,
        export_yup=settings.export_yup,
        export_apply=settings.export_apply,
        export_animations=settings.export_animations,
        export_frame_range=settings.export_frame_range,
        export_frame_step=settings.export_frame_step,
        export_force_sampling=settings.export_force_sampling,
        export_animation_mode=settings.export_animation_mode,
        export_nla_strips_merged_animation_name=settings.export_nla_strips_merged_animation_name,
        export_def_bones=settings.export_def_bones,
        export_optimize_animation_size=settings.export_optimize_animation_size,
        export_optimize_animation_keep_anim_armature=settings.export_optimize_animation_keep_anim_armature,
        export_optimize_animation_keep_anim_object=settings.export_optimize_animation_keep_anim_object,
        export_negative_frame=settings.export_negative_frame,
        export_anim_slide_to_zero=settings.export_anim_slide_to_zero,
        export_reset_pose_bones=settings.export_reset_pose_bones,
        export_bake_animation=settings.export_bake_animation,
        export_anim_single_armature=settings.export_anim_single_armature,
        export_current_frame=settings.export_current_frame,
        export_rest_position_armature=settings.export_rest_position_armature,
        export_anim_scene_split_object=settings.export_anim_scene_split_object,
        export_skins=settings.export_skins,
        export_all_influences=settings.export_all_influences,
        export_morph=settings.export_morph,
        export_morph_normal=settings.export_morph_normal,
        export_morph_tangent=settings.export_morph_tangent,
        export_morph_animation=settings.export_morph_animation,
        export_lights=settings.export_lights,
        will_save_settings=settings.will_save_settings,
    )


def export_blender_4_2(file_path, settings):
    return bpy.ops.export_scene.gltf(
        filepath=file_path,
        check_existing=True,
        export_format="GLTF_SEPARATE",
        export_copyright=settings.export_copyright,
        export_image_format=settings.export_image_format,
        export_jpeg_quality=settings.export_jpeg_quality,
        export_texture_dir=settings.export_texture_dir,
        export_keep_originals=settings.export_keep_originals,
        export_texcoords=settings.export_texcoords,
        export_normals=settings.export_normals,
        export_draco_mesh_compression_enable=settings.export_draco_mesh_compression_enable,
        export_draco_mesh_compression_level=settings.export_draco_mesh_compression_level,
        export_draco_position_quantization=settings.export_draco_position_quantization,
        export_draco_normal_quantization=settings.export_draco_normal_quantization,
        export_draco_texcoord_quantization=settings.export_draco_texcoord_quantization,
        export_draco_color_quantization=settings.export_draco_color_quantization,
        export_draco_generic_quantization=settings.export_draco_generic_quantization,
        export_tangents=settings.export_tangents,
        export_materials=settings.export_materials,
        export_original_specular=False,
        export_attributes=settings.export_attributes,
        use_mesh_edges=settings.use_mesh_edges,
        use_mesh_vertices=settings.use_mesh_vertices,
        export_cameras=settings.export_cameras,
        use_selection=settings.use_selection,
        use_visible=settings.use_visible,
        use_renderable=False,
        use_active_collection=False,
        use_active_scene=False,
        export_yup=settings.export_yup,
        export_apply=settings.export_apply,
        export_animations=settings.export_animations,
        export_frame_range=settings.export_frame_range,
        export_frame_step=settings.export_frame_step,
        export_force_sampling=settings.export_force_sampling,
        export_animation_mode=settings.export_animation_mode,
        export_def_bones=settings.export_def_bones,
        export_optimize_animation_size=settings.export_optimize_animation_size,
        export_optimize_animation_keep_anim_armature=settings.export_optimize_animation_keep_anim_armature,
        export_optimize_animation_keep_anim_object=settings.export_optimize_animation_keep_anim_object,
        export_negative_frame=settings.export_negative_frame,
        export_anim_slide_to_zero=settings.export_anim_slide_to_zero,
        export_reset_pose_bones=settings.export_reset_pose_bones,
        export_bake_animation=settings.export_bake_animation,
        export_anim_single_armature=settings.export_anim_single_armature,
        export_current_frame=settings.export_current_frame,
        export_rest_position_armature=settings.export_rest_position_armature,
        export_anim_scene_split_object=settings.export_anim_scene_split_object,
        export_skins=settings.export_skins,
        export_all_influences=settings.export_all_influences,
        export_morph=settings.export_morph,
        export_morph_normal=settings.export_morph_normal,
        export_morph_tangent=settings.export_morph_tangent,
        export_morph_animation=settings.export_morph_animation,
        export_lights=settings.export_lights,
        will_save_settings=settings.will_save_settings,
        export_extras=settings.export_extras,
        export_gn_mesh=settings.export_gn_mesh,
        export_gpu_instances=settings.export_gpu_instances,
        export_hierarchy_flatten_objs=settings.export_hierarchy_flatten_objs,
        export_hierarchy_full_collections=settings.export_hierarchy_full_collections,
        export_vertex_color=settings.export_vertex_color,
        export_all_vertex_colors=settings.export_all_vertex_colors,
        export_active_vertex_color_when_no_material=settings.export_active_vertex_color_when_no_material,
        export_image_add_webp=settings.export_image_add_webp,
        export_image_webp_fallback=settings.export_image_webp_fallback,
        export_unused_images=settings.export_unused_images,
        export_unused_textures=settings.export_unused_textures,
        export_try_sparse_sk=settings.export_try_sparse_sk,
        export_try_omit_sparse_sk=settings.export_try_omit_sparse_sk,
        export_armature_object_remove=settings.export_armature_object_remove,
        export_influence_nb=settings.export_influence_nb,
        export_import_convert_lighting_mode=settings.export_import_convert_lighting_mode,
        export_optimize_disable_viewport=settings.export_optimize_disable_viewport,
    )


# Operators
class MSFS2020_OT_MultiExportGLTF2(bpy.types.Operator):
    bl_idname = "export_scene.multi_export_gltf"
    bl_label = "Multi-Export glTF 2.0"

    @staticmethod
    def export(file_path):
        settings = bpy.context.scene.msfs_multi_exporter_settings
        bpy.context.scene.msfs_exporter_settings.use_unique_id = settings.use_unique_id
        gltf = None
        if bpy.app.version < (3, 3, 0):
            gltf = export_blender_under_3_3(file_path, settings)
        elif bpy.app.version < (3, 6, 0):
            gltf = export_blender_3_3(file_path, settings)
        elif bpy.app.version < (4, 2, 0):
            gltf = export_blender_3_6(file_path, settings)
        else:
            gltf = export_blender_4_2(file_path, settings)

        if gltf is None:
            print("[ASOBO] Export failed.")

    def execute(self, context):
        if context.scene.msfs_multi_exporter_current_tab == "OBJECTS":
            from .msfs_multi_export_objects import MSFS2020_LODGroupUtility

            lod_groups = context.scene.msfs_multi_exporter_lod_groups
            sort_by_collection = context.scene.multi_exporter_grouped_by_collections

            for lod_group in lod_groups:
                export_folder_path = lod_group.folder_path
                if export_folder_path == "//\\":
                    export_folder_path = export_folder_path.rsplit("\\")[0]
                export_folder_path = bpy.path.abspath(export_folder_path)
                # Generate XML if needed
                if lod_group.generate_xml:
                    xml_path = os.path.join(
                        export_folder_path, lod_group.group_name + ".xml"
                    )
                    found_guid = None

                    if os.path.exists(xml_path):
                        tree = etree.parse(xml_path)
                        found_guid = tree.getroot().attrib.get("guid")

                    if lod_group.overwrite_guid or found_guid is None:
                        root = etree.Element(
                            "ModelInfo",
                            guid="{" + str(uuid.uuid4()) + "}",
                            version="1.1",
                        )
                    else:
                        root = etree.Element(
                            "ModelInfo", guid=found_guid, version="1.1"
                        )

                    lods = etree.SubElement(root, "LODS")

                    lod_files = {}

                    for lod in lod_group.lods:
                        if not MSFS2020_LODGroupUtility.lod_is_visible(context, lod):
                            continue

                        if lod.enabled:
                            lod_files[lod.file_name] = lod.lod_value

                    lod_files = sorted(lod_files.items())
                    last_lod = list(lod_files)[-1:]

                    for file_name, lod_value in lod_files:
                        lod_element = etree.SubElement(lods, "LOD")

                        if file_name != last_lod[0]:
                            lod_element.set("minSize", str(lod_value))

                        lod_element.set(
                            "ModelFile", os.path.splitext(file_name)[0] + ".gltf"
                        )

                    if lod_files:
                        # Format XML
                        dom = xml.dom.minidom.parseString(etree.tostring(root))
                        xml_string = dom.toprettyxml(encoding="utf-8")

                        with open(xml_path, "wb") as f:
                            f.write(xml_string)
                            f.close()

                # Export glTF
                for lod in lod_group.lods:
                    if not MSFS2020_LODGroupUtility.lod_is_visible(context, lod):
                        continue

                    if lod.enabled:
                        # Use selected objects in order to specify what to export
                        for obj in bpy.context.selected_objects:
                            obj.select_set(False)

                        def select_recursive(obj):
                            if obj in list(bpy.context.window.view_layer.objects):
                                obj.select_set(True)
                                for child in obj.children:
                                    select_recursive(child)

                        if sort_by_collection:
                            for obj in lod.collection.all_objects:
                                obj.select_set(True)
                        else:
                            select_recursive(lod.objectLOD)

                        if export_folder_path != "":
                            exportPath = bpy.path.ensure_ext(
                                os.path.join(
                                    export_folder_path,
                                    os.path.splitext(lod.file_name)[0],
                                ),
                                ".gltf",
                            )
                            MSFS2020_OT_MultiExportGLTF2.export(exportPath)
                        else:
                            self.report(
                                {"ERROR"},
                                "[EXPORT][ERROR] Object : "
                                + lod.file_name
                                + " does not have an export path set.",
                            )

        elif context.scene.msfs_multi_exporter_current_tab == "PRESETS":
            presets = bpy.context.scene.msfs_multi_exporter_presets
            for preset in presets:
                if preset.enabled:
                    # Clear currently selected objects
                    for obj in bpy.context.selected_objects:
                        obj.select_set(False)

                    # Loop through all enabled layers and select all objects
                    for layer in preset.layers:
                        if layer.enabled:
                            for obj in layer.collection.all_objects:
                                if obj in list(bpy.context.window.view_layer.objects):
                                    obj.select_set(True)

                    if preset.folder_path != "":
                        export_folder_path = preset.folder_path
                        if export_folder_path == "//\\":
                            export_folder_path = export_folder_path.rsplit("\\")[0]
                        export_folder_path = bpy.path.abspath(export_folder_path)
                        exportPath = bpy.path.ensure_ext(
                            os.path.join(export_folder_path, preset.name), ".gltf"
                        )
                        MSFS2020_OT_MultiExportGLTF2.export(exportPath)
                    else:
                        self.report(
                            {"ERROR"},
                            "[EXPORT][ERROR] Preset : "
                            + preset.name
                            + " does not have an export path set.",
                        )

        return {"FINISHED"}


class MSFS2020_OT_ChangeTab(bpy.types.Operator):
    bl_idname = "msfs2020.multi_export_change_tab"
    bl_label = "Change tab"

    current_tab: bpy.props.StringProperty()

    def execute(self, context):
        context.scene.msfs_multi_exporter_current_tab = self.current_tab
        return {"FINISHED"}


# Panels
class MSFS2020_PT_MultiExporter(bpy.types.Panel):
    bl_label = "Multi-Export glTF 2.0"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Micorosoft Flight Simulator 2020 Tools"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    @classmethod
    def poll(cls, context):
        return context.scene.msfs_exporter_settings

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        current_tab = context.scene.msfs_multi_exporter_current_tab

        row = layout.row(align=True)
        row.operator(
            MSFS2020_OT_ChangeTab.bl_idname,
            text="Objects",
            depress=(current_tab == "OBJECTS"),
        ).current_tab = "OBJECTS"
        row.operator(
            MSFS2020_OT_ChangeTab.bl_idname,
            text="Presets",
            depress=(current_tab == "PRESETS"),
        ).current_tab = "PRESETS"
        row.operator(
            MSFS2020_OT_ChangeTab.bl_idname,
            text="Settings",
            depress=(current_tab == "SETTINGS"),
        ).current_tab = "SETTINGS"


def register_panel():
    # Register the panel on demand, we need to be sure to only register it once
    # This is necessary because the panel is a child of the extensions panel,
    # which may not be registered when we try to register this extension
    try:
        bpy.utils.register_class(MSFS2020_PT_MultiExporter)
    except Exception:
        pass

    # If the glTF exporter is disabled, we need to unregister the extension panel
    # Just return a function to the exporter so it can unregister the panel
    return unregister_panel


def unregister_panel():
    try:
        bpy.utils.unregister_class(MSFS2020_PT_MultiExporter)
    except Exception:
        pass


def register():
    bpy.types.Scene.msfs_multi_exporter_current_tab = bpy.props.EnumProperty(
        items=(
            ("OBJECTS", "Objects", ""),
            ("PRESETS", " Presets", ""),
            ("SETTINGS", "Settings", ""),
        )
    )


def unregister():
    try:
        del bpy.types.Scene.msfs_multi_exporter_current_tab
    except:
        pass
