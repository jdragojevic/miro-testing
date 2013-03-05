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

@attr('downloading')
@attr('torrent')
class TestCaseTorrentFeeds(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestCaseTorrentFeeds, cls).setUpClass()
        cls.miro = MiroApp(cls.reg)
        cls.sidebar = SidebarTab(cls.reg)
        cls.mainview = MainView(cls.reg)
        cls.dialog = Dialogs(cls.reg)
        subscribe_file = (os.path.abspath(os.path.join('tests.sikuli',
                             'test_downloading', 'dl_feeds.miro')))
        #cls.dialog.import_opml(subscribe_file)

    def check(self, check, *args):
        tc = "_".join(['check', check])
        return getattr(self, tc)(*args)

    def check_title(self, title):
        """Check title is displayed correctly."""
        self.logger.info('Check title is displayed correctly.')
        assert_true(self.mainview.item_metadata(title))

    def check_downloading(self):
        """Check downloading is in progress. """
        self.logger.info('Check downloading is in progress')
        assert_equal('in_progress', self.mainview.check_download_started())

    def check_thumbnail(self, thumb=None):
        """Check thumbnail updated from default. """
        self.logger.info('Check default thumb is updated')
        waitVanish(Pattern(self.mainview.DEFAULT_VIDEO_THUMB))
        if thumb:
            assert_true(exists(Pattern(thumb)))

    def check_playback(self, title):
        """Check video can be played. """
        assert_true(self.mainview.verify_video_playback(title))

    def check_db_size(self):
        return os.path.getsize(self.get_db())


    def check_errors(self, title, error_img):
        self.mainview.tab_search(title)
        assert_true(exists(Pattern(error_img), 30),
                    'Did not find %s for %s' % (error_img, title))

    def test_empty_container(self):
        """Torrent item that point to empty dir gives corrupt torrent error.

        """
        feed = "Empty"
        url = 'http://qa.pculture.org/feeds_test/feed20.rss'
        self.sidebar.add_feed(url, feed)
        self.mainview.download_all_items()
        self.check_errors(feed, 'corrupt_torrent.png')

    def test_password_protected(self):
        """Must provide valid pw before protected feed is displayed.

        """
        self.remove_http_auth_file()
        feed = "Empty"
        url = 'http://qa.pculture.org/feeds_test/torrentpasswordrss.rss'
        self.sidebar.add_feed(url, feed, click_feed=False)
        self.dialog.http_auth('tester', 'pcf-is-the-best')
        assert_true(self.dialog.password_dialog())
        self.dialog.http_auth('miro1', 'pcf.torrent')
        assert_true(self.sidebar.exists_podcast('Extra Videos'))

    def test_duplicate_items(self):
        """Display one 1 item in download tab for duplicate torrents.

        """
        feed_url = 'http://feeds.feedburner.com/VodoPromotedWorks'
        feed = 'VODO'
        title = 'Mixtape'
        legit_title = 'download'

        torrent_url = ('http://www.legittorrents.info/download.php?id='
                      '7c4614f70d6132c645c54e8594d792fb39759133&f='
                      'VODO+Mixtape+%231+%282010+Xvid%29.torrent')
        self.logger.info('Download Mixtape item from VODO feed')
        self.sidebar.add_feed(feed_url, feed)
        self.mainview.tab_search(title)
        self.mainview.download_all_items()
        self.sidebar.click_library_tab("Downloading")
        self.logger.info('Add legittorrent url for item with same hash')
        self.dialog.download_from_a_url(torrent_url)
        self.logger.info('Wait for second item to appear')
        assert_true(self.mainview.m.exists(legit_title, 20))
        self.logger.info('Check item vanishes')
        assert_true(waitVanish(self.mainview.m.getLastMatch(), 40))
        self.mainview.cancel_all_downloads()
        self.logger.info('Check item displays after 1 dl is cancelled.')
        assert_true(self.mainview.m.exists(legit_title, 20))
        self.mainview.cancel_all_downloads()


    def test_bogus_data_torrent(self):
        """Corrupt torrent files are detected, not downloaded or stored in db.

        """
        feed = "Bogus"
        url = 'http://qa.pculture.org/feeds_test/hugebogustorrent.rss'
        self.sidebar.add_feed(url, feed)
        b4_dl_db_size = self.check_db_size()
        self.mainview.download_all_items()
        corruptions = ['Zeroed', 'Bencoded Zero', 'Bencoded Almost Correct']
        for c in corruptions:
            yield self.check_errors, c, 'corrupt_torrent.png'
        assert_equal(self.check_db_size(), b4_dl_db_size)
        self.logger.info(b4_dl_db_size)

    @attr('slow')
    def test_video_torrent_dl(self):
        """Add a torrent feed and check that items download and playback"""
        url = "http://www.suprnova.org/shows/the-infographics-show/feed"
        feed = "SuprNova"
        title = "Fast Food"
        self.sidebar.add_feed(url, feed)
        self.mainview.tab_search(title)
        self.mainview.download_all_items()
        self.check_downloading()
        self.sidebar.click_library_tab('Videos')
        self.mainview.wait_for_item(title, wait_time=1000)
        yield self.check, 'playback', title
        yield self.check, 'thumbnail'
        yield self.check, 'title' , title

