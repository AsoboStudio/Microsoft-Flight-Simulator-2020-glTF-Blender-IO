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
import struct
from urllib.parse import quote, unquote

import bpy
import numpy as np

from io_scene_gltf2.io.com.gltf2_io import Accessor, Buffer, BufferView

# glTF component types
BYTE = 5120
UNSIGNED_BYTE = 5121
SHORT = 5122
UNSIGNED_SHORT = 5123
UNSIGNED_INT = 5125
FLOAT = 5126

COMPONENT_DTYPES = {
    BYTE: np.int8,
    UNSIGNED_BYTE: np.uint8,
    SHORT: np.int16,
    UNSIGNED_SHORT: np.uint16,
    UNSIGNED_INT: np.uint32,
    FLOAT: np.float32,
}
TYPE_SIZES = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}

# DXGI formats for BC5 stored with a DX10 header
DXGI_FORMAT_BC5_UNORM = 83
DXGI_FORMAT_BC5_SNORM = 84


class MSFS2020OptimizedAsset:
    """
    Makes glTF files built by the MSFS2020 Package Builder (ASOBO_asset_optimized) importable.

    The Package Builder packs vertex data into formats that aren't valid glTF (half floats
    stored as SHORT, int8 normals and tangents), points textures at DDS files through
    MSFT_texture_dds, and writes skins whose vertices aren't in the space the inverse bind
    matrices expect. Everything is fixed up before the Khronos importer reads the data.
    """

    extension_name = "ASOBO_asset_optimized"

    def __new__(cls, *args, **kwargs):
        raise RuntimeError(f"{cls} should not be instantiated")

    @staticmethod
    def is_optimized(gltf):
        extensions = gltf.data.asset.extensions or {}
        return MSFS2020OptimizedAsset.extension_name in extensions

    @staticmethod
    def prepare(gltf):
        if not MSFS2020OptimizedAsset.is_optimized(gltf):
            return

        decoder = _AccessorDecoder(gltf)
        decoder.decode_meshes()
        decoder.rebind_skins()
        decoder.commit()

        MSFS2020OptimizedAsset.resolve_textures(gltf)

    # region Textures
    @staticmethod
    def resolve_textures(gltf):
        for texture in gltf.data.textures or []:
            dds = (texture.extensions or {}).get("MSFT_texture_dds")
            if dds is not None and texture.source is None:
                texture.source = dds["source"]

        model_dir = os.path.dirname(os.path.abspath(gltf.filename))
        search_dirs = MSFS2020OptimizedAsset.texture_search_dirs(model_dir)
        listings = {}

        for image in gltf.data.images or []:
            if not image.uri or image.uri.startswith("data:"):
                continue
            uri = image.uri.replace("\\", "/")
            if os.path.isfile(os.path.join(model_dir, uri)):
                image.uri = uri
                continue

            file_name = os.path.basename(uri).lower()
            for directory in search_dirs:
                if directory not in listings:
                    listings[directory] = {f.lower(): f for f in os.listdir(directory)}
                match = listings[directory].get(file_name)
                if match:
                    path = os.path.relpath(os.path.join(directory, match), model_dir)
                    image.uri = quote(path.replace(os.sep, "/"))
                    break
            else:
                gltf.log.warning(f"MSFS2020: could not find texture {uri}")

    @staticmethod
    def texture_search_dirs(model_dir):
        """
        Textures of a packaged aircraft live next to the model folder, in texture.* folders
        that can fall back to each other through texture.cfg. Liveries (folders with a
        texture.cfg) come first, followed by their fallbacks, then any remaining folder.
        """
        root = os.path.dirname(model_dir)
        folders = sorted(
            os.path.join(root, f)
            for f in os.listdir(root)
            if f.lower().startswith("texture") and os.path.isdir(os.path.join(root, f))
        )

        ordered = []

        def add(directory):
            directory = os.path.normpath(directory)
            if os.path.isdir(directory) and directory not in ordered:
                ordered.append(directory)

        for folder in folders:
            config = os.path.join(folder, "texture.cfg")
            if not os.path.isfile(config):
                continue
            add(folder)
            with open(config, errors="ignore") as f:
                for line in f:
                    key, _, value = line.partition("=")
                    if key.strip().lower().startswith("fallback"):
                        add(os.path.join(folder, value.strip().replace("\\", os.sep)))

        for folder in folders:
            add(folder)

        return ordered

    @staticmethod
    def load_bc5(gltf, img, blender_image):
        """
        Blender can't read BC5 DDS files, which the Package Builder uses for normal maps.
        Decode them here and replace the image the Khronos importer failed to load.
        """
        if not img.uri or not img.uri.lower().endswith(".dds"):
            return

        model_dir = os.path.dirname(os.path.abspath(gltf.filename))
        path = os.path.normpath(os.path.join(model_dir, unquote(img.uri.replace("\\", "/"))))
        if not os.path.isfile(path):
            return

        with open(path, "rb") as f:
            header = f.read(148)
        if len(header) < 128 or header[:4] != b"DDS ":
            return

        height, width = struct.unpack_from("<2I", header, 12)
        fourcc = header[84:88]
        offset = 128
        if fourcc in (b"BC5S",):
            signed = True
        elif fourcc in (b"BC5U", b"ATI2"):
            signed = False
        elif fourcc == b"DX10":
            dxgi_format = struct.unpack_from("<I", header, 128)[0]
            if dxgi_format not in (DXGI_FORMAT_BC5_UNORM, DXGI_FORMAT_BC5_SNORM):
                return
            signed = dxgi_format == DXGI_FORMAT_BC5_SNORM
            offset = 148
        else:
            return

        blocks_x, blocks_y = max(1, (width + 3) // 4), max(1, (height + 3) // 4)
        data = np.fromfile(path, np.uint8, count=blocks_x * blocks_y * 16, offset=offset)
        pixels = decode_bc5(data, width, height, signed)

        name = blender_image.name if blender_image else os.path.basename(path)
        if blender_image:
            bpy.data.images.remove(blender_image)
        image = bpy.data.images.new(name, width, height, alpha=False)
        # Must be set before the pixels, changing it regenerates the buffer
        image.colorspace_settings.name = "Non-Color"
        image.pixels.foreach_set(pixels.ravel())
        image.pack()
        img.blender_image_name = image.name

    # endregion


class _AccessorDecoder:
    """Rewrites the Package Builder vertex data into a new buffer of plain float accessors."""

    def __init__(self, gltf):
        self.gltf = gltf
        self.data = gltf.data
        self.buffer = bytearray()
        self.buffer_index = len(self.data.buffers)
        self.converted = {}
        self.parents = {
            child: index
            for index, node in enumerate(self.data.nodes or [])
            for child in (node.children or [])
        }

    # region Node transforms
    def local_matrix(self, node_index):
        node = self.data.nodes[node_index]
        if node.matrix is not None:
            return np.array(node.matrix, dtype=np.float64).reshape(4, 4).T

        x, y, z, w = node.rotation if node.rotation is not None else (0, 0, 0, 1)
        matrix = np.eye(4)
        matrix[:3, :3] = np.array(
            [
                [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
            ]
        ) * np.array(node.scale if node.scale is not None else (1, 1, 1))
        matrix[:3, 3] = node.translation if node.translation is not None else (0, 0, 0)
        return matrix

    def world_matrix(self, node_index):
        matrix = self.local_matrix(node_index)
        while node_index in self.parents:
            node_index = self.parents[node_index]
            matrix = self.local_matrix(node_index) @ matrix
        return matrix

    # endregion

    # region Reading / writing
    def read(self, accessor_index, dtype=None):
        from io_scene_gltf2.io.imp.gltf2_io_binary import BinaryData

        accessor = self.data.accessors[accessor_index]
        array = BinaryData.decode_accessor_obj(self.gltf, accessor)
        if dtype is not None:
            array = np.ascontiguousarray(array).view(dtype)
        return array

    def write(self, array, accessor_type, target=None, bounds=False, component_type=FLOAT):
        array = np.ascontiguousarray(array, dtype=COMPONENT_DTYPES[component_type])
        while len(self.buffer) % 4:
            self.buffer.append(0)

        buffer_view = BufferView.from_dict(
            {
                "buffer": self.buffer_index,
                "byteOffset": len(self.buffer),
                "byteLength": array.nbytes,
                **({"target": target} if target else {}),
            }
        )
        self.buffer.extend(array.tobytes())
        self.data.buffer_views.append(buffer_view)

        accessor = {
            "bufferView": len(self.data.buffer_views) - 1,
            "componentType": component_type,
            "count": len(array),
            "type": accessor_type,
        }
        if bounds:
            accessor["min"] = array.min(axis=0).tolist()
            accessor["max"] = array.max(axis=0).tolist()
        self.data.accessors.append(Accessor.from_dict(accessor))
        return len(self.data.accessors) - 1

    def commit(self):
        if not self.buffer:
            return
        self.data.buffers.append(Buffer.from_dict({"byteLength": len(self.buffer)}))
        self.gltf.buffers[self.buffer_index] = memoryview(bytes(self.buffer))

    # endregion

    # region Attributes
    def convert(self, semantic, accessor_index, transform=None):
        key = (semantic, accessor_index, None if transform is None else transform.tobytes())
        if key in self.converted:
            return self.converted[key]

        accessor = self.data.accessors[accessor_index]
        component_type = accessor.component_type
        result = accessor_index

        if semantic == "POSITION" and transform is not None:
            positions = self.read(accessor_index).astype(np.float64)
            positions = positions @ transform[:3, :3].T + transform[:3, 3]
            result = self.write(positions, "VEC3", target=34962, bounds=True)

        elif semantic in ("NORMAL", "TANGENT") and (component_type == BYTE or transform is not None):
            vectors = self.read(accessor_index).astype(np.float64)
            xyz = vectors[:, :3]
            if transform is not None:
                linear = transform[:3, :3]
                xyz = xyz @ (linear if semantic == "TANGENT" else np.linalg.inv(linear).T).T
            xyz /= np.maximum(np.linalg.norm(xyz, axis=1, keepdims=True), 1e-9)
            if semantic == "NORMAL":
                result = self.write(xyz, "VEC3", target=34962)
            else:
                handedness = np.where(vectors[:, 3:4] < 0, -1.0, 1.0)
                result = self.write(np.hstack([xyz, handedness]), "VEC4", target=34962)

        elif semantic.startswith("TEXCOORD_") and component_type in (SHORT, UNSIGNED_SHORT):
            # Half floats, despite the component type
            uvs = self.read(accessor_index, np.float16).astype(np.float32)
            result = self.write(uvs, "VEC2", target=34962)

        elif semantic.startswith("COLOR_") and not accessor.normalized:
            if component_type in (SHORT, UNSIGNED_SHORT):
                colors = self.read(accessor_index, np.float16).astype(np.float32)
            elif component_type in (BYTE, UNSIGNED_BYTE):
                colors = self.read(accessor_index, np.uint8) / 255.0
            else:
                colors = None
            if colors is not None:
                result = self.write(np.clip(colors, 0.0, 1.0), accessor.type, target=34962)

        self.converted[key] = result
        return result

    def decode_meshes(self):
        skinned = self.skinned_mesh_transforms()

        for mesh_index, mesh in enumerate(self.data.meshes or []):
            transform = skinned.get(mesh_index)
            for primitive in mesh.primitives:
                primitive.attributes = {
                    semantic: self.convert(semantic, accessor_index, transform)
                    for semantic, accessor_index in primitive.attributes.items()
                }
                if primitive.indices is not None:
                    primitive.indices = self.convert_indices(primitive)

    def convert_indices(self, primitive):
        """
        Primitives of a mesh share one index accessor: extras.ASOBO_primitive says which
        slice each one draws (StartIndex, PrimitiveCount triangles), plus a BaseVertexIndex
        used to address past 65535 with 16 bit indices. Triangles are also wound clockwise,
        the opposite of glTF.
        """
        info = (primitive.extras or {}).get("ASOBO_primitive") or {}
        indices = self.read(primitive.indices).reshape(-1).astype(np.uint32)
        if "PrimitiveCount" in info:
            start = info.get("StartIndex", 0)
            indices = indices[start:start + 3 * info["PrimitiveCount"]]
            indices = indices + info.get("BaseVertexIndex", 0)
        indices = indices.reshape(-1, 3)[:, [0, 2, 1]].reshape(-1)
        return self.write(indices, "SCALAR", target=34963, component_type=UNSIGNED_INT)

    # endregion

    # region Skins
    def skin_space(self, skin):
        """
        Package Builder skinned vertices are expressed in the space of the parent of the
        skin's skeleton root, not in the bind space of the inverse bind matrices.
        """
        root = skin.skeleton if skin.skeleton is not None else skin.joints[0]
        if root in self.parents:
            return self.world_matrix(self.parents[root])
        return np.eye(4)

    def skinned_mesh_transforms(self):
        transforms = {}
        for node in self.data.nodes or []:
            if node.skin is None or node.mesh is None:
                continue
            transform = self.skin_space(self.data.skins[node.skin])
            previous = transforms.setdefault(node.mesh, transform)
            if not np.allclose(previous, transform):
                self.gltf.log.warning(
                    f"MSFS2020: mesh {node.mesh} is skinned in different spaces, using the first one"
                )
        return transforms

    def rebind_skins(self):
        # Vertices are now in model space, so bind every joint at its rest pose
        for skin in self.data.skins or []:
            inverse_bind_matrices = np.array(
                [np.linalg.inv(self.world_matrix(joint)) for joint in skin.joints]
            )
            # glTF matrices are column major
            columns = inverse_bind_matrices.transpose(0, 2, 1).reshape(-1, 16)
            skin.inverse_bind_matrices = self.write(columns, "MAT4")

    # endregion


def decode_bc4(blocks, signed):
    """Decodes BC4 blocks (n, 8) into texel values (n, 16) in the [-1, 1] or [0, 1] range."""
    endpoints = blocks[:, :2].view(np.int8 if signed else np.uint8).astype(np.float32)
    e0, e1 = endpoints[:, 0:1], endpoints[:, 1:2]

    bits = np.zeros(len(blocks), dtype=np.uint64)
    for i in range(6):
        bits |= blocks[:, 2 + i].astype(np.uint64) << np.uint64(8 * i)
    indices = (bits[:, None] >> (np.arange(16, dtype=np.uint64) * np.uint64(3))) & np.uint64(7)

    weights = np.arange(1, 7, dtype=np.float32)
    eight = np.hstack([e0, e1] + [((7 - w) * e0 + w * e1) / 7 for w in weights])
    low, high = (-127.0, 127.0) if signed else (0.0, 255.0)
    six = np.hstack(
        [e0, e1]
        + [((5 - w) * e0 + w * e1) / 5 for w in weights[:4]]
        + [np.full_like(e0, low), np.full_like(e0, high)]
    )
    palette = np.where(e0 > e1, eight, six)
    values = np.take_along_axis(palette, indices.astype(np.intp), axis=1)
    return np.clip(values / 127.0, -1.0, 1.0) if signed else values / 255.0


def decode_bc5(data, width, height, signed):
    """Decodes a BC5 normal map into Blender RGBA pixels (bottom-up), rebuilding the Z channel."""
    blocks_x, blocks_y = max(1, (width + 3) // 4), max(1, (height + 3) // 4)
    blocks = data.reshape(-1, 16)

    channels = []
    for half in (blocks[:, :8], blocks[:, 8:]):
        values = decode_bc4(np.ascontiguousarray(half), signed)
        if not signed:
            values = values * 2.0 - 1.0
        # (blocks_y, blocks_x, 4, 4) -> (rows, columns)
        values = values.reshape(blocks_y, blocks_x, 4, 4).transpose(0, 2, 1, 3)
        channels.append(values.reshape(blocks_y * 4, blocks_x * 4)[:height, :width])

    x, y = channels
    z = np.sqrt(np.clip(1.0 - x * x - y * y, 0.0, 1.0))
    rgb = np.stack([x, y, z], axis=-1) * 0.5 + 0.5
    rgba = np.concatenate([rgb, np.ones_like(x)[..., None]], axis=-1)
    return np.flipud(rgba).astype(np.float32)
