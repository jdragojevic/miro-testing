from nose.tools import assert_true, assert_false, assert_equal
from nose.plugins.attrib import attr

from sikuli.Sikuli import *

from base_setup import BaseTestCase
from miro_ui import MiroApp
from miro_ui.sidebar_tab import SidebarTab
from miro_ui.main_view import MainView
from miro_ui.dialogs import Dialogs

@attr(tags=['podcast'])
class TestCaseSubscribePodcasts(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestCaseSubscribePodcasts, cls).setUpClass()
        cls.miro = MiroApp(cls.reg)
        cls.sidebar = SidebarTab(cls.reg)
        cls.mainview = MainView(cls.reg)
        cls.dialog = Dialogs(cls.reg)


    def check_podcast_metadata(self, *args):
        """Verify feed has metadata."""
        check = args[0][1]
        assert_true(self.mainview.item_metadata(check), 'not found %s' % check)

    def item_not_present(self, metadata):
        assert_false(self.mainview.item_metadata(metadata), 'found %s' 
                     % metadata)


    def test_rss20_yahoo(self):
        """Add an rss 2.0 feed with yahoo enclosures.
        """
        url = "http://qa.pculture.org/feeds_test/feed1.rss"
        feed = "Yah"
        self.sidebar.add_feed(url, feed)
        data_checks = {'description': 'download quickly',
                       'title': 'Video',
                      }
        for d in data_checks.items():
            yield self.check_podcast_metadata, d


    def test_yahoo_and_rss_enclosures(self):
        """Add an rss 2.0 feed with yahoo and rss enclosures.
        """
        url = "http://qa.pculture.org/feeds_test/feed3.rss"
        feed = "RSS 2"
        self.sidebar.add_feed(url, feed)
        data_checks = {'description': 'download quickly',
                       'title': 'Video',
                      }
        for d in data_checks.items():
            yield self.check_podcast_metadata, d

    def test_no_enclosures(self):
        """RSS 2.0 feed with no enclosures, video 2 should not display.
        """
        url = "http://qa.pculture.org/feeds_test/no-enclosures.rss"
        feed = "No enclosures"
        self.sidebar.add_feed(url, feed)
        data_checks = {'description': 'should work',
                       'title': 'Video',
                      }
        for d in data_checks.items():
            yield self.check_podcast_metadata, d
        yield self.item_not_present, "second test"

    def test_zipped_enclosures(self):
        """Add a feed with gzipped enclosures.
        """
        self.feeds = ['Escape']
        url = "http://escapepod.org/feed"
        feed = "Escape"
        self.sidebar.add_feed(url, feed)
        self.mainview.download_all_items()
        assert_equal('in_progress', self.mainview.check_download_started())


    @attr('current')
    def test_argss_in_enclosure_url(self):
        """Items download from feed with arguments in the item url.

           Ref: http://bugzilla.pculture.org/show_bug.cgi?id=19540
        """
        self.feeds = ['Le fait']
        url = "http://www.rtl.fr/podcast/le-fait-politique.xml"
        feed = "Le fait"
        self.sidebar.add_feed(url, feed)
        self.mainview.download_all_items()
        assert_equal('in_progress', self.mainview.check_download_started())

    def test_add_duplicate(self):
        url = "http://qa.pculture.org/feeds_test/feed1.rss"
        feed = "Yah"
        self.sidebar.add_feed(url, feed)
        self.mainview.download_all_items()
        self.sidebar.add_feed(url, feed)
        self.sidebar.click_library_tab('Podcasts')
        assert_equal (1, self.sidebar.count_images(feed, self.sidebar.s))

