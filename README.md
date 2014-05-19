Mathematical Open Type fonts
============================

License
-------

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at
[http://mozilla.org/MPL/2.0/](http://mozilla.org/MPL/2.0/).

Description
-----------

This repository contains some open source OpenType fonts with a MATH table and
their associated text fonts (if any). They are available in WOFF format
together with the documentation and licensed. A sample `mathfont.css` stylesheet
is provided so that you can use these fonts on your Web site. For completeness,
some proprietary math fonts are also listed here.

This [test page](http://fred-wang.github.io/MathFonts/) allows to check the
rendering of the various fonts in your browser. Currently, the fonts are only
partially supported in Gecko 31 or higher. Work is still in progress for WebKit
browsers.

Using Math fonts on your Web site
---------------------------------

Clone this repository with `git` or download the
[zip archive](https://github.com/fred-wang/MathFonts/archive/master.zip). Choose
one family for your web site and place the corresponding subdirectory somewhere.
Make your pages link to the `mathfonts.css` stylesheet. The MathML formulas
will then render with the specified font. It's good to make them consistent
with the surrounding text, especially for inline expressions. To do that,
use the `htmlmathparagraph` class, e.g. `<body class="htmlmathparagraph">`.

By default, the local fonts installed on the system will be used and otherwise
WOFF Web fonts will be used as a fallback (for open source fonts only). Note
that at the moment there are known bugs in browsers and fonts.

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
