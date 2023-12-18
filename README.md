## Fonts for CircuitPython

<!-- SPDX-FileCopyrightText: 2023 Jeff Epler for Adafruit Industries -->
<!-- SPDX-License-Identifier: MIT -->

The goal of this repository is to generate a number of fonts that can be
used in CircuitPython by simply importing them.

It can be used with circup for easy installation:

```
circup bundle-add jepler/circuitpython-fonts
circup install font_mono_9_ascii
```

The font can be used like so:
```
from font_mono_9_ascii import FONT as MONO_9
from adafruit_display_text.bitmap_label import Label

# ...
label = Label(font=MONO_9, text="Hi Mom!")
```

## Adding new fonts

 * Copy the font into `fonts/`
 * Add a reuse-recognized `.license` file for it
 * Add it to the `[FONTS]` section of `config.toml`

Presently all fonts are generated at the same range of sizes, `SIZES` in `config.toml`. This restriction could be lifted if it's for a good reason.

## Variants

Two variants of each font are generated: The ASCII variant with code points 32-126, and the full variant with all glyphs in the original font. The ASCII variant can be especially useful when flash space is at a premium.

More variants could be added for a good reason; it should be configurable in config.toml and possibly be settable per font.

## Font Sizing

The font sizes in this bundle are in pixels.
Or, to be more technically accurte, they are rendered at a resolution of 1 pixel = 1/72 inch = 1 point.
If you follow the [directions on learn](https://learn.adafruit.com/custom-fonts-for-pyportal-circuitpython-display/use-otf2bdf) your font is rendered at a scale of 1 pixel = 1/100 inch = 0.72 points.
This means the resulting font pixel sizes are 33-40% larger for the Learn guide instructions vs the fonts in this bundle.
In any case, you will likely need to manually test font sizes until you find the best one for your application and display.
