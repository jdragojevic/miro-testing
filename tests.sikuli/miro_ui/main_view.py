# All actions on the preferences panel
#!/usr/bin/python
from sikuli.Sikuli import *
from miro_ui import MiroApp

class MainView(MiroApp):
    _ITEM_BADGES = {'download error': "badge_dl_error.png",
                    'currently playing': "item_currently_playing.png",
                    'download': 'button_download.png'}

    _FILTER_TOGGLES = {'two_filter': Pattern('2_filter_toggle.png'),
                       'three_filter': Pattern('3_filter_toggle.png')
                      }
    _CONVERSION_PROGRESS = "item-renderer-conversion-progress-left.png"
    _CLEAR_FINISHED_CONVERSIONS = "button_clear_finished.png"
    _BUTTONS = {'Autodownload': 'button_autodownload.png', 
                'Remove Podcast': 'button_remove_podcast.png',
                'Settings': 'button_settings.png',
                'Save as Podcast': 'button_save_as_podcast.png',
                'Save as Playlist': 'button_save_as_playlist.png'}

    _SEARCH = {'clear': 'tabsearch_clear.png',
               'inactive': 'tabsearch_inactive.png'}
    DEFAULT_VIDEO_THUMB = Pattern('thumb-default-video.png')
    _PLAYBACK_NORMAL = Pattern('item-renderer-play.png')

    #PODCAST TABS
    _SELECTED_PODCASTS = {'folder': Pattern('NewFolder.png'),
                          'delete': Pattern('button_mv_delete_all.png')}
    #DOWNLOADING TAB
    _CANCEL_ALL_DOWNLOADS = Pattern('download-cancel.png')


    def click_item(self, title):
        self.tab_search(title)
        self.m.click(title)
        self.clear_search()

    def add_to_folder_or_delete(self, action):
        button = self._SELECTED_PODCASTS[action]
        if self.m.exists(button, 4):
            click(self.m.getLastMatch())
        else:
            self.logger.info("Can't find %s button in main view" % button)
            raise ValueError('Image not found for %s' % button)


    def hybrid_filter(self):
        self.m.find(self._FILTER_TOGGLES['three_filter'])
        if action == 'click':
            click(self.m.getLastMatch())

    def list_filter(self):
        for filter in self._FILTER_TOGGLES.iterkeys():
            if self.m.exists(filter, 1):
                break
        click(self.m.getLastMatch().right(25))

    def normal_filter(self):
        for filter in self._FILTER_TOGGLES.iterkeys():
            if self.m.exists(filter, 1):
                break
        click(self.m.getLastMatch().left(25))

    def open_podcast_settings(self):
        self.m.find(self._BUTTONS['Settings'])
        click(self.m.getLastMatch())

    def save_as_a_podcast(self):
        img = Pattern(self._BUTTONS["Save as Podcast"])
        self.logger.info('Looking for %s' % img)
        exists(img, 20)
        click(getLastMatch())

    def autodownload(self, action='click'):
        self.m.find(self._BUTTONS["Autodownload"])
        if action == 'click':
            click(self.m.getLastMatch())

    def save_as_a_playlist(self, action='click'):
        self.m.find(self._BUTTONS["Save as Playlist"])
        if action == 'click':
            click(self.m.getLastMatch())

    def multi_select(self, region, item_list):
        """Use the CTRL or CMD key as os appropriate to select items in a region.

        Return a list of the items that we successfully selected.
        """
        selected_items = []
        #press the ctrl / cmd key
        if config.get_os_name() == "osx":
                keyDown(Key.CMD)
        else:
            keyDown(Key.CTRL)
        #select each item in the list if it is found
        time.sleep(2)
        for x in item_list:
            print x
            if region.exists(x):
                region.click(x)
                time.sleep(2)
                selected_items.append(x)
        #release the ctrl /cmd key
        if config.get_os_name() == "osx":
                keyUp(Key.CMD)
        else:
            keyUp(Key.CTRL)

    def set_podcast_autodownload(self, setting="Off"):
        """Set the feed autodownload setting using the button at the bottom of the mainview.

        """
        b = Region(self.m)
        b.setY(b.getY()+500)
        b.find(self._BUTTONS["Autodownload"])
        b1 = Region(b.getLastMatch().right(80))
        for x in range(0,3):
            if not b1.exists(setting,2):
                   b.click(self._BUTTONS["Autodownload"])
                   time.sleep(2)

    def click_remove_podcast(self):
        self.m.find(self._BUTTONS['Remove Podcast'])
        click(self.m.getLastMatch())

    def delete_items(self, title, item_type):
        """Remove video audio music other items from the library.

        """
        self.tab_search(title)
        if self.m.exists(title,10):
            click(self.m.getLastMatch())
            type(Key.DELETE)
            self.dialog.remove_confirm("delete_item")

    def delete_current_selection(self):
        """Wherever you are, remove what is currently selected.

        """
        type(Key.DELETE)
        self.remove_confirm("remove")

    def tab_search(self, title, confirm_present=False):
        """enter text in the search box.

        """
        self.logger.info('Searching current tab for %s' % title)
        self.enter_search_box_text(title.upper())
        if confirm_present != False:
            term = title.split()[-1].upper()
            if self.m.exists(term, 5):
                return True
            elif self.m.exists(Pattern("item-context-button.png")):
                return True
            else:
                self.logger.info("Item %s not found in the tab" % title)
            return False

    def enter_search_box_text(self, term):
        search_box = self.clear_search()
        if search_box is not None:
            click(search_box)
        else:
            self.mtb.click(self._SEARCH["inactive"])
        type(term)


    def clear_search(self):
        if self.mtb.exists(self._SEARCH["clear"] ,5):
            self.logger.info('clearing search text')
            click(self.mtb.getLastMatch())
            return self.mtb.getLastMatch().left(10)

    def search_tab_search(self, term, engine=None):
        """perform a search in the search tab.  """
        self.enter_search_box_text(term.upper())
        # Use the search text to create a region for specifying the search engine
        if not engine:
            type(Key.ENTER)
        else:
            l = self.mtb.find(term.upper())
            l1= Region(int(l.getX()-20), l.getY(), 8, 8,)
            click(l1)
            l2 = Region(int(l.getX()-15), l.getY(), 300, 600,)
            if engine == "YouTube":
                l3 = Region(l2.find("YouTube User").above())
                l3.click(engine)
            else:
                l2.click(engine)
            type("\n") #enter the search


    def expand_item_details(self):
        if self.m.exists(Pattern("item_expand_details.png").exact()):
            click(self.m.getLastMatch())

    def toggle_normal(self):
        """toggle to the normal view.

        """
        print "toggling to normal view"
        # Find the search box to set the area.

        if self.mtb.exists(self._SEARCH["clear"], 5): # this should always be found on gtk
            treg = Region(self.mtb.getLastMatch().left(350))
        elif self.mtb.exists(self._SEARCH['inactive'] ,5):
            treg = Region(self.mtb.getLastMatch().left(350))
        treg.setH(treg.getH()+14)
        treg.setY(treg.getY()-8)
        if treg.exists(Pattern("standard-view.png").similar(.91),3):
            click(treg.getLastMatch())

    def toggle_list(self):
        """toggle to the list view.

        """
        print "toggling to list view"
        # Find the search box to set the area.
        if self.mtb.exists(self._SEARCH["clear"], 5): # this should always be found on gtk
            treg = Region(self.mtb.getLastMatch().left(350))
        elif self.mtb.exists(self._SEARCH['inactive'] ,5):
            treg = Region(self.mtb.getLastMatch().left(350))
        treg.setH(treg.getH()+14)
        treg.setY(treg.getY()-8)
        if treg.exists(Pattern("list-view.png").similar(.91),3):
            click(treg.getLastMatch())


    def download_all_items(self):
        print "downloading all the items"
        if self.m.exists(Pattern("button_download.png"),3):
            mm = []
            f = self.m.findAll("button_download.png") # find all matches
            while f.hasNext(): # loop as long there is a first and more matches
                print "found 1"
                mm.append(f.next())     # access next match and add to mm
            for x in mm:
                click(x)
        else:
            self.logger.info('No donwload badges found') 

    def check_download_started(self, title=None):
        """Tries to verify the file download started.

        Handles and already download(ed / ing) messages
        """
        if title is not None:
            self.tab_search(title)
        if self.m.exists(Pattern("badge_dl_error.png"),2):
            downloaded = "errors"
        elif self.m.exists(Pattern("item-renderer-download-pause.png"), 10):
            downloaded = "in_progress"
        else:
            downloaded = "item not located"
        return downloaded


    def wait_download_complete(self, feed_dl=True):
        """Wait for a download to complete before continuing test.

        provide title - to verify item present itemtitle_'title'.png

        """
        if self.m.exists(Pattern("item-renderer-download-pause.png"), .65):
            waitVanish(self.m.getLastMatch(), FOREVER)
        if feed_dl:
            wait(Pattern('item_play_unplayed.png'), 300)

    def cancel_all_downloads(self):
        """Cancel all in progress downloads.

        If the tab exists, cancel all dls and seeding.
        Click off downloads tab and confirm tab disappears.

        """
        if self.mtb.exists(self._CANCEL_ALL_DOWNLOADS):
            click(self.mtb.getLastMatch())
            if self.m.exists("Seeding"):
                mm = []
                f = self.m.findAll("button_download.png") # find all matches
                while f.hasNext(): # loop as long there is a first and more matches
                    print "found 1"
                    mm.append(f.next())     # access next match and add to mm
                for x in mm:
                    click(x)

    def wait_for_item(self, item, wait_time=90):
        """Search for the item and wait for it to display, or fail."""
        self.logger.info('Waiting for %s to display' % item)
        self.tab_search(item)
        return self.m.wait(item, wait_time)

    def item_metadata(self, metadata):
        """Check for a  piece of metadata displayed in  main view."""
        self.logger.info("Checking for %s" % metadata)
        if self.m.exists(metadata, 15):
            return self.m.getLastMatch()

    def wait_conversions_complete(self, reg, title, conv):
        """Waits for a conversion to complete.

        Catches the status and copies the log to a more identifyable name.
        Then it clears out the finished conversions.

        """
        while reg.m.exists(title):
            if reg.m.exists(Pattern("item-renderer-conversion-progress-left.png")):
                waitVanish(reg.m.getLastMatch(),60)
            if reg.m.exists("Open log",5):
                sstatus = "fail"
            else:
                sstatus = "pass"

            #fix - it's possible that I am clicking the wrong button
            if reg.mtb.exists("button_clear_finished.png",2) or \
               reg.mtb.exists("Clear Finished",5):
                click(reg.mtb.getLastMatch())
            return status

    def downloaded(self):
        if self.m.exists(self._PLAYBACK_NORMAL):
            return self.m.getLastMatch()

    def start_playback(self, title):
        self.tab_search(title)
        type(Key.TAB)
        type(Key.ENTER)

    def verify_video_playback(self, title):
        playback = False
        self.start_playback(title)
        if exists(Pattern("playback_bar_video.png"), 5):
            playback = True
            self.shortcut("d")
            waitVanish(Pattern("playback_bar_video.png"),20)
        return playback

    def verify_audio_playback(self, title):
        if self.m.exists("item_currently_playing.png"):
            playback = True
        else:
            playback = False
        return playback

    def stop_audio_playback(self, title):
        self.m.click(title)
        self.shortcut("d")
        self.m.waitVanish("item_currently_playing.png",20)


