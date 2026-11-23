# Extensions and Blender source

## Design the add-on

Use a script for a one-off operation. Use an add-on when the user needs a registered operator, persistent settings, UI, or a distributable extension. Use the existing layout when maintaining an add-on. For a new 5.2 extension, put `__init__.py` and `blender_manifest.toml` at the package root.

- Keep build or scene logic callable without panel drawing code. Use `invoke()` for UI interaction such as selection dialogs and `execute()` for the operation. Enable `UNDO` on operators that make undoable scene edits.
- Use Blender property annotations for registered classes. Register classes and hooks in dependency order. Remove menu callbacks, RNA properties, keymaps, handlers, and timers before unregistering the classes they depend on. Exercise enable, disable, and enable again.
- Use relative imports. An extension's module name includes its repository namespace, so set `AddonPreferences.bl_idname` to the root add-on package identifier (usually root `__package__`). Use `bpy.utils.extension_path_user(root_package, path="", create=True)` for add-on-owned writable data. That directory is removed on uninstall.
- If the extension accesses the internet, respect `bpy.app.online_access` and declare applicable manifest permissions. Bundle dependency wheels targeting the embedded Python ABI and supported platforms. Validate native wheels on a real target runtime.

[Add-on development setup](https://developer.blender.org/docs/handbook/extensions/addon_dev_setup/), [add-on extension rules](https://docs.blender.org/manual/en/5.2/advanced/extensions/addons.html), [add-on tutorial](https://docs.blender.org/manual/en/5.2/advanced/scripting/addon_tutorial.html). The tutorial uses legacy `bl_info`. Use a manifest for new extensions.

## Build and test the package

Set the manifest compatibility floor based on the features used. Use `blender_version_min = "5.2.0"` when 5.2 is the genuine minimum. Include the extension ID, version, name, tagline, maintainer, type, schema version, and SPDX license metadata. Validate with the same executable that will run the extension:

```sh
blender_bin="/Applications/Blender.app/Contents/MacOS/Blender"
"$blender_bin" --command extension validate "/path/to/extension"
"$blender_bin" --command extension build --source-dir "/path/to/extension" --output-dir "/path/to/dist"
"$blender_bin" --command extension validate "/path/to/dist/extension_id-0.1.0.zip"
```

Test registration, teardown, and one functional operation in Blender. For a deliverable plugin, also exercise Install from Disk using the built ZIP in the target application. CLI validation checks packaging and metadata. Validate any viewport-dependent UI in an interactive build. [Create Extensions](https://docs.blender.org/manual/en/5.2/advanced/extensions/getting_started.html), [extension CLI](https://docs.blender.org/manual/en/5.2/advanced/command_line/extension_arguments.html)

## Investigate or modify Blender itself

Start with the installed build's `bpy.app.build_hash` or the corresponding release tag in the official [Blender source repository](https://projects.blender.org/blender/blender). For RNA behavior, find the operator or property definition using Blender's [RNA architecture documentation](https://developer.blender.org/docs/features/core/rna/). Follow the implementation and its poll or update callbacks when the generated API reference does not explain the behavior.

When a core build is in scope, run `make update` from the chosen Blender checkout to synchronize dependencies, then build using the matching platform guide. Keep generated files outside the source tree and avoid iCloud-synced build trees on macOS. Run the relevant tests with `ctest` from the build directory or `make test` from the source tree. A binary from a different build does not verify a source change. [macOS build guide](https://developer.blender.org/docs/handbook/building_blender/mac/), [Blender test setup](https://developer.blender.org/docs/handbook/testing/setup/)
