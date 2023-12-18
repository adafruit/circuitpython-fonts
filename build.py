# SPDX-FileCopyrightText: 2023 Jeff Epler for Adafruit Industries
# SPDX-License-Identifier: MIT

from collections import deque
from multiprocessing import Pool
from subprocess import check_call
import textwrap
from pathlib import Path
import tomllib

from convert import convert

with open("config.toml", "rb") as f:
    config = tomllib.load(f)


def build(src, dest, size, variant):
    src = Path("fonts") / src
    font_license = src.with_suffix(src.suffix + ".license")
    uvariant = variant.replace("-", "_")
    destdir = Path(
        f"libraries/circuitpython-font-{dest.replace('_', '-')}-{size}{variant}"
    )
    print(destdir)

    package = f"circuitpython_font_{dest}_{size}{uvariant}"
    packagedir = destdir / package
    packagedir.mkdir(parents=True)
    init_py = packagedir / "__init__.py"
    init_py.write_text(
        textwrap.dedent(
            """\
            # SPDX-FileCopyrightText: 2023 Jeff Epler for Adafruit Industries
            # SPDX-License-Identifier: Unlicense

            from adafruit_bitmap_font import bitmap_font
            FONT = bitmap_font.load_font(__file__.rsplit("/", 1)[0] + "/font.pcf")
            """
        )
    )
    readme_text = destdir / "README.txt"
    readme_text.write_text(
        textwrap.dedent(
            f"""\
            # SPDX-FileCopyrightText: 2023 Jeff Epler for Adafruit Industries
            # SPDX-License-Identifier: Unlicense

            CircuitPython font generated from {src} @{size}{variant}
            """
        )
    )
    convert(src, packagedir / "font.pcf", size, "32_126" if variant else None)

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


if __name__ == "__main__":
    targets = [
        (src, dest, size, variant)
        for dest, src in config["FONTS"].items()
        for size in config["SIZES"]
        for variant in ("", "-ascii")
    ]

    with Pool() as pool:
        # This construct causes all the individual calls to finish, discarding the results
        deque(pool.starmap(build, targets), 0)

    check_call(
        "circuitpython-build-bundles --output_directory dist --filename_prefix circuitpython-font --library_location libraries/ --library_depth 1",
        shell=True,
    )
