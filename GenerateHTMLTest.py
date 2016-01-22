# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function
from bisect import bisect_left
from datetime import datetime
from math import sqrt
import fontforge
import sys
import unicodedata

# Parameters describing the size of stretchy operators as a geometric sequence.
kStartSize = .25 # size of the first operator (in em)
kConsecutiveSizeRatio = sqrt(2) # ratio between size i+1 and size i
kNumberOfSizes = 12 # number of sizes

# List op "largeop" operators. See http://www.w3.org/TR/MathML3/appendixc.html
kLargeOperators = [0x220F, 0x2210, 0x2211, 0x222B, 0x222C, 0x222D, 0x222E,
                   0x222F, 0x2230, 0x2231, 0x2232, 0x2233, 0x22C0, 0x22C1,
                   0x22C2, 0x22C3, 0x2A00, 0x2A01, 0x2A02, 0x2A03, 0x2A04,
                   0x2A05, 0x2A06, 0x2A07, 0x2A08, 0x2A09, 0x2A0A, 0x2A0B,
                   0x2A0C, 0x2A0D, 0x2A0E, 0x2A0F, 0x2A10, 0x2A11, 0x2A12,
                   0x2A13, 0x2A14, 0x2A15, 0x2A16, 0x2A17, 0x2A18, 0x2A19,
                   0x2A1A, 0x2A1B, 0x2A1C, 0x2AFC, 0x2AFF]

# List of "prescripted" operators.
# See http://www.w3.org/TR/MathML3/appendixc.html
kPreScriptedOperators = [0x2032, 0x2033, 0x2034, 0x2035, 0x2036, 0x2037, 0x2057]

# MathML box with resizable height/depth/width
kBox = "<mrow class=\"resizable\"><mpadded depth=\"0px\" height=\"1height\"><mtext><span></span></mtext></mpadded><mpadded height=\"0px\" depth=\"1height\" voffset=\"-1height\"><mtext><span></span></mtext></mpadded></mrow>"

# CSS style
kStyle = "<style type=\"text/css\">\n\
.missingBox {\n\
  display: inline-block;\n\
  width: .75em;\n\
  height: .75em;\n\
  background: red;\n\
}\n\
table {\n\
  border-collapse: collapse;\n\
}\n\
th, td {\n\
  text-align:center;\n\
  border: 1px solid black;\n\
}\n\
mrow.resizable {\n\
  font-size: 1px; /* limit the handle size */\n\
  background: linear-gradient(70deg, red, orange);\n\
}\n\
mrow.resizable > mpadded > mtext > span {\n\
  display: inline-block; width: 8px; height: 3px;\n\
  overflow: hidden;\n\
}\n\
mrow.resizable > mpadded:first-child > mtext > span {\n\
  border-bottom: 1px solid black;\n\
  resize: vertical;\n\
}\n\
mrow.resizable > mpadded:last-child > mtext > span {\n\
  border-right: 1px solid black;\n\
  resize: both;\n\
}\n\
</style>"

def isLargeOp(aCodePoint):
    # Binary search in the largeop list.
    i = bisect_left(kLargeOperators, aCodePoint)
    return i != len(kLargeOperators) and kLargeOperators[i] == aCodePoint

def unicodeName(aCodePoint):
    return unicodedata.name(unichr(aCodePoint), "UNKNOWN CHARACTER NAME")

def printCodePoint(aTestFile, aCodePoint):
    print("<a href=\"https://duckduckgo.com/?q=U%%2B%06X\">U+%06X</a>" %
          (aCodePoint, aCodePoint), file=aTestFile)

def printCharacter(aTestFile, aFont, aCodePoint):
    if aCodePoint in aFont:
        print("<span title=\"U+%06X %s\"><math><mn>&#x%X;</mn></math></span>"
              % (aCodePoint, unicodeName(aCodePoint), aCodePoint),
              file=aTestFile)
    else:
        print("<span title=\"U+%06X %s\" class=\"missingBox\"></span>"
              % (aCodePoint, unicodeName(aCodePoint)),
              file=aTestFile)

def printUnicodeCoverage(aTestFile, aFont):
    print("<h2 id=\"unicode_coverage\">Unicode Coverage</h2><p>", file=aTestFile)
    coverage = []
    for glyph in aFont.glyphs():
        if glyph.unicode != -1:
            coverage.append(glyph.unicode)
    coverage.sort()

    for codePoint in coverage:
        print("U+%06X <math><mn>&#x%X;</mn></math> %s<br/>" %
              (codePoint, codePoint, unicodeName(codePoint)),
              file=aTestFile)

    print("</p>", file=aTestFile)

def printCharacterRange(aTestFile, aFont, aCodePointStart, aCodePointEnd):
    for codePoint in range(aCodePointStart, aCodePointEnd+1):
        printCharacter(aTestFile, aFont, codePoint)

def referenceBar(aFont, aValue, aVertical):
    v1 = abs(1. * aValue) / aFont.em
    v2 = 2 * v1
    if v2 < 2:
        v2 = 2
    bar = "<math><mspace width=\"%fem\" height=\"%fem\" mathbackground=\"#0f0\"/></math>"
    if aVertical:
        return (bar % (v2, v1))
    else:
        return (bar % (v1, v2))

def printBasicFontInfo(aTestFile, aFont):
    print("<h2 id=\"font_info\">Font Info</h2><table>\
    <tr><th>familyname</th><td>%s</td></tr>\
    <tr><th>fontname</th><td>%s</td></tr>\
    <tr><th>fullname</th><td>%s</td></tr>\
    <tr><th>version</th><td>%s</td></tr>\
    <tr><th>em</th><td>%s</td></tr>\
    <tr><th>hhea_ascent</th><td>%s</td></tr>\
    <tr><th>hhea_ascent_add</th><td>%s</td></tr>\
    <tr><th>hhea_descent</th><td>%s</td></tr>\
    <tr><th>hhea_descent_add</th><td>%s</td></tr>\
    <tr><th>hhea_linegap</th><td>%s</td></tr>\
    <tr><th>os2_typoascent</th><td>%s</td></tr>\
    <tr><th>os2_typoascent_add</th><td>%s</td></tr>\
    <tr><th>os2_typodescent</th><td>%s</td></tr>\
    <tr><th>os2_typodescent_add</th><td>%s</td></tr>\
    <tr><th>os2_typodescent</th><td>%s</td></tr>\
    <tr><th>os2_use_typo_metric</th><td>%s</td></tr>\
    <tr><th>os2_winascent</th><td>%s</td></tr>\
    <tr><th>os2_winascent_add</th><td>%s</td></tr>\
    <tr><th>os2_windescent</th><td>%s</td></tr>\
    <tr><th>os2_windescent_add</th><td>%s</td></tr>\
    </table>" % (aFont.familyname,
                 aFont.fontname,
                 aFont.fullname,
                 aFont.version,
                 aFont.em,
                 aFont.hhea_ascent,
                 aFont.hhea_ascent,
                 aFont.hhea_descent,
                 aFont.hhea_descent,
                 aFont.hhea_linegap,
                 aFont.os2_typoascent,
                 aFont.os2_typoascent_add,
                 aFont.os2_typodescent,
                 aFont.os2_typodescent_add,
                 aFont.os2_typodescent,
                 aFont.os2_use_typo_metrics,
                 aFont.os2_winascent,
                 aFont.os2_winascent_add,
                 aFont.os2_windescent,
                 aFont.os2_windescent_add),
          file=aTestFile)

def printConstruction(aTestFile, aConstruction):
    if aConstruction is None:
        print("N/A", file=aTestFile)
        return

    for c in aConstruction:
        if c[1]:
            print("[%s]" % c[0], file=aTestFile)
        else:
            print("%s" % c[0], file=aTestFile)

def printMathVariants(aTestFile, aFont):
    print("\
    <h2 id=\"mathvariants_table\">MathVariants Table</h2>\n\
    <table>\n\
      <tr>\n\
        <th>Code Point</th>\n\
        <th>Base Glyph</th>\n\
        <th style=\"width: 50%%\">Stretched Glyphs</th>\n\
        <th>MathGlyphVariantRecord</th>\n\
        <th>GlyphAssembly (extenders in brackets)</th>\n\
      </tr>\n", file=aTestFile)

    for glyph in aFont.glyphs():
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
        print("<tr><td>", file=aTestFile)
        printCodePoint(aTestFile, glyph.unicode)
        print("</td>", file=aTestFile)
        print("\
         <td><math><mo stretchy=\"false\">&#x%X;</mo></math></td>\n\
         <td>" % glyph.unicode, file=aTestFile)

        if isLargeOp(glyph.unicode):
            print("<math><mstyle displaystyle=\"false\"><mo mathcolor=\"#00f\">&#x%X;</mo></mstyle><mstyle displaystyle=\"true\"><mo mathcolor=\"#f00\">&#x%X;</mo></mstyle></math><br/>" % (glyph.unicode, glyph.unicode), file=aTestFile)

        size = kStartSize
        for i in range(1, kNumberOfSizes):
            blue = (kNumberOfSizes - i) * 256 / kNumberOfSizes
            red = i * 256 / kNumberOfSizes
            if isVertical:
                print("<math><mrow><mspace height=\"%fem\" depth=\"%fem\" width=\"1px\" mathbackground=\"#%02X00%02X\"/><mo symmetric=\"false\" mathcolor=\"#%02X00%02X\" stretchy=\"true\">&#x%X;</mo></mrow></math>" % (size/2, size/2, red, blue, red, blue, glyph.unicode), file=aTestFile)
            else:
                print("<math><mover><mspace width=\"%fem\" height=\"1px\" mathbackground=\"#%02X00%02X\"/><mo mathcolor=\"#%02X00%02X\" stretchy=\"true\">&#x%X;</mo></mover></math><br/>" % (i*.5, red, blue, red, blue, glyph.unicode), file=aTestFile)
            size *= kConsecutiveSizeRatio

        print("</td>", file=aTestFile)

        # Print size variants
        if glyph.verticalVariants:
            variants = glyph.verticalVariants
        elif glyph.horizontalVariants:
            variants = glyph.horizontalVariants
        else:
            print("<td>N/A</td>", file=aTestFile);
            variants = None
        if variants:
            print("<td>", file=aTestFile);
            for v in variants.split():
                print("%s<br/>" % v, file=aTestFile);
            print("</td>", file=aTestFile);

        # Print glyph
        print("<td>", file=aTestFile)
        if isVertical:
            printConstruction(aTestFile, glyph.verticalComponents)
        else:
            printConstruction(aTestFile, glyph.horizontalComponents)
        print("</td>", file=aTestFile)

        print("\n\
      </tr>\n", file=aTestFile)

    print("\
    </table>\n", file=aTestFile)

def printLargeOp(aTestFile, aFont):
    print("\
    <h2 id=\"largeop\">Large Operators</h2>\
<p>Source: <a href=\"http://www.w3.org/TR/MathML3/appendixc.html#oper-dict.entries-table\">MathML Operator Dictionary</a></p>\
    <table><tr><th>Code Point</th><th>Base Size</th><th>Display Style</th><th>Italic Correction</th>\n",
          file=aTestFile)

    for u in kLargeOperators:
        print("<tr><td>", file=aTestFile)
        printCodePoint(aTestFile, u)
        print("</td>", file=aTestFile)
        if u in aFont:
            print("<td><math><mo>&#x%X;</mo></math></td>" % u, file=aTestFile)
            glyph = aFont[u]
            if (glyph.verticalVariants is not None or
                glyph.verticalComponents is not None):
                print("\
        <td><math display=\"block\"><msubsup><mo mathcolor=\"#f00\">&#x%X;</mo><mspace width=\"8px\" height=\"4px\" depth=\"4px\" mathbackground=\"#0f0\"/><mspace width=\"8px\" height=\"4px\" depth=\"4px\" mathbackground=\"#00f\"/></msubsup></math></td>" % u,
                      file=aTestFile)
                value = glyph.italicCorrection
                if value != fontforge.unspecifiedMathValue:
                    print("<td>%d</td>" % value, file=aTestFile)
                else:
                    print("<td>N/A</td>", file=aTestFile)
            else:
                print("<td>N/A</td><td>N/A</td>", file=aTestFile)
        else:
            print("<td>N/A</td><td>N/A</td><td>N/A</td>", file=aTestFile)

        print("</tr>", file=aTestFile)

    print("</table>\n", file=aTestFile)


def printMathematicalAlphanumericCharacters(aTestFile, aFont):
    print("<h2 id=\"math_alpha_char\">Mathematical Alphanumeric Characters</h2>\
<p>Source: <a href=\"http://www.w3.org/TR/xml-entity-names/Overview.html#alphabets\">XML Entity Definitions for Characters</a>.</p>\
    <table><tr><th>mathvariant</th><th>Characters</th></tr>\n",
          file=aTestFile)

    print("<tr><td>bold</td><td>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1D400, 0x1D433)
    print("<br/>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1D6A8, 0x1D6E1)
    print("<br/>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1D7CA, 0x1D7CB)
    print("<br/>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1D7CE, 0x1D7D7)
    print("</td></tr>", file=aTestFile)

    print("<tr><td>italic<br/>(default on single-char variables)</td><td>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1D434, 0x1D454)
    printCharacter(aTestFile, aFont, 0x210E)
    printCharacterRange(aTestFile, aFont, 0x1D456, 0x1D467)
    print("<br/>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1D6A4, 0x1D6A5)
    print("<br/>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1D6E2, 0x1D6D6)
    print("</td></tr>", file=aTestFile)

    print("<tr><td>bold-italic</td><td>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1D468, 0x1D49B)
    print("<br/>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1D71C, 0x1D755)
    print("</td></tr>", file=aTestFile)

    print("<tr><td>script</td><td>", file=aTestFile)
    printCharacter(aTestFile, aFont, 0x1D49C)
    printCharacter(aTestFile, aFont, 0x212C)
    printCharacterRange(aTestFile, aFont, 0x1D49E, 0x1D49F)
    printCharacterRange(aTestFile, aFont, 0x2130, 0x2131)
    printCharacter(aTestFile, aFont, 0x1D4A2)
    printCharacter(aTestFile, aFont, 0x210B)
    printCharacter(aTestFile, aFont, 0x2110)
    printCharacterRange(aTestFile, aFont, 0x1D4A5, 0x1D4A6)
    printCharacter(aTestFile, aFont, 0x2112)
    printCharacter(aTestFile, aFont, 0x2133)
    printCharacterRange(aTestFile, aFont, 0x1D4A9, 0x1D4AC)
    printCharacter(aTestFile, aFont, 0x211B)
    printCharacterRange(aTestFile, aFont, 0x1D4AE, 0x1D4B9)
    printCharacter(aTestFile, aFont, 0x212F)
    printCharacter(aTestFile, aFont, 0x1D4BB)
    printCharacter(aTestFile, aFont, 0x210A)
    printCharacterRange(aTestFile, aFont, 0x1D4BD, 0x1D4C3)
    printCharacter(aTestFile, aFont, 0x2134)
    printCharacterRange(aTestFile, aFont, 0x1D4C5, 0x1D4CF)
    print("</td></tr>", file=aTestFile)

    print("<tr><td>bold-script</td><td>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1D4D0, 0x1D503)
    print("</td></tr>", file=aTestFile)

    print("<tr><td>fraktur</td><td>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1D504, 0x1D505)
    printCharacter(aTestFile, aFont, 0x212D)
    printCharacterRange(aTestFile, aFont, 0x1D507, 0x1D50A)
    printCharacter(aTestFile, aFont, 0x210C)
    printCharacter(aTestFile, aFont, 0x2111)
    printCharacterRange(aTestFile, aFont, 0x1D50D, 0x1D514)
    printCharacter(aTestFile, aFont, 0x211C)
    printCharacterRange(aTestFile, aFont, 0x1D516, 0x1D51C)
    printCharacter(aTestFile, aFont, 0x2128)
    printCharacterRange(aTestFile, aFont, 0x1D51E, 0x1D537)
    print("</td></tr>", file=aTestFile)

    print("<tr><td>bold-fraktur</td><td>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1D56C, 0x1D59F)
    print("</td></tr>", file=aTestFile)

    print("<tr><td>sans-serif</td><td>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1D5A0, 0x1D5D3)
    print("<br/>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1D7E2, 0x1D7EB)
    print("</td></tr>", file=aTestFile)

    print("<tr><td>bold-sans-serif</td><td>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1D5D4, 0x1D607)
    print("<br/>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1D756, 0x1D78F)
    print("<br/>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1D7EC, 0x1D7F5)
    print("</td></tr>", file=aTestFile)

    print("<tr><td>sans-serif-italic</td><td>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1D608, 0x1D63B)
    print("</td></tr>", file=aTestFile)

    print("<tr><td>sans-serif-bold-italic</td><td>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1D63C, 0x1D66F)
    print("<br/>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1D790, 0x1D7C9)
    print("</td></tr>", file=aTestFile)

    print("<tr><td>monospace</td><td>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1D670, 0x1D6A3)
    print("<br/>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1D7F6, 0x1D7FF)
    print("</td></tr>", file=aTestFile)

    print("<tr><td>double-struck</td><td>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1D538, 0x1D539)
    printCharacter(aTestFile, aFont, 0x2102)
    printCharacterRange(aTestFile, aFont, 0x1D53B, 0x1D53E)
    printCharacter(aTestFile, aFont, 0x210D)
    printCharacterRange(aTestFile, aFont, 0x1D540, 0x1D544)
    printCharacter(aTestFile, aFont, 0x2115)
    printCharacter(aTestFile, aFont, 0x1D546)
    printCharacterRange(aTestFile, aFont, 0x2119, 0x211A)
    printCharacter(aTestFile, aFont, 0x211D)
    printCharacterRange(aTestFile, aFont, 0x1D54A, 0x1D550)
    printCharacter(aTestFile, aFont, 0x2124)
    printCharacterRange(aTestFile, aFont, 0x1D552, 0x1D56B)
    print("<br/>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1D7D8, 0x1D7E1)
    print("<br/>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1EEA1, 0x1EEA3)
    printCharacterRange(aTestFile, aFont, 0x1EEA5, 0x1EEA9)
    printCharacterRange(aTestFile, aFont, 0x1EEAB, 0x1EEBB)
    print("</td></tr>", file=aTestFile)

    print("<tr><td>initial</td><td>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1EE21, 0x1EE22)
    printCharacter(aTestFile, aFont, 0x1EE24)
    printCharacter(aTestFile, aFont, 0x1EE27)
    printCharacterRange(aTestFile, aFont, 0x1EE29, 0x1EE32)
    printCharacterRange(aTestFile, aFont, 0x1EE34, 0x1EE37)
    printCharacter(aTestFile, aFont, 0x1EE39)
    printCharacter(aTestFile, aFont, 0x1EE3B)
    print("</td></tr>", file=aTestFile)

    print("<tr><td>tailed</td><td>", file=aTestFile)
    printCharacter(aTestFile, aFont, 0x1EE42)
    printCharacter(aTestFile, aFont, 0x1EE47)
    printCharacter(aTestFile, aFont, 0x1EE49)
    printCharacter(aTestFile, aFont, 0x1EE4B)
    printCharacterRange(aTestFile, aFont, 0x1EE4D, 0x1EE4F)
    printCharacterRange(aTestFile, aFont, 0x1EE51, 0x1EE52)
    printCharacter(aTestFile, aFont, 0x1EE54)
    printCharacter(aTestFile, aFont, 0x1EE57)
    printCharacter(aTestFile, aFont, 0x1EE59)
    printCharacter(aTestFile, aFont, 0x1EE5B)
    printCharacter(aTestFile, aFont, 0x1EE5D)
    printCharacter(aTestFile, aFont, 0x1EE5F)
    print("</td></tr>", file=aTestFile)

    print("<tr><td>looped</td><td>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1EE80, 0x1EE89)
    printCharacterRange(aTestFile, aFont, 0x1EE8B, 0x1EE9B)
    print("</td></tr>", file=aTestFile)

    print("<tr><td>stretched</td><td>", file=aTestFile)
    printCharacterRange(aTestFile, aFont, 0x1EE61, 0x1EE62)
    printCharacter(aTestFile, aFont, 0x1EE64)
    printCharacterRange(aTestFile, aFont, 0x1EE67, 0x1EE6A)
    printCharacterRange(aTestFile, aFont, 0x1EE6C, 0x1EE72)
    printCharacterRange(aTestFile, aFont, 0x1EE74, 0x1EE77)
    printCharacterRange(aTestFile, aFont, 0x1EE79, 0x1EE7C)
    printCharacter(aTestFile, aFont, 0x1EE7E)
    print("</td></tr>", file=aTestFile)

    print("</table>\n", file=aTestFile)

def printScriptedOperators(aTestFile, aFont):
    print("\
    <h2 id=\"scriptedop_ssty\">Prescripted Operators / ssty tables</h2>\
<p>Source: <a href=\"http://www.w3.org/TR/MathML3/appendixc.html#oper-dict.entries-table\">MathML Operator Dictionary</a></p>\
    <table><tr><th>Code Point</th><th>Normal</th><th>Scripted Level 1</th><th>Scripted Level 2</th><th>ssty table</th>\n",
          file=aTestFile)
    for u in kPreScriptedOperators:
        print("<tr><td>", file=aTestFile)
        printCodePoint(aTestFile, u)
        print("</td>", file=aTestFile)
        if u in aFont:
            print("<td><math><mn>A</mn><mo>&#x%X;</mo></math></td>\
<td><math><msup><mn>A</mn><mo>&#x%X;</mo></msup></math></td>\
<td><math><msup><mn>A</mn><msup><mn>B</mn><mo>&#x%X;</mo></msup></math></msup></td>" % (u, u, u), file=aTestFile)
            glyph = aFont[u]
            print("<td>", file=aTestFile)
            foundSSTY = False
            for table in glyph.getPosSub("*"):
                if table[0].find("ssty") > 0:
                    print(table[1:], file=aTestFile)
                    foundSSTY=True
                    break
            if not foundSSTY:
                print("N/A", file=aTestFile)
            print("</td>", file=aTestFile)
        else:
            print("<td>N/A</td><td>N/A</td>", file=aTestFile)

        print("</tr>", file=aTestFile)

    print("</table>\n", file=aTestFile)

def printMathConstants(aTestFile, aFont):
    print("\
    <h2 id=\"mathconstants_table\">MathConstants tables</h2>\
    <table width=\"100%%\"><tr><th>Constant</th><th>Value</th><th>Reference</th><th width=\"80%%\">Samples</th></tr>",
          file=aTestFile)

    # DisplayOperatorMinHeight
    print("<tr><td>DisplayOperatorMinHeight</td><td>%d</td><td>%s</td><td><math><mstyle displaystyle=\"false\"><mo mathcolor=\"#00f\">&#x2211;</mo></mstyle><mstyle displaystyle=\"true\"><mo mathcolor=\"#f00\">&#x2211;</mo></mstyle><mo mathcolor=\"#00f\">&#x222C;</mo></mstyle><mstyle displaystyle=\"true\"><mo mathcolor=\"#f00\">&#x222C;</mo></mstyle></math></td></tr>" %
          (aFont.math.DisplayOperatorMinHeight,
           referenceBar(aFont, aFont.math.DisplayOperatorMinHeight, True)),
          file=aTestFile)

    # Axis Height
    box = "<mspace width=\"20px\" depth=\"10px\" height=\"10px\" mathbackground=\"#f00\"/>"
    print("<tr><td>AxisHeight</td><td>%d</td><td>%s</td><td><math><mrow><mtext>baseline &#x2192;</mtext><mspace height=\".5px\" depth=\".5px\" width=\"100px\" mathbackground=\"black\"/><mfrac><mspace width=\"100px\"/><mspace/></mfrac><mtext>&#x2190; axis</mtext></mrow></math></td></tr>" %
          (aFont.math.AxisHeight,
           referenceBar(aFont, aFont.math.AxisHeight, True)),
          file=aTestFile)

    # AccentBaseHeight
    print("<tr><td>AccentBaseHeight</td><td>%d</td><td>%s</td><td><math><mover accent=\"true\">%s%s</mover></math></td></tr></tr>" %
          (aFont.math.AccentBaseHeight,
           referenceBar(aFont, aFont.math.AccentBaseHeight, True),
           kBox, kBox),
           file=aTestFile)

    # Scripts
    boxAfter = "<mspace width=\"1px\" depth=\"50px\" height=\"50px\" mathbackground=\"#000\"/><mspace width=\"1em\"/>"
    scriptsTest = "<mrow><mtext>msub:</mtext><msub>%s%s</msub>%s<mtext>msup:</mtext><msup>%s%s</msup>%s<mtext>msubsup:</mtext><msubsup>%s%s%s</msubsup>%s<mtext>mmultiscripts:</mtext><mmultiscripts>%s%s%s%s%s<mprescripts/>%s%s%s%s</mmultiscripts>%s</mrow>" % (kBox, kBox, boxAfter, kBox, kBox, boxAfter, kBox, kBox, kBox, boxAfter, kBox, kBox, kBox, kBox, kBox, kBox, kBox, kBox, kBox, boxAfter)

    print("<tr><td>SubscriptShiftDown</td><td>%d</td><td>%s</td><td rowspan=\"10\"><math display=\"block\"><mfrac><mrow><mtext>Not Cramped:</mtext><mspace width=\"2em\"/>%s</mrow><mrow><mtext>Cramped:</mtext><mspace width=\"2em\"/>%s</mrow></mfrac></math></td></tr>" % (aFont.math.SubscriptShiftDown, referenceBar(aFont, aFont.math.SubscriptShiftDown, True), scriptsTest, scriptsTest), file=aTestFile)

    print("<tr><td>SubscriptTopMax</td><td>%d</td><td>%s</td></tr>" % (aFont.math.SubscriptTopMax, referenceBar(aFont, aFont.math.SubscriptTopMax, True)), file=aTestFile)

    print("<tr><td>SubscriptBaselineDropMin</td><td>%d</td><td>%s</td></tr>" % (aFont.math.SubscriptBaselineDropMin, referenceBar(aFont, aFont.math.SubscriptBaselineDropMin, True)), file=aTestFile)

    print("<tr><td>SuperscriptShiftUp</td><td>%d</td><td>%s</td></tr>" % (aFont.math.SuperscriptShiftUp, referenceBar(aFont, aFont.math.SuperscriptShiftUp, True)), file=aTestFile)

    print("<tr><td>SuperscriptShiftUpCramped</td><td>%d</td><td>%s</td></tr>" % (aFont.math.SuperscriptShiftUpCramped, referenceBar(aFont, aFont.math.SuperscriptShiftUpCramped, True)), file=aTestFile)

    print("<tr><td>SuperscriptBottomMin</td><td>%d</td><td>%s</td></tr>" % (aFont.math.SuperscriptBottomMin, referenceBar(aFont, aFont.math.SuperscriptBottomMin, True)), file=aTestFile)

    print("<tr><td>SuperscriptBaselineDropMax</td><td>%d</td><td>%s</td></tr>" % (aFont.math.SuperscriptBaselineDropMax, referenceBar(aFont, aFont.math.SuperscriptBaselineDropMax, True)), file=aTestFile)

    print("<tr><td>SubSuperscriptGapMin</td><td>%d</td><td>%s</td></tr>" % (aFont.math.SubSuperscriptGapMin, referenceBar(aFont, aFont.math.SubSuperscriptGapMin, True)), file=aTestFile)

    print("<tr><td>SuperscriptBottomMaxWithSubscript</td><td>%d</td><td>%s</td></tr>" % (aFont.math.SuperscriptBottomMaxWithSubscript, referenceBar(aFont, aFont.math.SuperscriptBottomMaxWithSubscript, True)), file=aTestFile)

    print("<tr><td>SpaceAfterScript</td><td>%d</td><td>%s</td></tr>" % (aFont.math.SpaceAfterScript, referenceBar(aFont, aFont.math.SpaceAfterScript, False)), file=aTestFile)

    # Limits
    print("<tr><td>UpperLimitGapMin</td><td>%d</td><td>%s</td><td rowspan=\"4\"><math><munderover>%s%s%s</munderover></math></td></tr>" % (aFont.math.UpperLimitGapMin, referenceBar(aFont, aFont.math.UpperLimitGapMin, True), kBox, kBox, kBox), file=aTestFile)

    print("<tr><td>UpperLimitBaselineRiseMin</td><td>%d</td><td>%s</td></tr>" % (aFont.math.UpperLimitBaselineRiseMin, referenceBar(aFont, aFont.math.UpperLimitBaselineRiseMin, True)), file=aTestFile)

    print("<tr><td>LowerLimitGapMin</td><td>%d</td><td>%s</td></tr>" % (aFont.math.LowerLimitGapMin, referenceBar(aFont, aFont.math.LowerLimitGapMin, True)), file=aTestFile)

    print("<tr><td>LowerLimitBaselineDropMin</td><td>%d</td><td>%s</td></tr>" % (aFont.math.LowerLimitBaselineDropMin, referenceBar(aFont, aFont.math.LowerLimitBaselineDropMin, True)), file=aTestFile)

    # Stack
    print("<tr><td>StackTopShiftUp</td><td>%s</td><td>%s</td><td rowspan=\"6\"><math><mtext>Inline Style:</mtext><mfrac linethickness=\"0px\">%s%s</mfrac><mspace width=\"1em\"/><mtext>Display Style:</mtext><mstyle displaystyle=\"true\"><mfrac linethickness=\"0px\">%s%s</mfrac></mstyle></math></td></tr>" % (aFont.math.StackTopShiftUp, referenceBar(aFont, aFont.math.StackTopShiftUp, True), kBox, kBox, kBox, kBox), file=aTestFile)

    print("<tr><td>StackTopDisplayStyleShiftUp</td><td>%d</td><td>%s</td></tr>" % (aFont.math.StackTopDisplayStyleShiftUp, referenceBar(aFont, aFont.math.StackTopDisplayStyleShiftUp, True)), file=aTestFile)

    print("<tr><td>StackBottomShiftDown</td><td>%d</td><td>%s</td></tr>" % (aFont.math.StackBottomShiftDown, referenceBar(aFont, aFont.math.StackBottomShiftDown, True)), file=aTestFile)

    print("<tr><td>StackBottomDisplayStyleShiftDown</td><td>%d</td><td>%s</td></tr>" % (aFont.math.StackBottomDisplayStyleShiftDown, referenceBar(aFont, aFont.math.StackBottomDisplayStyleShiftDown, True)), file=aTestFile)

    print("<tr><td>StackGapMin</td><td>%d</td><td>%s</td></tr>" % (aFont.math.StackGapMin, referenceBar(aFont, aFont.math.StackGapMin, True)), file=aTestFile)

    print("<tr><td>StackDisplayStyleGapMin</td><td>%d</td><td>%s</td></tr>" % (aFont.math.StackDisplayStyleGapMin, referenceBar(aFont, aFont.math.StackDisplayStyleGapMin, True)), file=aTestFile)

    # Fraction
    print("<tr><td>FractionNumeratorShiftUp</td><td>%s</td><td>%s</td><td rowspan=\"9\"><math><mtext>Inline Style:</mtext><mfrac>%s%s</mfrac><mspace width=\"1em\"/><mtext>Display Style:</mtext><mstyle displaystyle=\"true\"><mfrac>%s%s</mfrac></mstyle></math></td></tr>" % (aFont.math.FractionNumeratorShiftUp, referenceBar(aFont, aFont.math.FractionNumeratorShiftUp, True), kBox, kBox, kBox, kBox), file=aTestFile)

    print("<tr><td>FractionNumeratorDisplayStyleShiftUp</td><td>%d</td><td>%s</td></tr>" % (aFont.math.FractionNumeratorDisplayStyleShiftUp, referenceBar(aFont, aFont.math.FractionNumeratorDisplayStyleShiftUp, True)), file=aTestFile)

    print("<tr><td>FractionDenominatorShiftDown</td><td>%d</td><td>%s</td></tr>" % (aFont.math.FractionDenominatorShiftDown, referenceBar(aFont, aFont.math.FractionDenominatorShiftDown, True)), file=aTestFile)

    print("<tr><td>FractionDenominatorDisplayStyleShiftDown</td><td>%d</td><td>%s</td></tr>" % (aFont.math.FractionDenominatorDisplayStyleShiftDown, referenceBar(aFont, aFont.math.FractionDenominatorDisplayStyleShiftDown, True)), file=aTestFile)

    print("<tr><td>FractionNumeratorGapMin</td><td>%d</td><td>%s</td></tr>" % (aFont.math.FractionNumeratorGapMin, referenceBar(aFont, aFont.math.FractionNumeratorGapMin, True)), file=aTestFile)

    print("<tr><td>FractionNumeratorDisplayStyleGapMin</td><td>%d</td><td>%s</td></tr>" % (aFont.math.FractionNumeratorDisplayStyleGapMin, referenceBar(aFont, aFont.math.FractionNumeratorDisplayStyleGapMin, True)), file=aTestFile)

    print("<tr><td>FractionRuleThickness</td><td>%d</td><td>%s</td></tr>" % (aFont.math.FractionRuleThickness, referenceBar(aFont, aFont.math.FractionRuleThickness, True)), file=aTestFile)

    print("<tr><td>FractionDenominatorGapMin</td><td>%d</td><td>%s</td></tr>" % (aFont.math.FractionDenominatorGapMin, referenceBar(aFont, aFont.math.FractionDenominatorGapMin, True)), file=aTestFile)

    print("<tr><td>FractionDenominatorDisplayStyleGapMin</td><td>%d</td><td>%s</td></tr>" % (aFont.math.FractionDenominatorDisplayStyleGapMin, referenceBar(aFont, aFont.math.FractionDenominatorDisplayStyleGapMin, True)), file=aTestFile)

    # Radical
    rootTest = "<mspace width=\"1px\" depth=\"50px\" height=\"50px\" mathbackground=\"#000\"/><mroot>%s%s</mroot>" % (kBox, kBox)
    print("<tr><td>RadicalVerticalGap</td><td>%d</td><td>%s</td><td rowspan=\"7\"><math><mtext>Inline Style:</mtext>%s<mspace width=\"1em\"/><mtext>Display Style:</mtext><mstyle displaystyle=\"true\">%s</mstyle></math></td></tr>" % (aFont.math.RadicalVerticalGap, referenceBar(aFont, aFont.math.RadicalVerticalGap, True), rootTest, rootTest), file=aTestFile)

    print("<tr><td>RadicalDisplayStyleVerticalGap</td><td>%d</td><td>%s</td></tr>" % (aFont.math.RadicalDisplayStyleVerticalGap, referenceBar(aFont, aFont.math.RadicalDisplayStyleVerticalGap, True)), file=aTestFile)

    print("<tr><td>RadicalRuleThickness</td><td>%d</td><td>%s</td></tr>" % (aFont.math.RadicalRuleThickness, referenceBar(aFont, aFont.math.RadicalRuleThickness, True)), file=aTestFile)

    print("<tr><td>RadicalExtraAscender</td><td>%d</td><td>%s</td></tr>" % (aFont.math.RadicalExtraAscender, referenceBar(aFont, aFont.math.RadicalExtraAscender, True)), file=aTestFile)

    print("<tr><td>RadicalKernBeforeDegree</td><td>%d</td><td>%s</td></tr>" % (aFont.math.RadicalKernBeforeDegree, referenceBar(aFont, aFont.math.RadicalKernBeforeDegree, False)), file=aTestFile)

    print("<tr><td>RadicalKernAfterDegree</td><td>%d</td><td>%s</td></tr>" % (aFont.math.RadicalKernAfterDegree, referenceBar(aFont, aFont.math.RadicalKernAfterDegree, False)), file=aTestFile)

    print("<tr><td>RadicalDegreeBottomRaisePercent</td><td>%d</td><td></td></tr>" % aFont.math.RadicalDegreeBottomRaisePercent, file=aTestFile)

    print("</table>\n", file=aTestFile)

def main(aDirectory, aFont):
    testfile = open("./%s/index.html" % aDirectory, "w+")
    print("\
<!doctype html>\n\
<html><head><title>%s</title><meta charset=\"utf-8\"/>\n\
  <link rel=\"stylesheet\" type=\"text/css\" href=\"./mathfonts.css\"/>\n\
  %s\n\
  <body class=\"htmlmathparagraph\">\n\
    <h1>%s</h1>\n\
    <a href=\"./CheckFontLog.txt\">CheckFontLog.txt</a> - \
    <a href=\"./CheckFontError.txt\">CheckFontError.txt</a>" %
          (aFont, kStyle, aFont), file=testfile)

    font = fontforge.open("%s/%s" % (aDirectory, aFont))
    printBasicFontInfo(testfile, font)
    printMathConstants(testfile, font)
    printMathVariants(testfile, font)
    printLargeOp(testfile, font)
    printMathematicalAlphanumericCharacters(testfile, font)
    printScriptedOperators(testfile, font)
    printUnicodeCoverage(testfile, font)
    font.close()

    print("\
  </body>\n\
</html>", file=testfile)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python %s [directory] [opentype-math-font]" % sys.argv[0],
              file=sys.stderr)
        exit(1)
    main(sys.argv[1], sys.argv[2])
