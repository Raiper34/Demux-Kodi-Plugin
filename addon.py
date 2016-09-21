"""
SmartDemux Kodi Plugin
@Author: Filip "Raiper34" Gulan
@Website: http:www.raiper34.net
@Mail: raipergm34@gmail.com
"""

import sys
import urlparse
from smartDemux import SmartDemux

tv = SmartDemux(sys.argv[0], int(sys.argv[1]), urlparse.parse_qs(sys.argv[2][1:]))
tv.start()