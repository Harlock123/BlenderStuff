import bpy


# ---------------------------------------------------------------------------
# Main panel — just the create button, always visible
# ---------------------------------------------------------------------------
class TEXT_EXTRUDER_PT_main(bpy.types.Panel):
    bl_label = "Text Extruder"
    bl_idname = "TEXT_EXTRUDER_PT_main"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Text Extruder"

    def draw(self, context):
        self.layout.operator("text_extruder.create", icon="MESH_DATA")


# ---------------------------------------------------------------------------
# Sub-panel: Text
# ---------------------------------------------------------------------------
class TEXT_EXTRUDER_PT_text(bpy.types.Panel):
    bl_label = "Text"
    bl_idname = "TEXT_EXTRUDER_PT_text"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Text Extruder"
    bl_parent_id = "TEXT_EXTRUDER_PT_main"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        props = context.scene.text_extruder

        layout.prop(props, "text_body")
        layout.prop(props, "font_size")
        layout.prop(props, "use_custom_font")
        if props.use_custom_font:
            layout.prop(props, "custom_font_path")
        else:
            layout.prop(props, "font_path")


# ---------------------------------------------------------------------------
# Sub-panel: Extrusion
# ---------------------------------------------------------------------------
class TEXT_EXTRUDER_PT_extrusion(bpy.types.Panel):
    bl_label = "Extrusion"
    bl_idname = "TEXT_EXTRUDER_PT_extrusion"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Text Extruder"
    bl_parent_id = "TEXT_EXTRUDER_PT_main"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        props = context.scene.text_extruder

        layout.prop(props, "face_up_axis")
        layout.prop(props, "extrusion_axis")
        layout.prop(props, "extrusion_depth")


# ---------------------------------------------------------------------------
# Sub-panel: Chamfer
# ---------------------------------------------------------------------------
class TEXT_EXTRUDER_PT_chamfer(bpy.types.Panel):
    bl_label = "Chamfer"
    bl_idname = "TEXT_EXTRUDER_PT_chamfer"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Text Extruder"
    bl_parent_id = "TEXT_EXTRUDER_PT_main"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.prop(context.scene.text_extruder, "enable_chamfer", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        props = context.scene.text_extruder

        layout.active = props.enable_chamfer
        layout.prop(props, "chamfer_width")
        layout.prop(props, "chamfer_segments")


# ---------------------------------------------------------------------------
# Helper to draw a material section (color + metallic/roughness on one row)
# ---------------------------------------------------------------------------
def _draw_material(layout, props, prefix):
    layout.use_property_split = True
    layout.use_property_decorate = False
    layout.prop(props, f"{prefix}_color")
    row = layout.row(align=True)
    row.prop(props, f"{prefix}_metallic")
    row.prop(props, f"{prefix}_roughness")


# ---------------------------------------------------------------------------
# Sub-panel: Face Material
# ---------------------------------------------------------------------------
class TEXT_EXTRUDER_PT_mat_face(bpy.types.Panel):
    bl_label = "Face Material"
    bl_idname = "TEXT_EXTRUDER_PT_mat_face"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Text Extruder"
    bl_parent_id = "TEXT_EXTRUDER_PT_main"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        _draw_material(self.layout, context.scene.text_extruder, "face")


# ---------------------------------------------------------------------------
# Sub-panel: Edge Material
# ---------------------------------------------------------------------------
class TEXT_EXTRUDER_PT_mat_edge(bpy.types.Panel):
    bl_label = "Edge Material"
    bl_idname = "TEXT_EXTRUDER_PT_mat_edge"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Text Extruder"
    bl_parent_id = "TEXT_EXTRUDER_PT_main"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        _draw_material(self.layout, context.scene.text_extruder, "edge")


# ---------------------------------------------------------------------------
# Sub-panel: Chamfer Material
# ---------------------------------------------------------------------------
class TEXT_EXTRUDER_PT_mat_chamfer(bpy.types.Panel):
    bl_label = "Chamfer Material"
    bl_idname = "TEXT_EXTRUDER_PT_mat_chamfer"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Text Extruder"
    bl_parent_id = "TEXT_EXTRUDER_PT_main"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return context.scene.text_extruder.enable_chamfer

    def draw(self, context):
        _draw_material(self.layout, context.scene.text_extruder, "chamfer")


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------
_classes = (
    TEXT_EXTRUDER_PT_main,
    TEXT_EXTRUDER_PT_text,
    TEXT_EXTRUDER_PT_extrusion,
    TEXT_EXTRUDER_PT_chamfer,
    TEXT_EXTRUDER_PT_mat_face,
    TEXT_EXTRUDER_PT_mat_edge,
    TEXT_EXTRUDER_PT_mat_chamfer,
)


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
