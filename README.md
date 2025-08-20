# mm-test-adapters

This builds device adapters commonly used for testing and
development of mmCoreAndDevices (micro-manager).

- DemoCamera
- Utilities
- SequenceTester
- NotificationTester

## Build

```sh
# update submodules, and apply meson-build patches
uv run make submodule

# build
uv run make
```

> note, the makefile also works on Windows if you have git for windows.

## Usage on CI

To use these on CI see <https://github.com/pymmcore-plus/setup-mm-test-adapters>

```yaml
- name: Install MM test adapters
  uses: pymmcore-plus/setup-mm-test-adapters@main
  with:
    # all inputs are optional
    version: latest  # or a specific YYYYMMDD version
    destination: ./mm-test-adapters
```

## Usage locally

[Download the release](https://github.com/pymmcore-plus/mm-test-adapters/releases/) you would like to use,
then place it wherever Micro-Manager is looking for device adapters.  To have them found by pymmcore-plus,
place them in the default [pymmcore-plus](https://github.com/pymmcore-plus/pymmcore-plus) install location,
named `Micro-Manager-YYYYMMDD`

- **Windows**: `$LOCALAPPDATA/pymmcore-plus/pymmcore-plus/mm/Micro-Manager-YYYYMMDD`
- **macOS**: `$HOME/Library/Application Support/pymmcore-plus/mm/Micro-Manager-YYYYMMDD`
- **Linux**: `$HOME/.local/share/pymmcore-plus/mm/Micro-Manager-YYYYMMDD`

> [!TIP]
> On macOS, you will need to give permissions to allow the shared libraries to run:
>
> ```sh
> xattr -r -d com.apple.quarantine ~/Library/Application\ Support/pymmcore-plus/mm/Micro-Manager-*
> ```
>
