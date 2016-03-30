"""
addon = xbmcaddon.Addon(id='multimedia.kodi.platform')
title = addon.getAddonInfo('name')
icon = addon.getAddonInfo('icon')
webcamURL = addon.getSetting('channelURL')    

li = xbmcgui.ListItem(label=title, iconImage=icon, thumbnailImage=icon, path=webcamURL)
li.setInfo(type='Video', infoLabels={ "Title" : title })
li.setProperty('IsPlayable', 'true')

xbmc.Player().play(item=webcamURL, listitem=li)
"""

import sys
from urlparse import parse_qsl
import urllib, urllib2
import json
import xbmcgui
import xbmcplugin
import xbmcaddon

addon = xbmcaddon.Addon(id='multimedia.kodi.platform')
title = addon.getAddonInfo('name')
icon = addon.getAddonInfo('icon')

##################################
channelName = addon.getSetting('channelName')
channelURL = "http://" + addon.getSetting('channelURL') + ":" + str(addon.getSetting(id="channelPort")) + "/" + addon.getSetting('channelExtendURL')
channelAvatar = addon.getSetting('channelAvatar')
enableChannel = str(addon.getSetting(id="enableChannel"))

##################################
fileName = addon.getSetting('fileName')
fileURL = addon.getSetting('fileURL')
fileTypeKey = int(addon.getSetting('fileType'))

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

_channels = "All channels"
_files = "All files shared"


VIDEOS = {_channels: []}

FILES = {_files: []}
        

def get_channels_categories():
    return VIDEOS.keys()


def get_channels_videos(category): 
    return VIDEOS[category]


def list_channels_categories():
    # Get video categories
    categories = get_channels_categories()
    # Create a list for our items.
    listing = []
    
    # Iterate through categories
    for category in categories:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category, thumbnailImage=VIDEOS[category][0]['thumb'])
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': VIDEOS[category][0]['thumb'],
                          'icon': VIDEOS[category][0]['thumb'],
                          'fanart': VIDEOS[category][0]['thumb']})
        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # http://mirrors.xbmc.org/docs/python-docs/15.x-isengard/xbmcgui.html#ListItem-setInfo
        list_item.setInfo('video', {'title': category})
        # Create a URL for the plugin recursive callback.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = '{0}?action=listing_channel&category_channel={1}'.format(_url, category)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the listing as a 3-element tuple.
        listing.append((url, list_item, is_folder))
    # Add our listing to Kodi.
    # Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
    # instead of adding one by ove via addDirectoryItem.
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def list_channels_videos(category):
    # Get the list of videos in the category.
    videos = get_channels_videos(category)
    # Create a list for our items.
    listing = []
    
    # Iterate through videos.
    for video in videos:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=video['name'])
        # Set additional info for the list item.
        list_item.setInfo('video', {'title': video['name']})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['thumb']})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for the plugin recursive callback.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/vids/crab.mp4
        url = '{0}?action=play_channel&video_channel={1}'.format(_url, video['video'])
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the listing as a 3-element tuple.
        listing.append((url, list_item, is_folder))
    
    # Add our listing to Kodi.
    # Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
    # instead of adding one by ove via addDirectoryItem.
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)
#######################################################
def get_files_categories():
    return FILES.keys()


def get_files_videos(category): 
    return FILES[category]


def list_files_categories():
    categories = get_files_categories()

    listing = []

    for category in categories:
        list_item = xbmcgui.ListItem(label=category)

        list_item.setInfo('video', {'title': category})

        url = '{0}?action=listing_file&category_file={1}'.format(_url, category)

        is_folder = True

        listing.append((url, list_item, is_folder))

    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))

    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)

    xbmcplugin.endOfDirectory(_handle)


def list_files_videos(category):

    videos = get_files_videos(category)

    listing = []
    
    # Iterate through videos.
    for video in videos:
        list_item = xbmcgui.ListItem(label=video['name'])

        list_item.setInfo('video', {'title': video['name']})

        list_item.setProperty('IsPlayable', 'true')

        url = '{0}?action=play_file&video_file={1}'.format(_url, video['path'])

        is_folder = False

        listing.append((url, list_item, is_folder))

    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))

    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)

    xbmcplugin.endOfDirectory(_handle)

###############################################
def play_video(path):
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)
###############################################
def router(paramstring):
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listing_channel':
            # Display the list of videos in a provided category.
            list_channels_videos(params['category_channel'])
        elif params['action'] == 'listing_file':
            list_files_videos(params['category_file'])
        elif params['action'] == 'play_channel':
            # Play a video from a provided URL.
            play_video(params['video_channel'])
        elif params['action'] == 'play_file':
            play_video(params['video_file'])
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_channels_categories()
        list_files_categories()
######################################################        
######################################################   
def enable_my_channel():
    url = 'http://iot.nguyenhoangbaoduy.info/enableMyChannel.php'
    req = urllib2.Request(url)
    
    if enableChannel == 'true':       
        sql = urllib.urlencode({'name': channelName,
                                   'thumb': channelAvatar,
                                   'video': channelURL,
                                   'enable': 1}) 
    else:
        sql = urllib.urlencode({'name': channelName,
                                   'thumb': channelAvatar,
                                   'video': channelURL,
                                   'enable': 0}) 
        
    response = urllib2.urlopen(req, sql)
    json_source = json.load(response)
    response.close()

def load_list_channels():
    url = 'http://iot.nguyenhoangbaoduy.info/getListChannel.php'
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    json_source = json.load(response)
    response.close()
    
    #category = "channels"
    
    for channel in json_source['channels']:
        try:
            friend_name     =   channel['name'].encode('utf-8')
            friend_thumb    =   channel['thumb'].encode('utf-8')
            friend_video    =   channel['video'].encode('utf-8')
            
            VIDEOS[_channels].append({'name': friend_name,
                       'thumb': friend_thumb,
                       'video': friend_video})
        except:
            pass 

def share_my_file():
    url = 'http://iot.nguyenhoangbaoduy.info/shareMyFile.php'
    req = urllib2.Request(url)     
    sql = urllib.urlencode({'name': fileName,
                               'path': fileURL,
                               'channel': channelName,
                               'type': fileTypeKey}) 
        
    response = urllib2.urlopen(req, sql)
    json_source = json.load(response)
    response.close()
    
def load_list_files():
    url = 'http://iot.nguyenhoangbaoduy.info/getListFile.php'
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    json_source = json.load(response)
    response.close()
    
    #category = "channels"
    
    for channel in json_source['files']:
        try:
            file_name    =   channel['name'].encode('utf-8')
            file_path    =   channel['path'].encode('utf-8')
            
            FILES[_files].append({'name': file_name,
                       'path': file_path})
        except:
            pass 
######################################################
######################################################        

if __name__ == '__main__':
    load_list_channels()
    enable_my_channel()
    load_list_files()
    share_my_file()
    
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
 


