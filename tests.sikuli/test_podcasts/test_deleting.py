from nose.tools import assert_true, assert_false, assert_equal
from nose.plugins.attrib import attr

from sikuli.Sikuli import *

from base_setup import BaseTestCase
from miro_ui import MiroApp
from miro_ui.sidebar_tab import SidebarTab
from miro_ui.main_view import MainView
from miro_ui.dialogs import Dialogs


@attr('current')
@attr('podcast')
class TestCaseDeletePodcasts(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestCaseDeletePodcasts, cls).setUpClass()
        cls.miro = MiroApp(cls.reg)
        cls.sidebar = SidebarTab(cls.reg)
        cls.mainview = MainView(cls.reg)
        cls.dialog = Dialogs(cls.reg)

    def test_delete__podcast(self):
        """Add an rss 2.0 feed with yahoo enclosures.
        """
        url = "http://qa.pculture.org/feeds_test/feed1.rss"
        feed = "Yah"
        self.sidebar.add_feed(url, feed)
        self.sidebar.delete_podcast()
        self.dialog.remove_confirm()
        assert_true (self.sidebar.s.waitVanish(feed, 10))

    def test_delete__downloads_inprogress(self):
        """Delete a feed with in-progress downloads.
        """
        self.feeds = ['Escape']
        url = "http://escapepod.org/feed"
        feed = "Escape"
        self.sidebar.add_feed(url, feed)
        self.mainview.download_all_items()
        assert_equal('in_progress', self.mainview.check_download_started())
        self.sidebar.delete_podcast(feed)
        self.dialog.remove_confirm()
        assert_true (self.sidebar.s.waitVanish(feed, 10))

    def test_delete__keep_downloaded(self):
        url = "http://qa.pculture.org/feeds_test/2stupidvideos.xml"
        feed = "TWO STUPID"

        #1. Add the feed and start dl
        self.sidebar.add_feed(url, feed)
        self.mainview.download_all_items()
        self.sidebar.click_library_tab('Videos')

        self.mainview.wait_for_item("Dinosaur")
        self.sidebar.delete_podcast(feed)
        self.dialog.remove_confirm(action="keep")
        self.sidebar.click_library_tab("Videos")
        assert_true(self.mainview.item_metadata("Dinosaur"))

    def test_delete__delete_downloaded(self):
        url = "http://qa.pculture.org/feeds_test/list-of-guide-feeds.xml"
        feed = "Static"
        title = "Fireplace"
        self.sidebar.add_feed(url, feed)
        self.mainview.tab_search(title)
        self.mainview.download_all_items()
        self.sidebar.click_library_tab("Videos")
        self.mainview.wait_for_item(title)
        self.sidebar.delete_podcast(feed)
        self.dialog.remove_confirm()
        self.sidebar.click_library_tab("Videos")
        assert_false(self.mainview.item_metadata(title))

    def test_delete_multiple_cancel(self):
        """Choose a to delete a few feeds then cancel."""
        self.feeds = ['Static', 'Center', 'Eats', 'pculture']
        url = "http://qa.pculture.org/feeds_test/list-of-guide-feeds.xml"
        feed = "Static"
        feedlist = ["Center", "Earth"]
        self.sidebar.add_feed(url, feed)
        for f in feedlist:
            self.mainview.tab_search(f)
            self.mainview.m.click("Add this")
        self.sidebar.click_podcast(feed)
        type(Key.DOWN,  KeyModifier.SHIFT)
        type(Key.DOWN,  KeyModifier.SHIFT)
        self.mainview.add_to_folder_or_delete('delete')
        self.dialog.remove_confirm("cancel")
        self.sidebar.click_podcast(feed)
        assert_true (self.sidebar.exists_podcast("Center"))

    def test_641(self):
        """Delete a feed that has an invalid url.
        """

        url = ("http://subscribe.getmiro.com/?url1=http%3A%2F%2F"
               "participatoryculture.org%2Ffeeds_test%2Ffeed1.rss")
        feed = "subscribe"
        self.sidebar.add_feed(url, feed, click_feed=False)
        if self.mainview.m.exists("anyway",15) or self.mainview.m.exists('Yes'):
            type(Key.ENTER)
        self.sidebar.click_last("Podcasts")
        type(Key.DELETE)
        self.dialog.remove_confirm("remove")
        assert_false(self.sidebar.exists_podcast(feed))

