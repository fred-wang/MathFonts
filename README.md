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
