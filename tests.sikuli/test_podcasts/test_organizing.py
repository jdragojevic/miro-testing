from nose.tools import assert_true, assert_false, assert_equal
from nose.plugins.attrib import attr

from sikuli.Sikuli import *

from base_setup import BaseTestCase
from miro_ui import MiroApp
from miro_ui.sidebar_tab import SidebarTab
from miro_ui.main_view import MainView
from miro_ui.dialogs import Dialogs

@attr('current')
@attr(tags=['podcast'])
class TestCasePodcastOrganizing(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestCasePodcastOrganizing, cls).setUpClass()
        cls.miro = MiroApp(cls.reg)
        cls.sidebar = SidebarTab(cls.reg)
        cls.mainview = MainView(cls.reg)
        cls.dialog = Dialogs(cls.reg)

    def test_rename(self):
        url = "http://qa.pculture.org/feeds_test/2stupidvideos.xml"
        feed = "TWO STUPID"

        #1. Add the feed and start dl
        self.sidebar.add_feed(url, feed)
        self.dialog.rename_podcast('NEW NAME')
        assert_true(self.sidebar.exists_podcast('NEW NAME'))
 
