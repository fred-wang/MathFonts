# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function
from fontTools.ttLib import TTFont, sfnt
from os.path import splitext
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: python %s filename" % sys.argv[0], file=sys.stderr)
        sys.exit(1)
    filename = sys.argv[1]
    basename = splitext(filename)[0]

    sfnt.USE_ZOPFLI = True
    for flavor in ["woff", "woff2"]:
        outfilename = "%s.%s" % (basename, flavor)
        print("Processing %s => %s" % (filename, outfilename))
        font = TTFont(filename, recalcBBoxes=False, recalcTimestamp=False)
        for t in font.keys():
            if hasattr(font[t], "compile"):
                font[t].compile(font)
        font.flavor = flavor
        font.save(outfilename, reorderTables=False)
