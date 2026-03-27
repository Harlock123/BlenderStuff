# Text Extruder — Blender 5.1 Extension

A Blender extension that creates 3D extruded text objects with configurable chamfering and independent materials for the face, edges, and chamfer surfaces.

## Features

- **3D text extrusion** from any text string with adjustable depth
- **Chamfer/bevel** on all edges with configurable width and segment count
- **Three independent materials** — assign different colors, metallic, and roughness values to:
  - **Face** — the front and back readable surfaces
  - **Edge** — the extruded side walls
  - **Chamfer** — the beveled transition surfaces
- **Axis control** — choose which axis the readable face points toward and which axis the text stands upright along
- **Font selection** — pick from any system-installed `.ttf`/`.otf` font via a dropdown, or browse for a custom font file
- **Cross-platform font scanning** — automatically finds fonts on macOS, Windows, and Linux
- **Collapsible UI** — organized into sub-panels that expand/collapse independently so the sidebar stays compact

## Requirements

- Blender **5.1.0** or later

## Installation

1. Download `text_extruder.zip`
2. Open Blender
3. Go to **Edit > Preferences > Get Extensions**
4. Click the dropdown menu (top-right) and select **Install from Disk**
5. Navigate to and select `text_extruder.zip`
6. The extension is enabled automatically

To uninstall, return to **Get Extensions**, find "Text Extruder" in the list, and click the remove button.

## Usage

### Opening the Panel

1. In the **3D Viewport**, press **N** to open the sidebar
2. Click the **Text Extruder** tab

### Panel Layout

The panel is organized into collapsible sections. Click a section header to expand or collapse it.

```
▼ Text Extruder
    [Create Extruded Text]     ← always visible at the top
  ► Text                       ← text content, font size, font selection
  ► Extrusion                  ← face-up axis, extrusion axis, depth
  ► ☑ Chamfer                  ← toggle + width and segment controls
  ► Face Material              ← color, metallic, roughness for front/back
  ► Edge Material              ← color, metallic, roughness for sides
  ► Chamfer Material           ← color, metallic, roughness for bevels
```

### Creating Extruded Text

1. Expand the **Text** section and type your text. Choose a font size and optionally select a system font or browse for a custom `.ttf`/`.otf` file.

2. Expand the **Extrusion** section to configure orientation:
   - **Face Up Axis** — the axis the readable face of the text points toward (default: **Y**, facing the front viewport)
   - **Extrusion Axis** — the axis the text characters stand upright along (default: **Z**, characters point up)
   - **Extrusion Depth** — the thickness/depth of the text object
   - Face Up and Extrusion axes must be different.

3. In the **Chamfer** section, toggle chamfering on/off using the checkbox in the header. When enabled:
   - **Chamfer Width** — how far the bevel extends from each edge
   - **Chamfer Segments** — number of subdivisions (1 = flat chamfer, higher = smoother/rounder)

4. Configure materials in the **Face Material**, **Edge Material**, and **Chamfer Material** sections. Each has:
   - **Color** — base color (RGBA)
   - **Metallic** — 0.0 (dielectric) to 1.0 (fully metallic)
   - **Roughness** — 0.0 (mirror-smooth) to 1.0 (fully rough)

5. Click **Create Extruded Text**.

The resulting mesh object is placed at the world origin with materials applied automatically. Each time you click Create, a new independent mesh object is generated — you can adjust settings between clicks to create multiple text objects with different configurations.

### Material Assignment

Materials are assigned automatically based on the angle of each mesh face's normal relative to the Face Up axis:

| Surface | Normal angle to Face Up axis | Default color |
|---------|------------------------------|---------------|
| Face    | Within 30°  (nearly parallel) | Red           |
| Edge    | Beyond 60°  (nearly perpendicular) | Blue    |
| Chamfer | Between 30°–60° (transition)  | Gold          |

All materials use Blender's **Principled BSDF** shader and are fully editable in the Shader Editor after creation.

## Project Structure

```
text_extruder/
├── blender_manifest.toml   — Extension metadata (replaces bl_info)
├── __init__.py             — Registration entry point
├── properties.py           — All user-configurable properties
├── operators.py            — Core logic: text creation, orientation, materials
├── panels.py               — Sidebar UI with collapsible sub-panels
└── fonts.py                — Cross-platform system font scanner
```

## License

GPL-3.0-or-later (compatible with Blender's license)
