# Sample Animation: Text Fly-In, Tumble, and Fly-Out

A step-by-step guide to creating an animation in Blender where a Text Extruder object flies into view from behind the default camera, tumbles in the center of the screen, and then flies back out through the camera.

## 1. Create the Text Object

1. Open the **Text Extruder** sidebar panel (press **N** in the 3D Viewport)
2. Configure your text, font, materials, etc.
3. Click **Create Extruded Text**
4. Note the object name in the Outliner (e.g., `TextExtrude_Hello`)

## 2. Set Up the Timeline

1. At the bottom of the screen, find the **Timeline** editor
2. Set the frame range: **Start = 1**, **End = 180** (that gives you ~7.5 seconds at 24fps)
3. Press **Numpad 0** to switch to the camera view so you can see what you're framing

## 3. Keyframe the Animation

The animation has 3 phases:
- **Frames 1–40**: Fly in from behind the camera
- **Frames 40–140**: Tumble in the center
- **Frames 140–180**: Fly out back through the camera

### Phase 1: Starting Position (Behind Camera)

1. Select your text object
2. Go to **Frame 1** (click in the Timeline or type `1` in the frame field)
3. Press **N** to open the sidebar, switch to the **Item** tab
4. Set the object's **Location**:
   - X = **0**, Y = **-15**, Z = **0**
   - (This places it behind the default camera, which sits at roughly Y = -7)
5. Set **Rotation** to X = **0**, Y = **0**, Z = **0**
6. Hover over the **Location** fields, press **I** to insert a keyframe (they turn yellow)
7. Hover over the **Rotation** fields, press **I** to insert a keyframe

### Phase 2: Arrive at Center (Frame 40)

1. Go to **Frame 40**
2. Set **Location**: X = **0**, Y = **0**, Z = **0**
3. Set **Rotation**: X = **0**, Y = **0**, Z = **0**
4. Insert keyframes on both Location (**I**) and Rotation (**I**)

### Phase 3: Mid-Tumble (Frame 70)

1. Go to **Frame 70**
2. Keep **Location**: X = **0**, Y = **0**, Z = **0**
3. Set **Rotation**: X = **120**, Y = **45**, Z = **90**
4. Insert keyframes on both Location and Rotation

### Phase 4: Continue Tumble (Frame 100)

1. Go to **Frame 100**
2. **Location**: X = **0**, Y = **0**, Z = **0**
3. **Rotation**: X = **240**, Y = **-60**, Z = **200**
4. Insert keyframes on both

### Phase 5: Settle Before Exit (Frame 140)

1. Go to **Frame 140**
2. **Location**: X = **0**, Y = **0**, Z = **0**
3. **Rotation**: X = **360**, Y = **0**, Z = **360**
4. Insert keyframes on both

### Phase 6: Fly Out Behind Camera (Frame 180)

1. Go to **Frame 180**
2. **Location**: X = **0**, Y = **-15**, Z = **0**
3. **Rotation**: X = **360**, Y = **0**, Z = **360**
4. Insert keyframes on both

## 4. Smooth the Motion Curves

By default Blender uses Bezier interpolation, which is fine, but the fly-in and fly-out look better with easing:

1. Select the text object
2. Open the **Graph Editor** (change an editor panel type, or go to the **Animation** workspace via the tabs at the top)
3. Press **A** to select all keyframe curves
4. Press **T** to open the interpolation menu
5. For a smooth cinematic feel, choose **Bezier** (default) — or try **Back** for a slight overshoot effect on the fly-in

To make the tumble feel more playful:

6. In the Graph Editor, find the **Rotation** curves (the middle keyframes between frames 40–140)
7. Select individual handles and drag them to create more dramatic arcs
8. You can also press **N** in the Graph Editor to adjust handle types in the sidebar

## 5. Add Motion Blur (Optional)

1. Go to **Render Properties** (camera icon in the Properties panel)
2. Check **Motion Blur**
3. Set **Shutter** to **0.5** for a natural look

## 6. Preview the Animation

1. Switch to camera view (**Numpad 0**)
2. Press **Space** (or **Alt+A** in older Blender versions) to play the animation
3. Adjust keyframe positions or rotation values if the timing feels off

## 7. Render

1. Set your output path in **Output Properties** > **Output** > **File Path**
2. Choose a format (e.g., **FFmpeg Video** for MP4, or **PNG** sequence for frames)
3. If using FFmpeg, under **Encoding** set Container to **MPEG-4** and Codec to **H.264**
4. Go to **Render > Render Animation** (or press **Ctrl+F12**)

## Quick Reference: Keyframe Summary

| Frame | Location (X, Y, Z) | Rotation (X, Y, Z) | Phase |
|-------|-------------------|-------------------|-------|
| 1     | 0, -15, 0         | 0, 0, 0           | Behind camera |
| 40    | 0, 0, 0           | 0, 0, 0           | Arrive center |
| 70    | 0, 0, 0           | 120, 45, 90       | Tumbling |
| 100   | 0, 0, 0           | 240, -60, 200     | Tumbling |
| 140   | 0, 0, 0           | 360, 0, 360       | Settle |
| 180   | 0, -15, 0         | 360, 0, 360       | Fly out |

## Tips

- **Adjust Y = -15** if your camera is in a different position — the goal is to start/end behind the camera so the text isn't visible.
- To make the tumble more chaotic, add extra keyframes between frames 40–140 with wilder rotation values.
- To make it smoother, reduce the number of tumble keyframes and let Bezier interpolation do the work.
- Add a **light source** (Shift+A > Light > Area) pointing at the origin so the materials are visible during the animation.
