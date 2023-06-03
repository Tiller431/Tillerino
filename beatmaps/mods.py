
class mods:
    NOMOD       = 0
    NOFAIL      = 1
    EASY        = 2
    TOUCHSCREEN = 4
    HIDDEN      = 8
    HARDROCK    = 16
    SUDDENDEATH = 32
    DOUBLETIME  = 64
    RELAX       = 128
    HALFTIME    = 256
    NIGHTCORE   = 512
    FLASHLIGHT  = 1024
    AUTOPLAY    = 2048
    SPUNOUT     = 4096
    RELAX2      = 8192
    PERFECT     = 16384
    KEY4        = 32768
    KEY5        = 65536
    KEY6        = 131072
    KEY7        = 262144
    KEY8        = 524288
    KEYMOD      = 1015808
    FADEIN      = 1048576
    RANDOM      = 2097152
    LASTMOD     = 4194304
    KEY9        = 16777216
    KEY10       = 33554432
    KEY1        = 67108864
    KEY3        = 134217728
    KEY2        = 268435456
    SCOREV2     = 536870912

def readableMods(m):
	r = ""
	if m == 0:
		return "nomod"
	if m & mods.NOFAIL > 0:
		r += "NF"
	if m & mods.EASY > 0:
		r += "EZ"
	if m & mods.HIDDEN > 0:
		r += "HD"
	if m & mods.HARDROCK > 0:
		r += "HR"
	if m & mods.DOUBLETIME > 0:
		r += "DT"
	if m & mods.HALFTIME > 0:
		r += "HT"
	if m & mods.FLASHLIGHT > 0:
		r += "FL"
	if m & mods.SPUNOUT > 0:
		r += "SO"
	if m & mods.TOUCHSCREEN > 0:
		r += "TD"
	return r

def modsToEnum(r):
    m = 0
    r = r.upper()
    if r.find("NF") > -1:
        m |= mods.NOFAIL
    if r.find("EZ") > -1:
        m |= mods.EASY
    if r.find("HD") > -1:
        m |= mods.HIDDEN
    if r.find("HR") > -1:
        m |= mods.HARDROCK
    if r.find("DT") > -1:
        m |= mods.DOUBLETIME
    if r.find("HT") > -1:
        m |= mods.HALFTIME
    if r.find("FL") > -1:
        m |= mods.FLASHLIGHT
    if r.find("SO") > -1:
        m |= mods.SPUNOUT
    if r.find("TD") > -1:
        m |= mods.TOUCHSCREEN
    return m


def fullModsToEnum(str):
    m = 0
    str = str.upper()
    if str.find("NOFAIL") > -1:
        m |= mods.NOFAIL
    if str.find("EASY") > -1:
        m |= mods.EASY
    if str.find("HIDDEN") > -1:
        m |= mods.HIDDEN
    if str.find("HARDROCK") > -1:
        m |= mods.HARDROCK
    if str.find("DOUBLETIME") > -1:
        m |= mods.DOUBLETIME
    if str.find("HALFTIME") > -1:
        m |= mods.HALFTIME
    if str.find("FLASHLIGHT") > -1:
        m |= mods.FLASHLIGHT
    if str.find("SPUNOUT") > -1:
        m |= mods.SPUNOUT
    if str.find("TOUCHSCREEN") > -1:
        m |= mods.TOUCHSCREEN

    return m