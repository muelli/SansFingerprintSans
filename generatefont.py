#!/usr/bin/env python
from itertools import chain
import logging
import string
import sys

from fontTools.ttLib import TTFont
from fontTools.feaLib.builder import Builder, addOpenTypeFeatures, addOpenTypeFeaturesFromString
from fontTools.unicode import Unicode



translation_table = {
    '0': r'\zero',
    '1': r'\one',
    '2': r'\two',
    '3': r'\three',
    '4': r'\four',
    '5': r'\five',
    '6': r'\six',
    '7': r'\seven',
    '8': r'\eight',
    '9': r'\nine',
    ' ': r'\space'
}
for c in string.ascii_uppercase:
    translation_table[c] = '\\'+c


attacked_fingerprint = sys.argv[1]
replacement_fingerprint = sys.argv[2]
attacked_font = sys.argv[3]
font = TTFont(attacked_font)

# Somehow, I cannot add an "intermediate" glyph to the font, so we're using some glyph that is available.
# This is a bit dirty, because it changes all occurences of that glyph into our new fingerprint.
unichars = chain.from_iterable([y for y in x.cmap.items() if y[1].startswith("uni")] for x in font["cmap"].tables)
last_unichar = list(unichars)[-1] # we take the last "uni...." glyph, because we believe it's used less often than the first ones...
# The main problem being, that I can only make "uni...." replacements in the feature file
last_uni = last_unichar[1]
# If we can't pass here, the font doesn't have any "uni" characters.

attacked_sub = " ".join((translation_table[c] for c in attacked_fingerprint))
replacement_sub = " ".join((translation_table[c] for c in replacement_fingerprint))


features = r'''
lookup ligaStandardLigaturesinLatinlookup3 {
  lookupflag 0;
''' f"    sub {attacked_sub}   by {last_uni};" '''
} ligaStandardLigaturesinLatinlookup3;

lookup ligaStandardLigaturesinLatinlookup4 {
  lookupflag 0;
''' f"    sub {last_uni} by {replacement_sub} ;" '''
} ligaStandardLigaturesinLatinlookup4;

feature RQD  {

 script latn;
     language dflt ;
      lookup ligaStandardLigaturesinLatinlookup3;
      lookup ligaStandardLigaturesinLatinlookup4;
} RQD ;

feature liga {

 script latn;
     language dflt ;
      lookup ligaStandardLigaturesinLatinlookup3;
      lookup ligaStandardLigaturesinLatinlookup4;
} liga;
'''

addOpenTypeFeaturesFromString(font, features)

save_new_font_path = sys.argv[4]
font.save(save_new_font_path)
