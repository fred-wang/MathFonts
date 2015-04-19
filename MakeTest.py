# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function
from bisect import bisect_left
from math import sqrt
import fontforge
import sys

# Parameters describing the size of stretchy operators as a geometric sequence.
kStartSize = .25 # size of the first operator (in em)
kConsecutiveSizeRatio = sqrt(2) # ratio between size i+1 and size i
kNumberOfSizes = 12 # number of sizes

# List op "largeop" operators. See http://www.w3.org/TR/MathML3/appendixc.html
kLargeOp = [0x220F, 0x2210, 0x2211, 0x222B, 0x222C, 0x222D, 0x222E, 0x222F,
            0x2230, 0x2231, 0x2232, 0x2233, 0x22C0, 0x22C1, 0x22C2, 0x22C3,
            0x2A00, 0x2A01, 0x2A02, 0x2A03, 0x2A04, 0x2A05, 0x2A06, 0x2A07,
            0x2A08, 0x2A09, 0x2A0A, 0x2A0B, 0x2A0C, 0x2A0D, 0x2A0E, 0x2A0F,
            0x2A10, 0x2A11, 0x2A12, 0x2A13, 0x2A14, 0x2A15, 0x2A16, 0x2A17,
            0x2A18, 0x2A19, 0x2A1A, 0x2A1B, 0x2A1C, 0x2AFC, 0x2AFF, 0x228E,
            0x2295, 0x2296, 0x2297, 0x2299]

def isLargeOp(aCodePoint):
    # Binary search in the largeop list.
    i = bisect_left(kLargeOp, aCodePoint)
    return i != len(kLargeOp) and kLargeOp[i] == aCodePoint

def usage():
    print("usage: python %s [directory] [opentype-math-font]" % sys.argv[0],
          file=sys.stderr)

def main(aDirectory, aFont):
    testfile = open("./%s/index.html" % aDirectory, "w+")
    print("\
<!doctype html>\n\
<html>\n\
  <head>\n\
    <title>OpenType MATH testcase - %s</title>\n\
    <meta charset=\"utf-8\"/>\n\
    <link rel=\"stylesheet\" type=\"text/css\" href=\"./mathfonts.css\"/>\n\
    <style type=\"text/css\">\n\
      table {\n\
        border-collapse: collapse;\n\
      }\n\
      th, td {\n\
        text-align:center;\n\
        border: 1px solid black;\n\
      }\n\
    </style>\n\
  </head>\n\
  <body class=\"htmlmathparagraph\">\n\
    <h1>%s</h1>\n\
    <table>\n\
      <tr>\n\
        <th>Code Point</th>\n\
        <th>Base Glyph</th>\n\
        <th>Stretched Glyphs</th>\n\
      </tr>\n" % (aFont, aFont), file=testfile)

    font = fontforge.open("%s/%s" % (aDirectory, aFont))

    for glyph in font.glyphs():
         if glyph.unicode == -1:
             # Ignore non-unicode character.
             continue

         # Try and determine the stretch direction
         isHorizontal = (glyph.horizontalVariants is not None or
                         glyph.horizontalComponents is not None)
         isVertical = (glyph.verticalVariants is not None or
                       glyph.verticalComponents is not None)
         if (not isHorizontal) and (not isVertical):
             continue
         if isHorizontal and isVertical:
             print("Warning: Could not determined stretch direction for glyph \
U+%06X" % glyph.unicode, file=sys.stderr)
             continue

         # Print a table row for this operator.
         print("\
       <tr>\n\
         <td>U+%06X</td>\n\
         <td><math><mo stretchy=\"false\">&#x%X;</mo></math></td>\n\
         <td>" % (glyph.unicode, glyph.unicode), file=testfile)

         if (isLargeOp(glyph.unicode)):
             print("<math><mstyle displaystyle=\"false\"><mo mathcolor=\"#00f\">&#x%X;</mo></mstyle><mstyle displaystyle=\"true\"><mo mathcolor=\"#f00\">&#x%X;</mo></mstyle></math><br/>" % (glyph.unicode, glyph.unicode), file=testfile)

         size = kStartSize
         for i in range(1, kNumberOfSizes):
             blue = (kNumberOfSizes - i) * 256 / kNumberOfSizes
             red = i * 256 / kNumberOfSizes
             if isVertical:
                 print("<math><mrow><mspace height=\"%fem\" depth=\"%fem\" width=\"1px\" mathbackground=\"#%02X00%02X\"/><mo symmetric=\"false\" mathcolor=\"#%02X00%02X\" stretchy=\"true\">&#x%X;</mo></mrow></math>" % (size/2, size/2, red, blue, red, blue, glyph.unicode), file=testfile)
             else:
                 print("<math><mover><mspace width=\"%fem\" height=\"1px\" mathbackground=\"#%02X00%02X\"/><mo mathcolor=\"#%02X00%02X\" stretchy=\"true\">&#x%X;</mo></mover></math><br/>" % (i*.5, red, blue, red, blue, glyph.unicode), file=testfile)
             size *= kConsecutiveSizeRatio

         print("</td>\n\
       </tr>\n", file=testfile);

    font.close()
    print("\
    </table>\n\
  </body>\n\
</html>", file=testfile)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage()
        exit(1)
    main(sys.argv[1], sys.argv[2])
