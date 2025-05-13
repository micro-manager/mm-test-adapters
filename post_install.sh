#!/usr/bin/env sh
if [ -z "$MESON_INSTALL_PREFIX" ]; then
    ADAPTER_DIR="${PWD}/adapters"
else
    ADAPTER_DIR="${DESTDIR}${MESON_INSTALL_PREFIX}/adapters"
fi

# fix library names based on what MMCore PluginManager.cpp is expecting
for lib in "$ADAPTER_DIR"/*; do

    # if it ends with .dylib remove the extension
    if [[ "$lib" == *.dylib ]]; then
        # remove the extension
        lib_name="${lib%.*}"
        mv "$lib" "$lib_name"
    fi

    # if it ends with .so, make sure it ends in `.so.0`
    if [[ "$lib" == *.so ]]; then
        # remove the extension
        lib_name="${lib%.*}"
        mv "$lib" "$lib_name.so.0"
    fi

done
