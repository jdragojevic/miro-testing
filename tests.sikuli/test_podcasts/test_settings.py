from nose.tools import assert_true, assert_false, assert_equal
from nose.plugins.attrib import attr

from sikuli.Sikuli import *

from base_setup import BaseTestCase
from miro_ui import MiroApp
from miro_ui.sidebar_tab import SidebarTab
from miro_ui.main_view import MainView
from miro_ui.dialogs import Dialogs

@attr(tags=['podcast'])
class TestCasePodcastSettings(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestCasePodcastSettings, cls).setUpClass()
        cls.miro = MiroApp(cls.reg)
        cls.sidebar = SidebarTab(cls.reg)
        cls.mainview = MainView(cls.reg)
        cls.dialog = Dialogs(cls.reg)


    def test_clear_old_items(self):
        """Use podcast settings dialog to clear out old items. """
        url = "http://bluesock.org/~willg/cgi-bin/newitemsfeed.cgi"
        feed = "my feed"
        self.sidebar.add_feed(url, feed)
        self.sidebar.click_library_tab("Podcasts")
        self.mainview.tab_search("my feed")
        self.mainview.toggle_list()
        self.sidebar.click_podcast(feed)
        for x in range(0,3):
            self.sidebar.shortcut("r")
            time.sleep(3)
        self.mainview.open_podcast_settings()
        self.dialog.change_podcast_settings(option="Podcast Items",
                                            setting="Keep 0")
        self.mainview.click_library_tab("Podcasts")
        assert_equal(5, self.mainview.count_images(img="my feed"))
