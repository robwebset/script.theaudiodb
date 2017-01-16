# -*- coding: utf-8 -*-
import time
import xbmcgui
import xbmcaddon

# Import the common settings
from resources.lib.settings import log
from resources.lib.settings import Settings
from resources.lib.sync import LibrarySync


ADDON = xbmcaddon.Addon(id='script.theaudiodb.sync')


##################################
# Main of TheAudioDBSync Script
##################################
if __name__ == '__main__':
    log("TheAudioDBSync Starting %s" % ADDON.getAddonInfo('version'))

    # Get the username
    username = Settings.getUsername()

    if username in [None, ""]:
        # Show a dialog detailing that the username is not set
        xbmcgui.Dialog().ok(ADDON.getLocalizedString(32001), ADDON.getLocalizedString(32005))
    else:
        performResync = True
        # Before performing the resync, check when the last time a resync was done, we want
        # to try and discourage people doing too many resyncs in quick succession
        lastResyncTimeStr = Settings.getLastSyncTime()
        if lastResyncTimeStr not in [None, ""]:
            currentTime = int(time.time())
            # check if the last resync was within 5 minuted
            if currentTime < (int(lastResyncTimeStr) + 300):
                performResync = xbmcgui.Dialog().yesno(ADDON.getLocalizedString(32001), ADDON.getLocalizedString(32016))

        if performResync:
            # Perform the resync operation and display the status
            numAlbumsUpdated, numTracksUpdated = LibrarySync.syncToLibrary(username, True)

            # Display a summary of what was performed
            summaryAlbums = "%d %s" % (numAlbumsUpdated, ADDON.getLocalizedString(32010))
            summaryTracks = "%d %s" % (numTracksUpdated, ADDON.getLocalizedString(32011))
            xbmcgui.Dialog().ok(ADDON.getLocalizedString(32001), summaryAlbums, summaryTracks)

    log("TheAudioDBSync Finished")
