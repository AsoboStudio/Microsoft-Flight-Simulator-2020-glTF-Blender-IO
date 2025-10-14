# glTF-Blender-IO-MSFS2020
# Copyright 2018-2021 The glTF-Blender-IO authors
# Copyright 2022 The glTF-Blender-IO-MSFS2020 authors
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


EXPORT_IMAGE_FORMAT = ()
EXPORT_ANIMATION_MODE = ()

if bpy.app.version < (4, 2, 0):
    EXPORT_IMAGE_FORMAT = (
        (
            "AUTO",
            "Automatic",
            "Save PNGs as PNGs and JPEGs as JPEGs. If neither one, use PNG",
        ),
        (
            "JPEG",
            "JPEG Format (.jpg)",
            "Save images as JPEGs. (Images that need alpha are saved as PNGs though.) "
            "Be aware of a possible loss in quality",
        ),
        (
            "NONE",
            "None",
            "Don\'t export images"
        )
    )
    
    EXPORT_ANIMATION_MODE = (
        (
            "ACTIONS",
            "Actions",
            "Export actions (actives and on NLA tracks) as separate animations"
        ),
        (
            "ACTIVE_ACTIONS",
            "Active actions merged",
            "All the currently assigned actions become one glTF animation"
        ),
        (
            "NLA_TRACKS",
            "NLA Tracks",
            "Export individual NLA Tracks as separate animation"
        ),
        (
            "SCENE",
            "Scene",
            "Export baked scene as a single animation"
        )
    )
else:
    EXPORT_IMAGE_FORMAT = (
        (
            "AUTO", 
            "Automatic",
            "Save PNGs as PNGs, JPEGs as JPEGs, WebPs as WebPs. "
            "For other formats, use PNG"
        ),
        (
            "JPEG",
            "JPEG Format (.jpg)",
            "Save images as JPEGs. (Images that need alpha are saved as PNGs though.) "
            "Be aware of a possible loss in quality"
        ),
        (
            "WEBP",
            "WebP Format",
            "Save images as WebPs as main image (no fallback)"
        ),
        (
            "NONE",
            "None",
            "Don\'t export images"
        )
    )
    
    EXPORT_ANIMATION_MODE = (
        (
            "ACTIONS",
            "Actions",
            "Export actions (actives and on NLA tracks) as separate animations"
        ),
        (
            "ACTIVE_ACTIONS",
            "Active actions merged",
            "All the currently assigned actions become one glTF animation"
        ),
        (
            "BROADCAST",
            "Broadcast actions",
            "Broadcast all compatible actions to all objects. "
            "Animated objects will get all actions compatible with them, "
            "others will get no animation at all"
        ),
        (
            "NLA_TRACKS",
            "NLA Tracks",
            "Export individual NLA Tracks as separate animation"
        ),
        (
            "SCENE",
            "Scene",
            "Export baked scene as a single animation"
        )
    )
