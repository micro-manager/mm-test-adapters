import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Sequence

DEFAULT_DEVICES = ("DemoCamera", "Utilities", "NotificationTester", "SequenceTester")
DEFAULT_REPO = "https://github.com/micro-manager/mmCoreAndDevices"
DEFAULT_LIBDIR = "src/mm_test_adapters/libs"
DEFAULT_DEST = "src/mmCoreAndDevices"
DIV_RE = re.compile(r"#define DEVICE_INTERFACE_VERSION (\d+)")


def get_version(dest: str = DEFAULT_DEST) -> str:
    if not (Path(dest) / "MMDevice" / "MMDevice.h").exists():
        raise FileNotFoundError(
            f"Sources not found in {dest}. "
            "Please ensure the repository is cloned correctly."
        )
    match = DIV_RE.search((Path(dest) / "MMDevice" / "MMDevice.h").read_text())
    assert match, "Could not find DEVICE_INTERFACE_VERSION in MMDevice.h"
    real_sha = subprocess.check_output(["git", "-C", dest, "rev-parse", "HEAD"])
    short_sha = real_sha.decode("utf-8").strip()[:7]
    date = (
        subprocess.check_output(
            ["git", "-C", dest, "log", "-1", "--format=%cd", "--date=format:'%Y%m%d'"]
        )
        .decode("utf-8")
        .strip()
        .replace("'", "")
    )
    return f"{match.group(1)}.{date}.dev+g{short_sha}"


def fix_library_names(lib_dir: str | Path) -> None:
    """Fix names of *nix libraries in the specified directory.

    - For each file in the adapters directory:
      - If it ends with .dylib, rename to remove the extension
      - If it ends with .so, rename to end with .so.0
    """
    if not (adapters := Path(lib_dir)).exists():
        raise ValueError(f"Adapters directory does not exist: {adapters}")

    for entry in adapters.iterdir():
        if entry.is_file():
            name = entry.name
            if name.endswith(".dylib"):
                entry.rename(entry.with_suffix(""))
            elif name.endswith(".so"):
                entry.rename(entry.with_suffix(".so.0"))


def fetch_sources(
    repo: str = DEFAULT_REPO,
    sha: str = "main",
    devices: Sequence[str] = DEFAULT_DEVICES,
    dest: str = DEFAULT_DEST,
) -> str:
    if not os.path.exists(dest):
        subprocess.check_call(
            ["git", "clone", "--filter=blob:none", "--sparse", repo, dest]
        )
    try:
        subprocess.check_call(["git", "-C", dest, "checkout", sha])
    except subprocess.CalledProcessError:
        print(f"Failed to checkout SHA {sha!r}")
    subprocess.check_call(["git", "-C", dest, "sparse-checkout", "init", "--no-cone"])
    subprocess.check_call(
        ["git", "-C", dest, "sparse-checkout", "set", "/MMDevice/MMDevice.h"]
        + [f"DeviceAdapters/{device}" for device in devices]
    )
    return get_version(dest)


def build_libs(libdir: str = DEFAULT_LIBDIR):
    subprocess.check_call(
        [
            "meson",
            "setup",
            "builddir",
            "--buildtype=release",
            "-Dmmdevice:tests=disabled",
            f"--libdir={libdir}",
        ]
    )
    subprocess.run(["meson", "compile", "-C", "builddir"])
    subprocess.run(["meson", "install", "--tags", "runtime", "-C", "builddir"])
    fix_library_names(libdir)


def main(
    repo: str = DEFAULT_REPO,
    sha: str = "main",
    devices: Sequence[str] = DEFAULT_DEVICES,
    dest: str = DEFAULT_DEST,
    build: bool = False,
    clean: bool = False,
    libdir: str = DEFAULT_LIBDIR,
):
    fetch_sources(repo, sha, devices, dest)
    version = get_version(dest)
    if build:
        build_libs(libdir)

    if clean:
        shutil.rmtree("builddir", ignore_errors=True)
        shutil.rmtree("include", ignore_errors=True)
        shutil.rmtree(dest, ignore_errors=True)

    return version


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--sha", default="main")
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument("--libdir", default=DEFAULT_LIBDIR, help="Library directory")
    parser.add_argument("--build", action="store_true", help="Build the repository")
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()

    version = main(
        repo=args.repo,
        sha=args.sha,
        build=args.build,
        clean=args.clean,
        libdir=args.libdir,
    )

    print(f">> VERSION: {version}")
