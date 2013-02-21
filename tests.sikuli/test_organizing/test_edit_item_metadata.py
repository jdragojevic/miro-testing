from base_setup import BaseTestCase
from sikuli.Sikuli import *
from miro_ui import MiroApp
from miro_ui.sidebar_tab import SidebarTab
from miro_ui.main_view import MainView
from miro_ui.dialogs import Dialogs
from nose.tools import assert_true

class TestCaseEditItemMetadata(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestCaseEditItemMetadata, cls).setUpClass()
        cls.miro = MiroApp(cls.reg)
        cls.sidebar = SidebarTab(cls.reg)
        cls.mainview = MainView(cls.reg)
        cls.dialog = Dialogs(cls.reg)

    def test_edit_metadata(self):
        """Edit metadata for mulitple items.

        1. add Static List feed
        2. download the Earth Eats item
        3. Edit item metadata
        """
        self.feeds = ['Static']
        url = "http://qa.pculture.org/feeds_test/list-of-guide-feeds.xml"
        feed = "Static"
        term = "Fireplace"
        title = "Fireplace"
        self.sidebar.add_feed(url, feed)
        metadata_list = [("Name", "Earth Day Everyday"),
                         ("Artist", "Oliver and Katerina"),
                         ("Album", "Barki Barks"),
                         ("Genre", "family"),
                        ]
        self.mainview.tab_search(term)
        self.mainview.download_all_items()
        self.sidebar.click_library_tab("Videos")
        self.mainview.wait_for_item(item=title)
        self.mainview.click_item(title)
        self.dialog.edit_item_general_metadata(metadata_list)
        assert_true (self.mainview.item_metadata('Earth Day'))

