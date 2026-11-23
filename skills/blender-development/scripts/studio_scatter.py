"""Create an original Geometry Nodes set-dressing study in Blender 5.2 LTS."""

import argparse
from pathlib import Path
import sys

import bpy


def add_node(tree, node_type, label, x, y):
    node = tree.nodes.new(node_type)
    node.label = label
    node.location = x, y
    return node


def add_material(name, color):
    material = bpy.data.materials.new(name)
    material.diffuse_color = color
    shader = material.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = color
    shader.inputs["Roughness"].default_value = 0.85
    return material


def create_scatter():
    floor_mesh = bpy.data.meshes.new("Clearing")
    floor_mesh.from_pydata(
        [(-3, -2, 0), (3, -2, 0), (3, 2, 0), (-3, 2, 0)], [], [(0, 1, 2, 3)]
    )
    floor_mesh.update()
    floor_mesh.materials.append(add_material("Moss green", (0.10, 0.24, 0.16, 1)))
    floor = bpy.data.objects.new("Clearing · Rock Scatter", floor_mesh)
    bpy.context.scene.collection.objects.link(floor)
    bpy.context.view_layer.objects.active = floor
    floor.select_set(True)

    tree = bpy.data.node_groups.new("Rock Scatter", "GeometryNodeTree")
    interface = tree.interface
    interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    density = interface.new_socket(name="Density", in_out="INPUT", socket_type="NodeSocketFloat")
    density.default_value = 1.25
    density.min_value = 0.0
    seed = interface.new_socket(name="Seed", in_out="INPUT", socket_type="NodeSocketInt")
    seed.default_value = 11
    realize = interface.new_socket(
        name="Realize for Export", in_out="INPUT", socket_type="NodeSocketBool"
    )
    realize.description = "Expand the rock instances into geometry for mesh export"

    group_input = add_node(tree, "NodeGroupInput", "Artist controls", -850, 260)
    points = add_node(tree, "GeometryNodeDistributePointsOnFaces", "Place rocks", -610, 260)
    points.distribute_method = "RANDOM"
    ico = add_node(tree, "GeometryNodeMeshIcoSphere", "Rock mesh", -850, -120)
    ico.inputs["Radius"].default_value = 0.24
    ico.inputs["Subdivisions"].default_value = 1
    shape = add_node(tree, "GeometryNodeTransform", "Flatten and lift", -610, -145)
    shape.inputs["Scale"].default_value = (1.0, 0.74, 0.48)
    shape.inputs["Translation"].default_value = (0.0, 0.0, 0.10)
    paint = add_node(tree, "GeometryNodeSetMaterial", "Slate material", -365, -145)
    paint.inputs["Material"].default_value = add_material("Warm slate", (0.30, 0.21, 0.16, 1))
    instances = add_node(tree, "GeometryNodeInstanceOnPoints", "Reuse the same rock", -120, 260)
    baked = add_node(tree, "GeometryNodeRealizeInstances", "Expand only for export", 105, -85)
    switch = add_node(tree, "GeometryNodeSwitch", "Editable or realized", 330, 260)
    switch.input_type = "GEOMETRY"
    join = add_node(tree, "GeometryNodeJoinGeometry", "Ground and rocks", 550, 260)
    group_output = add_node(tree, "NodeGroupOutput", "Clearing geometry", 775, 260)

    link = tree.links.new
    link(group_input.outputs["Geometry"], points.inputs["Mesh"])
    link(group_input.outputs["Density"], points.inputs["Density"])
    link(group_input.outputs["Seed"], points.inputs["Seed"])
    link(ico.outputs["Mesh"], shape.inputs["Geometry"])
    link(shape.outputs["Geometry"], paint.inputs["Geometry"])
    link(points.outputs["Points"], instances.inputs["Points"])
    link(points.outputs["Rotation"], instances.inputs["Rotation"])
    link(paint.outputs["Geometry"], instances.inputs["Instance"])
    link(instances.outputs["Instances"], baked.inputs["Geometry"])
    link(instances.outputs["Instances"], switch.inputs["False"])
    link(baked.outputs["Geometry"], switch.inputs["True"])
    link(group_input.outputs["Realize for Export"], switch.inputs["Switch"])
    link(group_input.outputs["Geometry"], join.inputs["Geometry"])
    link(switch.outputs["Output"], join.inputs["Geometry"])
    link(join.outputs["Geometry"], group_output.inputs["Geometry"])

    modifier = floor.modifiers.new("Rock Scatter", "NODES")
    modifier.node_group = tree
    inputs = modifier.properties.inputs
    return floor, getattr(inputs, density.identifier), getattr(inputs, seed.identifier), getattr(
        inputs, realize.identifier
    )


def mesh_positions(obj):
    obj.update_tag()
    bpy.context.view_layer.update()
    evaluated = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh = evaluated.to_mesh()
    try:
        return sorted(tuple(round(coord, 5) for coord in vert.co) for vert in mesh.vertices)
    finally:
        evaluated.to_mesh_clear()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path, help="Path for a new .blend file")
    arguments = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    output = parser.parse_args(arguments).out.expanduser().resolve()
    if not bpy.app.background:
        parser.error("Run in a separate Blender process with --background")
    if bpy.app.version[:2] < (5, 2):
        parser.error("This example needs the Blender 5.2 Geometry Nodes modifier API")
    if output.suffix != ".blend" or output.exists():
        parser.error("Choose a new .blend output path")

    bpy.ops.wm.read_factory_settings(use_empty=True)
    floor, density, seed, realize = create_scatter()
    realize.value = True
    baseline = mesh_positions(floor)
    assert len(baseline) > 4, "Expected realized rocks in addition to the ground"
    density.value *= 2
    assert len(mesh_positions(floor)) > len(baseline), "Density should add rocks"
    density.value /= 2
    seed.value += 1
    assert mesh_positions(floor) != baseline, "Seed should change the layout"
    seed.value -= 1
    assert mesh_positions(floor) == baseline, "Restoring controls should restore the layout"
    realize.value = False
    floor.update_tag()
    bpy.context.view_layer.update()

    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == "VIEW_3D":
                area.spaces.active.shading.color_type = "MATERIAL"
    output.parent.mkdir(parents=True, exist_ok=True)
    assert bpy.ops.wm.save_as_mainfile(filepath=str(output)) == {"FINISHED"}
    print(f"Verified editable scatter scene: {output}")


if __name__ == "__main__":
    main()
