"""
SmartDemux Kodi Plugin
@Author: Filip "Raiper34" Gulan
@Website: http:www.raiper34.net
@Mail: raipergm34@gmail.com
"""

import urllib
import urllib2
import cookielib
import re

cookies = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))

page = opener.open('http://smart.demux.cz/ucp.php?mode=login', urllib.urlencode({'username': 'filip', 'password': 'raiper', 'redirect':'index.php', 'sid':'', 'login':'Login'}))
pageContent = page.read()

categoryAreaText = re.findall("<p class=\"breadcrumbs\">.*<p class=\"breadcrumbs\">", pageContent, re.DOTALL)
categoryLineText = re.findall("<a href=\".*?</a>", categoryAreaText[0], re.DOTALL)

for line in categoryLineText:
    name = re.findall("(?<=\">).*(?=</a>)", line, re.DOTALL)
    link = re.findall("(?<=<a href=\").*(?=\">)", line, re.DOTALL)
    #print(name[0])
    #print(link[0])
    #print('http://smart.demux.cz/' + link[0])
    try:
        page = opener.open('http://smart.demux.cz/' + link[0])
        pageContent = page.read()
    except:
        continue
    channelAreaText = re.findall("<table class=\"channels-table\".*</table>", pageContent, re.DOTALL)
    channelLineText = re.findall("<td class=\"img-td\">.*?</tr>", channelAreaText[0], re.DOTALL)
    for line in channelLineText:
        name = re.findall("(?<=<td class=\"name-td\" id=\").*?(?=\")", line, re.DOTALL)
        link = re.findall("(?<=<a href=\").*?(?=\")", line, re.DOTALL)
        logo = re.findall("(?<=<img src=\").*?(?=\")", line, re.DOTALL)
        print(name[0] + ' ' + link[0] + ' ' + logo[0])
        try:
            page = opener.open('http://smart.demux.cz/' + link[0])
            pageContent = page.read()
        except:
            continue
        video = re.findall("(?<=<a href=\").*?(?=\" id=\"play-pause\"><img src=\"images/play_vlc.png\"></a>)", pageContent)
        print(video[0])



