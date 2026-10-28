# AGENTS.md

Notes for anyone, human or AI agent, changing this code. `README.md` covers installing and using the add-on, and
`SAMPLEANIMATIONHOWTO.md` walks through an animation made with it; this file covers how the code fits together and
how to change it safely.

## What this is

Text Extruder is a Blender extension (an add-on, written in Python against `bpy`). It makes 3D extruded text with an
optional chamfer, and gives the face, side walls and chamfer three separate materials. It needs Blender 5.1.0 or
later (`blender_version_min` in the manifest) and runs only inside Blender. `0001-0180.mp4` is a sample render of
the animation in the how-to.

## Commands

```bash
cd text_extruder && blender --command extension build --output-dir ..   # Blender's own packager
zip -r text_extruder.zip text_extruder -x '*/__pycache__/*' '*.pyc'      # matches the layout of the committed zip
```

To try a change, install the zip from Blender's Edit > Preferences > Get Extensions > Install from Disk, then open
the 3D Viewport sidebar (N) and its Text Extruder tab. There are no tests.

## Layout

- `text_extruder/blender_manifest.toml`: the extension's id, version, minimum Blender version and licence. It
  replaces the old `bl_info`.
- `text_extruder/__init__.py`: registers properties, then operators, then panels, and unregisters them in reverse.
- `text_extruder/properties.py`: `TextExtruderProperties`, every setting, attached as `bpy.types.Scene.text_extruder`.
- `text_extruder/operators.py`: `TEXT_EXTRUDER_OT_create` (`text_extruder.create`) does the work.
  - It adds a text object, extrudes and bevels it, converts it to a mesh and applies the rotation.
  - Then it gives each face a material by the angle of its normal to the Face Up axis: within 30 degrees is face,
    beyond 60 is edge, and between is chamfer.
- `text_extruder/panels.py`: the sidebar panel and its collapsible sub-panels (`TEXT_EXTRUDER_PT_*`), all in the
  "Text Extruder" category.
- `text_extruder/fonts.py`: finds `.ttf` and `.otf` fonts in the usual folders on macOS, Windows and Linux, for the
  font drop-down.
- `text_extruder.zip`: the packaged extension, committed for download.

## Rules that keep it working

- **Register in order.** Properties must exist before the operator and panels that read them. Keep the order in
  `__init__.py`, and add each new class to its module's `register()` and `unregister()`.
- **Keep Blender's naming.** Operators are `TEXT_EXTRUDER_OT_*` with a `text_extruder.*` id, and panels are
  `TEXT_EXTRUDER_PT_*`, as Blender expects (it warns about other class names).
- **Rebuild the zip with the code.** The committed `text_extruder.zip` is what people install. It holds the same
  files as `text_extruder/`, so rebuild it in the same change, and bump `version` in the manifest when you
  release.
- **Face Up and Extrusion axes must differ.** The operator reports an error and stops when they are the same,
  because it needs two axes to work out the orientation.
- **Materials follow the normals.** Without a chamfer, only the face and edge materials are used. A change to the
  geometry can move faces across the 30 and 60 degree lines, so check the materials after one.
