#!/usr/bin/env sh
if [ -z "$MESON_INSTALL_PREFIX" ]; then
    ADAPTER_DIR="${PWD}/adapters"
else
    ADAPTER_DIR="${DESTDIR}${MESON_INSTALL_PREFIX}/adapters"
fi

# remove the .dylib or .so extension from all files in the adapters directory
# this is how the micro-manager plugin loader expects the files to be named
# for every file in the adapters directory
for lib in "$ADAPTER_DIR"/*; do
    # if it ends with .dylib or .so, remove the extension
    if [[ "$lib" == *.dylib || "$lib" == *.so ]]; then
        # remove the extension
        lib_name="${lib%.*}"
        mv "$lib" "$lib_name"
    fi
done
