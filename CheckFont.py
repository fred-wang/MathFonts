# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function
from bisect import bisect_left
from datetime import datetime
from math import sqrt
import fontforge
import sys

# List op "largeop" operators. See http://www.w3.org/TR/MathML3/appendixc.html
kLargeOperators = [0x220F, 0x2210, 0x2211, 0x222B, 0x222C, 0x222D, 0x222E,
                   0x222F, 0x2230, 0x2231, 0x2232, 0x2233, 0x22C0, 0x22C1,
                   0x22C2, 0x22C3, 0x2A00, 0x2A01, 0x2A02, 0x2A03, 0x2A04,
                   0x2A05, 0x2A06, 0x2A07, 0x2A08, 0x2A09, 0x2A0A, 0x2A0B,
                   0x2A0C, 0x2A0D, 0x2A0E, 0x2A0F, 0x2A10, 0x2A11, 0x2A12,
                   0x2A13, 0x2A14, 0x2A15, 0x2A16, 0x2A17, 0x2A18, 0x2A19,
                   0x2A1A, 0x2A1B, 0x2A1C, 0x2AFC, 0x2AFF]

# List of Unicode Constructions
# Based on https://mxr.mozilla.org/mozilla-central/source/layout/mathml/mathfontUnicode.properties
# construction = (codePoint, isVertical, variants, assemblies)
# variants = (codePointSize1, codePointSize2, ...)
# assemblies = ((codePoint, isExtender), ...)
kUnicodeConstructions = [
    (0x0028, True, None, ((0x239D, 0), (0x239C, 1), (0x239B, 0))), # LEFT PARENTHESIS (
    (0x0029, True, None, ((0x23A0, 0), (0x239F, 1), (0x239E, 0))), # RIGHT PARENTHESIS )
    (0x005B, True, None, ((0x23A3, 0), (0x23A2, 1), (0x23A1, 0))), # LEFT SQUARE BRACKET [
    (0x005D, True, None, ((0x23A6, 0), (0x23A5, 1), (0x23A4, 0))), # RIGHT SQUARE BRACKET ]
    (0x007B, True, None, ((0x23A9, 0), (0x23AA, 1), (0x23A8, 0), (0x23AA, 1), (0x23A7, 0))), # LEFT CURLY BRACKET {
    (0x007C, True, None, ((0x007C, 0), (0x007C, 1))), # VERTICAL LINE |
    (0x007D, True, None, ((0x23AD, 0), (0x23AA, 1), (0x23AC, 0), (0x23AA, 1), (0x23AB, 0))), # RIGHT CURLY BRACKET }

    (0x00AF, False, None, ((0x00AF, 0), (0x00AF, 1))), # MACRON
    (0x203E, False, None, ((0x00AF, 0), (0x00AF, 1))), # OVERLINE
    (0x005F, False, None, ((0x005F, 0), (0x005F, 1))), # LOW LINE _
    (0x003D, False, None, ((0x003D, 0), (0x003D, 1))), # EQUALS SIGN =

    (0x2016, True, None, ((0x2016, 0), (0x2016, 1))), # DOUBLE VERTICAL LINE

    (0x2190, False, (0x27F5,), ((0x2190, 0), (0x23AF, 1))), # LEFTWARDS ARROW
    (0x2191, True, None, ((0x23D0, 1), (0x2191, 0))), # UPWARDS ARROW
    (0x2192, False, (0x27F6,), ((0x23AF, 1), (0x2192, 0))), # RIGHTWARDS ARROW
    (0x2193, True, None, ((0x2193, 0), (0x23D0, 1))), # DOWNWARDS ARROW
    (0x2194, False, (0x27F7,), ((0x2190, 0), (0x23AF, 1), (0x2192, 0))), # LEFT RIGHT ARROW
    (0x2195, True, None, ((0x2193, 0), (0x23D0, 1), (0x2191, 0))), # UP DOWN ARROW

    (0x21A4, False, (0x27FB,), ((0x2190, 0), (0x23AF, 1), (0x22A3, 0))), # LEFTWARDS ARROW FROM BAR
    (0x21A6, False, (0x27FC,), ((0x22A2, 0), (0x23AF, 1), (0x2192, 0))), # RIGHTWARDS ARROW FROM BAR
    (0x295A, False, None, ((0x21BC, 0), (0x23AF, 1), (0x22A3, 0))), # LEFTWARDS HARPOON WITH BARB UP FROM BAR
    (0x295B, False, None, ((0x22A2, 0), (0x23AF, 1), (0x21C0, 0))), # RIGHTWARDS HARPOON WITH BARB UP FROM BAR
    (0x295E, False, None, ((0x21BD, 0), (0x23AF, 1), (0x22A3, 0))), # LEFTWARDS HARPOON WITH BARB DOWN FROM BAR
    (0x295F, False, None, ((0x22A2, 0), (0x23AF, 1), (0x21C1, 0))), # RIGHTWARDS HARPOON WITH BARB DOWN FROM BAR

    (0x21C0, False, None, ((0x23AF, 1), (0x21C0, 0))), # RIGHTWARDS HARPOON WITH BARB UPWARDS
    (0x21C1, False, None, ((0x23AF, 1), (0x21C1, 0))), # RIGHTWARDS HARPOON WITH BARB DOWNWARDS
    (0x21BC, False, None, ((0x21BC, 0), (0x23AF, 1))), # LEFTWARDS HARPOON WITH BARB UPWARDS
    (0x21BD, False, None, ((0x21BD, 0), (0x23AF, 1))), # LEFTWARDS HARPOON WITH BARB DOWNWARDS
    (0x21D0, False, (0x27F8,), None), # LEFTWARDS DOUBLE ARROW
    (0x21D2, False, (0x27F9,), None), # RIGHTWARDS DOUBLE ARROW
    (0x21D4, False, (0x27FA,), None), # LEFT RIGHT DOUBLE ARROW

    (0x222B, True, None, ((0x2321, 0), (0x23AE, 0), (0x2320, 0))), # INTEGRAL

    (0x2308, True, None, ((0x23A2, 1), (0x23A1, 0))), # LEFT CEILING
    (0x2309, True, None, ((0x23A5, 1), (0x23A4, 0))), # RIGHT CEILING
    (0x230A, True, None, ((0x23A3, 0), (0x23A2, 1))), # LEFT FLOOR
    (0x230B, True, None, ((0x23A6, 0), (0x23A5, 1))), # RIGHT FLOOR

    (0x23B0, True, None, ((0x23AD, 0), (0x23AA, 1), (0x23A7, 0))), # lmoustache
    (0x23B1, True, None, ((0x23A9, 0), (0x23AA, 1), (0x23AB, 0))), # rmoustache

    (0x27F5, False, None, ((0x27F5, 0), (0x23AF, 1))), # LONG LEFTWARDS ARROW
    (0x27F6, False, None, ((0x23AF, 1), (0x27F6, 0))), # LONG RIGHTWARDS ARROW
    (0x27F7, False, None, ((0x2190, 0), (0x23AF, 1), (0x2192, 0))), # LONG LEFT RIGHT ARROW

    (0x294E, False, None, ((0x21BC, 0), (0x23AF, 1), (0x21C0, 0))), # LEFT BARB UP RIGHT BARB UP HARPOON
    (0x2950, False, None, ((0x21BD, 0), (0x23AF, 1), (0x21C1, 0))), # LEFT BARB DOWN RIGHT BARB DOWN HARPOON
]

def warnMissingGlyph(aCodePoint):
    if aCodePoint < 0x7F:
        print("Missing glyph for ASCII character '%s' (U+%02X)!" %
              (chr(aCodePoint), aCodePoint), file=sys.stderr)
    else:
        print("Missing glyph for Unicode character U+%06X!" %
              aCodePoint, file=sys.stderr)

def main(aFontFile):

    # Open the font
    print("Opening file %s... " % aFontFile, end="")
    try:
        font = fontforge.open(aFontFile)
    except EnvironmentError:
        print("Failed!")
        exit(1)
    print("OK")

    tolerance = font.em / 50

    # Ensure that the font has glyphs for all the ASCII characters.
    print("Testing Basic Latin Unicode Block... ", end="")
    for u in range(0x20, 0x7F):
        if u not in font:
            print("Failed")
            warnMissingGlyph(u)
            exit(1)
    print("OK")

    # Ensure that the MathConstants table exists.
    print("Testing MathConstants table... ", end="")
    if not font.math.exists():
        print("Not found!")
        print("Creating a new MathConstants table... OK")
        # Dummy read operation to force the creation of the table.
        font.math.ScriptPercentScaleDown
    else:
        print("OK")

    # ScriptPercentScaleDown
    # Suggested value: 80%

    # ScriptScriptPercentScaleDown
    # Suggested value: 60%

    # DelimitedSubFormulaMinHeight
    # Suggested value: normal line height x 1.5

    # DisplayOperatorMinHeight
    # MathLeading

    # AxisHeight
    # Note: FontForge defaults to zero.
    # See https://github.com/fontforge/fontforge/pull/2242
    plusBoundingBox = font[0x2B].boundingBox()
    suggestedValue = (plusBoundingBox[1] + plusBoundingBox[3]) / 2
    print("Testing AxisHeight... ", end="")
    if font.math.AxisHeight == 0:
        print("Failed")
        print("Error: AxisHeight is set to 0!", file=sys.stderr)
        print("Setting AxisHeight to %d." % suggestedValue)
        font.math.AxisHeight = suggestedValue
    else:
        print("OK")
        if (abs(font.math.AxisHeight - suggestedValue) > tolerance):
            print("Warning: AxisHeight is set to %d while the center of the\
plus sign is %d." % (font.math.AxisHeight, suggestedValue),
                  file=sys.stderr)

    # AccentBaseHeight
    # FlattenedAccentBaseHeight
    # SubscriptShiftDown
    # SubscriptTopMax
    # SubscriptBaselineDropMin
    # SuperscriptShiftUp
    # SuperscriptShiftUpCramped
    # SuperscriptBottomMin
    # SuperscriptBaselineDropMax
    # SubSuperscriptGapMin
    # SuperscriptBottomMaxWithSubscript
    # SpaceAfterScript
    # UpperLimitGapMin
    # UpperLimitBaselineRiseMin
    # LowerLimitGapMin
    # LowerLimitBaselineDropMin
    # StackTopShiftUp
    # StackTopDisplayStyleShiftUp
    # StackBottomShiftDown
    # StackBottomDisplayStyleShiftDown
    # StackGapMin
    # StackDisplayStyleGapMin
    # StretchStackTopShiftUp
    # StretchStackBottomShiftDown
    # StretchStackGapAboveMin
    # StretchStackGapBelowMin
    # FractionNumeratorShiftUp
    # FractionNumeratorDisplayStyleShiftUp
    # FractionDenominatorShiftDown
    # FractionDenominatorDisplayShiftDown
    # FractionNumeratorGapMin
    # FractionNumDisplayStyleGapMin

    # FractionRuleThickness
    # Suggested value: default rule thickness
    print("Testing FractionRuleThickness... ", end="")
    if font.math.FractionRuleThickness == 0:
        print("Failed")
        print("Error: FractionRuleThickness is set to 0!", file=sys.stderr)
        print("Setting FractionRuleThickness to %d." % font.uwidth)
        font.math.FractionRuleThickness = font.uwidth
    else:
        print("OK")

    # FractionDenominatorGapMin
    # FractionDenomDisplayStyleGapMin
    # SkewedFractionHorizontalGap
    # SkewedFractionVerticalGap
    # OverbarVerticalGap

    # OverbarRuleThickness
    # Suggested value: default rule thickness
    print("Testing OverbarRuleThickness... ", end="")
    if font.math.OverbarRuleThickness == 0:
        print("Failed")
        print("Error: OverbarRuleThickness is set to 0!", file=sys.stderr)
        print("Setting OverBarRuleThickness to %d." % font.uwidth)
        font.math.OverbarRuleThickness = font.uwidth
    else:
        print("OK")

    # OverbarExtraAscender
    # UnderbarVerticalGap

    # UnderbarRuleThickness
    print("Testing UnderbarRuleThickness... ", end="")
    if font.math.UnderbarRuleThickness == 0:
        print("Failed")
        print("Error: UnderbarRuleThickness is set to 0!", file=sys.stderr)
        print("Setting OverBarRuleThickness to %d." % font.uwidth)
        font.math.UnderbarRuleThickness = font.uwidth
    else:
        print("OK")

    # UnderbarExtraDescender
    # RadicalVerticalGap

    # RadicalDisplayStyleVerticalGap
    # Suggested value: default rule thickness + 1/4 x-height
    # Note: FontForge defaults to zero.
    # See https://github.com/fontforge/fontforge/pull/2224
    print("Testing RadicalDisplayStyleVerticalGap... ", end="")
    suggestedValue = font.uwidth + font.xHeight / 4
    if font.math.RadicalDisplayStyleVerticalGap == 0:
        print("Failed")
        print("Error: RadicalDisplayStyleVerticalGap is set to 0!", file=sys.stderr)
        print("Setting RadicalDisplayStyleVerticalGap to %d." % suggestedValue)
        font.math.RadicalDisplayStyleVerticalGap = suggestedValue
    else:
        print("OK")

    # RadicalRuleThickness
    # Suggested value: default rule thickness
    # Note: FontForge defaults to zero.
    # See https://github.com/fontforge/fontforge/pull/2224
    print("Testing RadicalRuleThickness... ", end="")
    if font.math.RadicalRuleThickness == 0:
        print("Failed")
        print("Error: RadicalRuleThickness is set to 0!", file=sys.stderr)
        print("Setting RadicalRuleThickness to %d." % font.uwidth)
        font.math.RadicalRuleThickness = font.uwidth
    else:
        print("OK")

    # RadicalExtraAscender
    # RadicalKernBeforeDegree
    # RadicalKernAfterDegree
    # RadicalDegreeBottomRaisePercent

    # Verify that we have MathVariant table for the possible Unicode
    # Constructions.
    print("Testing MathVariant table for Unicode Constructions...")
    for c in kUnicodeConstructions:

        codePoint = c[0]
        isVertical = c[1]
        variants = c[2]
        parts = c[3]
        if variants is None and parts is None:
            raise("no data provided for glyph U+%04X" % codePoint)
            continue

        # Verify whether the character is present.
        print("Testing base glyph for U+%04X... " % codePoint, end="")
        if codePoint not in font:
            print("Failed")
            warnMissingGlyph(codePoint)
            continue
        print("OK")
        glyph = font[codePoint]

        # Verify whether the variants are available.
        if variants is not None:
            print("Testing variants for U+%04X... " % codePoint, end="")
            v = None
            if isVertical:
                v = glyph.verticalVariants
            else:
                v = glyph.horizontalVariants
            if v is not None:
                print("OK")
            else:
                print("Failed")
                print("Warning: missing variants for operator U+%04X!"
                      % codePoint, file=sys.stderr)
                print("Setting variants for operator U+%04X... " % codePoint,
                      end="")
                # FIXME: Is it really necessary to specify the base glyph?
                # This is done in Latin Modern but not XITS.
                v = "%s " % font[codePoint].glyphname
                allGlyphsAvailable = True
                for u in variants:
                    if u not in font:
                        warnMissingGlyph(u)
                        allGlyphsAvailable = False
                        break
                    v += "%s " % font[u].glyphname
                if not allGlyphsAvailable:
                    print("Failed")
                else:
                    # Set the variants
                    if isVertical:
                        glyph.verticalVariants = v
                    else:
                        glyph.horizontalVariants = v
                    print("OK")

        # Verify whether the components are available.
        if parts is not None:
            print("Testing components for U+%04X... " % codePoint, end="")
            components = None
            if isVertical:
                components = glyph.verticalComponents
            else:
                components = glyph.horizontalComponents
            if components:
                print("OK")
            else:
                print("Failed")
                print("Warning: missing components for operator U+%04X!"
                      % codePoint, file=sys.stderr)
                print("Setting components for operator U+%04X... " % codePoint,
                      end="")

                # Verify that all parts are available
                allGlyphsAvailable = True
                components = []
                overlap = font.math.MinConnectorOverlap
                i = 0
                for p in parts:
                    if p[0] not in font:
                        warnMissingGlyph(p[0])
                        allGlyphsAvailable = False
                        break
                    if i == 0:
                        startConnectorLength = 0
                    else:
                        startConnectorLength = overlap
                    if i == len(parts) - 1:
                        endConnectorLength = 0
                    else:
                        endConnectorLength = overlap
                    boundingBox = font[p[0]].boundingBox()
                    if isVertical:
                        fullAdvance = int(boundingBox[3] - boundingBox[1])
                    else:
                        fullAdvance = int(boundingBox[2] - boundingBox[0])
                    components.append(
                        (font[p[0]].glyphname, p[1],
                         startConnectorLength, endConnectorLength, fullAdvance))
                    i = i + 1

                if not allGlyphsAvailable:
                    print("Failed")
                else:
                    # Set the components.
                    # Note: this makes FontForge crash.
                    # See https://github.com/fontforge/fontforge/pull/2225
                    components = tuple(components)
                    if isVertical:
                        glyph.verticalComponents = components
                    else:
                        glyph.horizontalComponents = components
                    print("OK")

    font.save("%s.out.sfd" % aFontFile)
    font.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        exit(1)
    main(sys.argv[1])
