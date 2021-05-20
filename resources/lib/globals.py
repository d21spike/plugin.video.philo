from typing import TYPE_CHECKING
from http.cookiejar import MozillaCookieJar
import xbmc, xbmcvfs, xbmcplugin, xbmcgui, xbmcaddon
import requests, traceback, uuid, json, os, urllib, sys

KODI_VERSION_MAJOR = int(xbmc.getInfoLabel('System.BuildVersion').split('.')[0])
ADDON_NAME = "Philo"
ADDON_ID = "plugin.video.philo"
ADDON_URL = "plugin://plugin.video.philo/"
SETTINGS = xbmcaddon.Addon(id=ADDON_ID)
SETTINGS_LOC = SETTINGS.getAddonInfo("profile")
ADDON_VERSION = SETTINGS.getAddonInfo("version")
ADDON_PATH = SETTINGS.getAddonInfo("path")
COOKIE_PATH = xbmcvfs.translatePath(os.path.join(SETTINGS_LOC, "cookies"))
DEBUG = SETTINGS.getSetting("Enable_Debugging") == "true"
ICON = SETTINGS.getAddonInfo("icon")
EMAIL = SETTINGS.getSetting("Email")
DEVICE_ID = SETTINGS.getSetting("Device_ID")
STRINGS = SETTINGS.getLocalizedString
CONTENT_TYPE = "Episodes"
UPDATE_LISTING = False
CACHE = False

def inputDialog(heading=ADDON_NAME, default='', key=xbmcgui.INPUT_ALPHANUM, opt=0, close=0):
    retval = xbmcgui.Dialog().input(heading, default, key, opt, close)
    if len(retval) > 0: return retval

def log(message, function="", level=xbmc.LOGDEBUG):
    if DEBUG == False and level != xbmc.LOGERROR: return
    if level == xbmc.LOGERROR: message += ' ,' + traceback.format_exc()
    print ("%s-%s::%s() -> %s" % (ADDON_ID, ADDON_VERSION, function, message))

def notificationDialog(message, header=ADDON_NAME, sound=False, time=1000, icon=ICON):
    xbmcgui.Dialog().notification(header, message, icon, time, sound)
