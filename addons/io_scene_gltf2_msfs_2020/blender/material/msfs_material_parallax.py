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
from ..msfs_material_function import MSFS_Material
from .utils.msfs_material_enum import (
    MSFS_FrameNodes,
    MSFS_PrincipledBSDFInputs,
    MSFS_ShaderNodes,
    MSFS_ShaderNodesTypes
)


class MSFS_Parallax(MSFS_Material):
    def __init__(self, material, buildTree=False):
        super().__init__(material, buildTree)

    def customShaderTree(self):
        super().defaultShadersTree()
        self.parallaxShaderTree()

    def parallaxShaderTree(self):
        ## Parallax Frame
        parallaxFrame = self.addNode(
            name = MSFS_FrameNodes.parallaxFrame.value,
            typeNode = MSFS_ShaderNodesTypes.nodeFrame.value,
            color = (0.5, 0.1, 0.3)
        )

        ## Behind Glass Texture
        # Out[0] : Albedo Detail Mix -> In[2]
        behindGlassTexNode = self.addNode(
            name = MSFS_ShaderNodes.behindGlassTex.value,
            typeNode = MSFS_ShaderNodesTypes.shaderNodeTexImage.value,
            location = (500, 500.0),
            frame = parallaxFrame
        )

        ## Albedo Detail Mix
        # In[2] :  Behind Glass Texture -> Out[0]
        albedoDetailMixNode = self.addNode(
            name = MSFS_ShaderNodes.albedoDetailMix.value,
            typeNode = MSFS_ShaderNodesTypes.shaderNodeMixRGB.value,
            blend_type = "MIX",
            location = (800.0, 500.0),
            frame = parallaxFrame
        )
        ##Links
        self.link(behindGlassTexNode.outputs[0], albedoDetailMixNode.inputs[2])

    def setDetailColorTex(self, tex):
        nodeAlbedoDetailMix = self.getNodeByName(MSFS_ShaderNodes.albedoDetailMix.value)
        nodeBehindGlassTex = self.getNodeByName(MSFS_ShaderNodes.behindGlassTex.value)
        nodeBaseColorMulRGB = self.getNodeByName(MSFS_ShaderNodes.baseColorMulRGB.value)
        nodePrincipledBSDF = self.getNodeByName(MSFS_ShaderNodes.principledBSDF.value)

        nodeBehindGlassTex.image = tex
        self.updateColorLinks()
        
        ## TODO - check if this is good
        self.link(
            nodeBaseColorMulRGB.outputs[0],
            nodeAlbedoDetailMix.inputs[1]
        )
        self.link(
            nodeAlbedoDetailMix.outputs[0],
            nodePrincipledBSDF.inputs[MSFS_PrincipledBSDFInputs.baseColor.value]
        )
