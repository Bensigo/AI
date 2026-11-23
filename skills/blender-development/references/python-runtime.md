# Python runtime and scene data

## Live Blender and background runs

For a live scene, use Blender Lab's official MCP with its add-on enabled and Blender running. Use `codex mcp get blender` to inspect registration if tool discovery fails. The official bridge uses its own protocol. Use its Codex tools for live work. [Blender Lab MCP](https://www.blender.org/lab/mcp-server/)

Check the runtime without editing the scene:

```python
import sys
import bpy

result = {
    "blender": bpy.app.version_string,
    "python": sys.version.split()[0],
    "background": bpy.app.background,
    "scene": bpy.context.scene.name,
}
```

Use the same Python code inside a script and print or assert the relevant result for command-line tests. Use the configured Blender 5.2 executable. The standard macOS application path is shown here:

```sh
"/Applications/Blender.app/Contents/MacOS/Blender" \
  --background --factory-startup --python-exit-code 1 --python "/path/to/check.py"
```

To test a file, add its absolute path before `--python`. Use a scratch copy for scripts that save or mutate fixtures. Keep UI-dependent work in the Blender window. If a background process fails before Python starts, look at the native startup log or crash report. [5.2 command-line arguments](https://docs.blender.org/manual/en/5.2/advanced/command_line/arguments.html)

## Context and operators

- Identify the scene, view layer, target datablock, and mode. Selection and the active object are separate. Set `bpy.context.view_layer.objects.active = obj` and `obj.select_set(True)` when the operation needs both. Restore user state when a script changes it as a side effect.
- Inspect an operator's actual arguments with `op.get_rna_type().properties`. Use `op.poll()` in the context in which it will run. Check the returned status set, treating `CANCELLED` as a failed operation and `RUNNING_MODAL` as pending.
- Use `with bpy.context.temp_override(...)` where required. A `region` must belong to the chosen `area`, and the area must be in the chosen window. Some operators query state outside the override. If a poll depends on a genuine window, switch to an interactive runtime or use the data API instead. [Context](https://docs.blender.org/api/5.2/bpy.types.Context.html), [operator gotchas](https://docs.blender.org/api/5.2/info_gotchas_operators.html)

## Original data, Edit Mode, and evaluated data

- New objects from `bpy.data.objects.new()` become part of a scene when linked to a collection in it. Check `obj.data.users` before making mesh or material edits intended for one object. Copy shared datablocks when the requested edit should affect only the target. Keep the returned reference after creating or renaming a datablock because names can be suffixed.
- In mesh Edit Mode, access the live mesh with `bmesh.from_edit_mesh(mesh)` and write changes with `bmesh.update_edit_mesh(mesh, destructive=topology_changed)`. Blender owns that BMesh. For an independently allocated `bmesh.new()`, write back with `bm.to_mesh(mesh)` when needed and call `bm.free()` when done. [BMesh](https://docs.blender.org/api/5.2/bmesh.html)
- For geometry after modifiers, obtain the current graph via `bpy.context.evaluated_depsgraph_get()` and use `obj.evaluated_get(depsgraph)`. Pair `evaluated_obj.to_mesh()` with `evaluated_obj.to_mesh_clear()` in a `finally` block. Read values before the graph is updated again. For a persistent mesh datablock, use `bpy.data.meshes.new_from_object(evaluated_obj)` with an explicit consumer. [Depsgraph examples](https://docs.blender.org/api/5.2/bpy.types.Depsgraph.html)
- Re-resolve RNA references after operations that can remove or replace their backing data, such as Undo or loading a new file. Copy values like matrices if they must survive reevaluation. When sampling animation use `scene.frame_set(frame)` to evaluate that frame. [RNA lifetime and deferred evaluation](https://docs.blender.org/api/5.2/info_gotchas_internal_data_and_python_objects.html)

## Long-running scripts and callbacks

Keep `bpy` operations on Blender's main thread. Use bounded timer callbacks or modal operators for interactive work that needs progress. A timer returning `None` stops, and a float schedules the next callback. Pass only plain data across process boundaries. Remove registered timers and handlers when an add-on is disabled. Handlers that mutate data during rendering need particular care because rendering and viewport updates can access the same data concurrently. [Threading gotchas](https://docs.blender.org/api/5.2/info_gotchas_threading.html), [timers](https://docs.blender.org/api/5.2/bpy.app.timers.html), [handlers](https://docs.blender.org/api/5.2/bpy.app.handlers.html)

For Blender 5.2 background jobs that use the `gpu` API, check whether `gpu.init()` is needed and verify the actual machine's backend. Ordinary scene scripting doesn't require calling it. [5.2 Python API changes](https://developer.blender.org/docs/release_notes/5.2/python_api/)
