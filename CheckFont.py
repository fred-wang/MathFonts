# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function
from datetime import datetime
from math import sqrt
import fontforge
import psMat
import sys
import argparse

# List op "largeop" operators. See http://www.w3.org/TR/MathML3/appendixc.html
kLargeOperators = [0x220F, 0x2210, 0x2211, 0x222B, 0x222C, 0x222D, 0x222E,
                   0x222F, 0x2230, 0x2231, 0x2232, 0x2233, 0x22C0, 0x22C1,
                   0x22C2, 0x22C3, 0x2A00, 0x2A01, 0x2A02, 0x2A03, 0x2A04,
                   0x2A05, 0x2A06, 0x2A07, 0x2A08, 0x2A09, 0x2A0A, 0x2A0B,
                   0x2A0C, 0x2A0D, 0x2A0E, 0x2A0F, 0x2A10, 0x2A11, 0x2A12,
                   0x2A13, 0x2A14, 0x2A15, 0x2A16, 0x2A17, 0x2A18, 0x2A19,
                   0x2A1A, 0x2A1B, 0x2A1C, 0x2AFC, 0x2AFF]
kLargeOpMinDisplayOperatorFactor = 1.3
kLargeOpDisplayOperatorFactor = sqrt(2)
kLargeOpIntegrals = [0x222B, 0x222C, 0x222D, 0x222E, 0x222F, 0x2230, 0x2231,
                     0x2232, 0x2233, 0x2A0B, 0x2A0C, 0x2A0D, 0x2A0E, 0x2A0F,
                     0x2A10, 0x2A11, 0x2A12, 0x2A13, 0x2A14, 0x2A15, 0x2A16,
                     0x2A17, 0x2A18, 0x2A19, 0x2A1A, 0x2A1B, 0x2A1C]

# List of "prescripted" operators.
# See http://www.w3.org/TR/MathML3/appendixc.html
kPreScriptedOperators = [0x2032, 0x2033, 0x2034, 0x2035, 0x2036, 0x2037, 0x2057]

# mapping from math alpha num to BMP
mathvariantToBMP = [
    (0x0210E, 0x0068),
    (0x1D400, 0x0041),
    (0x1D401, 0x0042),
    (0x1D402, 0x0043),
    (0x1D403, 0x0044),
    (0x1D404, 0x0045),
    (0x1D405, 0x0046),
    (0x1D406, 0x0047),
    (0x1D407, 0x0048),
    (0x1D408, 0x0049),
    (0x1D409, 0x004A),
    (0x1D40A, 0x004B),
    (0x1D40B, 0x004C),
    (0x1D40C, 0x004D),
    (0x1D40D, 0x004E),
    (0x1D40E, 0x004F),
    (0x1D40F, 0x0050),
    (0x1D410, 0x0051),
    (0x1D411, 0x0052),
    (0x1D412, 0x0053),
    (0x1D413, 0x0054),
    (0x1D414, 0x0055),
    (0x1D415, 0x0056),
    (0x1D416, 0x0057),
    (0x1D417, 0x0058),
    (0x1D418, 0x0059),
    (0x1D419, 0x005A),
    (0x1D41A, 0x0061),
    (0x1D41B, 0x0062),
    (0x1D41C, 0x0063),
    (0x1D41D, 0x0064),
    (0x1D41E, 0x0065),
    (0x1D41F, 0x0066),
    (0x1D420, 0x0067),
    (0x1D421, 0x0068),
    (0x1D422, 0x0069),
    (0x1D423, 0x006A),
    (0x1D424, 0x006B),
    (0x1D425, 0x006C),
    (0x1D426, 0x006D),
    (0x1D427, 0x006E),
    (0x1D428, 0x006F),
    (0x1D429, 0x0070),
    (0x1D42A, 0x0071),
    (0x1D42B, 0x0072),
    (0x1D42C, 0x0073),
    (0x1D42D, 0x0074),
    (0x1D42E, 0x0075),
    (0x1D42F, 0x0076),
    (0x1D430, 0x0077),
    (0x1D431, 0x0078),
    (0x1D432, 0x0079),
    (0x1D433, 0x007A),
    (0x1D434, 0x0041),
    (0x1D435, 0x0042),
    (0x1D436, 0x0043),
    (0x1D437, 0x0044),
    (0x1D438, 0x0045),
    (0x1D439, 0x0046),
    (0x1D43A, 0x0047),
    (0x1D43B, 0x0048),
    (0x1D43C, 0x0049),
    (0x1D43D, 0x004A),
    (0x1D43E, 0x004B),
    (0x1D43F, 0x004C),
    (0x1D440, 0x004D),
    (0x1D441, 0x004E),
    (0x1D442, 0x004F),
    (0x1D443, 0x0050),
    (0x1D444, 0x0051),
    (0x1D445, 0x0052),
    (0x1D446, 0x0053),
    (0x1D447, 0x0054),
    (0x1D448, 0x0055),
    (0x1D449, 0x0056),
    (0x1D44A, 0x0057),
    (0x1D44B, 0x0058),
    (0x1D44C, 0x0059),
    (0x1D44D, 0x005A),
    (0x1D44E, 0x0061),
    (0x1D44F, 0x0062),
    (0x1D450, 0x0063),
    (0x1D451, 0x0064),
    (0x1D452, 0x0065),
    (0x1D453, 0x0066),
    (0x1D454, 0x0067),
    (0x1D456, 0x0069),
    (0x1D457, 0x006A),
    (0x1D458, 0x006B),
    (0x1D459, 0x006C),
    (0x1D45A, 0x006D),
    (0x1D45B, 0x006E),
    (0x1D45C, 0x006F),
    (0x1D45D, 0x0070),
    (0x1D45E, 0x0071),
    (0x1D45F, 0x0072),
    (0x1D460, 0x0073),
    (0x1D461, 0x0074),
    (0x1D462, 0x0075),
    (0x1D463, 0x0076),
    (0x1D464, 0x0077),
    (0x1D465, 0x0078),
    (0x1D466, 0x0079),
    (0x1D467, 0x007A),
    (0x1D468, 0x0041),
    (0x1D469, 0x0042),
    (0x1D46A, 0x0043),
    (0x1D46B, 0x0044),
    (0x1D46C, 0x0045),
    (0x1D46D, 0x0046),
    (0x1D46E, 0x0047),
    (0x1D46F, 0x0048),
    (0x1D470, 0x0049),
    (0x1D471, 0x004A),
    (0x1D472, 0x004B),
    (0x1D473, 0x004C),
    (0x1D474, 0x004D),
    (0x1D475, 0x004E),
    (0x1D476, 0x004F),
    (0x1D477, 0x0050),
    (0x1D478, 0x0051),
    (0x1D479, 0x0052),
    (0x1D47A, 0x0053),
    (0x1D47B, 0x0054),
    (0x1D47C, 0x0055),
    (0x1D47D, 0x0056),
    (0x1D47E, 0x0057),
    (0x1D47F, 0x0058),
    (0x1D480, 0x0059),
    (0x1D481, 0x005A),
    (0x1D482, 0x0061),
    (0x1D483, 0x0062),
    (0x1D484, 0x0063),
    (0x1D485, 0x0064),
    (0x1D486, 0x0065),
    (0x1D487, 0x0066),
    (0x1D488, 0x0067),
    (0x1D489, 0x0068),
    (0x1D48A, 0x0069),
    (0x1D48B, 0x006A),
    (0x1D48C, 0x006B),
    (0x1D48D, 0x006C),
    (0x1D48E, 0x006D),
    (0x1D48F, 0x006E),
    (0x1D490, 0x006F),
    (0x1D491, 0x0070),
    (0x1D492, 0x0071),
    (0x1D493, 0x0072),
    (0x1D494, 0x0073),
    (0x1D495, 0x0074),
    (0x1D496, 0x0075),
    (0x1D497, 0x0076),
    (0x1D498, 0x0077),
    (0x1D499, 0x0078),
    (0x1D49A, 0x0079),
    (0x1D49B, 0x007A),
    (0x1D5A0, 0x0041),
    (0x1D5A1, 0x0042),
    (0x1D5A2, 0x0043),
    (0x1D5A3, 0x0044),
    (0x1D5A4, 0x0045),
    (0x1D5A5, 0x0046),
    (0x1D5A6, 0x0047),
    (0x1D5A7, 0x0048),
    (0x1D5A8, 0x0049),
    (0x1D5A9, 0x004A),
    (0x1D5AA, 0x004B),
    (0x1D5AB, 0x004C),
    (0x1D5AC, 0x004D),
    (0x1D5AD, 0x004E),
    (0x1D5AE, 0x004F),
    (0x1D5AF, 0x0050),
    (0x1D5B0, 0x0051),
    (0x1D5B1, 0x0052),
    (0x1D5B2, 0x0053),
    (0x1D5B3, 0x0054),
    (0x1D5B4, 0x0055),
    (0x1D5B5, 0x0056),
    (0x1D5B6, 0x0057),
    (0x1D5B7, 0x0058),
    (0x1D5B8, 0x0059),
    (0x1D5B9, 0x005A),
    (0x1D5BA, 0x0061),
    (0x1D5BB, 0x0062),
    (0x1D5BC, 0x0063),
    (0x1D5BD, 0x0064),
    (0x1D5BE, 0x0065),
    (0x1D5BF, 0x0066),
    (0x1D5C0, 0x0067),
    (0x1D5C1, 0x0068),
    (0x1D5C2, 0x0069),
    (0x1D5C3, 0x006A),
    (0x1D5C4, 0x006B),
    (0x1D5C5, 0x006C),
    (0x1D5C6, 0x006D),
    (0x1D5C7, 0x006E),
    (0x1D5C8, 0x006F),
    (0x1D5C9, 0x0070),
    (0x1D5CA, 0x0071),
    (0x1D5CB, 0x0072),
    (0x1D5CC, 0x0073),
    (0x1D5CD, 0x0074),
    (0x1D5CE, 0x0075),
    (0x1D5CF, 0x0076),
    (0x1D5D0, 0x0077),
    (0x1D5D1, 0x0078),
    (0x1D5D2, 0x0079),
    (0x1D5D3, 0x007A),
    (0x1D5D4, 0x0041),
    (0x1D5D5, 0x0042),
    (0x1D5D6, 0x0043),
    (0x1D5D7, 0x0044),
    (0x1D5D8, 0x0045),
    (0x1D5D9, 0x0046),
    (0x1D5DA, 0x0047),
    (0x1D5DB, 0x0048),
    (0x1D5DC, 0x0049),
    (0x1D5DD, 0x004A),
    (0x1D5DE, 0x004B),
    (0x1D5DF, 0x004C),
    (0x1D5E0, 0x004D),
    (0x1D5E1, 0x004E),
    (0x1D5E2, 0x004F),
    (0x1D5E3, 0x0050),
    (0x1D5E4, 0x0051),
    (0x1D5E5, 0x0052),
    (0x1D5E6, 0x0053),
    (0x1D5E7, 0x0054),
    (0x1D5E8, 0x0055),
    (0x1D5E9, 0x0056),
    (0x1D5EA, 0x0057),
    (0x1D5EB, 0x0058),
    (0x1D5EC, 0x0059),
    (0x1D5ED, 0x005A),
    (0x1D5EE, 0x0061),
    (0x1D5EF, 0x0062),
    (0x1D5F0, 0x0063),
    (0x1D5F1, 0x0064),
    (0x1D5F2, 0x0065),
    (0x1D5F3, 0x0066),
    (0x1D5F4, 0x0067),
    (0x1D5F5, 0x0068),
    (0x1D5F6, 0x0069),
    (0x1D5F7, 0x006A),
    (0x1D5F8, 0x006B),
    (0x1D5F9, 0x006C),
    (0x1D5FA, 0x006D),
    (0x1D5FB, 0x006E),
    (0x1D5FC, 0x006F),
    (0x1D5FD, 0x0070),
    (0x1D5FE, 0x0071),
    (0x1D5FF, 0x0072),
    (0x1D600, 0x0073),
    (0x1D601, 0x0074),
    (0x1D602, 0x0075),
    (0x1D603, 0x0076),
    (0x1D604, 0x0077),
    (0x1D605, 0x0078),
    (0x1D606, 0x0079),
    (0x1D607, 0x007A),
    (0x1D608, 0x0041),
    (0x1D609, 0x0042),
    (0x1D60A, 0x0043),
    (0x1D60B, 0x0044),
    (0x1D60C, 0x0045),
    (0x1D60D, 0x0046),
    (0x1D60E, 0x0047),
    (0x1D60F, 0x0048),
    (0x1D610, 0x0049),
    (0x1D611, 0x004A),
    (0x1D612, 0x004B),
    (0x1D613, 0x004C),
    (0x1D614, 0x004D),
    (0x1D615, 0x004E),
    (0x1D616, 0x004F),
    (0x1D617, 0x0050),
    (0x1D618, 0x0051),
    (0x1D619, 0x0052),
    (0x1D61A, 0x0053),
    (0x1D61B, 0x0054),
    (0x1D61C, 0x0055),
    (0x1D61D, 0x0056),
    (0x1D61E, 0x0057),
    (0x1D61F, 0x0058),
    (0x1D620, 0x0059),
    (0x1D621, 0x005A),
    (0x1D622, 0x0061),
    (0x1D623, 0x0062),
    (0x1D624, 0x0063),
    (0x1D625, 0x0064),
    (0x1D626, 0x0065),
    (0x1D627, 0x0066),
    (0x1D628, 0x0067),
    (0x1D629, 0x0068),
    (0x1D62A, 0x0069),
    (0x1D62B, 0x006A),
    (0x1D62C, 0x006B),
    (0x1D62D, 0x006C),
    (0x1D62E, 0x006D),
    (0x1D62F, 0x006E),
    (0x1D630, 0x006F),
    (0x1D631, 0x0070),
    (0x1D632, 0x0071),
    (0x1D633, 0x0072),
    (0x1D634, 0x0073),
    (0x1D635, 0x0074),
    (0x1D636, 0x0075),
    (0x1D637, 0x0076),
    (0x1D638, 0x0077),
    (0x1D639, 0x0078),
    (0x1D63A, 0x0079),
    (0x1D63B, 0x007A),
    (0x1D63C, 0x0041),
    (0x1D63D, 0x0042),
    (0x1D63E, 0x0043),
    (0x1D63F, 0x0044),
    (0x1D640, 0x0045),
    (0x1D641, 0x0046),
    (0x1D642, 0x0047),
    (0x1D643, 0x0048),
    (0x1D644, 0x0049),
    (0x1D645, 0x004A),
    (0x1D646, 0x004B),
    (0x1D647, 0x004C),
    (0x1D648, 0x004D),
    (0x1D649, 0x004E),
    (0x1D64A, 0x004F),
    (0x1D64B, 0x0050),
    (0x1D64C, 0x0051),
    (0x1D64D, 0x0052),
    (0x1D64E, 0x0053),
    (0x1D64F, 0x0054),
    (0x1D650, 0x0055),
    (0x1D651, 0x0056),
    (0x1D652, 0x0057),
    (0x1D653, 0x0058),
    (0x1D654, 0x0059),
    (0x1D655, 0x005A),
    (0x1D656, 0x0061),
    (0x1D657, 0x0062),
    (0x1D658, 0x0063),
    (0x1D659, 0x0064),
    (0x1D65A, 0x0065),
    (0x1D65B, 0x0066),
    (0x1D65C, 0x0067),
    (0x1D65D, 0x0068),
    (0x1D65E, 0x0069),
    (0x1D65F, 0x006A),
    (0x1D660, 0x006B),
    (0x1D661, 0x006C),
    (0x1D662, 0x006D),
    (0x1D663, 0x006E),
    (0x1D664, 0x006F),
    (0x1D665, 0x0070),
    (0x1D666, 0x0071),
    (0x1D667, 0x0072),
    (0x1D668, 0x0073),
    (0x1D669, 0x0074),
    (0x1D66A, 0x0075),
    (0x1D66B, 0x0076),
    (0x1D66C, 0x0077),
    (0x1D66D, 0x0078),
    (0x1D66E, 0x0079),
    (0x1D66F, 0x007A),
    (0x1D670, 0x0041),
    (0x1D671, 0x0042),
    (0x1D672, 0x0043),
    (0x1D673, 0x0044),
    (0x1D674, 0x0045),
    (0x1D675, 0x0046),
    (0x1D676, 0x0047),
    (0x1D677, 0x0048),
    (0x1D678, 0x0049),
    (0x1D679, 0x004A),
    (0x1D67A, 0x004B),
    (0x1D67B, 0x004C),
    (0x1D67C, 0x004D),
    (0x1D67D, 0x004E),
    (0x1D67E, 0x004F),
    (0x1D67F, 0x0050),
    (0x1D680, 0x0051),
    (0x1D681, 0x0052),
    (0x1D682, 0x0053),
    (0x1D683, 0x0054),
    (0x1D684, 0x0055),
    (0x1D685, 0x0056),
    (0x1D686, 0x0057),
    (0x1D687, 0x0058),
    (0x1D688, 0x0059),
    (0x1D689, 0x005A),
    (0x1D68A, 0x0061),
    (0x1D68B, 0x0062),
    (0x1D68C, 0x0063),
    (0x1D68D, 0x0064),
    (0x1D68E, 0x0065),
    (0x1D68F, 0x0066),
    (0x1D690, 0x0067),
    (0x1D691, 0x0068),
    (0x1D692, 0x0069),
    (0x1D693, 0x006A),
    (0x1D694, 0x006B),
    (0x1D695, 0x006C),
    (0x1D696, 0x006D),
    (0x1D697, 0x006E),
    (0x1D698, 0x006F),
    (0x1D699, 0x0070),
    (0x1D69A, 0x0071),
    (0x1D69B, 0x0072),
    (0x1D69C, 0x0073),
    (0x1D69D, 0x0074),
    (0x1D69E, 0x0075),
    (0x1D69F, 0x0076),
    (0x1D6A0, 0x0077),
    (0x1D6A1, 0x0078),
    (0x1D6A2, 0x0079),
    (0x1D6A3, 0x007A),
    (0x1D6A4, 0x0131),
    (0x1D6A5, 0x0237),
    (0x1D6A8, 0x0391),
    (0x1D6A9, 0x0392),
    (0x1D6AA, 0x0393),
    (0x1D6AB, 0x0394),
    (0x1D6AC, 0x0395),
    (0x1D6AD, 0x0396),
    (0x1D6AE, 0x0397),
    (0x1D6AF, 0x0398),
    (0x1D6B0, 0x0399),
    (0x1D6B1, 0x039A),
    (0x1D6B2, 0x039B),
    (0x1D6B3, 0x039C),
    (0x1D6B4, 0x039D),
    (0x1D6B5, 0x039E),
    (0x1D6B6, 0x039F),
    (0x1D6B7, 0x03A0),
    (0x1D6B8, 0x03A1),
    (0x1D6B9, 0x03F4),
    (0x1D6BA, 0x03A3),
    (0x1D6BB, 0x03A4),
    (0x1D6BC, 0x03A5),
    (0x1D6BD, 0x03A6),
    (0x1D6BE, 0x03A7),
    (0x1D6BF, 0x03A8),
    (0x1D6C0, 0x03A9),
    (0x1D6C1, 0x2207),
    (0x1D6C2, 0x03B1),
    (0x1D6C3, 0x03B2),
    (0x1D6C4, 0x03B3),
    (0x1D6C5, 0x03B4),
    (0x1D6C6, 0x03B5),
    (0x1D6C7, 0x03B6),
    (0x1D6C8, 0x03B7),
    (0x1D6C9, 0x03B8),
    (0x1D6CA, 0x03B9),
    (0x1D6CB, 0x03BA),
    (0x1D6CC, 0x03BB),
    (0x1D6CD, 0x03BC),
    (0x1D6CE, 0x03BD),
    (0x1D6CF, 0x03BE),
    (0x1D6D0, 0x03BF),
    (0x1D6D1, 0x03C0),
    (0x1D6D2, 0x03C1),
    (0x1D6D3, 0x03C2),
    (0x1D6D4, 0x03C3),
    (0x1D6D5, 0x03C4),
    (0x1D6D6, 0x03C5),
    (0x1D6D7, 0x03C6),
    (0x1D6D8, 0x03C7),
    (0x1D6D9, 0x03C8),
    (0x1D6DA, 0x03C9),
    (0x1D6DB, 0x2202),
    (0x1D6DC, 0x03F5),
    (0x1D6DD, 0x03D1),
    (0x1D6DE, 0x03F0),
    (0x1D6DF, 0x03D5),
    (0x1D6E0, 0x03F1),
    (0x1D6E1, 0x03D6),
    (0x1D6E2, 0x0391),
    (0x1D6E3, 0x0392),
    (0x1D6E4, 0x0393),
    (0x1D6E5, 0x0394),
    (0x1D6E6, 0x0395),
    (0x1D6E7, 0x0396),
    (0x1D6E8, 0x0397),
    (0x1D6E9, 0x0398),
    (0x1D6EA, 0x0399),
    (0x1D6EB, 0x039A),
    (0x1D6EC, 0x039B),
    (0x1D6ED, 0x039C),
    (0x1D6EE, 0x039D),
    (0x1D6EF, 0x039E),
    (0x1D6F0, 0x039F),
    (0x1D6F1, 0x03A0),
    (0x1D6F2, 0x03A1),
    (0x1D6F3, 0x03F4),
    (0x1D6F4, 0x03A3),
    (0x1D6F5, 0x03A4),
    (0x1D6F6, 0x03A5),
    (0x1D6F7, 0x03A6),
    (0x1D6F8, 0x03A7),
    (0x1D6F9, 0x03A8),
    (0x1D6FA, 0x03A9),
    (0x1D6FB, 0x2207),
    (0x1D6FC, 0x03B1),
    (0x1D6FD, 0x03B2),
    (0x1D6FE, 0x03B3),
    (0x1D6FF, 0x03B4),
    (0x1D700, 0x03B5),
    (0x1D701, 0x03B6),
    (0x1D702, 0x03B7),
    (0x1D703, 0x03B8),
    (0x1D704, 0x03B9),
    (0x1D705, 0x03BA),
    (0x1D706, 0x03BB),
    (0x1D707, 0x03BC),
    (0x1D708, 0x03BD),
    (0x1D709, 0x03BE),
    (0x1D70A, 0x03BF),
    (0x1D70B, 0x03C0),
    (0x1D70C, 0x03C1),
    (0x1D70D, 0x03C2),
    (0x1D70E, 0x03C3),
    (0x1D70F, 0x03C4),
    (0x1D710, 0x03C5),
    (0x1D711, 0x03C6),
    (0x1D712, 0x03C7),
    (0x1D713, 0x03C8),
    (0x1D714, 0x03C9),
    (0x1D715, 0x2202),
    (0x1D716, 0x03F5),
    (0x1D717, 0x03D1),
    (0x1D718, 0x03F0),
    (0x1D719, 0x03D5),
    (0x1D71A, 0x03F1),
    (0x1D71B, 0x03D6),
    (0x1D71C, 0x0391),
    (0x1D71D, 0x0392),
    (0x1D71E, 0x0393),
    (0x1D71F, 0x0394),
    (0x1D720, 0x0395),
    (0x1D721, 0x0396),
    (0x1D722, 0x0397),
    (0x1D723, 0x0398),
    (0x1D724, 0x0399),
    (0x1D725, 0x039A),
    (0x1D726, 0x039B),
    (0x1D727, 0x039C),
    (0x1D728, 0x039D),
    (0x1D729, 0x039E),
    (0x1D72A, 0x039F),
    (0x1D72B, 0x03A0),
    (0x1D72C, 0x03A1),
    (0x1D72D, 0x03F4),
    (0x1D72E, 0x03A3),
    (0x1D72F, 0x03A4),
    (0x1D730, 0x03A5),
    (0x1D731, 0x03A6),
    (0x1D732, 0x03A7),
    (0x1D733, 0x03A8),
    (0x1D734, 0x03A9),
    (0x1D735, 0x2207),
    (0x1D736, 0x03B1),
    (0x1D737, 0x03B2),
    (0x1D738, 0x03B3),
    (0x1D739, 0x03B4),
    (0x1D73A, 0x03B5),
    (0x1D73B, 0x03B6),
    (0x1D73C, 0x03B7),
    (0x1D73D, 0x03B8),
    (0x1D73E, 0x03B9),
    (0x1D73F, 0x03BA),
    (0x1D740, 0x03BB),
    (0x1D741, 0x03BC),
    (0x1D742, 0x03BD),
    (0x1D743, 0x03BE),
    (0x1D744, 0x03BF),
    (0x1D745, 0x03C0),
    (0x1D746, 0x03C1),
    (0x1D747, 0x03C2),
    (0x1D748, 0x03C3),
    (0x1D749, 0x03C4),
    (0x1D74A, 0x03C5),
    (0x1D74B, 0x03C6),
    (0x1D74C, 0x03C7),
    (0x1D74D, 0x03C8),
    (0x1D74E, 0x03C9),
    (0x1D74F, 0x2202),
    (0x1D750, 0x03F5),
    (0x1D751, 0x03D1),
    (0x1D752, 0x03F0),
    (0x1D753, 0x03D5),
    (0x1D754, 0x03F1),
    (0x1D755, 0x03D6),
    (0x1D756, 0x0391),
    (0x1D757, 0x0392),
    (0x1D758, 0x0393),
    (0x1D759, 0x0394),
    (0x1D75A, 0x0395),
    (0x1D75B, 0x0396),
    (0x1D75C, 0x0397),
    (0x1D75D, 0x0398),
    (0x1D75E, 0x0399),
    (0x1D75F, 0x039A),
    (0x1D760, 0x039B),
    (0x1D761, 0x039C),
    (0x1D762, 0x039D),
    (0x1D763, 0x039E),
    (0x1D764, 0x039F),
    (0x1D765, 0x03A0),
    (0x1D766, 0x03A1),
    (0x1D767, 0x03F4),
    (0x1D768, 0x03A3),
    (0x1D769, 0x03A4),
    (0x1D76A, 0x03A5),
    (0x1D76B, 0x03A6),
    (0x1D76C, 0x03A7),
    (0x1D76D, 0x03A8),
    (0x1D76E, 0x03A9),
    (0x1D76F, 0x2207),
    (0x1D770, 0x03B1),
    (0x1D771, 0x03B2),
    (0x1D772, 0x03B3),
    (0x1D773, 0x03B4),
    (0x1D774, 0x03B5),
    (0x1D775, 0x03B6),
    (0x1D776, 0x03B7),
    (0x1D777, 0x03B8),
    (0x1D778, 0x03B9),
    (0x1D779, 0x03BA),
    (0x1D77A, 0x03BB),
    (0x1D77B, 0x03BC),
    (0x1D77C, 0x03BD),
    (0x1D77D, 0x03BE),
    (0x1D77E, 0x03BF),
    (0x1D77F, 0x03C0),
    (0x1D780, 0x03C1),
    (0x1D781, 0x03C2),
    (0x1D782, 0x03C3),
    (0x1D783, 0x03C4),
    (0x1D784, 0x03C5),
    (0x1D785, 0x03C6),
    (0x1D786, 0x03C7),
    (0x1D787, 0x03C8),
    (0x1D788, 0x03C9),
    (0x1D789, 0x2202),
    (0x1D78A, 0x03F5),
    (0x1D78B, 0x03D1),
    (0x1D78C, 0x03F0),
    (0x1D78D, 0x03D5),
    (0x1D78E, 0x03F1),
    (0x1D78F, 0x03D6),
    (0x1D790, 0x0391),
    (0x1D791, 0x0392),
    (0x1D792, 0x0393),
    (0x1D793, 0x0394),
    (0x1D794, 0x0395),
    (0x1D795, 0x0396),
    (0x1D796, 0x0397),
    (0x1D797, 0x0398),
    (0x1D798, 0x0399),
    (0x1D799, 0x039A),
    (0x1D79A, 0x039B),
    (0x1D79B, 0x039C),
    (0x1D79C, 0x039D),
    (0x1D79D, 0x039E),
    (0x1D79E, 0x039F),
    (0x1D79F, 0x03A0),
    (0x1D7A0, 0x03A1),
    (0x1D7A1, 0x03F4),
    (0x1D7A2, 0x03A3),
    (0x1D7A3, 0x03A4),
    (0x1D7A4, 0x03A5),
    (0x1D7A5, 0x03A6),
    (0x1D7A6, 0x03A7),
    (0x1D7A7, 0x03A8),
    (0x1D7A8, 0x03A9),
    (0x1D7A9, 0x2207),
    (0x1D7AA, 0x03B1),
    (0x1D7AB, 0x03B2),
    (0x1D7AC, 0x03B3),
    (0x1D7AD, 0x03B4),
    (0x1D7AE, 0x03B5),
    (0x1D7AF, 0x03B6),
    (0x1D7B0, 0x03B7),
    (0x1D7B1, 0x03B8),
    (0x1D7B2, 0x03B9),
    (0x1D7B3, 0x03BA),
    (0x1D7B4, 0x03BB),
    (0x1D7B5, 0x03BC),
    (0x1D7B6, 0x03BD),
    (0x1D7B7, 0x03BE),
    (0x1D7B8, 0x03BF),
    (0x1D7B9, 0x03C0),
    (0x1D7BA, 0x03C1),
    (0x1D7BB, 0x03C2),
    (0x1D7BC, 0x03C3),
    (0x1D7BD, 0x03C4),
    (0x1D7BE, 0x03C5),
    (0x1D7BF, 0x03C6),
    (0x1D7C0, 0x03C7),
    (0x1D7C1, 0x03C8),
    (0x1D7C2, 0x03C9),
    (0x1D7C3, 0x2202),
    (0x1D7C4, 0x03F5),
    (0x1D7C5, 0x03D1),
    (0x1D7C6, 0x03F0),
    (0x1D7C7, 0x03D5),
    (0x1D7C8, 0x03F1),
    (0x1D7C9, 0x03D6),
    (0x1D7CA, 0x03DC),
    (0x1D7CB, 0x03DD),
    (0x1D7CE, 0x0030),
    (0x1D7CF, 0x0031),
    (0x1D7D0, 0x0032),
    (0x1D7D1, 0x0033),
    (0x1D7D2, 0x0034),
    (0x1D7D3, 0x0035),
    (0x1D7D4, 0x0036),
    (0x1D7D5, 0x0037),
    (0x1D7D6, 0x0038),
    (0x1D7D7, 0x0039),
    (0x1D7E2, 0x0030),
    (0x1D7E3, 0x0031),
    (0x1D7E4, 0x0032),
    (0x1D7E5, 0x0033),
    (0x1D7E6, 0x0034),
    (0x1D7E7, 0x0035),
    (0x1D7E8, 0x0036),
    (0x1D7E9, 0x0037),
    (0x1D7EA, 0x0038),
    (0x1D7EB, 0x0039),
    (0x1D7EC, 0x0030),
    (0x1D7ED, 0x0031),
    (0x1D7EE, 0x0032),
    (0x1D7EF, 0x0033),
    (0x1D7F0, 0x0034),
    (0x1D7F1, 0x0035),
    (0x1D7F2, 0x0036),
    (0x1D7F3, 0x0037),
    (0x1D7F4, 0x0038),
    (0x1D7F5, 0x0039),
    (0x1D7F6, 0x0030),
    (0x1D7F7, 0x0031),
    (0x1D7F8, 0x0032),
    (0x1D7F9, 0x0033),
    (0x1D7FA, 0x0034),
    (0x1D7FB, 0x0035),
    (0x1D7FC, 0x0036),
    (0x1D7FD, 0x0037),
    (0x1D7FE, 0x0038),
    (0x1D7FF, 0x0039)
]

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
        print("Warning: Missing glyph for ASCII character '%s' (U+%02X)!" %
              (chr(aCodePoint), aCodePoint), file=sys.stderr)
    else:
        print("Warning: Missing glyph for Unicode character U+%06X!" %
              aCodePoint, file=sys.stderr)

def testSSTY(aFont, aCodePoint):
    print("Testing ssty for U+%04X... " % aCodePoint, end="")
    for table in aFont[aCodePoint].getPosSub("*"):
        if table[0].find("ssty") > 0:
            print("Done")
            return
    print("Warning: Missing ssty table for prescripted operator U+%02X!" %
          aCodePoint, file=sys.stderr)
    print("Failed")

def testItalicCorrection(aGlyph):
    print("Testing italic correction for glyph '%s'... " % aGlyph.glyphname,
          end="")
    if aGlyph.italicCorrection == fontforge.unspecifiedMathValue:
        print("Failed")
        print("Warning: Missing italic correction for glyph '%s'!" %
              aGlyph.glyphname, file=sys.stderr)
        return
    if not (aGlyph.italicCorrection > 0):
        print("Failed")
        print("Warning: Italic correction for glyph '%s' is not positive!" %
              aGlyph.glyphname, file=sys.stderr)
        return
    print("Done")

def testMathVariants(aFont, aVariantName, aRanges, aFallbackFont=None):
    # Open fallback font file, if specified.
    fallbackFont = None
    if aFallbackFont is not None:
        try:
            fallbackFont = fontforge.open(aFallbackFont)
        except EnvironmentError:
            None

    print("Testing %s mathvariants..." % aVariantName)
    for r in aRanges:
        lower = r[0]
        if len(r) == 2:
            upper = r[1]
        else:
            upper = lower
        for u in range(lower,upper+1):
            print("Testing mathvariant U+%04X... " % u, end="")
            if u not in aFont:
                print("Failed")
                warnMissingGlyph(u)
                if fallbackFont:
                    # binary search in mathvariantToBMP
                    v = 0
                    lo = 0
                    hi = len(mathvariantToBMP)
                    while hi >= lo:
                        mid = (lo+hi)//2
                        if mathvariantToBMP[mid][0] == u:
                            v = mathvariantToBMP[mid][1]
                            break
                        elif mathvariantToBMP[mid][0] < u: lo = mid + 1
                        else: hi = mid - 1
                    if v > 0 and v in fallbackFont:
                        print("Copying U+%04X from fallback font..." % u,
                              end="")
                        fallbackFont.selection.select(v)
                        fallbackFont.copy()
                        aFont.selection.select(u)
                        aFont.paste()
                        print("Done")
            else:
                print("Done")
    print("")

    # close fallback font
    if fallbackFont is not None:
        fallbackFont.close()

def main(aArgs):

    ############################################################################
    # Open the font
    print("Opening file %s... " % aArgs.input, end="")
    try:
        font = fontforge.open(aArgs.input)
    except EnvironmentError:
        print("Failed!")
        exit(1)
    print("Done")
    print("")

    tolerance = font.em / 50

    ############################################################################
    # Ensure that the font has glyphs for all the ASCII characters.
    print("Testing Basic Latin Unicode Block... ")
    for u in range(0x20, 0x7F):
        print("Testing U+%2X... " % u, end="")
        if u not in font:
            print("Failed")
            warnMissingGlyph(u)
        else:
            print("Done")
    print("")

    ############################################################################
    # Test the "use typo metrics" bit
    print("Testing OS/2 version... ", end="")
    if font.os2_version and font.os2_version < 4:
        print("Failed")
        print("Warning: OS/2 version does not support USE_TYPO_METRICS!",
              file=sys.stderr)
    else:
        print("Done")

    print("Testing USE_TYPO_METRICS... ", end="")
    if not font.os2_use_typo_metrics:
        print("Failed")
        print("Warning: USE_TYPO_METRICS set to false in the OS/2 table!",
              file=sys.stderr)
    else:
        print("Done")
    print("")

    ############################################################################
    # Ensure that the MathConstants table exists.
    print("Testing MathConstants table... ", end="")
    if not font.math.exists():
        print("Not found!")
        print("Creating a new MathConstants table... Done")
        # Dummy read operation to force the creation of the table.
        font.math.ScriptPercentScaleDown
    else:
        print("Done")
    print("")

    # ScriptPercentScaleDown
    # Suggested value: 80%

    # ScriptScriptPercentScaleDown
    # Suggested value: 60%

    # DelimitedSubFormulaMinHeight
    # Suggested value: normal line height x 1.5

    # DisplayOperatorMinHeight
    print("Testing DisplayOperatorMinHeight... ")
    if font.math.DisplayOperatorMinHeight == 0:
        print("Error: DisplayOperatorMinHeight is set to 0!", file=sys.stderr)
        if 0x4F in font:
            # use the height of the letter 'O'
            box = font[0x4F].boundingBox()
            suggestedValue = (box[3] - box[1]) * \
                             kLargeOpMinDisplayOperatorFactor
            print("Setting DisplayOperatorMinHeight to %d." % suggestedValue)
            font.math.DisplayOperatorMinHeight = suggestedValue
    for c in kLargeOperators:
        # Verify that the DisplayOperatorMinHeight ensure that the size of
        # operator will really be increased in display mode.
        if c not in font:
            continue
        print("Testing large operator U+%04X... " % c, end="")
        glyph = font[c]
        box = glyph.boundingBox()
        baseHeight = box[3] - box[1]
        print("Done")
        if (font.math.DisplayOperatorMinHeight <
            kLargeOpMinDisplayOperatorFactor * baseHeight):
            print("Warning: DisplayOperatorMinHeight is less than %f times the base height of U+%04X." % (kLargeOpMinDisplayOperatorFactor, c),
                  file=sys.stderr)
    print("")

    # MathLeading

    # AxisHeight
    # Note: FontForge defaults to zero.
    # See https://github.com/fontforge/fontforge/pull/2242
    if 0x2B in font:
        plusBoundingBox = font[0x2B].boundingBox()
        suggestedValue = (plusBoundingBox[1] + plusBoundingBox[3]) / 2
    else:
        suggestedValue = 0
    print("Testing AxisHeight... ", end="")
    if font.math.AxisHeight == 0:
        print("Failed")
        print("Error: AxisHeight is set to 0!", file=sys.stderr)
        if suggestedValue > 0:
            print("Setting AxisHeight to %d." % suggestedValue)
            font.math.AxisHeight = suggestedValue
    else:
        print("Done")
        if (suggestedValue > 0 and
            (abs(font.math.AxisHeight - suggestedValue) > tolerance)):
            print("Warning: AxisHeight is set to %d while the center of the\
plus sign is %d." % (font.math.AxisHeight, suggestedValue),
                  file=sys.stderr)
    print("")

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
        print("Done")
    print("")

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
        print("Done")
    print("")

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
        print("Done")
    print("")

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
        print("Done")
    print("")

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
        print("Done")
    print("")

    # RadicalExtraAscender
    # RadicalKernBeforeDegree
    # RadicalKernAfterDegree
    # RadicalDegreeBottomRaisePercent

    ############################################################################
    # Verify whether the MathVariant table has appropriate data for some basic
    # unicode constructions.
    print("Testing Unicode Constructions in the MathVariant table...")
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
        print("Done")
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
                print("Done")
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
                    print("Done")

        # Verify whether the components are available.
        if parts is not None:
            print("Testing components for U+%04X... " % codePoint, end="")
            components = None
            if isVertical:
                components = glyph.verticalComponents
            else:
                components = glyph.horizontalComponents
            if components:
                print("Done")
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
                    print("Done")
    print("")

    ############################################################################
    # Verify whether the MathVariant table has appropriate data for large
    # operators.
    print("Testing large operators in the MathVariant table...")
    for c in kLargeOperators:

        # Verify whether the character is present.
        print("Testing base glyph for large operator U+%04X... " % c, end="")
        if c not in font:
            print("Failed")
            warnMissingGlyph(c)
            continue
        print("Done")
        glyph = font[c]

        # Verify variants
        print("Testing variants for large operator U+%04X... " % c, end="")
        if glyph.verticalVariants is not None:
            # Verify whether DisplayOperatorMinHeight can be satisfied.
            variants = glyph.verticalVariants.split(" ")
            hasDisplaySize = False
            for v in variants:
                if v in font:
                    box = font[v].boundingBox()
                    height = box[3] - box[1]
                    if font.math.DisplayOperatorMinHeight <= height:
                        hasDisplaySize = True
                        break
            if hasDisplaySize:
                print("Done")
            else:
                print("Failed")
                print("Warning: U+%04X does not have any size variant of height at least DisplayOperatorMinHeight" % c, file=sys.stderr)
        else:
            print("Failed")
            print("Setting variants for operator U+%04X... " % c,
                  end="")
            # Add a glyph for the operator in display mode
            baseGlyphName = font[c].glyphname
            displayGlyphName = "%s.display" % baseGlyphName
            g = font.createChar(-1, displayGlyphName)
            font.selection.select(baseGlyphName)
            font.copy()
            font.selection.select(displayGlyphName)
            font.paste()
            g.transform(psMat.scale(kLargeOpDisplayOperatorFactor),
                        ("round",))
            # FIXME: Is it really necessary to specify the base glyph?
            # This is done in Latin Modern but not XITS.
            glyph.verticalVariants = "%s %s" % (baseGlyphName, displayGlyphName)
            print("Done")
    print("")

    ############################################################################
    # Verify whether integrals have italic correction
    print("Testing italic correction for integrals...")
    for c in kLargeOpIntegrals:
        if c not in font:
            continue
        print("Testing italic correction for operator U+%04X..." % c)

        # Get the list of variants, including the base size
        variants = font[c].verticalVariants.split(" ")
        baseGlyphName = font[c].glyphname
        if variants[0] != baseGlyphName:
            variants.insert(0, baseGlyphName)

        # Test italic correction for each variant
        for v in variants:
            if v in font:
                testItalicCorrection(font[v])
    print("")

    ############################################################################
    # Testing Prescripted Operators / ssty tables
    print("Testing Prescripted Operators / ssty tables...")
    for c in kPreScriptedOperators:
        testSSTY(font, c)
    print("")

    ############################################################################
    # Testing Mathematical Alphanumeric Characters
    testMathVariants(font, "bold",
                     ((0x1D400, 0x1D433),
                      (0x1D6A8, 0x1D6E1),
                      (0x1D7CA, 0x1D7CB),
                      (0x1D7CE, 0x1D7D7)), aArgs.bold)

    testMathVariants(font, "italic",
                     ((0x1D434, 0x1D454),
                      (0x210E,),
                      (0x1D456, 0x1D467),
                      (0x1D6A4, 0x1D6A5),
                      (0x1D6E2, 0x1D6D6)), aArgs.italic)

    testMathVariants(font, "bold-italic",
                     ((0x1D468, 0x1D49B),
                      (0x1D71C, 0x1D755)), aArgs.bold_italic)

    testMathVariants(font, "script",
                     ((0x1D49C,),
                      (0x212C,),
                      (0x1D49E, 0x1D49F),
                      (0x2130, 0x2131),
                      (0x1D4A2,),
                      (0x210B,),
                      (0x2110,),
                      (0x1D4A5, 0x1D4A6),
                      (0x2112,),
                      (0x2133,),
                      (0x1D4A9, 0x1D4AC),
                      (0x211B,),
                      (0x1D4AE, 0x1D4B9),
                      (0x212F,),
                      (0x1D4BB,),
                      (0x210A,),
                      (0x1D4BD, 0x1D4C3),
                      (0x2134,),
                      (0x1D4C5, 0x1D4CF)), None)

    testMathVariants(font, "bold-script",
                     ((0x1D4D0, 0x1D503),), None)

    testMathVariants(font, "fraktur",
                     ((0x1D504, 0x1D505),
                      (0x212D,),
                      (0x1D507, 0x1D50A),
                      (0x210C,),
                      (0x2111,),
                      (0x1D50D, 0x1D514),
                      (0x211C,),
                      (0x1D516, 0x1D51C),
                      (0x2128,),
                      (0x1D51E, 0x1D537)), None)

    testMathVariants(font, "bold-fraktur",
                     ((0x1D56C, 0x1D59F),), None)

    testMathVariants(font, "sans-serif",
                     ((0x1D5A0, 0x1D5D3),
                      (0x1D7E2, 0x1D7EB)), aArgs.sans_serif)

    testMathVariants(font, "sans-serif-bold",
                     ((0x1D5D4, 0x1D607),
                      (0x1D756, 0x1D78F),
                      (0x1D7EC, 0x1D7F5)), aArgs.sans_serif_bold)

    testMathVariants(font, "sans-serif-italic",
                     ((0x1D608, 0x1D63B),), aArgs.sans_serif_italic)

    testMathVariants(font, "sans-serif-bold-italic",
                     ((0x1D63C, 0x1D66F),
                      (0x1D790, 0x1D7C9)), aArgs.sans_serif_bold_italic)

    testMathVariants(font, "monospace",
                     ((0x1D670, 0x1D6A3),
                      (0x1D7F6, 0x1D7FF)), aArgs.monospace)

    testMathVariants(font, "double-struck",
                     ((0x1D538, 0x1D539),
                      (0x2102,),
                      (0x1D53B, 0x1D53E),
                      (0x210D,),
                      (0x1D540, 0x1D544),
                      (0x2115,),
                      (0x1D546,),
                      (0x2119, 0x211A),
                      (0x211D,),
                      (0x1D54A, 0x1D550),
                      (0x2124,),
                      (0x1D552, 0x1D56B),
                      (0x1D7D8, 0x1D7E1),
                      (0x1EEA1, 0x1EEA3),
                      (0x1EEA5, 0x1EEA9),
                      (0x1EEAB, 0x1EEBB)), None)

    testMathVariants(font, "initial",
                     ((0x1EE21, 0x1EE22),
                      (0x1EE24,),
                      (0x1EE27,),
                      (0x1EE29, 0x1EE32),
                      (0x1EE34, 0x1EE37),
                      (0x1EE39,),
                      (0x1EE3B,)), None)

    testMathVariants(font, "tailed",
                     ((0x1EE42,),
                      (0x1EE47,),
                      (0x1EE49,),
                      (0x1EE4B,),
                      (0x1EE4D, 0x1EE4F),
                      (0x1EE51, 0x1EE52),
                      (0x1EE54,),
                      (0x1EE57,),
                      (0x1EE59,),
                      (0x1EE5B,),
                      (0x1EE5D,),
                      (0x1EE5F,)), None)

    testMathVariants(font, "looped",
                     ((0x1EE80, 0x1EE89),
                      (0x1EE8B, 0x1EE9B)), None)

    testMathVariants(font, "stretched",
                     ((0x1EE61, 0x1EE62),
                      (0x1EE64,),
                      (0x1EE67, 0x1EE6A),
                      (0x1EE6C, 0x1EE72),
                      (0x1EE74, 0x1EE77),
                      (0x1EE79, 0x1EE7C),
                      (0x1EE7E,)), None)
    ############################################################################
    if aArgs.output:
        # Output the modified font.
        output = "%s.fixed.sfd" % aArgs.input
        print("Saving file %s... " % output, end="")
        font.save(output)
        print("Done")
    font.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check math features of a font and optionally fixes issues.")
    parser.add_argument("input", type=str, help="Font to verify.")
    parser.add_argument("--output", action="store_true", help="Whether to output a version with some issues fixed.")
    parser.add_argument("--italic", type=str, help="Font from which to take italic glyphs.")
    parser.add_argument("--bold", type=str, help="Font from which to take bold glyphs.")
    parser.add_argument("--bold-italic", type=str, help="Font from which to take bold-italic glyphs.")
    parser.add_argument("--sans-serif", type=str, help="Font from which to take sans-serif glyphs.")
    parser.add_argument("--sans-serif-italic", type=str, help="Font from which to take sans-serif italic glyphs.")
    parser.add_argument("--sans-serif-bold", type=str, help="Font from which to take sans-serif bold glyphs.")
    parser.add_argument("--sans-serif-bold-italic", type=str, help="Font from which to take sans-serif bold italic glyphs.")
    parser.add_argument("--monospace", type=str, help="Font from which to take monospace glyphs.")
    args = parser.parse_args()
    main(args)
