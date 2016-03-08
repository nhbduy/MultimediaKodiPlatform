import xbmc
import xbmcgui
import xbmcaddon

addon       =   xbmcaddon.Addon(id='multimedia.kodi.platform')
title       =   addon.getAddonInfo('name')
icon        =   addon.getAddonInfo('icon')
webcamURL   =   addon.getSetting('localwebcam')    

li  =   xbmcgui.ListItem(label=title, iconImage=icon, thumbnailImage=icon, path=webcamURL)
li.setInfo(type='Video', infoLabels={ "Title" : title })
li.setProperty('IsPlayable', 'true')

xbmc.Player().play(item=webcamURL, listitem=li)