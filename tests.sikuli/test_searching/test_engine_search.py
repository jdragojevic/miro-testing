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

@attr('search')
class TestCaseWebSearching(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestCaseWebSearching, cls).setUpClass()
        cls.miro = MiroApp(cls.reg)
        cls.sidebar = SidebarTab(cls.reg)
        cls.mainview = MainView(cls.reg)
        cls.dialog = Dialogs(cls.reg)


    def check_saved_search(self, engine, term):
        """Verify search saved as a podcast"""
        if engine == 'User':
            engine = 'Youtube User'
        feed_name = "%s for %s" % (engine, term)
        assert_true(self.mainview.tab_search(feed_name, confirm_present=True))

    def test_search_engine_podcast(self):
        """Save a feed of search engine results.  """
        self.sidebar.click_library_tab("Search")

        searches = {"Blip": "python",
                    "YouTube": "cosmicomics",
                    "User": 'janetefinn',
                    "DailyMotion": "Russia",
                    "Google": "Toronto",
                    "5min": "eat fire",
                    "Search All": "shark"}

        for engine, term in searches.iteritems():
            self.mainview.search_tab_search(term, engine)
            self.mainview.save_as_a_podcast()
            time.sleep(4)
        pr = self.sidebar.click_library_tab("Podcasts")
        for engine, term in searches.iteritems():
            yield self.check_saved_search, engine, term

    def test_remember_last_search(self):

        term = 'President Obama'
        engine = 'Blip'
        self.sidebar.click_library_tab("Search")
        self.mainview.search_tab_search(term, engine)
        time.sleep(4)
        self.sidebar.click_library_tab("Podcasts")
        self.sidebar.click_library_tab("Search")
        assert_true(exists(term.upper()))


    def test_menu__new_search_feed(self):
        """Create a search podcast via the New Search menu. """
        engine = 'Blip'
        term = 'WHITE TIGERS'

        self.dialog.new_search_feed(term=term, radio="Search", source=engine)
        self.sidebar.click_library_tab("Podcasts")
        self.check_saved_search(engine, term)

    def test_80(self):
        """Create a search podcast by scraping a url."""

        source = "http://www.ubu.com"
        term = "MP3"
        self.dialog.new_search_feed(term=term, radio='URL', source=source)
        if exists("compatible",45):
            type(Key.ENTER)
        time.sleep(10)
        self.sidebar.click_library_tab("Podcasts")
        self.check_saved_search(source, term)


