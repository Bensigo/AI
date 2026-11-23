# Nodes, animation, and export

## Node interfaces and modifier inputs

Use `node_tree.interface.new_socket(..., in_out='INPUT', socket_type=...)` to add a group input. Iterate `node_tree.interface.items_tree` when inspecting a group. Check `item_type` before treating a panel or other item as a socket. Read socket identifiers from the actual tree. For built-in nodes, inspect their inputs and outputs after setting properties that affect their socket layouts. Blender 5.2 changed the identifiers of Compare and Random Value sockets. [Node tree interface](https://docs.blender.org/api/5.2/bpy.types.NodeTreeInterface.html), [5.2 Python API changes](https://developer.blender.org/docs/release_notes/5.2/python_api/)

In Blender 5.2, modifier values are RNA properties. For a known float input socket on the group already assigned to the modifier:

```python
setting = getattr(modifier.properties.inputs, interface_socket.identifier)
if getattr(setting, "type", None) == 'ATTRIBUTE':
    setting.type = 'VALUE'
setting.value = 2.5
modifier.id_data.update_tag()
bpy.context.view_layer.update()
```

Check an observable result on the evaluated object. On 5.2.2, a Python assignment could read back the new value while evaluated geometry stayed cached until the object was tagged for update. For a field-capable socket, an attribute input uses `setting.type = 'ATTRIBUTE'` and `setting.attribute_name`. Output attribute names live under `modifier.properties.outputs` for outputs that support them. Inspect the specific settings before assigning. Older scripts that write `modifier[socket_id]` and keys ending in `_use_attribute` or `_attribute_name` need the 5.2 migration. Read socket identifiers from the assigned group, since a display name can be changed or duplicated. [5.2 modifier migration](https://developer.blender.org/docs/release_notes/5.2/python_api/)

## Actions and F-curves

For ordinary keying, set the property and use `keyframe_insert(data_path=..., frame=..., index=...)` on the owner. For low-level edits, find the action and slot assigned to the target. Read or modify the matching channelbag in the appropriate keyframe strip. Use `bpy_extras.anim_utils.animdata_get_channelbag_for_assigned_slot(anim_data)` when the first matching channelbag is sufficient. When creating a simple action, `action_ensure_channelbag_for_slot(action, slot)` can construct the first layer and keyframe strip. Assign both `anim_data.action` and `anim_data.action_slot` when binding it.

```python
from bpy_extras.anim_utils import action_ensure_channelbag_for_slot

# Create a new action for an object that should receive this animation.
action = bpy.data.actions.new("Vertical travel")
slot = action.slots.new(obj.id_type, obj.name)
channelbag = action_ensure_channelbag_for_slot(action, slot)
curve = channelbag.fcurves.new(data_path="location", index=2)
curve.keyframe_points.insert(1, 0.0)
curve.keyframe_points.insert(10, 3.0)

anim_data = obj.animation_data_create()
anim_data.action = action
anim_data.action_slot = slot
```

Find existing channels and keys when editing an action in place. Check action and slot sharing before changing curves. For rigs, distinguish rest bones, edit bones, and pose bones. Re-resolve edit-bone references after leaving Armature Edit Mode. [Animation quickstart](https://docs.blender.org/api/5.2/info_quickstart.html#animation), [animation helpers](https://docs.blender.org/api/5.2/bpy_extras.anim_utils.html), [armature gotchas](https://docs.blender.org/api/5.2/info_gotchas_armatures_and_bones.html)

## Asset import and export

Confirm the target format, object set, axes, scale, and whether evaluated geometry or editable source data is required. Inspect the operator RNA and relevant format options on the installed build. Selection flags differ by operator:

| Format | Blender 5.2 operator | Selection option |
| --- | --- | --- |
| glTF or GLB | `bpy.ops.export_scene.gltf` | `use_selection` |
| OBJ | `bpy.ops.wm.obj_export` | `export_selected_objects` |
| USD | `bpy.ops.wm.usd_export` | `selected_objects_only` |

For GLB use `export_format='GLB'` and a destination ending in `.glb`. Pass `export_apply=True` to export evaluated mesh modifiers. This excludes armature modifiers from application and prevents shape-key export. For Geometry Nodes instances, realize them in a scratch export copy when you need ordinary mesh geometry. The exporter also offers experimental `export_gn_mesh=True` for Geometry Nodes instances. Include required parents, rigs, and other dependencies in the export scope. When a format cannot represent a feature directly, decide whether to bake it based on the target. Validate a consequential export by re-importing in a separate scene or the consumer and checking the hierarchy, bounds, materials, and animation features the task depends on. [glTF operator](https://docs.blender.org/api/5.2/bpy.ops.export_scene.html), [window-manager operators](https://docs.blender.org/api/5.2/bpy.ops.wm.html), [glTF format guide](https://docs.blender.org/manual/en/5.2/addons/scene_gltf2.html)
