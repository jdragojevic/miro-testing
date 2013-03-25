from nose.tools import assert_true, assert_false, assert_equal
from nose.plugins.attrib import attr

from sikuli.Sikuli import *

from base_setup import BaseTestCase
from miro_ui import MiroApp
from miro_ui.sidebar_tab import SidebarTab
from miro_ui.main_view import MainView
from miro_ui.dialogs import Dialogs


@attr('settings')
@attr('podcast')
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
        self.mainview.toggle_list()
        for x in range(0,3):
            self.sidebar.shortcut("r")
            self.mainview.m.exists('status-icon-new.png', 5)
            time.sleep(2)
        self.mainview.open_podcast_settings()
        self.dialog.change_podcast_settings(option="Podcast Items",
                                            setting="Keep 0")
        time.sleep(3)
        assert_equal(5, self.mainview.count_images(img="newly.png"))
