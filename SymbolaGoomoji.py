#
# How to generate SymbolaGoomoji.ttf
#
# 1. Get DroidSans.ttf from Android device.
# 2. % fontforge -script SymbolaGoomoji.py -lang py
# 3. % fontforge SymbolaGoomoji.sfd
#    Set TTF UniqueID to 'SymbolaGoomoji' manually, then
#    generate TrueType font 'SymbolaGoomoji.ttf'.
#

import fontforge
import urllib2
from xml.etree import ElementTree

request = urllib2.Request('http://emoji4unicode.googlecode.com/svn/trunk/data/emoji4unicode.xml')
response = urllib2.urlopen(request)
emoji4unicode = response.read()

table = ElementTree.ElementTree(ElementTree.fromstring(emoji4unicode))
elem = table.getroot()

font = fontforge.open("Symbola.ttf")
DroidSans = fontforge.open('DroidSans.ttf')

mapping = dict()
for e in elem.findall(".//e"):
    try:
        goo = e.get("google")
        uni = e.get("unicode")
        gooNo = int(goo, 16)
        uniNo = int(uni, 16)
        if uni:
            if goo:
                mapping[uniNo] = gooNo
            else:
                mapping[uniNo] = False
    except:
        pass

removes = dict()

# Remove glyphs which is not emoji.
for g in font.glyphs():
    removes[g.unicode] = True
    if 0x1f300 <= g.unicode and g.unicode <= 0x1f5ff:
        removes[g.unicode] = False
    if 0x1f600 <= g.unicode and g.unicode <= 0x1f64f:
        removes[g.unicode] = False
    if 0x1f680 <= g.unicode and g.unicode <= 0x1f6ff:
        removes[g.unicode] = False
    if 0x2600 <= g.unicode and g.unicode <= 0x26ff:
        removes[g.unicode] = False

# Remove glyphs which is included in DroidSans font.
for g in DroidSans.glyphs():
    if -1 != font.findEncodingSlot(g.unicode):
        removes[g.unicode] = True

# copy unicode emoji to goomoji
for g in font.glyphs():
    if g.unicode in mapping:
        if mapping[g.unicode]:
            if g.unicode in removes and removes[g.unicode]:
                g.unicode = mapping[g.unicode]
            else:
                g.altuni = ((mapping[g.unicode], -1, 0))

for g in font.glyphs():
    if g.unicode in removes and removes[g.unicode]:
        font.removeGlyph(g)

font.familyname = "SymbolaGoomoji"
font.fontname = "SymbolaGoomoji"
font.fullname = "SymbolaGoomoji"
font.ascent = DroidSans.ascent
font.descent = DroidSans.descent
# I could not find how to set TTF UniqueId to "SymbolaGoomoji"

font.save("SymbolaGoomoji.sfd")
