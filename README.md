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
