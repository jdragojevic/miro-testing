import os
import time

from nose.tools import assert_true, assert_false, assert_equal 
from nose.plugins.attrib import attr

from sikuli.Sikuli import *

from base_setup import BaseTestCase
from miro_ui import MiroApp
from miro_ui.sidebar_tab import SidebarTab
from miro_ui.main_view import MainView
from miro_ui.dialogs import Dialogs


@attr(tags='podcast')
class TestCaseRenameFeed(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestCaseRenameFeed, cls).setUpClass()
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

@attr('podcast')
class TestCaseFolders(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestCaseFolders, cls).setUpClass()
        cls.miro = MiroApp(cls.reg)
        cls.sidebar = SidebarTab(cls.reg)
        cls.mainview = MainView(cls.reg)
        cls.dialog = Dialogs(cls.reg)

    def add_feeds_opml(self):
        subscribe_file = (os.path.abspath(os.path.join('tests.sikuli',
                             'test_podcasts', 'podcast_folders.miro')))
        self.dialog.import_opml(subscribe_file)

    def test_create_folder(self):
        """Create a new feed folder. """
        folder = 'MY FEEDS'
        self.feeds = [folder]
        self.dialog.create_feed_folder(folder)
        assert_true(self.sidebar.exists_podcast(folder))

    def test_rename_folder(self):

        """Create a new feed folder. """
        folder = 'INCREDIBLE'
        new_name = 'AWFUL'
        self.feeds = [folder]
        self.dialog.create_feed_folder(folder)
        self.sidebar.click_podcast(folder)
        self.dialog.rename_podcast(new_name)
        assert_true(self.sidebar.exists_podcast(new_name))

    def test_create_and_delete_folder_with_feeds(self):
        """Select multiple feeds and add them to a folder."""
        self.add_feeds_opml()
        folder = 'FAV FEEDS'
        feeds = [folder, 'ONION', 'LES', 'VIM', 'BIRCHBOX']
        self.sidebar.click_podcast(feeds[1])
        for x in range(len(feeds)-1):
            type(Key.DOWN,  KeyModifier.SHIFT)
        self.mainview.add_to_folder_or_delete('folder')
        type(folder)
        type(Key.ENTER)
        self.sidebar.click_podcast(folder)
        self.sidebar.delete_podcast(folder)
        del_feeds = self.dialog.feeds_in_confirmation(feeds)
        self.dialog.remove_confirm()
        self.feeds = [x for x in feeds if x not in del_feeds]
        self.feeds.append('GEEKY')
        assert_equal(del_feeds, feeds,
                     'Did not find %s in %s' % (del_feeds, feeds))

    def test_drag_feeds_to_folder(self):
        """Select multiple feeds and add them to a folder."""
        self.add_feeds_opml()
        folder = 'GEEKY'
        y = find(folder)
        feeds = [folder, 'ONION', 'LES', 'VIMEO', 'BIRCHBOX']
        p = self.sidebar.click_podcast(feeds[1])
        for x in range(len(feeds)-1):
            type(Key.DOWN,  KeyModifier.SHIFT)
        mouseDown(Button.LEFT)
        mouseMove(y)
        dropAt(y)
        self.sidebar.click_podcast(folder)
        self.sidebar.delete_podcast(folder)
        del_feeds = self.dialog.feeds_in_confirmation(feeds)
        self.dialog.remove_confirm()
        self.feeds = [x for x in feeds if x not in del_feeds]
        assert_equal(del_feeds, feeds,
                     'Did not find %s in %s' % (del_feeds, feeds))

    def test_reorder_feeds(self):
        """Reorder feeds in the sidebar."""
        self.add_feeds_opml()
        time.sleep(3)
        self.feeds = ['GEEKY', 'ONION', 'LES', 'VIM', 'BIRCHBOX']
        feed1 = 'GEEKY'
        feed2 = 'VIM'
        y = self.sidebar.exists_podcast(feed2)
        x = self.sidebar.exists_podcast(feed1)
        dragDrop(x,y.right(40).above(30))
        time.sleep(2)
        gloc = self.sidebar.exists_podcast(feed1)
        gloc.setX(gloc.getX() -10)
        gloc.setW(gloc.getW() +30)
        above = gloc.above(300)
        assert_true(above.exists(feed2))

