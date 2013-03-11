import os

from nose.tools import assert_true, assert_false, assert_equal
from nose.plugins.attrib import attr

from sikuli.Sikuli import *

from base_setup import BaseTestCase
from miro_ui import MiroApp
from miro_ui.sidebar_tab import SidebarTab
from miro_ui.main_view import MainView
from miro_ui.dialogs import Dialogs

@attr('downloading')
class TestCaseIndividualDownloads(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestCaseIndividualDownloads, cls).setUpClass()
        cls.miro = MiroApp(cls.reg)
        cls.sidebar = SidebarTab(cls.reg)
        cls.mainview = MainView(cls.reg)
        cls.dialog = Dialogs(cls.reg)

    def check(self, check, *args):
        tc = "_".join(['check', check])
        return getattr(self, tc)(*args)

    def check_title(self, title):
        """Check title is displayed correctly."""
        self.logger.info('Check title is displayed correctly.')
        assert_true(self.mainview.item_metadata(title))


    def check_thumbnail(self, thumb=None):
        """Check thumbnail updated from default. """
        self.logger.info('Check default thumb is updated')
        waitVanish(Pattern(self.mainview.DEFAULT_VIDEO_THUMB))
        if thumb:
            assert_true(exists(Pattern(thumb)))

    def check_playback(self, title):
        """Check video can be played. """
        assert_true(self.mainview.verify_video_playback(title))

    def check_downloading(self, title=None):
        """Check downloading is in progress. """
        self.logger.info('Check downloading is in progress')
        if title:
            self.mainview.tab_search(title)
        assert_equal('in_progress', self.mainview.check_download_started())
        if title:
            self.mainview.clear_search()

    def download_and_locate(self, url, title):
        self.dialog.download_from_a_url(url)
        if self.sidebar.click_library_tab('Downloading'):
            if title == 'watch':
                return
            self.check_downloading(title)
            self.mainview.wait_download_complete(feed_dl=False)
        self.sidebar.click_library_tab('Videos')
        self.mainview.wait_for_item(title)

    def test_file_download(self):
        """Download a file from a url."""
        url = 'http://qa.pculture.org/amara_tests/Birds_short.oggtheora.ogg'
        title = "Birds"
        self.download_and_locate(url, title)
        yield self.check, 'playback', title
        yield self.check, 'thumbnail'
        yield self.check, 'title' , title

    def test_youtube_download(self):
        """Download a youtube individual file. """
        url = "http://www.youtube.com/watch?v=5pB3gAjivrY"
        title = "Andrew"
        thumb = "andrew_garcia_straight_up.png"
        self.download_and_locate(url, title)
        yield self.check, 'playback', title
        yield self.check, 'thumbnail', thumb
        yield self.check, 'title' , title

    def test_https_download(self):
        """Download a file with https url """
        url = "https://www.youtube.com/watch?v=pOle1AnPOc4"
        title = "Charlie"
        thumb = "charlie_bit_me.png"
        self.download_and_locate(url, title)
        yield self.check, 'playback', title
        yield self.check, 'thumbnail', thumb
        yield self.check, 'title' , title

    @attr('torrent')
    def test_torrent_download(self):
        url = "http://bitlove.org/jed/feed1/py1.mov.torrent"
        title = 'py1'
        self.download_and_locate(url, title)
        yield self.check, 'playback', title
        yield self.check, 'title' , title

    @attr('torrent')
    def test_magnet_download(self):
        url = ("magnet:?xt=urn:btih:29b30533f99a7a9d199babc57729f765bd0ee7ef"
               "&dn=Stargazer%20%7C%20Creative%20Commons%20PDF%20eBook%20Sci"
               "ence%20Fiction%20Novel&tr=udp%3A%2F%2Ftracker.openbittorrent"
               ".com%3A80&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80&tr=udp%3A"
               "%2F%2Ftracker.ccc.de%3A80")
        self.dialog.download_from_a_url(url)
        self.sidebar.click_library_tab('Downloading')
        self.check_downloading('Stargazer')
        self.mainview.cancel_all_downloads()

    @attr('torrent')
    def test_open_torrent_file(self):
        torrent_file = (os.path.abspath(os.path.join('tests.sikuli',
                          'test_downloading', 
                          'paz - young broke and fameless_ the mixtape.torrent')))
        self.dialog.open_file(torrent_file)
        self.sidebar.click_library_tab('Downloading')
        self.check_downloading('paz')
        self.mainview.cancel_all_downloads()

    def test_dl_errors(self):
        """On download failure, file stays in downloading tab, showing error.

        """
        url = "http://www.youtube.com/watch?v=LU-ZQWZSGfc&feature=fvhr"
        title = "watch"
        self.download_and_locate(url, title)
        assert_true(exists(Pattern("file_not_found.png")))

    def test_503_retry(self):
        """Retry dialog displayed when file download returns 503 retry later.

        """
        url = "http://qa.pculture.org/feeds_test/503.php"
        self.dialog.download_from_a_url(url)
        for x in range(0,2):
            assert_true(exists(Pattern("retry_dialog.png").similar(0.5), 5))
            type(Key.ENTER)
        assert_true(exists(Pattern("retry_dialog.png").similar(0.5), 5))
        type(Key.ESC)
        time.sleep(4)
        assert_true(waitVanish(Pattern("retry_dialog.png").similar(0.5), 3))


