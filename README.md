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
text (if any). The fonts are converted into WOFF format
using [sfnt2woff](https://people.mozilla.org/~jkew/woff/woff-code-latest.zip)
and are
[packaged](https://github.com/fred-wang/MathFonts/archive/gh-pages.zip) with
some documentation, a license and a `mathfont.css` stylesheet, so that you can
easily use them on your Web site. For completeness, some proprietary math fonts
are also listed but for obvious legal reasons they can not be provided
here. This [test page](http://fred-wang.github.io/MathFonts/) allows checking
the rendering of the various fonts in your browser.

Warning
-------

**It is important to note that the development and implementation of OpenType
MATH is still a work in progress**. The specification is available in the
[Open Font Format draft](http://mpeg.chiariglione.org/standards/mpeg-4/open-font-format/text-isoiec-cd-14496-22-3rd-edition) and 
there are known bugs in browsers and fonts. In particular note that:

- Gecko 31 has [support for the OpenType MATH table](https://wiki.mozilla.org/MathML:Open_Type_MATH_Table) but it is not complete yet.
- The OpenType MATH table is only used in WebKit Nightly to draw stretchy and
  large operators as well as radicals.
- The commercial Minion and LucidaBright fonts have not been tested at all in
  browsers.
- The Neo Euler font is incomplete and it has been pending an overhaul for a
  while.
- Latin Modern and TeX Gyre fonts have issues with ascent/descent in some
  browsers/operating systems, although some workarounds have been added in
  Gecko 31. The GUST group is currently working on fixing these issues.
- The STIX font is known to have many bugs that have been reported to the
  STIX consortium. [STIX 2.0.0 has been announced for early 2015](http://www.stixfonts.org/) but in the meantime you might want to use the XITS fork instead.

Using Math fonts on your Web site
---------------------------------

Clone the gh-pages branch with `git` or download the
[zip archive](https://github.com/fred-wang/MathFonts/archive/gh-pages.zip). Choose
one family for your web site and place the corresponding subdirectory somewhere.
Make your pages link to the `mathfonts.css` stylesheet. The MathML formulas
will then render with the specified font. It's good to make them consistent
with the surrounding text, especially for inline expressions. To do that,
use the `htmlmathparagraph` class, e.g. `<body class="htmlmathparagraph">`.
By default, the local fonts installed on the system will be used and otherwise
WOFF Web fonts will be used as a fallback (for open source fonts only).

Build Instructions
------------------

You need [GNU Core Utilities](https://en.wikipedia.org/wiki/GNU_Core_Utilities)
(or equivalent on UNIX systems) as well as `sed`, `grep`, `unzip`, `wget` and
[sfnt2woff](https://people.mozilla.org/~jkew/woff/woff-code-latest.zip). Type
the following command to build the font directories:

    ./configure
    make

Use `make clean` to remove intermediary files and `make distclean` to remove
all the files that are not tracked on GitHub.
