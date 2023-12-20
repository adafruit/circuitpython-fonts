## Fonts for CircuitPython

<!-- SPDX-FileCopyrightText: 2023 Jeff Epler for Adafruit Industries -->
<!-- SPDX-License-Identifier: MIT -->

The repository generates a large number of bitmap fonts that can be
used in CircuitPython by simply importing them.

It can be used with [circup](https://pypi.org/project/circup/) for easy installation.

Once you have installed circup and connected to a board, simply install the desired font(s):

```sh
circup bundle-add jepler/circuitpython-fonts # You only need to do this once
circup install font_free_mono_9
```

The font can be used like so:
```python
from font_free_mono_9 import FONT as MONO_9
from adafruit_display_text.bitmap_label import Label

# ...
label = Label(font=MONO_9, text="Hi Mom!")
```

## Adding new fonts

 * Copy the font into `fonts/`
 * Add a reuse-recognized `.license` file for it

## Variants

Two variants of each font are generated: The "latin1" variant with code points 32-255 inclusive, and the full variant with all glyphs in the original font. The "latin1" variant can be especially useful when flash space is at a premium.

More variants could be added for a good reason; it is configurable in config.toml. It is not currently settable per font but if for a good reason it could be.

## Font Sizing

The font sizes in this bundle are in pixels.
Or, to be more technically accurte, they are rendered at a resolution of 1 pixel = 1/72 inch = 1 point.
If you follow the [directions on learn](https://learn.adafruit.com/custom-fonts-for-pyportal-circuitpython-display/use-otf2bdf) your font is rendered at a scale of 1 pixel = 1/100 inch = 0.72 points.
This means the resulting font pixel sizes for these libraries are around 38% smaller than if you follow the Learn guide instructions.
In any case, you will likely need to manually test font sizes until you find the best one for your application and display.

## Building locally

The build process requires these programs (instructions to install on Debian and Ubuntu Linux in parentheses):
 * otf2bdf (sudo apt install otf2bdf)
 * bdftopcf (sudo apt install xfonts-utils)
 * circuitpython-build-bundles (sudo apt install pipx; pipx install circuitpython-build-tools)

Once the dependencies are installed, simply invoke `build.py` and after a few minutes you will get a fresh font bundle in `dist/`.
