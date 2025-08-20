# filepath: Makefile
.PHONY: all build clean

# use second to build and install the project
all: build

build:
	uv run fetch.py --build --clean --libdir adapters

clean:
	rm -rf builddir adapters src/mmCoreAndDevices
	rm -rf dist build builddir *.egg-info src/*.egg-info
	rm -f src/mm_test_adapters/_version.py uv.lock
	rm -rf src/mm_test_adapters/libs
