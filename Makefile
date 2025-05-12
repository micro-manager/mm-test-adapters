# filepath: Makefile
.PHONY: all update copy setup compile clean

all: cp-builds setup compile install

cp-builds:
	cp -r meson_build_files/* src/
	
setup:
	meson setup builddir --buildtype=release

compile:
	meson compile -C builddir

install:
	meson install --tags runtime -C builddir
	@if [ "$(OS)" != "Windows_NT" ]; then ./post_install.sh; fi

submodule:
	git submodule update --init --recursive
	$(MAKE) cp-builds

submodule-update:
	git submodule foreach --recursive 'git reset --hard && git clean -fdx'
	git submodule update --init --recursive --remote --force --checkout
	$(MAKE) cp-builds

clean:
	rm -rf builddir
	rm -rf adapters
