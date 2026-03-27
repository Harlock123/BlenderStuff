import bpy
from bpy.props import (
    StringProperty,
    FloatProperty,
    IntProperty,
    EnumProperty,
    FloatVectorProperty,
    BoolProperty,
)

from .fonts import font_enum_items


class TextExtruderProperties(bpy.types.PropertyGroup):
    # Text content
    text_body: StringProperty(
        name="Text",
        description="The text to create as a 3D object",
        default="Hello",
    )

    # Font size
    font_size: FloatProperty(
        name="Font Size",
        description="Size of the text",
        default=1.0,
        min=0.01,
        max=100.0,
    )

    # Font selection (system fonts dropdown)
    font_path: EnumProperty(
        name="Font",
        description="System font to use for the text",
        items=font_enum_items,
    )

    # Custom font file (fallback for fonts not in system directories)
    custom_font_path: StringProperty(
        name="Custom Font",
        description="Path to a .ttf or .otf font file",
        subtype="FILE_PATH",
        default="",
    )

    use_custom_font: BoolProperty(
        name="Use Custom Font",
        description="Use a custom font file instead of a system font",
        default=False,
    )

    # Extrusion axis
    extrusion_axis: EnumProperty(
        name="Extrusion Axis",
        description="Axis along which to extrude the text",
        items=[
            ("X", "X", "Extrude along the X axis"),
            ("Y", "Y", "Extrude along the Y axis"),
            ("Z", "Z", "Extrude along the Z axis (default forward)"),
        ],
        default="Z",
    )

    # Face up axis (which direction the readable face of the text points)
    face_up_axis: EnumProperty(
        name="Face Up Axis",
        description="Axis the readable face of the text points toward",
        items=[
            ("X", "X", "Face points along the X axis"),
            ("Y", "Y", "Face points along the Y axis"),
            ("Z", "Z", "Face points along the Z axis"),
        ],
        default="Y",
    )

    # Extrusion depth
    extrusion_depth: FloatProperty(
        name="Extrusion Depth",
        description="Depth of the extrusion",
        default=0.2,
        min=0.001,
        max=50.0,
    )

    # Chamfer / Bevel
    enable_chamfer: BoolProperty(
        name="Enable Chamfer",
        description="Add a chamfer (bevel) to the edges",
        default=True,
    )

    chamfer_width: FloatProperty(
        name="Chamfer Width",
        description="Width of the chamfer bevel",
        default=0.02,
        min=0.001,
        max=10.0,
    )

    chamfer_segments: IntProperty(
        name="Chamfer Segments",
        description="Number of segments in the chamfer (1 = flat chamfer, higher = rounder)",
        default=2,
        min=1,
        max=20,
    )

    # Face material properties
    face_color: FloatVectorProperty(
        name="Face Color",
        description="Color for the front and back faces",
        subtype="COLOR",
        size=4,
        default=(0.8, 0.2, 0.2, 1.0),
        min=0.0,
        max=1.0,
    )

    face_metallic: FloatProperty(
        name="Face Metallic",
        description="Metallic value for face material",
        default=0.0,
        min=0.0,
        max=1.0,
    )

    face_roughness: FloatProperty(
        name="Face Roughness",
        description="Roughness value for face material",
        default=0.5,
        min=0.0,
        max=1.0,
    )

    # Edge (extruded side) material properties
    edge_color: FloatVectorProperty(
        name="Edge Color",
        description="Color for the extruded side surfaces",
        subtype="COLOR",
        size=4,
        default=(0.2, 0.2, 0.8, 1.0),
        min=0.0,
        max=1.0,
    )

    edge_metallic: FloatProperty(
        name="Edge Metallic",
        description="Metallic value for edge material",
        default=0.5,
        min=0.0,
        max=1.0,
    )

    edge_roughness: FloatProperty(
        name="Edge Roughness",
        description="Roughness value for edge material",
        default=0.3,
        min=0.0,
        max=1.0,
    )

    # Chamfer material properties
    chamfer_color: FloatVectorProperty(
        name="Chamfer Color",
        description="Color for the chamfer/bevel surfaces",
        subtype="COLOR",
        size=4,
        default=(0.6, 0.6, 0.1, 1.0),
        min=0.0,
        max=1.0,
    )

    chamfer_metallic: FloatProperty(
        name="Chamfer Metallic",
        description="Metallic value for chamfer material",
        default=0.3,
        min=0.0,
        max=1.0,
    )

    chamfer_roughness: FloatProperty(
        name="Chamfer Roughness",
        description="Roughness value for chamfer material",
        default=0.4,
        min=0.0,
        max=1.0,
    )


def register():
    bpy.utils.register_class(TextExtruderProperties)
    bpy.types.Scene.text_extruder = bpy.props.PointerProperty(
        type=TextExtruderProperties
    )


def unregister():
    del bpy.types.Scene.text_extruder
    bpy.utils.unregister_class(TextExtruderProperties)
