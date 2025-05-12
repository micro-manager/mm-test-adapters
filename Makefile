# filepath: Makefile
.PHONY: all update copy setup compile clean

# use second to build and install the project

all: cp-builds setup compile install

# use first to update submodules and overwrite the meson_build_files

submodule:
	git submodule update --init --recursive --remote --merge --force
	$(MAKE) cp-builds

cp-builds:
	@if [ "$(OS)" = "Windows_NT" ]; then \
		powershell -Command "Copy-Item -Path meson_build_files/* -Destination src/ -Recurse -Force"; \
	else \
		cp -r meson_build_files/* src/ ; \
	fi

setup:
	meson setup builddir --buildtype=release

compile:
	meson compile -C builddir

install:
	meson install --tags runtime -C builddir
	@if [ "$(OS)" != "Windows_NT" ]; then ./post_install.sh; fi

clean:
	rm -rf builddir
	rm -rf adapters
