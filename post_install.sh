#!/usr/bin/env sh
# post_install.sh
# Meson sets DESTDIR and MESON_INSTALL_PREFIX for you.
# MESON_SOURCE_ROOT points at your source tree.

# this is empty unless you used DESTDIR, e.g. `DESTDIR=/foo ninja install`
echo "DESTDIR   = '$DESTDIR'"
echo "PREFIX    = '$MESON_INSTALL_PREFIX'"
ADAPTER_DIR="${DESTDIR}${MESON_INSTALL_PREFIX}/adapters"

# for every file in the adapters directory
for lib in "$ADAPTER_DIR"/*; do
    # if it ends with .dylib or .so, remove the extension
    if [[ "$lib" == *.dylib || "$lib" == *.so ]]; then
        # remove the extension
        lib_name="${lib%.*}"
        mv "$lib" "$lib_name"
    fi
done
