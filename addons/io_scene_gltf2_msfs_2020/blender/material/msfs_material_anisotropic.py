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
from ..msfs_material_function import MSFS2020_Material
from .utils.msfs_material_enum import (
    MSFS2020_AnisotropicNodes,
    MSFS2020_FrameNodes,
    MSFS2020_ShaderNodesTypes
)


class MSFS2020_Anisotropic(MSFS2020_Material):
    def __init__(self, material, buildTree=False):
        super().__init__(material, buildTree)

    def customShaderTree(self):
        super().defaultShadersTree()
        self.anisotropicShaderTree()
    
    def anisotropicShaderTree(self):
        anisotropicFrame = self.addNode(
            name = MSFS2020_FrameNodes.anisotropicFrame.value,
            typeNode = MSFS2020_ShaderNodesTypes.nodeFrame.value,
            color = (0.35, 0.6, 0.1)
        )
        ## Anisotropic Texture
        # Out[0] : Separate Anisotrpic -> In[0]
        anisotropicTexNode = self.addNode(
            name = MSFS2020_AnisotropicNodes.anisotropicTex.value,
            typeNode = "ShaderNodeTexImage",
            location = (-500.0, -800.0),
            width = 300.0,
            frame = anisotropicFrame)
        
        ## Separate Anisotropic
        # In[0] : Anisotropic Texture -> Out[0]
        separateAnisotropicNode = self.addNode(
            name = MSFS2020_AnisotropicNodes.separateAnisotropic.value,
            typeNode = "ShaderNodeSeparateRGB",
            location = (-100.0, -800.0),
            width = 300.0,
            frame = anisotropicFrame)
        # Links
        self.link(anisotropicTexNode.outputs[0], separateAnisotropicNode.inputs[0])
