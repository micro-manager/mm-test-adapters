# mm-test-adapters

This builds device adapters commonly used for testing and
development of mmCoreAndDevices (micro-manager).

- DemoCamera
- Utilities
- SequenceTester
- NotificationTester

```sh
# update submodules, and apply meson-build patches
make submodule

# build
uv run make
```

on windows:

```powershell
# update submodules, and apply meson-build patches
git submodule update --init --recursive
Copy-Item -Path meson_build_files/* -Destination src/ -Recurse -Force

# get boost
# (there is a wrap here, but it doesn't always work... system install is better)
choco install boost-msvc-14.3

# build
uv run meson setup builddir
uv run meson compile -C builddir
uv run meson install --tags runtime -C builddir
```