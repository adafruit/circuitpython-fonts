#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023 Jeff Epler for Adafruit Industries
# SPDX-License-Identifier: MIT

import glob
import os
import re
import shutil
import textwrap
import tomllib
from collections import deque
from multiprocessing import Pool
from pathlib import Path
from subprocess import check_call, check_output

from convert import convert

version = check_output(
    ["git", "describe", "--tags", "--always"],
    cwd=Path(__file__).parent,
    encoding="utf-8",
).strip()
print(f"{version=}")

with open("config.toml", "rb") as f:
    config = tomllib.load(f)


def build(src, dest, size, variant_name, variant_arg):
    src = Path("fonts") / src
    font_license = src.with_suffix(src.suffix + ".license")
    destdir = Path(
        f"libraries/font-{dest.replace('_', '-')}-{size}-{variant_name}".strip("-")
    )
    print(destdir)

    package = f"font_{dest}_{size}_{variant_name}".replace("-", "_").strip("_")
    packagedir = destdir / package
    packagedir.mkdir(parents=True)
    init_py = packagedir / "__init__.py"
    init_py.write_text(
        textwrap.dedent(
            f"""\
            # SPDX-FileCopyrightText: 2023 Jeff Epler for Adafruit Industries
            # SPDX-License-Identifier: Unlicense

            # CircuitPython font generated from {src} @{size}{" " if variant_name else ""}{variant_name}
            from adafruit_bitmap_font import bitmap_font
            __version__ = "{version}"
            FONT = bitmap_font.load_font(__file__.rsplit("/", 1)[0] + "/font.pcf")
            """
        )
    )
    requirements_text = destdir / "requirements.txt"
    requirements_text.write_text(
        textwrap.dedent(
            f"""\
            # SPDX-FileCopyrightText: 2023 Jeff Epler for Adafruit Industries
            # SPDX-License-Identifier: Unlicense

            adafruit-circuitpython-bitmap-font
            """
        )
    )
    readme_text = destdir / "README.txt"
    readme_text.write_text(
        textwrap.dedent(
            f"""\
            # SPDX-FileCopyrightText: 2023 Jeff Epler for Adafruit Industries
            # SPDX-License-Identifier: Unlicense

            CircuitPython font generated from {src} @{size}{" " if variant_name else ""}{variant_name}
            corresponding to circuitpython-fonts version {version}
            """
        )
    )
    convert(src, packagedir / "font.pcf", size, variant_arg)

    dest_font_license = packagedir / "font.pcf.license"
    dest_font_license.write_text(font_license.read_text())

    pyproject_toml = destdir / "pyproject.toml"
    pyproject_toml.write_text(
        textwrap.dedent(
            f"""\
            # SPDX-FileCopyrightText: 2023 Jeff Epler for Adafruit Industries
            # SPDX-License-Identifier: Unlicense
            [tool.setuptools]
            packages = ["{package}"]
            """
        )
    )

    exampledir = destdir / "examples"
    exampledir.mkdir()

    example_py = destdir / f"examples/{package}_example.py"
    example_py.write_text(
        textwrap.dedent(
            f"""\
            # SPDX-FileCopyrightText: 2023 Jeff Epler for Adafruit Industries
            # SPDX-License-Identifier: Unlicense

            from {package} import FONT
            print(FONT.get_bounding_box())
            """
        )
    )


def filename_to_package_name(filename):
    s = re.sub("[A-Z]+", lambda m: "_" + m.group(0).lower(), filename)
    s = re.sub("[^a-z0-9]+", "_", s)
    s = s.removeprefix("_")
    return s


def targets():
    defaults = config["defaults"]
    variants = config["variants"]
    font_files = [
        f for f in os.listdir("fonts") if f.lower().endswith((".ttf", ".otf"))
    ]
    for filename in font_files:
        basename = filename.rsplit(".", 1)[0]
        font_config = dict(defaults)
        font_config.update(config.get("font", {}).get(basename, {}))
        dest = filename_to_package_name(font_config.get("name", basename))
        print(config, dest, basename)
        for size in sorted(font_config["sizes"], reverse=True):
            yield (filename, dest, size, "", None)
            for variant_name, variant_arg in variants.items():
                yield (filename, dest, size, variant_name, variant_arg)


if __name__ == "__main__":
    if os.access("libraries", os.F_OK):
        shutil.rmtree("libraries")

    with Pool() as pool:
        # This construct causes all the individual calls to finish, discarding the results
        count = sum(1 for _ in pool.starmap(build, targets()))

    if not "BUILD_ONLY" in os.environ:
        check_call(
            [
                "circuitpython-build-bundles",
                "--output_directory",
                "dist",
                "--filename_prefix",
                "circuitpython-fonts",
                "--library_location",
                "libraries/",
                "--library_depth",
                "1",
            ]
        )

    print(f"Generated {count} font libraries")
