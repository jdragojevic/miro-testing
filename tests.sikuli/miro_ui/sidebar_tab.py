# All actions on the preferences panel
#!/usr/bin/python
from sikuli.Sikuli import *
from miro_ui import MiroApp


class SidebarTab(MiroApp):
    _FIXED_LIB_TABS_IMG = "sidebar_top.png"
    _FIXED_TABS = ["Miro", "Videos", "Music"]
    _HIDEABLE_TABS = ["Misc", "Downloading", "Converting"]
    _MOVEABLE_TABS = ["Misc", "Downloading", "Converting", "Search", "Connect"]
    _EXPANDABLE_TABS = ["Sources", "Stores", "Podcasts", "Playlists"]

    def _fixed_library_region(self):
        find(Pattern(self._FIXED_LIB_TABS_IMG).similar(0.5))
        fl = Region(getLastMatch())
        fl.setX(fl.getX()-10)
        fl.setW(self.s.getW())
        print fl
        return fl

    def _moveable_library_region(self):
        ml = self._fixed_library_region()
        ml.setY(ml.getY() + ml.getH())
        moveable_hgt = int(ml.getH()) * 1.45
        ml.setH(int(moveable_hgt))
        return ml

    def _expandable_tab_region(self, tab):
        """ Find the Region of the contents of expandible tabs.

        May have to page down in the sidebar to find the tab if there are many items.
        """
        r = self.s.offset(Location(0, 120))
        try:
            r.click(tab)
        except:
            r.click('Connect')
            r.click(tab)
        tab_rg = Region(r.getLastMatch())
        topx = int(tab_rg.getX() * .5)
        topy = tab_rg.getY()
        if self._EXPANDABLE_TABS.index(tab) + 1 >= len(self._EXPANDABLE_TABS):
            height = self.s.getH() + 20
        else:
            self.s.find(self._EXPANDABLE_TABS[self._EXPANDABLE_TABS.index(tab)+1])
            height = (tab_rg.getY() + 20) - Region(self.s.getLastMatch()).getY()
        width = self.s.getW()
        tab_region = Region(topx, topy, width, height)
        tab_region.setAutoWaitTimeout(20)
        return tab_region

    def find_library_tab(self, tab):
        """Click any default tab in the sidebar.

        """
        self.logger.info('Locating the  %s library tab.' % tab)
        if tab in self._FIXED_TABS:
            tabloc = self._fixed_library_region()
        elif tab in self._MOVEABLE_TABS:
            tabloc = self._moveable_library_region()
        elif tab in self._EXPANDABLE_TABS:
            tabloc = self._expandable_tab_region(tab)
        else:
            print "%s is an unrecognized library tab" % tab
        click(Pattern(self._FIXED_LIB_TABS_IMG).similar(0.5))
        if tabloc.exists(tab, 2):
            return Region(tabloc.getLastMatch())
        if tab in self._HIDEABLE_TABS:
            self.logger.info('Tab %s is not displayed' % tab)

    def click_library_tab(self, tab):
        self.logger.info('Clicking the %s tab' % tab)
        tr =  self.find_library_tab(tab)
        if tr:
            click(tr)
            return tr

    def click_podcast(self, podcast):
        self.logger.info('Clicking the podcast: %s' % podcast)
        podcast_region = self._expandable_tab_region("Podcasts")
        if podcast_region.exists(podcast, 25):
            click(podcast_region.getLastMatch())
            return Region(podcast_region.getLastMatch())

    def exists_podcast(self, podcast):
        self.logger.info('Checking if feed %s in sidebar' %podcast)
        podcast_region = self._expandable_tab_region("Podcasts")
        if podcast_region.exists(podcast, 10):
            return podcast_region.getLastMatch()

    def click_playlist(self, playlist):
        self.logger.info('Clicking the %s playlist tab' % playlist)
        playlist_region = self._expandable_tab_region("Playlists")
        playlist_region.click(playlist)
        return Region(playlist_region.getLastMatch())

    def click_source(self, source):
        self.logger.info('Clicking the %s source tab' % source)
        source_region = self._expandable_tab_region("Source")
        source_region.click(source)
        return Region(source_region.getLastMatch())

    def click_store(self, store):
        self.logger.info('Clicking the %s store tab' % store)
        store_region = self._expandable_tab_region("Store")
        store_region.click(store)
        return Region(store_region.getLastMatch())

    def click_last(self, section):
        self.logger.info('Clicking the last item in  %s section' % section)
        self.click_library_tab(section)
        if section == 'Playlists':
           raise ValueError('click_last does not work for Playlists')
        else:
            tab = self._EXPANDABLE_TABS[self._EXPANDABLE_TABS.index(section)+1]
            self.click_library_tab(tab)
            time.sleep(1)
            type(Key.UP)

    def add_feed(self, url, feed, click_feed=True):
        """Add a feed to miro, click on it in the sidebar.
        """
        self.logger.info("Adding the podcast: %s" % url)
        self.shortcut('n')
        time.sleep(2)
        type(url + "\n")
        if click_feed: self.click_podcast(feed)

    def delete_podcast(self, podcast=None):
        """Delete a podcast from the sidebar tab."""
        self.logger.info('Deleting the podcast: %s' % podcast)
        if podcast is not None:
            self.click_podcast(podcast)
        type(Key.DELETE)
