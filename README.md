## Fonts for CircuitPython

<!-- SPDX-FileCopyrightText: 2023 Jeff Epler for Adafruit Industries -->
<!-- SPDX-License-Identifier: MIT -->

The goal of this repository is to generate a number of fonts that can be
used in CircuitPython by simply importing them.

It can be used with circup for easy installation:

```
circup bundle-add jepler/circuitpython-fonts
circup install circuitpython_font_mono_9_ascii
```

The font can be used like so:
```
from circuitpython_font_mono_9_ascii import FONT as MONO_9
from adafruit_display_text.bitmap_label import Label

# ...
label = Label(font=MONO_9, text="Hi Mom!")
```

## Adding new fonts

 * Copy the font into `fonts/`
 * Add a reuse-recognized `.license` file for it
 * Add it to the `[FONTS]` section of `config.toml`

Presently all fonts are genreated at the same range of sizes, `SIZES` in `config.toml`.

## Variants

Two variants of each font are generated: The ASCII variant with code points 32-126, and the full variant with all glyphs in the original font. The ASCII variant can be especially useful when flash space is at a premium.
