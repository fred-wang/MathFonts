###########################################################################
############          The TeX Gyre Collection of Fonts         ############
############                 The font Pagella                  ############
###########################################################################

Font: TeX Gyre Pagella
Authors: Bogus\l{}aw Jackowski, Janusz M. Nowacki, Piotr Pianowski, and Piotr Strzelczyk
Version: 2.501
Date: 8 V 2018
Downloads: http://www.gust.org.pl/projects/e-foundry/tex-gyre/pagella


License:
  % Copyright 2007--2018 for TeX Gyre extensions by B. Jackowski,
  % J.M. Nowacki et al. (on behalf of TeX Users Groups). Vietnamese
  % characters were added by Han The Thanh.
  %
  % This work can be freely used and distributed under
  % the GUST Font License (GFL -- see GUST-FONT-LICENSE.txt)
  % which is actually an instance of the LaTeX Project Public License
  % (LPPL -- see http://www.latex-project.org/lppl.txt ).
  %
  % This work has the maintenance status "maintained". The Current Maintainer
  % of this work is Bogus\l{}aw Jackowski and Janusz M. Nowacki.
  %
  % This work consists of the files listed
  % in the MANIFEST-TeX-Gyre-Pagella.txt file.

###########################################################################
############         A BRIEF DESCRIPTION OF THE PACKAGE        ############
###########################################################################

The current package contains the most recent version of the TeX Gyre
Pagella family of fonts in the PostScript Type 1 and OpenType formats.
TeX Gyre Pagella is based on the URW Palladio L kindly released
by URW++ Design and Development Inc. under GFL (independently of the GPL
release accompanying Ghostscript). The Vietnamese glyphs were added
by Han The Thanh.

TeX Gyre Pagella can be used as a replacement for the renowned Palatino
font (designed by Hermann Zapf in the 1940's for the Stempel type foundry;
an interesting lifestory of Hermann Zapf can be found at:
http://www.linotype.com/1494/theschoolyears.html );

Note that the widths of the TeX Gyre Pagella glyphs are almost consistent
with the relevant Adobe metric data (for the glyphs from the Adobe Standard
Encoding):
  ftp://ftp.adobe.com/pub/adobe/type/win/all/afmfiles/base35/pob_____.afm
  ftp://ftp.adobe.com/pub/adobe/type/win/all/afmfiles/base35/pobi____.afm
  ftp://ftp.adobe.com/pub/adobe/type/win/all/afmfiles/base35/poi_____.afm
  ftp://ftp.adobe.com/pub/adobe/type/win/all/afmfiles/base35/por_____.afm

The only exception is `perthousand' in the regular variant (Adobe: 1144;
TeX Gyre: 1000 which is consistent with the width of perthousand in other
variants). The discrepancy (in the regular variant) between the width 
of the glyph `i' (291) and the width of `dotlessi' (287) was preserved
as optically irrelevant.

                           *   *   *

The TeX Gyre project, following the Latin Modern project, aims at providing
a rich collection of diacritical characters in the attempt to cover as many
Latin-based scripts as possible. To our knowledge, the repertoire of
characters covers all European languages as well as some other Latin-based
alphabets such as Vietnamese and Navajo; at the request of users, recent
extensions (following the enhancement of the Latin Modern collection)
provide glyphs sufficient for typesetting of romanized transliterations
of Arabic and Sanskrit scripts. We have frequently used the information
presented by Michael Everson at the ``The Alphabets of Europe''
( http://www.evertype.com/alphabets/ ) web site. If you know about European
languages that are not covered completely or if some glyphs have apparently
wrong shapes -- please let us know. Note, however, that Greek glyphs
bear provisional character.

The TeX Gyre Project was launched and is supported by TeX USERS GROUPS
(CS TUG, DANTE eV, GUST, NTG, TUG India, TUG). Hearty thanks to the
representatives of these groups and also to all people who helped with
comments, ideas, remarks, bug reports, objections, hints, consolations, etc.

                           *   *   *

The TeX Gyre Pagella family consists of 4 text fonts: regular,
italic, bold and bold italic (qplr, qplri, qplb, qplbi).

The TeX Gyre Pagella family can be freely used and distributed
under the GUST Font License (see above) which is actually
an instance of the LaTeX Project Public License
(LPPL; see http://www.latex-project.org/lppl.txt ).

                           *   *   *

The package consists of the files in the directories conforming
to the TeX Directory Structure (v. 1.1). The directories contain:

doc/fonts/tex-gyre             this file, manifest, licence, test files,
                               and, moreover, selected files used as input
                               for generating OTFs (meant as a technical
                               documentation of the OTFs)
tex/latex/tex-gyre             support for LaTeX (*.fd and *.sty files,
                               prepared by Marcin Woli\'nski)
fonts/enc/dvips/tex-gyre       support for dvips (*.enc files);
                               NOTE: all fonts of the TeX Gyre family
                                 share the same *.enc files with
                                 a few exceptions: CS, QX, and RM encodings
                                 for TeX Gyre Cursor (monospace) differ
                                 from the standard ones (because of the
                                 compatibility with Computer Modern
                                 typewriter fonts requested by users),
                                 and, moreover, CS, L7x, QX and RM encodings
                                 for TeX Gyre Chorus exploit exceptionally
                                 the `lslash_lslash' ligature
fonts/map/dvips/tex-gyre       support for dvips (*.map files)
fonts/opentype/public/tex-gyre fonts in the OpenType format (*.otf files)
fonts/type1/public/tex-gyre    PostScript (Type 1) font files and printer
                               font metric files (*.pfb and *.pfm,
                               respectively);
fonts/tfm/public/tex-gyre      TeX font metric files (*.tfm) for:
                               -- CS (CSTUG) encoding (cs-*.tfm),
                               -- EC (Cork) encoding (ec-*.tfm),
                               -- L7x (Lithuanian) encoding (l7x-*.tfm),
                               -- QX (GUST) encoding (qx-*.tfm),
                               -- RM (Regular Math or OT1) encoding (rm-*.tfm),
                               -- Y&Y's TeX'n'ANSI aka LY1 encoding
                                  (texnansi-*.tfm),
                               -- T5 (Vietnamese) encoding (t5-*.tfm),
                               -- Text Companion for EC fonts aka TS1
                                  (ts1-*.tfm).
                               Encodings CS, EC, L7x, QX, RM, Y&Y, and T5
                               have their cap-small-caps counterparts
                               (*-sc.tfm).
fonts/afm/public/tex-gyre      Adobe font metric files (*.afm);

Email contact: Bogus\l{}aw Jackowski aka Jacko, B_Jackowski@gust.org.pl

                           *   *   *

In ConTeXt, support for TeX Gyre Collection can be found in the typescript
definition files:

  ... /tex/context/base/type-enc.tex
  ... /tex/context/base/type-syn.tex
  ... /tex/context/base/type-exa.tex
  ... /tex/context/base/type-map.tex

Additional encoding and map files can be found under:

  ... /texmf/fonts/map/pdftex/context
  ... /texmf/fonts/enc/pdftex/context

                           *   *   *

All four font files, qplb, qplbi, qplr, qplri, share the same repertoire
of characters. The number of glyphs in the PFB/OTF files (.notdef ignored) equals
1616/1548; see qpl-info.pdf file in the relevant doc directory for details
