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

import bgl as bgl
import bmesh
import bpy
import gpu
import numpy as np

from math import radians
from gpu_extras.batch import batch_for_shader
from mathutils import Matrix


class MSFS2020GizmoProperties:
    def msfs_gizmo_type_update(self, context):
        empties = MSFS2020CollisionGizmoGroup.empties
        active_object = context.object
        if active_object not in empties:
            return
        
        if active_object.msfs_gizmo_type == empties[active_object].msfs_gizmo_type:
            return
        
        empties[active_object].msfs_gizmo_type = active_object.msfs_gizmo_type
        empties[active_object].create_custom_shape()

    bpy.types.Object.msfs_gizmo_type = bpy.props.EnumProperty(
        name="Type",
        description="Type of collision gizmo to add",
        items=(
            ("NONE", "Disabled", ""),
            ("sphere", "Sphere Collision Gizmo", ""),
            ("box", "Box Collision Gizmo", ""),
            ("cylinder", "Cylinder Collision Gizmo", ""),
        ),
        update=msfs_gizmo_type_update,
    )


class AddGizmo(bpy.types.Operator):
    bl_idname = "msfs_collision_gizmo.add_gizmo"
    bl_label = "Add MSFS2020 Collision Gizmo"
    bl_options = {"REGISTER", "UNDO"}

    msfs_gizmo_type: bpy.types.Object.msfs_gizmo_type
    
    def add_gizmo(self, context, parent):
        bpy.ops.object.empty_add()
        gizmo = context.object
        if self.msfs_gizmo_type == "sphere":
            gizmo.name = "Sphere Collision"
        elif self.msfs_gizmo_type == "box":
            gizmo.name = "Box Collision"
        elif self.msfs_gizmo_type == "cylinder":
            gizmo.name = "Cylinder Collision"

        gizmo.msfs_gizmo_type = self.msfs_gizmo_type
        if parent:
            gizmo.parent = parent

    def execute(self, context):
        if not context.selected_objects:
            self.add_gizmo(context, None)
            return {"FINISHED"}
        
        for selected_object in context.selected_objects:
            if selected_object.type == "MESH":
                self.add_gizmo(context, selected_object)
            else:
                self.add_gizmo(context, None)
        return {"FINISHED"}
        

class MSFS2020CollisionGizmo(bpy.types.Gizmo):
    bl_idname = "VIEW3D_GT_msfs_collision_gizmo"
    bl_label = "MSFS2020 Collision Gizmo"
    bl_options = {"UNDO"}

    __slots__ = (
        "empty",
        "msfs_gizmo_type",
        "custom_shape",
        "custom_shape_edges",
    )
    
    def __init__(self):
        super().__init__()
        self.custom_shape_edges = None
        self.custom_shape = None

    def _update_offset_matrix(self):
        pass

    def setup(self):
        if not hasattr(self, "custom_shape"):
            self.custom_shape = None

    def draw_line_3d(self, color, width, region, pos):
        shader = gpu.shader.from_builtin("3D_POLYLINE_UNIFORM_COLOR")
        batch = batch_for_shader(shader, "LINES", {"pos": pos})
        shader.bind()
        shader.uniform_float("color", color)
        shader.uniform_float("lineWidth", width)
        shader.uniform_float("viewportSize", (region.width, region.height))
        batch.draw(shader)

    def create_custom_shape(self):
        mesh = bpy.data.meshes.new("Gizmo Mesh")
        bm = bmesh.new()
        
        if self.msfs_gizmo_type == "sphere":
            bmesh.ops.create_circle(bm, segments=32, radius=1)
            bm.to_mesh(mesh)
            bmesh.ops.create_circle(
                bm, 
                segments=32,
                radius=1,
                matrix=Matrix.Rotation(radians(90), 4, "X")
            )
            bm.to_mesh(mesh)
            bmesh.ops.create_circle(
                bm,
                segments=32,
                radius=1,
                matrix=Matrix.Rotation(radians(90), 4, "Y")
            )
            bm.to_mesh(mesh)
            
        elif self.msfs_gizmo_type == "box":
            bmesh.ops.create_cube(bm, size=2)
            
        elif self.msfs_gizmo_type == "cylinder":
            bmesh.ops.create_cone(
                bm, 
                cap_ends=True,
                segments=32,
                radius1=1,
                radius2=1,
                depth=2
            )  # Create cone with both ends having the same diameter - this creates a cylinder

        bm.to_mesh(mesh)
        bm.free()

        edges = []
        for edge in mesh.edges:
            edge_verts = []
            for vert in edge.vertices:
                edge_verts.append(mesh.vertices[vert])
            edges.append(edge_verts)

        self.custom_shape_edges = edges

    def get_matrix(self):
        # Re-calculate matrix without rotation
        if self.empty.msfs_gizmo_type == "sphere":
            scale = self.empty.scale[0] * self.empty.scale[1] * self.empty.scale[2]
            scale_matrix = (
                Matrix.Scale(scale, 3, (1, 0, 0))
                @ Matrix.Scale(scale, 3, (0, 1, 0))
                @ Matrix.Scale(scale, 3, (0, 0, 1))
            )
            
        elif self.empty.msfs_gizmo_type == "cylinder":
            scale_xy = self.empty.scale[0] * self.empty.scale[1]
            scale_matrix = (
                Matrix.Scale(scale_xy, 3, (1, 0, 0))
                @ Matrix.Scale(scale_xy, 3, (0, 1, 0))
                @ Matrix.Scale(self.empty.scale[2], 3, (0, 0, 1))
            )
            
        else: # Box
            scale_matrix = (
                Matrix.Scale(self.empty.scale[0], 3, (1, 0, 0))
                @ Matrix.Scale(self.empty.scale[1], 3, (0, 1, 0))
                @ Matrix.Scale(self.empty.scale[2], 3, (0, 0, 1))
            )

        matrix = Matrix.LocRotScale(
            self.empty.matrix_world.to_translation(),
            self.empty.matrix_world.to_quaternion(),
            scale_matrix.to_scale(),
        )
        return matrix

    def draw(self, context):
        if not self.custom_shape_edges or self.empty.hide_get():
            return
        
        matrix = self.get_matrix()

        bgl.glEnable(bgl.GL_BLEND)
        bgl.glEnable(bgl.GL_LINE_SMOOTH)
        bgl.glEnable(bgl.GL_DEPTH_TEST)

        # Use Blender theme colors to keep everything consistent
        draw_color = list(context.preferences.themes[0].view_3d.empty)
        if self.empty.select_get():
            draw_color = list(context.preferences.themes[0].view_3d.object_active)

        # Add alpha (there isn't any functions in the Color class 
        # to add an alpha, so we have to convert to a list)
        draw_color.append(1)  

        vertex_pos = []
        for edge in self.custom_shape_edges:
            line_start = self.apply_vert_transforms(edge[0], matrix=matrix)
            line_end = self.apply_vert_transforms(edge[1], matrix=matrix)

            vertex_pos.extend([line_start, line_end])

        self.draw_line_3d(
            draw_color,
            2,
            context.region,
            vertex_pos
        )

        # Restore OpenGL defaults
        bgl.glLineWidth(1)
        bgl.glDisable(bgl.GL_BLEND)
        bgl.glDisable(bgl.GL_LINE_SMOOTH)

    def apply_vert_transforms(self, vert, matrix):
        vert = list(vert.co)
        vert.append(1)
        multiplied_matrix = np.array(matrix).dot(np.array(vert))
        return multiplied_matrix[:-1].tolist()


class MSFS2020CollisionGizmoGroup(bpy.types.GizmoGroup):
    bl_idname = "VIEW3D_GT_msfs_collision_gizmo_group"
    bl_label = "MSFS2020 Collision Gizmo Group"
    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"
    bl_options = {"3D", "PERSISTENT", "SHOW_MODAL_ALL", "SELECT"}

    empties = {}

    @classmethod
    def poll(cls, context):
        for blender_object in context.view_layer.objects:
            if (
                blender_object.type == "EMPTY" 
                and blender_object.msfs_gizmo_type != "NONE"
            ):
                return True
            
        return False

    def setup(self, context):
        for blender_object in context.view_layer.objects:
            if (
                blender_object.type == "EMPTY"
                and blender_object.msfs_gizmo_type != "NONE"
                and blender_object not in self.__class__.empties
            ):
                gz = self.gizmos.new(MSFS2020CollisionGizmo.bl_idname)

                gz.msfs_gizmo_type = blender_object.msfs_gizmo_type
                gz.empty = blender_object

                gz.create_custom_shape()

                self.__class__.empties[blender_object] = gz

    def refresh(self, context):
        # We have to get a list of gizmo empties in the scene first 
        # in order to avoid a crash due to referencing a removed object
        found_empties = []
        for blender_object in context.view_layer.objects:
            if blender_object.type == "EMPTY" and blender_object.msfs_gizmo_type != "NONE":
                found_empties.append(blender_object)

        for _, (empty, gizmo) in enumerate(self.__class__.empties.copy().items()):
            if empty in found_empties:
                continue
            
            del self.__class__.empties[empty]
            if gizmo:
                self.gizmos.remove(gizmo)

        # Check if there are any new gizmo empties, 
        # and if so create new gizmo. 
        # We can't do this in the above loop due to the crash mentioned above
        for blender_object in context.view_layer.objects:
            if (
                blender_object.type == "EMPTY" 
                and blender_object.msfs_gizmo_type != "NONE"
                and blender_object not in self.__class__.empties
            ):
                    self.setup(context)


class MSFS2020CollisionAddMenu(bpy.types.Menu):
    bl_idname = "VIEW3D_MT_msfs_collision_add_menu"
    bl_label = "Microsoft Flight Simulator 2020 Collision"

    def draw(self, context):
        self.layout.operator(
            AddGizmo.bl_idname, 
            text="Sphere Collision", 
            icon="MESH_UVSPHERE",
        ).msfs_gizmo_type = "sphere"
        
        self.layout.operator(
            AddGizmo.bl_idname,
            text="Box Collision",
            icon="MESH_CUBE",
        ).msfs_gizmo_type = "box"
        
        self.layout.operator(
            AddGizmo.bl_idname,
            text="Cylinder Collision",
            icon="MESH_CYLINDER",
        ).msfs_gizmo_type = "cylinder"


def draw_menu(self, context):
    self.layout.menu(menu=MSFS2020CollisionAddMenu.bl_idname, icon="SHADING_BBOX")


def register():
    bpy.types.VIEW3D_MT_add.append(draw_menu)


def unregister():
    bpy.types.VIEW3D_MT_add.remove(draw_menu)
