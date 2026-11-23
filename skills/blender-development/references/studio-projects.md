# Blender Studio project studies

Use these [Blender Studio productions](https://studio.blender.org/projects/) to choose a technique, then verify its implementation in Blender 5.2. The articles explain the original workflow. Some videos and production files require a Studio subscription. The exercises below use original geometry and require no project downloads.

## Sprite Fright · Reusable set dressing

The team established the large shapes of a set, filled them with reusable linked library assets, and used quick lighting to judge silhouettes and shadows. Its procedural leaf and moss systems helped dressing follow changes to the underlying branches and surfaces. For a new environment, place the major forms manually first. Give secondary dressing a few controls such as density, seed, or a painted mask so an artist can adjust it without rebuilding the graph. [Set Dressing Tips](https://studio.blender.org/blog/sprite-fright-set-dressing-tips/), [Leaves and Moss with Geometry Nodes](https://studio.blender.org/blog/right-end-stick-leaves-moss-geometry-nodes/)

## DOGWALK · Editable levels and engine handoff

The Studio assembled level areas out of linked set layers and used curves to make features such as paths and the creek editable. Geometry Nodes handled some foliage placement. Artists could convert selected procedural dressing to editable objects for local adjustments. The project used custom Blender-to-Godot tooling to preserve set and asset relationships. Use the same separation in a small exercise by making two set layers that reference one prop library, editing one layer, and exporting that layer alone. For a stock GLB handoff, verify what the destination importer actually preserves. [Assembling the World](https://studio.blender.org/blog/dogwalk-assembling-the-world/), [Blender and Godot workflow](https://studio.blender.org/blog/our-workflow-with-blender-and-godot/)

## Wing It! · Stylized shading and outlines

Artists used a face attribute to adjust a shared material's tone on selected faces. Environment outline geometry was generated from the camera view and rendered separately. For a 5.2 study, write a face-domain float with Store Named Attribute and read it with a shader Attribute node. Connect the factor to a mix between two tones. Inspect the evaluated attribute and compare the material from two camera angles before adding any outline pass. The published Dog rig targets Blender 3.6 LTS. Use the breakdown as a reference for the technique and check asset version requirements before opening production files. [Shading and Rendering](https://studio.blender.org/blog/shading-and-rendering-of-wing-it/), [Dog rig compatibility](https://studio.blender.org/characters/dog/v1/)

## Runnable example · Rock scatter

Run [studio_scatter.py](../scripts/studio_scatter.py) in a separate Blender process. It creates a simple clearing, distributes points on the ground, and instances an original low-poly rock. The example verifies that density changes the geometry count and that the seed changes the placement reproducibly. It saves an editable file with realization switched off.

```sh
"/Applications/Blender.app/Contents/MacOS/Blender" \
  --background --factory-startup --python-exit-code 1 \
  --python "/path/to/blender-development/scripts/studio_scatter.py" \
  -- --out "/path/to/new-rock-scatter.blend"
```

Open the result and select **Clearing · Rock Scatter**. Change **Density** and **Seed** under the **Rock Scatter** modifier. Turn on **Realize for Export** on a scratch copy when the destination needs ordinary mesh geometry. For an export test, select the clearing, export GLB with evaluated modifiers, then re-import and inspect the mesh. For individual editable placements in Blender, see Visual Geometry to Objects. [Distribute Points on Faces](https://docs.blender.org/manual/en/5.2/modeling/geometry_nodes/point/distribute_points_on_faces.html), [Instance on Points](https://docs.blender.org/manual/en/5.2/modeling/geometry_nodes/instances/instance_on_points.html), [Visual Geometry to Objects](https://docs.blender.org/manual/en/5.2/scene_layout/object/editing/apply.html#visual-geometry-to-objects)
