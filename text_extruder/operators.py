import math

import bpy
import bmesh
from mathutils import Matrix, Vector


def _create_material(name, color, metallic, roughness):
    """Create a Principled BSDF material with the given parameters."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
    return mat


def _axis_vector(axis_name):
    """Return a unit vector for the given axis name."""
    return {
        "X": Vector((1, 0, 0)),
        "Y": Vector((0, 1, 0)),
        "Z": Vector((0, 0, 1)),
    }[axis_name]


def _compute_orientation(face_up_axis, extrusion_axis):
    """Compute an Euler rotation that orients the text so its readable face
    points toward *-face_up_axis* (facing the viewer on that side) and the
    characters stand upright along *extrusion_axis*.

    Blender text defaults: front face = local +Z, character up = local +Y,
    reading direction = local +X.

    We map:
      local +Y (char up)   → +extrusion_axis
      local +Z (front face) → -face_up_axis  (so viewers on -face_up side see it)
      local +X (char right) → derived cross product
    """
    char_up = _axis_vector(extrusion_axis)
    face_normal = -_axis_vector(face_up_axis)
    char_right = char_up.cross(face_normal)

    # For counter-cyclic axis pairs the cross product points negative,
    # which would mirror the text.  Negate face_normal to keep text readable
    # (the face then points toward +face_up_axis instead of -face_up_axis).
    if char_right.x + char_right.y + char_right.z < 0:
        face_normal = -face_normal
        char_right = char_up.cross(face_normal)

    # Columns: [where X maps, where Y maps, where Z maps]
    rot_matrix = Matrix((char_right, char_up, face_normal)).transposed()
    return rot_matrix.to_euler()


def _classify_and_assign_materials(obj, axis_name, has_chamfer=False):
    """Assign material indices based on face normal angle to the face-up axis.

    Three-material classification (when chamfer is enabled):
      0 = front/back face  (normal nearly parallel to axis, dot >= cos 30°)
      1 = edge / side       (normal nearly perpendicular,    dot <= cos 60°)
      2 = chamfer            (normal at intermediate angle,   between the two)

    When chamfer is disabled, only indices 0 and 1 are used.
    """
    axis_vec = _axis_vector(axis_name)
    face_threshold = math.cos(math.radians(30.0))
    edge_threshold = math.cos(math.radians(60.0))

    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.faces.ensure_lookup_table()

    for face in bm.faces:
        dot = abs(face.normal.dot(axis_vec))
        if dot >= face_threshold:
            face.material_index = 0  # front/back face
        elif dot <= edge_threshold or not has_chamfer:
            face.material_index = 1  # extruded side / edge
        else:
            face.material_index = 2  # chamfer surface

    bm.to_mesh(obj.data)
    bm.free()


class TEXT_EXTRUDER_OT_create(bpy.types.Operator):
    """Create a 3D extruded text object with chamfer and multi-material"""

    bl_idname = "text_extruder.create"
    bl_label = "Create Extruded Text"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.text_extruder

        # Validate that face-up and extrusion axes are different.
        if props.face_up_axis == props.extrusion_axis:
            self.report(
                {"ERROR"},
                "Face Up Axis and Extrusion Axis must be different",
            )
            return {"CANCELLED"}

        # --- 1. Create the text object ---
        bpy.ops.object.text_add(location=(0, 0, 0))
        text_obj = context.active_object
        text_obj.data.body = props.text_body
        text_obj.data.size = props.font_size

        # --- Load font ---
        font_file = None
        if props.use_custom_font and props.custom_font_path:
            font_file = props.custom_font_path
        elif not props.use_custom_font and props.font_path != "__DEFAULT__":
            font_file = props.font_path

        if font_file:
            try:
                font_data = bpy.data.fonts.load(font_file)
                text_obj.data.font = font_data
            except RuntimeError:
                self.report({"WARNING"}, f"Could not load font: {font_file}")


        # Blender's native text extrusion is always along the local Z of the
        # text object.  We set the extrude value here, then rotate the object
        # so that the face-up and extrusion axes match the user's choices.
        text_obj.data.extrude = props.extrusion_depth / 2.0
        text_obj.data.offset_y = -props.font_size / 2.0

        # --- 3. Chamfer — applied at the curve level before mesh conversion ---
        if props.enable_chamfer:
            text_obj.data.bevel_depth = props.chamfer_width
            text_obj.data.bevel_resolution = props.chamfer_segments

        text_obj.data.align_x = "CENTER"
        text_obj.data.align_y = "CENTER"

        # Orient the text: face normal → face_up_axis, character up → extrusion_axis.
        text_obj.rotation_euler = _compute_orientation(
            props.face_up_axis, props.extrusion_axis,
        )

        # --- 2. Convert to mesh (chamfer geometry is already baked in) ---
        bpy.ops.object.convert(target="MESH")
        mesh_obj = context.active_object
        mesh_obj.name = f"TextExtrude_{props.text_body[:16]}"

        # Apply rotation so the mesh data reflects the world orientation.
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

        # --- 4. Create materials ---
        face_mat = _create_material(
            f"{mesh_obj.name}_FaceMat",
            props.face_color,
            props.face_metallic,
            props.face_roughness,
        )
        edge_mat = _create_material(
            f"{mesh_obj.name}_EdgeMat",
            props.edge_color,
            props.edge_metallic,
            props.edge_roughness,
        )

        mesh_obj.data.materials.append(face_mat)   # index 0
        mesh_obj.data.materials.append(edge_mat)    # index 1

        if props.enable_chamfer:
            chamfer_mat = _create_material(
                f"{mesh_obj.name}_ChamferMat",
                props.chamfer_color,
                props.chamfer_metallic,
                props.chamfer_roughness,
            )
            mesh_obj.data.materials.append(chamfer_mat)  # index 2

        # --- 5. Assign materials per face ---
        _classify_and_assign_materials(
            mesh_obj, props.face_up_axis, has_chamfer=props.enable_chamfer,
        )

        # --- 6. Smooth shading for nicer chamfer look ---
        bpy.ops.object.shade_smooth()

        self.report({"INFO"}, f"Created extruded text: {props.text_body}")
        return {"FINISHED"}


def register():
    bpy.utils.register_class(TEXT_EXTRUDER_OT_create)


def unregister():
    bpy.utils.unregister_class(TEXT_EXTRUDER_OT_create)
