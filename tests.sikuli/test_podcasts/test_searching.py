import os

from nose.tools import assert_true, assert_false, assert_equal
from nose.plugins.attrib import attr
from sikuli.Sikuli import *

from base_setup import BaseTestCase
from miro_ui import MiroApp
from miro_ui.sidebar_tab import SidebarTab
from miro_ui.main_view import MainView
from miro_ui.dialogs import Dialogs

@attr(tags=['podcast', 'search'])
class TestCasePodcastSearching(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestCasePodcastSearching, cls).setUpClass()
        cls.miro = MiroApp(cls.reg)
        cls.sidebar = SidebarTab(cls.reg)
        cls.mainview = MainView(cls.reg)
        cls.dialog = Dialogs(cls.reg)
        subscribe_file = (os.path.abspath(os.path.join('tests.sikuli',
                             'test_podcasts', 'podcast_search_feeds.miro')))
        cls.dialog.import_opml(subscribe_file)

    def test_save_search_feed(self):
        """Search in a podcast and save search as new podcast."""

        feed = "Static"
        term = "Gimp"
        title = "How"
        self.sidebar.click_podcast(feed)
        self.mainview.tab_search(term)
        self.mainview.save_as_a_podcast()
        self.sidebar.click_last("Podcasts")
        assert_true(self.mainview.item_metadata(title))
        self.sidebar.delete_podcast()
        self.dialog.remove_confirm()

    def test_save_search__spaces(self):
        """Search for podcast item with spaces in search term and save."""

        feed = "ThreeBlip"
        term = "Joo Joo"
        title = "Joo Joo"
        self.sidebar.click_podcast(feed)
        self.mainview.tab_search(term)
        self.mainview.save_as_a_podcast()
        self.sidebar.click_last("Podcasts")
        assert_true(self.mainview.item_metadata(title))
        self.sidebar.delete_podcast()
        self.dialog.remove_confirm()

    def test_search__delete_key(self):
        """Delete key works in the search tab."""
        feed = "TWO STUPID"
        title = "Flip"
        term = "dinosaur"
        self.sidebar.click_podcast(feed)
        self.mainview.tab_search(term)
        self.mainview.mtb.click(term.upper())
        for x in range(0,8):
            type(Key.LEFT)
        for x in range(0,8):
            type(Key.DELETE)

        assert_true(self.mainview.item_metadata(title))
        self.sidebar.delete_podcast()
        self.dialog.remove_confirm()


    def test_menu__new_search_feed(self):
        """From the menu, create a new search feed"""
        feed = "Static"
        term = "biking"
        title = "Travelling Two"
        self.dialog.new_search_feed(term, radio="Podcast",source=feed)
        self.sidebar.click_last("Podcasts")
        assert_true(self.mainview.item_metadata(title))
        self.sidebar.delete_podcast()
        self.dialog.remove_confirm()

    def test_dialog_search_defaults(self):
        """New search dialog uses current feed and search term as defaults.
        """
        feed = 'Static'
        term = "Voice"
        self.sidebar.click_podcast(feed)
        self.mainview.tab_search(term)

        self.dialog.new_search_feed(term, radio="Podcast", source=feed,
                                    defaults=True)
        self.sidebar.click_last("Podcasts")
        assert_true(self.mainview.item_metadata(term))
        self.sidebar.delete_podcast()
        self.dialog.remove_confirm()


    def test_watched_feeds(self):
        """Watched feeds are no included in saved search dialog sources list."""
        feed = "WatchTest"
        term = "monkey"
        folder_path = os.path.abspath(os.path.join('tests.sikuli',
                                      'TestData', 'WatchTest'))
        self.dialog.add_watched_folder(folder_path)
        self.sidebar.click_podcast("WatchTest")
        assert_true(self.dialog.new_search_feed(term, radio="Podcast", source=feed,
                                                watched=True))

    def test_remember_last_search(self):
        """Search text is remembered after switching tabs on ui."""
        feed = "TWO STUPID"
        term = "House"
        title = "Dinosaur"
        hidden_item = 'Flip'
        self.sidebar.click_podcast(feed)
        self.mainview.tab_search(term)
        assert_true(self.mainview.item_metadata(title))
        assert_false(self.mainview.item_metadata(hidden_item))
        self.sidebar.click_library_tab("Videos")
        self.sidebar.click_podcast(feed)
        assert_true(self.mainview.item_metadata(title))
        assert_false(self.mainview.item_metadata(hidden_item))


    def test_save_edited_search(self):
        """Edit remembered search and save it. """
        feed = "Static"
        first_term = 'Brooklyn'
        new_term = "Fireplace"
        first_item = 'FilmWeek'
        self.sidebar.click_podcast(feed)
        self.mainview.tab_search(first_term)
        self.sidebar.click_library_tab('Music')
        self.sidebar.click_podcast(feed) 
        self.mainview.tab_search(new_term)
        self.mainview.save_as_a_podcast()
        self.sidebar.click_last("Podcasts")
        assert_true(self.mainview.item_metadata(new_term))
        self.sidebar.delete_podcast()
        self.dialog.remove_confirm()

