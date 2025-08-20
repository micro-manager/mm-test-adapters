import os
import sys
from pathlib import Path
from typing import Any

from setuptools import setup
from setuptools.command.bdist_wheel import bdist_wheel
from setuptools.command.sdist import sdist
from setuptools.dist import Distribution

sys.path.append(".")
import fetch

VERSION_FILE = Path("src/mm_test_adapters/_version.py")


def write_version() -> str:
    version = fetch.fetch_sources()
    VERSION_FILE.write_text(f'__version__ = "{version}"\n')
    return version


def get_version():
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text().strip().split(" = ")[1].strip('"')
    else:
        try:
            return write_version()
        except Exception:
            return "0.0.0"


class CustomSdist(sdist):
    def run(self):
        write_version()
        super().run()


class CustomBdistWheel(bdist_wheel):
    def write_wheelfile(self, wheelfile_base: str, **kwargs: Any) -> None:
        lib_dir = os.path.join(str(self.bdist_dir), "mm_test_adapters", "libs")
        fetch.build_libs(lib_dir)
        super().write_wheelfile(wheelfile_base, **kwargs)


class BinaryDistribution(Distribution):
    def has_ext_modules(self) -> bool:
        return True  # Forces a platform-specific wheel


setup(
    version=get_version(),
    cmdclass={"sdist": CustomSdist, "bdist_wheel": CustomBdistWheel},
    package_data={"*": ["*"]},
    package_dir={"": "src"},
    packages=["mm_test_adapters"],
    distclass=BinaryDistribution,
)
