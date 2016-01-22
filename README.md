Mathematical Open Type fonts
============================

License
-------

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, you can obtain one at
[http://mozilla.org/MPL/2.0/](http://mozilla.org/MPL/2.0/).

Description
-----------

This repository contains a script to fetch various open source OpenType fonts
with a MATH table as well as the corresponding fonts to use for the surrounding
text (if any). The fonts are converted into WOFF and WOFF2 formats
using [sfnt2woff](https://people.mozilla.org/~jkew/woff/woff-code-latest.zip)
and [woff2_compress](https://github.com/google/woff2). They are
[packaged](https://github.com/fred-wang/MathFonts/archive/gh-pages.zip) with
some documentation, a license and a `mathfont.css` stylesheet, so that you can
easily use them on your Web site. Some proprietary fonts as well as incomplete
open source fonts are also listed but they are not provided.

Warning
-------

Note that only Gecko and WebKit have (more or less complete) support for MathML
and the OpenType MATH table. The WOFF2 format is not supported by all web
rendering engines. It is recommended to try the most recent versions.

The following open source math fonts have issues and are not provided yet:
- The DejaVu fonts have a MATH table, but the support is very limited.
- The Neo Euler font has design issues and has never been released.
- The development version of GNU Free fonts contains an OpenType MATH table
  but this is not available in the release yet.
- The STIX font is known to have many bugs that have been reported to the
  STIX consortium.
  [STIX 2.0.0 was announced for early 2015](http://www.stixfonts.org/)
  but it is not released (as of January 2016). In the meantime you might
  want to use the XITS fork instead.

Also some (but not all) of the fonts provide old style numbers and calligraphic
letters accessible via OpenType font features. Some CSS rules from the
[CSS Fonts Module Level](http://dev.w3.org/csswg/css-fonts/)
are provided to help selecting the corresponding glyphs, but these are not
implemented/enabled in all browsers yet.

Using Math fonts on your Web site
---------------------------------

Download the
[zip archive](https://github.com/fred-wang/MathFonts/archive/gh-pages.zip).
Choose one family for your web site and place the corresponding subdirectory
somewhere.
Make your pages link to the `mathfonts.css` stylesheet. The MathML formulas
will then render with the specified font. It's good to make them consistent
with the surrounding text, especially for inline expressions. To do that,
use the `htmlmathparagraph` class, e.g. `<body class="htmlmathparagraph">`.
By default, the local fonts installed on the system will be used. For open
source fonts, Web fonts in WOFF2 or WOFF format will be used as a fallback.

Most families provide old style numbers in the text font. You can use them via
the `oldstylenumbers` class, e.g.
`<span class="oldstylenumbers">0123456789</span>`. Some of the math fonts also
provide calligraphic style for the script characters, that you can select
with the `calligraphic` class e.g.
`<math><mi mathvariant="script" class="calligraphic">A</mi></math>` or
equivalently `<math><mi class="calligraphic">𝒜</mi></math>`.

Build Instructions
------------------

You need [GNU Core Utilities](https://en.wikipedia.org/wiki/GNU_Core_Utilities)
(or equivalent on UNIX systems) as well as `sed`, `grep`, `unzip`, `wget`,
[sfnt2woff](https://people.mozilla.org/~jkew/woff/woff-code-latest.zip) and
[woff2_compress](https://github.com/google/woff2). Type the following command
to build the font directories:

    ./configure
    make

Use `make clean` to remove intermediary files and `make distclean` to remove
all the files that are not tracked on GitHub.
