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


class MSFS_Clearcoat(MSFS_Material):
    def __init__(self, material, buildTree=False):
        super().__init__(material, buildTree)

    def customShaderTree(self):
        super().defaultShadersTree()
        self.clearcoatShaderTree()

    def clearcoatShaderTree(self):
        ## Clearcoat Frame
        clearcoatFrame = self.addNode(
            name = MSFS_FrameNodes.clearcoatFrame.value,
            typeNode = MSFS_ShaderNodesTypes.nodeFrame.value,
            color = (0.6, 0.2, 0.1)
        )

        ## Clearcoat Texture
        # Out[0] : ClearcoatSeparate -> In[0]
        clearcoatTexNode = self.addNode(
            name = MSFS_ShaderNodes.clearcoatTex.value,
            typeNode = MSFS_ShaderNodesTypes.shaderNodeTexImage.value,
            location = (-1000.0, -500.0),
            frame = clearcoatFrame
        )

        ## Clearcoat separate
        # In[0] : ClearcoatTexture -> Out[0]
        clearcoatSeparateNode = self.addNode(
            name = MSFS_ShaderNodes.clearcoatSeparate.value,
            typeNode = MSFS_ShaderNodesTypes.shaderNodeSeparateColor.value,
            location = (-800.0, -500.0),
            frame = clearcoatFrame
        )

        self.link(clearcoatTexNode.outputs[0], clearcoatSeparateNode.inputs[0])

    def setClearcoatDirtTexture(self, tex):
        nodeClearcoat = self.getNodeByName(MSFS_ShaderNodes.clearcoatTex.value)
        nodeClearcoatSeparate = self.getNodeByName(MSFS_ShaderNodes.clearcoatSeparate.value)
        nodePrincipledBSDF = self.getNodeByName(MSFS_ShaderNodes.principledBSDF.value)

        if tex:
            nodeClearcoat.image = tex
            nodeClearcoat.image.colorspace_settings.name = "Non-Color"

            self.link(
                nodeClearcoatSeparate.outputs[0], 
                nodePrincipledBSDF.inputs[MSFS_PrincipledBSDFInputs.clearcoat.value]
            )
            self.link(
                nodeClearcoatSeparate.outputs[1], 
                nodePrincipledBSDF.inputs[MSFS_PrincipledBSDFInputs.clearcoatRoughness.value]
            )
            return
        
        self.unLinkNodeInput(
            nodePrincipledBSDF,
            MSFS_PrincipledBSDFInputs.clearcoat.value
        )
        self.unLinkNodeInput(
            nodePrincipledBSDF,
            MSFS_PrincipledBSDFInputs.clearcoatRoughness.value
        )
