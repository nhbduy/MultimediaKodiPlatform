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
import xbmcgui
import xbmcplugin
import xbmcaddon

addon = xbmcaddon.Addon(id='multimedia.kodi.platform')
title = addon.getAddonInfo('name')
icon = addon.getAddonInfo('icon')
channelName = addon.getSetting('channelName')
channelURL = addon.getSetting('channelURL')
channelAvatar = addon.getSetting('channelAvatar')

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

# Free sample videos are provided by www.vidsplay.com
# Here we use a fixed set of properties simply for demonstrating purposes
# In a "real life" plugin you will need to get info and links to video files/streams
# from some web-site or online service.
VIDEOS = {'My channel': [{'name': channelName,
                       'thumb': channelAvatar,
                       'video': channelURL}
                      ],
            'Friends channel': [{'name': 'Friend A',
                      'thumb': 'http://www.vidsplay.com/vids/us_postal.jpg',
                      'video': 'http://www.vidsplay.com/vids/us_postal.mp4'},
                     {'name': 'Friend B',
                      'thumb': 'http://www.vidsplay.com/vids/traffic1.jpg',
                      'video': 'http://www.vidsplay.com/vids/traffic1.avi'},
                     {'name': 'Friend C',
                      'thumb': 'http://www.vidsplay.com/vids/traffic_arrows.jpg',
                      'video': 'http://www.vidsplay.com/vids/traffic_arrows.mp4'}
                     ]}


def get_categories():
    return VIDEOS.keys()


def get_videos(category):
    return VIDEOS[category]


def list_categories():
    # Get video categories
    categories = get_categories()
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
        url = '{0}?action=listing&category={1}'.format(_url, category)
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


def list_videos(category):
    # Get the list of videos in the category.
    videos = get_videos(category)
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
        url = '{0}?action=play&video={1}'.format(_url, video['video'])
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


def play_video(path):
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listing':
            # Display the list of videos in a provided category.
            list_videos(params['category'])
        elif params['action'] == 'play':
            # Play a video from a provided URL.
            play_video(params['video'])
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_categories()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])


