import xbmcaddon
import xbmcgui

addon       =   xbmcaddon.Addon()
addonname   =   addon.getAddonInfo('name')

line1   =   "Multimedia Kodi platform"
line2   =   "MULTIMEDIA BROADCASTING PLATFORM (ACCESSIBLE VIA KODI)"
line3   =   "Version 0.1 (beta)"

xbmcgui.Dialog().ok(addonname, line1, line2, line3)