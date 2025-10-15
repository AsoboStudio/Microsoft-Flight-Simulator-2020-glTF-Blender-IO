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

from ..com.msfs_constants import (
    EXPORT_ANIMATION_MODE,
    EXPORT_IMAGE_FORMAT
)

if bpy.app.version >= (4, 5, 0):
    from io_scene_gltf2.io.com import draco as gltf2_io_draco_compression_extension
else:
    from io_scene_gltf2.io.com import gltf2_io_draco_compression_extension


def on_enable_msfs_extension(self, context):
    # Set the properties in the glTF exporter 
    # accordingly to the multi exporter settings
    props = context.scene.msfs_exporter_settings
    props.enable_msfs_extension = self.enable_msfs_extension
    
    # Export NLA By default
    if bpy.app.version < (4, 2, 0):
        self.export_nla_strips = True
        return

    self.export_animation_mode = 'NLA_TRACKS'
    if self.enable_msfs_extension:
        self.export_influence_nb = min(self.export_influence_nb, 4)

def on_use_unique_id_extension_update(self, context):
    props = context.scene.msfs_exporter_settings
    props.use_unique_id = self.use_unique_id

def get_use_selection(self):
    return True

def set_influence_nb(self, value):
    self["export_influence_nb"] = value
    if not self.enable_msfs_extension:
        return

    if value > 4:
        self["export_influence_nb"] = 4

def get_influence_nb(self):
    return self.get("export_influence_nb", 4)

# region Properties Group
class MSFS2020_MultiExporterSettings(bpy.types.PropertyGroup):
    # region General Options
    name: bpy.props.StringProperty(name="Name")

    # keep original texture option Check
    export_keep_originals: bpy.props.BoolProperty(
        name="Keep original",
        description=(
            "Keep original textures files if possible. "
            "WARNING: if you use more than one texture, "
            "where pbr standard requires only one, only one texture will be used. "
            "This can lead to unexpected results"
        ),
        default=False,
    )

    # Texture directory path
    export_texture_dir: bpy.props.StringProperty(
        name="Textures",
        description=(
            "Folder to place texture files in (if you don't set an absolute path,"
             "it will be relative to your exported models)"
        ),
        default="",
    )

    # Copyright string UI
    export_copyright: bpy.props.StringProperty(
        name="Copyright",
        description="Legal rights and conditions for the model",
        default="",
    )

    # Remember export settings check
    will_save_settings: bpy.props.BoolProperty(
        name="Remember Export Settings",
        description="Store glTF export settings in the Blender project.",
        default=True,
    )
    # endregion

    # region MSFS2020 Parameters
    enable_msfs_extension: bpy.props.BoolProperty(
        name="Use Microsoft Flight Simulator 2024 Extensions",
        description="Enable Microsoft Flight Simulator 2024 Extensions",
        default=True,
        update=on_enable_msfs_extension,
    )

    ## Asobo Unique ID Check

    # Asobo Unique ID
    use_unique_id: bpy.props.BoolProperty(
        name="Use ASOBO Unique ID Extension",
        description="Enable ASOBO Unique ID extension",
        default=True,
        update=on_use_unique_id_extension_update,
    )
    # endregion

    # region Include Options
    # Export Selected Only Check
    use_selection: bpy.props.BoolProperty(
        name="Selected Objects",
        description=(
            "Export selected objects only. "
            "Disabled for the use of the MultiExporter (Needs to be always checked)"
        ),
        default=True,
        get=get_use_selection,
    )

    # Export Visible Only Check
    use_visible: bpy.props.BoolProperty(
        name="Visible Objects",
        description="Export visible objects only",
        default=False
    )

    # Export Custom Properties Check
    export_extras: bpy.props.BoolProperty(
        name="Custom Properties",
        description="Export custom properties as glTF extras. "
                    "Must be disabled for export dedicated to Microsoft Flight Simulator 2020",
        default=False,
    )

    # Export Camera Check
    export_cameras: bpy.props.BoolProperty(
        name="Cameras",
        description="Export cameras",
        default=False,
    )

    # Export Punctual Lights Check
    export_lights: bpy.props.BoolProperty(
        name="Punctual Lights",
        description=(
            "Export directional, point, and spot lights. "
            "Uses 'KHR_lights_punctual' glTF extension"
        ),
        default=True,
    )
    # endregion

    # region Transform Options
    # Y Up Check
    export_yup: bpy.props.BoolProperty(
        name="+Y Up", 
        description="Export using glTF convention, +Y up",
        default=True,
    )
    # endregion

    # region Scene Graph
    if bpy.app.version >= (4, 2, 0):
        # Export geometry node instances
        export_gn_mesh: bpy.props.BoolProperty(
            name="Geometry Nodes Instances (Experimental)",
            description="Export Geometry nodes instance meshes",
            default=False
        )

        # Export GPU instances
        export_gpu_instances: bpy.props.BoolProperty(
            name="GPU Instances",
            description="Export using EXT_mesh_gpu_instancing. "
                        "Limited to children of a given Empty. "
                        "Multiple materials might be omitted",
            default=False
        )

        # Flatten Objects
        export_hierarchy_flatten_objs: bpy.props.BoolProperty(
            name="Flatten Object Hierarchy",
            description="Flatten Object Hierarchy. "
                        "Useful in case of non decomposable transformation matrix",
            default=False
        )

        export_hierarchy_full_collections: bpy.props.BoolProperty(
            name="Full Collection Hierarchy",
            description="Export full hierarchy, including intermediate collections",
            default=False
        )
    # endregion

    # region Mesh
    # Export Meshes
    export_mesh: bpy.props.BoolProperty(
        name="",
        description=(
            "Enable/Disable export meshes"
            "(Useful to export animations only)"
        ),
        default=True,
    )

    # Export Apply Modifiers Check
    export_apply: bpy.props.BoolProperty(
        name="Apply Modifiers",
        description=(
            "Apply modifiers (excluding Armatures) to mesh objects. "
            "WARNING: prevents exporting shape keys"
        ),
        default=False,
    )

    # Export UVs Check
    export_texcoords: bpy.props.BoolProperty(
        name="UVs",
        description="Export UVs (texture coordinates) with meshes",
        default=True,
    )

    # Export Normals Check
    export_normals: bpy.props.BoolProperty(
        name="Normals",
        description="Export vertex normals with meshes",
        default=True,
    )

    # Export Tangents Check
    export_tangents: bpy.props.BoolProperty(
        name="Tangents",
        description="Export vertex tangents with meshes",
        default=False,
    )

    if bpy.app.version < (4, 2, 0):
        # Export Vertex Colors Check
        export_colors: bpy.props.BoolProperty(
            name="Vertex Colors",
            description="Export vertex colors with meshes",
            default=True,
        )
    else:
        export_vertex_color: bpy.props.EnumProperty(
            name="Use Vertex Color",
            items=(
                (
                    'MATERIAL',
                    'Material',
                    "Export vertex color when used by material"
                ),
                (
                    'NONE',
                    'None',
                    "Do not export vertex color"
                )
            ),
            description="How to export vertex color",
            default='MATERIAL'
        )

        export_all_vertex_colors: bpy.props.BoolProperty(
            name='Export all vertex colors',
            description=(
                'Export all vertex colors, even if not used by any material. '
                'If no Vertex Color is used in the mesh materials, a fake COLOR_0 will be created, '
                'in order to keep material unchanged'
            ),
            default=True
        )

        export_active_vertex_color_when_no_material: bpy.props.BoolProperty(
            name='Export active vertex color when no material',
            description='When there is no material on object, export active vertex color',
            default=True
        )

    # Export Attributes Colors Check
    export_attributes: bpy.props.BoolProperty(
        name='Attributes',
        description='Export Attributes (when starting with underscore)',
        default=False,
    )

    # Export Loose Edge Check
    use_mesh_edges: bpy.props.BoolProperty(
        name="Loose Edges",
        description=(
            "Export loose edges as lines, using the material from the first material slot"
        ),
        default=False,
    )

    # Export Loose Points Check
    use_mesh_vertices: bpy.props.BoolProperty(
        name="Loose Points",
        description=(
            "Export loose points as glTF points, using the material from the first material slot"
        ),
        default=False,
    )

    # endregion

    # region Material
    # Export materials option Check
    export_materials: bpy.props.EnumProperty(
        name="Materials",
        items=(
            ("EXPORT", "Export", "Export all materials used by included objects"),
            (
                "PLACEHOLDER",
                "Placeholder",
                "Do not export materials, but write multiple primitive groups per mesh, keeping material slot information",
            ),
            (
                "NONE",
                "No export",
                "Do not export materials, and combine mesh primitive groups, losing material slot information",
            ),
        ),
        description="Export materials ",
        default="EXPORT",
    )

    # Export Image format UI (Auto/Jpeg/None)
    export_image_format: bpy.props.EnumProperty(
        name="Images",
        items=EXPORT_IMAGE_FORMAT,
        description=(
            "Output format for images. PNG is lossless and generally preferred, but JPEG might be preferable for web "
            "applications due to the smaller file size. Alternatively they can be omitted if they are not needed"
        ),
        default="AUTO",
    )

    # JPEG Quality
    export_jpeg_quality: bpy.props.IntProperty(
        name='Image quality',
        description='Quality of image export',
        default=75,
        min=0,
        max=100,
    )

    # Create WebP
    export_image_add_webp: bpy.props.BoolProperty(
        name="Create WebP",
        description=(
            "Creates WebP textures for every texture. "
            "For already WebP textures, nothing happens"
        ),
        default=False,
    )

    # WebP Fallback
    export_image_webp_fallback: bpy.props.BoolProperty(
        name="WebP fallback",
        description=(
            "For all WebP textures, create a PNG fallback texture"
        ),
        default=False,
    )

    # Export unused images
    export_unused_images: bpy.props.BoolProperty(
        name="Unused images",
        description="Export images not assigned to any material",
        default=False,
    )

    # Export unused Textures
    export_unused_textures: bpy.props.BoolProperty(
        name="Prepare Unused textures",
        description=(
            "Export image texture nodes not assigned to any material. "
            "This feature is not standard and needs an external extension "
            "to be included in the glTF file"
        ),
        default=False,
    )
    # endregion

    # region Compression
    # Draco compression check
    export_draco_mesh_compression_enable: bpy.props.BoolProperty(
        name="Draco mesh compression",
        description="Compress mesh using Draco",
        default=False,
    )

    # Draco compression level
    export_draco_mesh_compression_level: bpy.props.IntProperty(
        name="Compression level",
        description=(
            "Compression level ("
            "0 = most speed,"
            " 6 = most compression,"
            " higher values currently not supported)"
        ),
        default=6,
        min=0,
        max=10,
    )

    # Draco compression position quatization
    export_draco_position_quantization: bpy.props.IntProperty(
        name="Position quantization bits",
        description="Quantization bits for position values (0 = no quantization)",
        default=14,
        min=0,
        max=30,
    )

    # Draco compression normal quatization
    export_draco_normal_quantization: bpy.props.IntProperty(
        name="Normal quantization bits",
        description="Quantization bits for normal values (0 = no quantization)",
        default=10,
        min=0,
        max=30,
    )

    # Draco compression texture coordinate quatization
    export_draco_texcoord_quantization: bpy.props.IntProperty(
        name="Texcoord quantization bits",
        description="Quantization bits for texture coordinate values (0 = no quantization)",
        default=12,
        min=0,
        max=30,
    )

    # Draco compression vertex color quatization
    export_draco_color_quantization: bpy.props.IntProperty(
        name="Color quantization bits",
        description="Quantization bits for color values (0 = no quantization)",
        default=10,
        min=0,
        max=30,
    )

    # Draco compression generic quantization
    export_draco_generic_quantization: bpy.props.IntProperty(
        name="Generic quantization bits",
        description="Quantization bits for generic coordinate "
                    "values like weights or joints (0 = no quantization)",
        default=12,
        min=0,
        max=30,
    )
    # endregion

    # region Lighting
    if bpy.app.version >= (3, 6, 0):
        # Lighting Modes
        export_import_convert_lighting_mode: bpy.props.EnumProperty(
            name="Lighting Mode",
            items=(
                (
                    "SPEC",
                    "Standard",
                    "Physically-based glTF lighting units (cd, lx, nt)"
                ),
                (
                    "COMPAT",
                    "Unitless",
                    "Non-physical,"
                    " unitless lighting. Useful when exposure controls are not available"
                ),
                (
                    "RAW",
                    "Raw (Deprecated)",
                    "Blender lighting strengths with no conversion"
                )
            ),
            description="Optional backwards compatibility for non-standard render engines. Applies to lights",
            default="SPEC",
        )

    # endregion

    # region Shape Keys
    # Export Shape Keys check
    export_morph: bpy.props.BoolProperty(
        name="Shape Keys",
        description=(
            "Export shape keys (morph targets). "
        ),
        default=False,
    )

    # Export Shape Keys Normals check
    export_morph_normal: bpy.props.BoolProperty(
        name="Shape Key Normals",
        description=(
            "Export vertex normals with shape keys (morph targets). "
        ),
        default=False,
    )

    # Export Shape Keys Tangent check
    export_morph_tangent: bpy.props.BoolProperty(
        name="Shape Key Tangents",
        description=(
            "Export vertex tangents with shape keys (morph targets). "
        ),
        default=False,
    )

    if bpy.app.version > (4, 2, 0):
        # Use Sparse Accessors
        export_try_sparse_sk: bpy.props.BoolProperty(
            name="Use Sparse Accessor if better",
            description="Try using Sparse Accessor if it saves space",
            default=True,
        )

        # Omit Sparse accessors if empty
        export_try_omit_sparse_sk: bpy.props.BoolProperty(
            name="Omitting Sparse Accessor if data is empty",
            description="Omitting Sparse Accessor if data is empty",
            default=False,
        )
    # endregion

    # region Skinning
    # Skinning Option Check
    export_skins: bpy.props.BoolProperty(
        name="Skinning", 
        description="Export skinning (armature) data",
        default=True,
    )

    # Export All Bone Influences Check
    export_all_influences: bpy.props.BoolProperty(
        name="Include All Bone Influences",
        description=(
            "Allow > 4 joint vertex influences. "
            "Models may appear incorrectly in many viewers"
        ),
        default=False,
    )

    if bpy.app.version >= (4, 2, 0):
        # Nb bone influence
        export_influence_nb: bpy.props.IntProperty(
            name="Bone Influences",
            description="Choose how many Bone influences to export",
            default=4,
            min=1,
            set=set_influence_nb,
            get=get_influence_nb,
        )

    # endregion

    # region Armature

    # Deformation Bones Only Check
    export_def_bones: bpy.props.BoolProperty(
        name="Export Deformation Bones Only",
        description="Export Deformation bones only (and needed bones for hierarchy)",
        default=False,
    )

    if bpy.app.version >= (3, 6, 0):
        # Use rest position check
        export_rest_position_armature: bpy.props.BoolProperty(
            name="Use Rest Position Armature",
            description=(
                "Export armatures using rest position as joints' rest pose. "
                "When off, current frame pose is used as rest pose"
            ),
            default=False,
        )

        # Flatten Bones Check
        export_hierarchy_flatten_bones: bpy.props.BoolProperty(
            name="Flatten Bone Hierarchy",
            description=(
                "Flatten Bone Hierarchy. "
                "Useful in case of non decomposable transformation matrix"
            ),
            default=False,
        )

    if bpy.app.version >= (4, 2, 0):
        # Remove Armature Object
        export_armature_object_remove: bpy.props.BoolProperty(
            name="Remove Armature Object",
            description=(
                "Remove Armature object if possible. "
                "If Armature has multiple root bones, object will not be removed"
            ),
            default=False,
        )
    # endregion

    # region Animation Options
    # Export Animation Options Check
    export_animations: bpy.props.BoolProperty(
        name="Animations",
        description="Exports active actions and NLA tracks as glTF animations",
        default=True,
    )

    # Use Current Frame Check
    export_current_frame: bpy.props.BoolProperty(
        name="Use Current Frame",
        description="Export the scene in the current animation frame",
        default=False,
    )

    # Limit to Playback Range Check
    export_frame_range: bpy.props.BoolProperty(
        name="Limit to Playback Range",
        description="Clips animations to selected playback range",
        default=True,
    )

    # Always Sample Animations Check
    export_force_sampling: bpy.props.BoolProperty(
        name="Always Sample Animations",
        description="Apply sampling to all animations",
        default=True,
    )

    # Sampling Rate Slider (1-120)
    export_frame_step: bpy.props.IntProperty(
        name="Sampling Rate",
        description="How often to evaluate animated values (in frames)",
        default=1,
        min=1,
        max=120,
    )

    # Animation mode export
    if bpy.app.version >= (3, 6, 0):
        export_animation_mode: bpy.props.EnumProperty(
            name="Animation mode",
            items=EXPORT_ANIMATION_MODE,
            description="Export Animation mode",
            default="NLA_TRACKS",
        )

        # Optimize Animation Force keeping channels for bones Check
        export_optimize_animation_keep_anim_armature: bpy.props.BoolProperty(
            name="Force keeping channels for bones",
            description=(
                "if all keyframes are identical in a rig, "
                "force keeping the minimal animation. "
                "When off, all possible channels for "
                "the bones will be exported, even if empty "
                "(minimal animation, 2 keyframes)"
            ),
            default=False,
        )

        # Optimize Animation Force keeping channels for objects Check
        export_optimize_animation_keep_anim_object: bpy.props.BoolProperty(
            name="Force keeping channel for objects",
            description=(
                "If all keyframes are identical for object transformations, "
                "force keeping the minimal animation"
            ),
            default=False,
        )

        # Export negative frames check
        export_negative_frame: bpy.props.EnumProperty(
            name="Negative Frames",
            items=(
                (
                    "SLIDE",
                    "Slide",
                    "Slide animation to start at frame 0"
                ),
               (
                   "CROP",
                   "Crop",
                   "Keep only frames above frame 0"
               )
           ),
            description="Negative Frames are slid or cropped",
            default="SLIDE",
        )

        # Set all glTF Animation starting at 0 check
        export_anim_slide_to_zero: bpy.props.BoolProperty(
            name="Set all glTF Animation starting at 0",
            description=(
                "Set all glTF animation starting at 0.0s. "
                "Can be useful for looping animations"
            ),
            default=False,
        )

        # Bake all objects animation check
        export_bake_animation: bpy.props.BoolProperty(
            name="Bake All Objects Animations",
            description=(
                "Force exporting animation on every object. "
                "Can be useful when using constraints or driver. "
                "Also useful when exporting only selection"
            ),
            default=False,
        )

        # Split animation by object when animation mode is set to scene check
        export_anim_scene_split_object: bpy.props.BoolProperty(
            name="Split Animation by Object",
            description=(
                "Export Scene as seen in Viewport, "
                "But split animation by Object"
            ),
            default=True,
        )

        # Reset pose bones between actions check
        export_reset_pose_bones: bpy.props.BoolProperty(
            name="Reset pose bones between actions",
            description=(
                "Reset pose bones between each action exported. "
                "This is needed when some bones are not keyed on some animations"
            ),
            default=True,
        )

    else:
        # Group by NLA Track Check
        export_nla_strips: bpy.props.BoolProperty(
            name="Group by NLA Track",
            description=(
                "When on, multiple actions become part of the same glTF animation if "
                "they're pushed onto NLA tracks with the same name. "
                "When off, all the currently assigned actions become one glTF animation"
            ),
            default=True,
        )

        # Export NLA strips merged animation name
        export_nla_strips_merged_animation_name: bpy.props.StringProperty(
            name="Merged Animation Name",
            description=(
                "Name of single glTF animation to be exported"
            ),
            default="Animation"
        )

    # Optimize Animation Size Check
    export_optimize_animation_size: bpy.props.BoolProperty(
        name="Optimize Animation Size",
        description=(
            "Reduces exported filesize by removing duplicate keyframes"
            "Can cause problems with stepped animation"
        ),
        default=True,
    )

    # Export all armature actions check
    export_anim_single_armature: bpy.props.BoolProperty(
        name="Export all Armature Actions",
        description=(
            "Export all actions, bound to a single armature. "
            "WARNING: Option does not support exports including multiple armatures"
        ),
        default=False,
    )

    # Export shape key animation check
    export_morph_animation: bpy.props.BoolProperty(
        name="Shape Key Animations",
        description="Export shape keys animations (morph targets)",
        default=False,
    )

    # Reset shape keys between actions check
    export_morph_reset_sk_data: bpy.props.BoolProperty(
        name="Reset shape keys between actions",
        description=(
            "Reset shape keys between each action exported. "
            "This is needed when some SK channels are not keyed on some animations"
        ),
        default=False,
    )

    if bpy.app.version >= (4, 2, 0):
        # Disable viewport for objects when exporting animations
        export_optimize_disable_viewport: bpy.props.BoolProperty(
            name="Disable viewport for other objects",
            description=(
                "When exporting animations, disable viewport for other objects "
                "(for performance)"
            ),
            default=True,
        )

    # endregion
# endregion

# region Panels
class MSFS2020_PT_export_main(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "General"
    bl_parent_id = "MSFS2020_PT_MultiExporter"
    bl_options = {"HIDE_HEADER"}
    
    @classmethod
    def get_multi_exporter_settings(cls, context):
        return context.scene.msfs_multi_exporter_settings
    
    @classmethod
    def get_multi_exporter_current_tab(cls, context):
        return context.scene.msfs_multi_exporter_current_tab
    
    @classmethod
    def poll(cls, context):

        return context.scene.msfs_multi_exporter_current_tab == "SETTINGS"

    def draw(self, context):
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)
        
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.
        
        layout.prop(settings, "export_copyright")
        layout.prop(settings, "will_save_settings")

class MSFS2020_PT_export_texture(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Textures"
    bl_parent_id = "MSFS2020_PT_MultiExporter"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        current_tab = MSFS2020_PT_export_main.get_multi_exporter_current_tab(context)
        return current_tab == "SETTINGS"

    def draw_header(self, context):
        self.layout.label(icon="FILE_IMAGE")

    def draw(self, context):
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)
        
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.prop(
            settings,
            "export_keep_originals"
        )
        
        if settings.export_keep_originals:
            return
        
        layout.prop(
            settings,
            "export_texture_dir",
            icon="FILE_FOLDER"
        )

# region MSFS2024
class MSFS2020_PT_export(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Microsoft Flight Simulator 2020"
    bl_parent_id = "MSFS2020_PT_MultiExporter"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        current_tab = MSFS2020_PT_export_main.get_multi_exporter_current_tab(context)
        return current_tab == "SETTINGS"

    def draw_header(self, context):
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)

        self.layout.label(icon='TOOL_SETTINGS')
        self.layout.prop(settings, "enable_msfs_extension", text="")

    def draw(self, context):
        return

class MSFS2020_PT_extension(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Extensions"
    bl_parent_id = "MSFS2020_PT_export"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        current_tab = MSFS2020_PT_export_main.get_multi_exporter_current_tab(context)
        return current_tab == "SETTINGS"

    def draw(self, context):
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.active = settings.enable_msfs_extension
        layout.prop(
            settings,
            "use_unique_id",
            text="Use ASOBO Unique ID extension for nodes"
        )

# endregion

class MSFS2020_PT_export_include(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Include"
    bl_parent_id = "MSFS2020_PT_MultiExporter"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        current_tab = MSFS2020_PT_export_main.get_multi_exporter_current_tab(context)
        return current_tab == "SETTINGS"

    def draw(self, context):
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)
        
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        # To use the MultiExporter panel, it's important to have "use selected" to True
        col = layout.column(heading="", align=True)
        col.prop(settings, "use_selection")
        col.enabled = False
        
        col = layout.column(heading="Limit to", align=True)
        col.prop(settings, "use_visible")

        if not settings.enable_msfs_extension:
            col = layout.column(heading="", align=True)
            col.prop(settings, "export_extras")

        col = layout.column(heading="Data", align=True)
        col.prop(settings, "export_cameras")
        col.prop(settings, "export_lights")

class MSFS2020_PT_export_transform(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Transform"
    bl_parent_id = "MSFS2020_PT_MultiExporter"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        current_tab = MSFS2020_PT_export_main.get_multi_exporter_current_tab(context)
        return current_tab == "SETTINGS"

    def draw(self, context):
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)
        
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.prop(settings, "export_yup")

class MSFS2020_PT_export_scene_graph(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Scene Graph"
    bl_parent_id = "MSFS2020_PT_MultiExporter"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)
        current_tab = MSFS2020_PT_export_main.get_multi_exporter_current_tab(context)

        return (
            current_tab == "SETTINGS"
            and not settings.enable_msfs_extension
            and bpy.app.version >= (4, 2, 0)
        )

    def draw(self, context):
        if bpy.app.version < (4, 2, 0):
            return
        
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.prop(settings, "export_gn_mesh")
        layout.prop(settings, "export_gpu_instances")
        layout.prop(settings, "export_hierarchy_flatten_objs")
        layout.prop(settings, "export_hierarchy_full_collections")

class MSFS2020_PT_export_geometry(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Mesh"
    bl_parent_id = "MSFS2020_PT_MultiExporter"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        current_tab = MSFS2020_PT_export_main.get_multi_exporter_current_tab(context)
        return current_tab == "SETTINGS"

    def draw_header(self, context):
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)

        self.layout.label(icon="MESH_DATA")
        self.layout.prop(settings, "export_mesh", text="")

    def draw(self, context):
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)
        
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.active = settings.export_mesh
        layout.prop(settings, "export_apply")
        layout.prop(settings, "export_texcoords")
        layout.prop(settings, "export_normals")

        col = layout.column()
        col.prop(settings, "export_tangents")
        col.active = settings.export_normals

        if bpy.app.version < (4, 2, 0):
            layout.prop(settings, "export_colors")

        if bpy.app.version >= (3, 6, 0):
            layout.prop(settings, "export_attributes")

        layout.prop(settings, "use_mesh_edges")
        layout.prop(settings, "use_mesh_vertices")

        if bpy.app.version >= (4, 2, 0):
            header, body = layout.panel(
                "MSFS2020_PT_export_vertex_colors",
                default_closed=True
            )
            header.label(text="Vertex Colors")
            if body:
                body.prop(settings, "export_vertex_color")
                body.prop(settings, "export_all_vertex_colors")
                body.prop(settings, "export_active_vertex_color_when_no_material")

class MSFS2020_PT_export_material(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Material"
    bl_parent_id = "MSFS2020_PT_MultiExporter"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        current_tab = MSFS2020_PT_export_main.get_multi_exporter_current_tab(context)
        return current_tab == "SETTINGS"

    def draw_header(self, context):
        self.layout.label(icon="MATERIAL_DATA")

    def draw(self, context):
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)
        
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.prop(settings, "export_materials")
        col = layout.column()
        col.active = settings.export_materials == "EXPORT"

        if settings.enable_msfs_extension:
            return

        col.prop(settings, "export_image_format")

        if bpy.app.version >= (3, 6, 0):
            col.prop(settings, "export_jpeg_quality")

        if bpy.app.version >= (4, 2, 0):
            col.prop(settings, "export_image_add_webp")
            col.prop(settings, "export_image_webp_fallback")

            header, body = layout.panel(
                "MSFS2020_PT_export_unused_images_textures",
                default_closed=True
            )
            header.label(text="Unused Textures & Images")
            if body:
                body.prop(settings, "export_unused_images")
                body.prop(settings, "export_unused_textures")

class MSFS2020_PT_export_shapekeys(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Shape Keys"
    bl_parent_id = "MSFS2020_PT_MultiExporter"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        current_tab = MSFS2020_PT_export_main.get_multi_exporter_current_tab(context)
        return current_tab == "SETTINGS"

    def draw_header(self, context):
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)

        self.layout.label(icon="SHAPEKEY_DATA")
        self.layout.prop(
            settings,
            "export_morph",
            text=""
        )

    def draw(self, context):
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)
        
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.
        
        layout.active = settings.export_morph

        layout.prop(settings, "export_morph_normal")
        col = layout.column()
        col.active = settings.export_morph_normal
        col.prop(settings, "export_morph_tangent")

        if settings.enable_msfs_extension:
            return
        
        if bpy.app.version < (4, 2, 0):
            return
        
        header, body = layout.panel(
            "MSFS2020_PT_export_optimize_shapekeys", 
            default_closed=True
        )
        header.label(text="Optimize Shape Keys")
        if not body:
            return
        col = body.column()
        col.prop(settings, "export_try_sparse_sk")
        col = body.column()
        col.active = settings.export_try_sparse_sk
        col.prop(settings, "export_try_omit_sparse_sk")

class MSFS2020_PT_export_armature(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Armature"
    bl_parent_id = "MSFS2020_PT_MultiExporter"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        current_tab = MSFS2020_PT_export_main.get_multi_exporter_current_tab(context)
        return (
            bpy.app.version >= (3, 3, 0)
            and current_tab == "SETTINGS"
        )

    def draw_header(self, context):
        self.layout.label(icon="ARMATURE_DATA")

    def draw(self, context):
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)
        
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.active = settings.export_skins

        if bpy.app.version >= (3, 6, 0):
            layout.prop(settings, "export_rest_position_armature")
            
        if bpy.app.version < (3, 3, 0):
            return
        
        row = layout.row()
        row.active = settings.export_force_sampling
        row.prop(settings, "export_def_bones")
        if (
            settings.export_force_sampling is False
            and settings.export_def_bones is True
        ):
            layout.label(
                text=(
                    "Export only deformation bones "
                    "is not possible when not sampling animation"
                ),
            )

        if bpy.app.version >= (4, 2, 0):
            layout.prop(settings, "export_armature_object_remove")

        if bpy.app.version >= (3, 6, 0):
            layout.prop(settings, "export_hierarchy_flatten_bones")

class MSFS2020_PT_export_skinning(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Skinning"
    bl_parent_id = "MSFS2020_PT_MultiExporter"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        current_tab = MSFS2020_PT_export_main.get_multi_exporter_current_tab(context)
        return current_tab == "SETTINGS"

    def draw_header(self, context):
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)

        self.layout.label(icon="MOD_SKIN")
        self.layout.prop(settings, "export_skins", text="")

    def draw(self, context):
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.
        layout.active = settings.export_skins

        if bpy.app.version >= (4, 2, 0):
            layout.prop(settings, "export_influence_nb")

        if not settings.enable_msfs_extension:
            layout.prop(settings, "export_all_influences")

class MSFS2020_PT_export_Lighting(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Lighting"
    bl_parent_id = "MSFS2020_PT_MultiExporter"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)
        current_tab = MSFS2020_PT_export_main.get_multi_exporter_current_tab(context)
        
        return (
            current_tab == "SETTINGS"
            and bpy.app.version >= (3, 6, 0)
            and not settings.enable_msfs_extension
        )

    def draw(self, context):
        if bpy.app.version < (3, 6, 0):
            return

        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)
        
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.prop(settings, "export_import_convert_lighting_mode")

class MSFS2020_PT_export_geometry_compression(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Compression"
    bl_parent_id = "MSFS2020_PT_export_geometry"
    bl_options = {'DEFAULT_CLOSED'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super(MSFS2020_PT_export_main).__init__(*args, **kwargs)
        self.is_draco_available = gltf2_io_draco_compression_extension.dll_exists(quiet=True)

    @classmethod
    def poll(cls, context):
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)
        current_tab = MSFS2020_PT_export_main.get_multi_exporter_current_tab(context)

        return (
            current_tab == "SETTINGS"
            and settings.export_draco_mesh_compression_enable
        )

    def draw_header(self, context):
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)
        self.layout.prop(settings, "export_draco_mesh_compression_enable", text="")

    def draw(self, context):
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)
        
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.active = settings.export_draco_mesh_compression_enable
        layout.prop(settings, "export_draco_mesh_compression_level")

        col = layout.column(align=True)
        col.prop(settings, "export_draco_position_quantization", text="Quantize Position")
        col.prop(settings, "export_draco_normal_quantization", text="Normal")
        col.prop(settings, "export_draco_texcoord_quantization", text="Tex Coord")
        col.prop(settings, "export_draco_color_quantization", text="Color")
        col.prop(settings, "export_draco_generic_quantization", text="Generic")

class MSFS2020_PT_export_animation(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Animation"
    bl_parent_id = "MSFS2020_PT_MultiExporter"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        current_tab = MSFS2020_PT_export_main.get_multi_exporter_current_tab(context)
        return current_tab == "SETTINGS"

    def draw_header(self, context):
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)

        self.layout.label(icon="ANIM")
        self.layout.prop(settings, "export_animations", text="")

    def draw(self, context):
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)
        
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.active = settings.export_animations

        if bpy.app.version >= (3, 6, 0):                
            row = layout.row()
            row.prop(settings, 'export_animation_mode')

            if settings.export_animation_mode == "ACTIVE_ACTIONS":
                layout.prop(settings, 'export_nla_strips_merged_animation_name')

            row = layout.row()
            row.active = (
                settings.export_force_sampling
                and settings.export_animation_mode in ['ACTIONS', 'ACTIVE_ACTIONS']
            )
            row.prop(settings, 'export_bake_animation')

            if settings.export_animation_mode == "SCENE":
                layout.prop(settings, 'export_anim_scene_split_object')
                
            return
        
        layout.prop(settings, "export_current_frame")
        layout.prop(settings, "export_frame_range")
        layout.prop(settings, "export_frame_step")
        layout.prop(settings, "export_force_sampling")
        
        row = layout.row()
        row.prop(settings, "export_nla_strips")

        if (
            settings.export_nla_strips is False
            and bpy.app.version >= (3, 3, 0)
        ):
            layout.prop(settings, "export_nla_strips_merged_animation_name")

        layout.prop(settings, "export_optimize_animation_size")
        if bpy.app.version >= (3, 3, 0):
            layout.prop(settings, "export_anim_single_armature")
        else:
            layout.prop(settings, 'export_def_bones')

class MSFS2020_PT_export_animation_notes(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Notes"
    bl_parent_id = "MSFS2020_PT_export_animation"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)
        current_tab = MSFS2020_PT_export_main.get_multi_exporter_current_tab(context)

        return (
            current_tab == "SETTINGS"
            and bpy.app.version >= (3, 6, 0)
            and settings.export_animation_mode in ["NLA_TRACKS", "SCENE"]
        )

    def draw(self, context):
        if bpy.app.version < (3, 6, 0):
            return

        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)
        
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        if settings.export_animation_mode == "SCENE":
            layout.label(text="Scene mode uses full bake mode:")
            layout.label(text="- sampling is active")
            layout.label(text="- baking all objects is active")
            layout.label(text="- Using scene frame range")
        elif settings.export_animation_mode == "NLA_TRACKS":
            layout.label(text="Track mode uses full bake mode:")
            layout.label(text="- sampling is active")
            layout.label(text="- baking all objects is active")

class MSFS2020_PT_export_animation_ranges(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Rest & Ranges"
    bl_parent_id = "MSFS2020_PT_export_animation"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (
            context.scene.msfs_multi_exporter_current_tab == "SETTINGS"
            and bpy.app.version >= (3, 6, 0)
        )

    def draw(self, context):
        if bpy.app.version < (3, 6, 0):
            return
        
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.prop(settings, 'export_current_frame')
        row = layout.row()
        row.active = settings.export_animation_mode in ['ACTIONS', 'ACTIVE_ACTIONS', 'NLA_TRACKS']
        row.prop(settings, 'export_frame_range')
        layout.prop(settings, 'export_anim_slide_to_zero')
        row = layout.row()
        row.active = settings.export_animation_mode in ['ACTIONS', 'ACTIVE_ACTIONS', 'NLA_TRACKS']
        layout.prop(settings, 'export_negative_frame')

class MSFS2020_PT_export_animation_armature(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Armature"
    bl_parent_id = "MSFS2020_PT_export_animation"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        current_tab = MSFS2020_PT_export_main.get_multi_exporter_current_tab(context)
        return (
            current_tab == "SETTINGS"
            and bpy.app.version >= (3, 6, 0)
        )

    def draw(self, context):
        if bpy.app.version < (3, 6, 0):
            return
        
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.active = settings.export_animations

        layout.prop(settings, 'export_anim_single_armature')
        layout.prop(settings, 'export_reset_pose_bones')

class MSFS2020_PT_export_animation_shapekeys(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Shape keys Animation"
    bl_parent_id = "MSFS2020_PT_export_animation"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        current_tab = MSFS2020_PT_export_main.get_multi_exporter_current_tab(context)
        return (
            current_tab == "SETTINGS"
            and bpy.app.version >= (3, 6, 0)
        )

    def draw_header(self, context):
        if bpy.app.version < (3, 6, 0):
            return

        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)

        self.layout.active = (
            settings.export_animations
            and settings.export_morph
        )
        self.layout.prop(settings, "export_morph_animation", text="")

    def draw(self, context):
        if bpy.app.version < (3, 6, 0):
            return
        
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)
        
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.active = settings.export_animations
        layout.prop(settings, "export_morph_reset_sk_data")

class MSFS2020_PT_export_animation_sampling(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Sampling Animations"
    bl_parent_id = "MSFS2020_PT_export_animation"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        current_tab = MSFS2020_PT_export_main.get_multi_exporter_current_tab(context)
        return (
            current_tab == "SETTINGS"
            and bpy.app.version >= (3, 6, 0)
        )

    def draw_header(self, context):
        if bpy.app.version < (3, 6, 0):
            return

        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)

        self.layout.active = (
            settings.export_animations
            and settings.export_animation_mode in ['ACTIONS', 'ACTIVE_ACTIONS']
        )
        self.layout.prop(settings, "export_force_sampling", text="")

    def draw(self, context):
        if bpy.app.version < (3, 6, 0):
            return
        
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)
        
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.active = settings.export_animations
        layout.prop(settings, 'export_frame_step')

class MSFS2020_PT_export_animation_optimize(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Optimize Animations"
    bl_parent_id = "MSFS2020_PT_export_animation"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        current_tab = MSFS2020_PT_export_main.get_multi_exporter_current_tab(context)
        return (
            current_tab == "SETTINGS"
            and bpy.app.version >= (3, 6, 0)
        )

    def draw(self, context):
        settings = MSFS2020_PT_export_main.get_multi_exporter_settings(context)
        
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.active = settings.export_animations

        layout.prop(settings, "export_optimize_animation_size")

        row = layout.row()
        row.prop(settings, "export_optimize_animation_keep_anim_armature")

        row = layout.row()
        row.prop(settings, "export_optimize_animation_keep_anim_object")

        if bpy.app.version >= (4, 2, 0):
            row = layout.row()
            row.prop(settings, "export_optimize_disable_viewport")

def register():
    bpy.types.Scene.msfs_multi_exporter_settings = bpy.props.PointerProperty(type=MSFS2020_MultiExporterSettings)
