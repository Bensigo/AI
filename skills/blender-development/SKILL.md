---
name: blender-development
description: Develop and debug Blender 5.2 LTS Python scripts, bpy scene automation, Geometry Nodes, animation, exporters, and add-on extensions. Use for version-specific API questions, repeatable Blender pipelines, or source-level investigation of Blender behavior.
---

# Blender Development

Target Blender 5.2 LTS. The examples were verified against Blender 5.2.2 (embedded Python 3.13). Confirm the version in the instance that will execute the code.

## Choose the runtime

- **Current scene.** Use Codex's official Blender Lab `blender` MCP with Blender open. Inspect the current file, scene, and relevant objects with the summary tools before changing them. Prefer the dedicated MCP tools when they cover the task. For Python, pass code to `execute_blender_code` and assign a JSON-serializable dictionary to `result`. Check the tool response and verify the resulting scene state. A successful call can still return an inner error.
- **Script, batch job, or regression test.** Run the target Blender binary in background mode against a scratch scene or a copy of the target file. Use `--python-exit-code` before `--python`. Load a supplied blend file before the script when the script expects its data. See [Python runtime and scene data](references/python-runtime.md).
- **Reusable Blender UI or distribution.** Develop an add-on with a reversible registration lifecycle and package it with Blender's extension CLI. See [Extensions and Blender source](references/extensions-and-source.md).
- **Blender itself.** Start with the matching Blender source tag or build hash and use the developer handbook. Read [Extensions and Blender source](references/extensions-and-source.md) for source and test routing.

## Use the 5.2 API

Start with the [Blender 5.2 Python API](https://docs.blender.org/api/5.2/) and [5.2 Python API release notes](https://developer.blender.org/docs/release_notes/5.2/python_api/). The Blender Lab MCP 1.0.3 bundle includes the Blender 5.1 API reference. When signatures or enums matter, confirm them with versioned docs and the installed runtime's RNA.

- Use `bpy.data` for explicit datablock operations. Use `bpy.ops` for operator workflows such as imports, exports, mode changes, and interactive undo. Establish the required context before calling an operator and check its return value.
- When working with Geometry Nodes inputs, animation curves, or asset export, read [Nodes, animation, and export](references/nodes-animation-export.md). Blender 5.2 changed Geometry Nodes modifier properties and several built-in node socket identifiers.
- For production techniques and an executable set-dressing example, read [Blender Studio project studies](references/studio-projects.md).
- Test the smallest observable behavior against the intended runtime. For scene edits, re-read the affected objects or values. For file outputs, verify them on disk and re-open or re-import when their contents matter. Use an isolated Blender process for fixtures, registration tests, and long-running or destructive jobs.
