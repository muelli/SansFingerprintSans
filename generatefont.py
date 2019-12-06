#!/usr/bin/env python
import logging
import string
import sys

from fontTools.ttLib import TTFont
from fontTools.feaLib.builder import Builder, addOpenTypeFeatures, addOpenTypeFeaturesFromString


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
}
for c in string.ascii_uppercase:
    translation_table[c] = '\\'+c


attacked_fingerprint = sys.argv[1]
replacement_fingerprint = sys.argv[2]

attacked_sub = " ".join((translation_table[c] for c in attacked_fingerprint))
replacement_sub = " ".join((translation_table[c] for c in replacement_fingerprint))


features = r'''
lookup ligaStandardLigaturesinLatinlookup3 {
  lookupflag 0;
    sub %s   by \uniE600;
} ligaStandardLigaturesinLatinlookup3;

lookup ligaStandardLigaturesinLatinlookup4 {
  lookupflag 0;
    sub \uniE600 by %s ;
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
''' % (attacked_sub, replacement_sub)

attacked_font = sys.argv[3]
font = TTFont("SansBullshitSans.ttf") # We work on a hard-coded font for now.
font = TTFont(attacked_font)
addOpenTypeFeaturesFromString(font, features)

save_new_font_path = sys.argv[4]
font.save(save_new_font_path)
