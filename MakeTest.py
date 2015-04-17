# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function
from math import sqrt
import fontforge
import sys

# Parameters describing the size of stretchy operators as a geometric sequence.
kStartSize = .25 # size of the first operator (in em)
kConsecutiveSizeRatio = sqrt(2) # ratio between size i+1 and size i
kNumberOfSizes = 12 # number of sizes

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
         <td><math><mo>&#x%X;</mo></math></td>\n\
         <td>" % (glyph.unicode, glyph.unicode), file=testfile)

         size = kStartSize
         for i in range(1, kNumberOfSizes):
             blue = (kNumberOfSizes - i) * 256 / kNumberOfSizes
             red = i * 256 / kNumberOfSizes
             if isVertical:
                 print("<math><mrow><mspace height=\"%fem\" depth=\"%fem\" width=\"1px\" mathbackground=\"#%02X00%02X\"/><mo mathcolor=\"#%02X00%02X\" stretchy=\"true\">&#x%X;</mo></mrow></math>" % (size/2, size/2, red, blue, red, blue, glyph.unicode), file=testfile)
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
