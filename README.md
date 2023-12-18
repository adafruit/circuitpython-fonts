## Fonts for CircuitPython

<!-- SPDX-FileCopyrightText: 2023 Jeff Epler for Adafruit Industries -->
<!-- SPDX-License-Identifier: MIT -->

The goal of this repository is to generate a number of fonts that can be
used in CircuitPython by simply importing them.

It can be used with circup for easy installation:

```sh
circup bundle-add jepler/circuitpython-fonts # You only need to do this once
circup install font_free_mono_9_ascii
```

The font can be used like so:
```python
from font_free_mono_9_ascii import FONT as MONO_9
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
