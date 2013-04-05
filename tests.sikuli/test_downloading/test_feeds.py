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

#@attr('downloading')
#@attr('podcasts')
class TestCaseFeedDownloads(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestCaseFeedDownloads, cls).setUpClass()
        cls.miro = MiroApp(cls.reg)
        cls.sidebar = SidebarTab(cls.reg)
        cls.mainview = MainView(cls.reg)
        cls.dialog = Dialogs(cls.reg)
        subscribe_file = (os.path.abspath(os.path.join('Data',
                         'dl_feeds.miro')))
        cls.dialog.import_opml(subscribe_file)

    def check(self, check, *args):
        tc = "_".join(['check', check])
        return getattr(self, tc)(*args)

    def check_title(self, title):
        """Check title is displayed correctly."""
        self.logger.info('Check title is displayed correctly.')
        assert_true(self.mainview.item_metadata(title))

    def check_downloading(self, title=None):
        """Check downloading is in progress. """
        self.logger.info('Check downloading is in progress')
        if title:
            self.mainview.tab_search(title)
        assert_equal('in_progress', self.mainview.check_download_started())
        if title:
            self.mainview.clear_search()

    def check_thumbnail(self, thumb=None):
        """Check thumbnail updated from default. """
        self.logger.info('Check default thumb is updated')
        waitVanish(Pattern(self.mainview.DEFAULT_VIDEO_THUMB))
        if thumb:
            assert_true(exists(Pattern(thumb)))

    def check_playback(self, title):
        """Check video can be played. """
        assert_true(self.mainview.verify_video_playback(title))

    def test_zipped_enclosures(self):
        """Download feed items with gzipped enclosures.
        """
        feed = "Escape"
        self.sidebar.click_podcast(feed)
        self.mainview.download_all_items()
        self.check_downloading()
        self.click_library_tab("Downloading")
        self.mainview.cancel_all_downloads()

    def test_args_in_enclosure_url(self):
        """Items download from feed with arguments in the item url.

           Ref: http://bugzilla.pculture.org/show_bug.cgi?id=19540
        """
        url = "http://www.rtl.fr/podcast/le-fait-politique.xml"
        feed = "Le fait"
        self.sidebar.add_feed(url, feed)
        self.mainview.download_all_items()
        self.check_downloading()

    def test_feed_youtube(self):
        """Add a feed and verify items download and display correctly. """
        url = "http://gdata.youtube.com/feeds/base/users/janetefinn/uploads"
        feed = "Uploads"
        title = "Birds"
        self.sidebar.add_feed(url, feed)
        self.mainview.download_all_items()
        self.check_downloading(title)
        self.mainview.wait_download_complete()
        yield self.check, 'playback', title
        yield self.check, 'thumbnail'
        yield self.check, 'title' , title
        self.sidebar.delete_podcast(feed)

    def test_feed_vimeo(self):
        """Add a vimeo feed and verify items download and display correctly. """
        url = 'http://vimeo.com/jfinn/likes/rss' 
        feed = "Vimeo"
        title = "Unusual"
        self.sidebar.add_feed(url, feed)
        self.mainview.tab_search(title)
        self.mainview.download_all_items()
        self.check_downloading(title)
        self.mainview.wait_download_complete()
        yield self.check, 'playback', title
        yield self.check, 'thumbnail'
        yield self.check, 'title' , title

    def test_feed_itunes(self):
        """Add an itunes format feed and verify items download and display correctly. """
        url_path = os.path.join(os.getcwd(), "Data","feeds", "dilbert-feed.xml")
        url = "file://"+url_path
        feed = "Dilbert"
        title = "Survey"
        thumb = "dilbert_survey_results.png"
        self.sidebar.add_feed(url, feed)
        self.mainview.tab_search(title)
        self.mainview.download_all_items()
        self.check_downloading(title)
        self.mainview.wait_download_complete()
        yield self.check, 'playback', title
        yield self.check, 'thumbnail', thumb
        yield self.check, 'title' , title

    def test_feed_nonascii_titles(self):
        """Add feed and download item with non-ascii titles. """
        feed = "UNICODE"
        title = "El"
        thumb = "non_ascii_item.png"

        self.mainview.tab_search(term)
        self.mainview.download_all_items()
        self.check_downloading(title)
        self.mainview.wait_download_complete()
        yield self.check, 'playback', title
        yield self.check, 'thumbnail', thumb
        yield self.check, 'title' , title

    def test_items_with_spaces(self):
        """Add feed and download item with spaces in title. """
        feed = "Videos with"
        titles = ['first', 'second', 'third']
        url = 'http://qa.pculture.org/feeds_test/feed-with-spaces.rss'
        self.sidebar.add_feed(url, feed)
        self.mainview.download_all_items()
        self.mainview.wait_download_complete()
        for x in titles:
            self.mainview.tab_search(x)
            yield self.check, 'title', 'Video'

    @attr('slow')
    def test_passworded_item(self):
        """Must enter correct password to download pw protected item.

        """
        self.remove_http_auth_file()
        feed = "Yah"
        title = 'Video 4'
        url = 'http://qa.pculture.org/feeds_test/feed1.rss'
        self.sidebar.add_feed(url, feed)
        self.mainview.tab_search(title)
        self.mainview.download_all_items()
        self.dialog.http_auth('tester', 'pcf-is-the-best')
        assert_true(self.dialog.password_dialog())
        self.dialog.http_auth('tester', 'pcfdudes')
        self.mainview.wait_download_complete()
        yield self.check, 'thumbnail'
        yield self.check, 'title' , title

    def check_errors(self, title, error_img):
        self.mainview.tab_search(title)
        if title == 'Timeout error':
            if not exists(error_img[1], 10):
                error_img = error_img[0]
        assert_true(exists(Pattern(error_img), 30),
                    'Did not find %s for %s' % (error_img, title))

    def test_downloading_errors(self):
        """Verify correct display of donwload error messages. """

        feed = "ERRORS"
        self.sidebar.click_podcast(feed)
        error_types = {"Server Closes Connection": "no_connection.png",
                       "File not found": "file_not_found.png",
                       "503 Error": "no_connection.png",
                       "Host not found": "no_connection.png",
                       "HTTP error": "http_error.png",
                       "Timeout error": ["starting_up.png", 'no_connection.png'],
                       }
        for error, image in error_types.iteritems():
                yield self.check_errors, error, image
        self.click_library_tab("Downloading")
        self.mainview.cancel_all_downloads()

