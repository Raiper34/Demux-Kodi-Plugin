"""
Smart Demux Class
@Author: Filip "Raiper34" Gulan
@Website: http:www.raiper34.net
@Mail: raipergm34@gmail.com
"""

#Python libraries
import urllib
import urllib2
import cookielib
import xml.dom.minidom
import re
#Xbmc libraries
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmcvfs

class SmartDemux():

    """
    Constructor
    """
    def __init__(self, baseUrl, addonHandle, arguments):
        self.baseUrl = baseUrl
        self.addonHandle = addonHandle
        self.arguments = arguments

        self.website = 'http://smart.demux.cz/'

        settings = xbmcaddon.Addon()
        self.username = settings.getSetting('username')
        self.password = settings.getSetting('password')

        cookies = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))

        self.addon = xbmcaddon.Addon()

    """
    Create xbmc url
    """
    def buildUrl(self, query):
        return self.baseUrl + '?' + urllib.urlencode(query)

    """
    Create Category list
    """
    def createCategories(self):
        page = self.opener.open(self.website + 'ucp.php?mode=login', urllib.urlencode({'username': self.username, 'password': self.password, 'redirect': 'index.php', 'sid': '', 'login': 'Login'}))
        pageContent = page.read()

        try:
            categoryAreaText = re.findall("<p class=\"breadcrumbs\">.*<p class=\"breadcrumbs\">", pageContent, re.DOTALL)
            categoryLineText = re.findall("<a href=\".*?</a>", categoryAreaText[0], re.DOTALL)
        except:
            xbmc.executebuiltin('Notification(%s, %s, %d)' % ('Info', 'Nespravne uzivatelske meno, alebo heslo!', 3000))
            return

        for line in categoryLineText:
            name = re.findall("(?<=\">).*(?=</a>)", line, re.DOTALL)
            link = re.findall("(?<=<a href=\").*(?=\">)", line, re.DOTALL)

            url = self.buildUrl({'mode': 'chanel', 'link': link[0]})
            item = xbmcgui.ListItem(name[0],iconImage='defaultFolder.png')
            xbmcplugin.addDirectoryItem(handle=self.addonHandle, url=url, listitem=item, isFolder=True)

        xbmcplugin.endOfDirectory(self.addonHandle)

    """
    Create Channel list
    """
    def createChannels(self):
        #Login
        page = self.opener.open(self.website + 'ucp.php?mode=login', urllib.urlencode({'username': self.username, 'password': self.password, 'redirect': 'index.php', 'sid': '', 'login': 'Login'}))
        try:
            page = self.opener.open(self.website + self.arguments['link'][0])
            pageContent = page.read()
        except:
            return
        channelAreaText = re.findall("<table class=\"channels-table\".*</table>", pageContent, re.DOTALL)
        channelLineText = re.findall("<td class=\"img-td\">.*?</tr>", channelAreaText[0], re.DOTALL)

        for line in channelLineText:
            name = re.findall("(?<=<td class=\"name-td\" id=\").*?(?=\")", line, re.DOTALL)
            link = re.findall("(?<=<a href=\").*?(?=\")", line, re.DOTALL)
            logo = re.findall("(?<=<img src=\").*?(?=\")", line, re.DOTALL)
            try:
                page = self.opener.open(self.website + link[0])
                pageContent = page.read()
            except:
                return
            video = 

            item = xbmcgui.ListItem(name[0], iconImage=logo[0])
            item.setLabel(name[0])
            item.setThumbnailImage(logo[0])
            xbmcplugin.addDirectoryItem(handle=self.addonHandle, url='url', listitem=item)

        xbmcplugin.endOfDirectory(self.addonHandle)

    """
    Pick mode, or decision what interface to generate
    """
    def pickMode(self):
        mode = self.arguments.get('mode', None)
        #Pick Mode
        if mode is None:
            self.createCategories()
        #Search in TV shows
        elif mode[0] == 'chanel':
            self.createChannels()

    """
    Start function, that generate xbmc interface
    """
    def start(self):
        #Username or Password is blank
        if self.password is "" or self.username is "":
            self.addon.openSettings()
            return

        xbmcplugin.setContent(self.addonHandle, 'movies')
        self.pickMode()
