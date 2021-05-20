# You should have received a copy of the GNU General Public License
# along with Philo.  If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-

from resources.lib.classes.philo import Philo
from resources.lib.globals import *

class Main(object):

    sysARG = None
    Handle_ID = -1
    name = None
    mode = None
    url = None
    params = None
    philo = None

    def __init__(self, sysARG):
        global FUNCTION
        FUNCTION = "__init__"
        self.log("Philo addon starting....")
        
        self.sysARG = sysARG
        self.Handle_ID = int(sysARG[1])
        
        self.getParams()

    def run(self):
        global FUNCTION, STRINGS
        FUNCTION = "run"
        self.philo = Philo()

        if self.philo.logIn():
            if self.mode is None: self.buildMenu()
            if self.mode == "play": self.play()
            if self.mode == "channels": self.channelMenu()
        else:
            notificationDialog(STRINGS(30103))
            sys.exit()

        xbmcplugin.setContent(self.Handle_ID, CONTENT_TYPE)
        xbmcplugin.addSortMethod(self.Handle_ID, xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.addSortMethod(self.Handle_ID, xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.addSortMethod(self.Handle_ID, xbmcplugin.SORT_METHOD_LABEL)
        xbmcplugin.addSortMethod(self.Handle_ID, xbmcplugin.SORT_METHOD_TITLE)
        xbmcplugin.endOfDirectory(self.Handle_ID, updateListing=UPDATE_LISTING, cacheToDisc=CACHE)

        xbmc.executebuiltin('Container.SetSortMethod(1)')

    def getParams(self):
        global FUNCTION
        FUNCTION = "getParams"
        self.log("Retrieving parameters")
        
        self.params = dict(urllib.parse.parse_qsl(self.sysARG[2][1:]))
        try: self.url = urllib.unquote(self.params['url'])
        except: pass
        try: self.name = urllib.unquote_plus(self.params['name'])
        except: pass
        try: self.mode = self.params['mode']
        except: pass

        self.log('\rName: %s | Mode: %s\rURL: %s%s\rParams:\r%s' % (self.name, self.mode, self.sysARG[0], self.sysARG[2], json.dumps(self.params, indent=1)))

    def buildMenu(self):
        global FUNCTION
        FUNCTION = "buildMenu"
        self.log("Building main menu")

    def play(self):
        global FUNCTION
        FUNCTION = "play"
        self.log("Attempting to play item")

    def channelMenu(self):
        global FUNCTION
        FUNCTION = "channelMenu"
        self.log("Building channel menu")

    def log(self, message):
        log(message=message, function=FUNCTION)
