#!/usr/bin/python
from sikuli.Sikuli import *
from miro_ui import MiroApp

class Dialogs(MiroApp):

    _DOWNLOAD_DIALOGS = {'downloaded': ["message_already_downloaded.png",
                                        "been downloaded"],
                         'in_progress': ["message_already_external_dl.png",
                                         "downloading now"],
                         'failed': ["badge_dl_error.png", "Error"]
                        }

    _REMOVE_CONFIRMATION_DIALOGS = ["dialog_are_you_sure.png",
                                    "dialog_one_of_these.png",
                                    "Remove",
                                    "Are you",
                                    "One of"
                                    "Cancel"]
    _EDIT_ITEM_DIALOG = "edit_item_dialog_top.png"
    _OK = "button_ok.png"

    def open_sidebar_menu(self):
        self.tl.click('idebar')

    def rename_podcast(self, new_name):
        self.open_sidebar_menu()
        self.tl.click('Rename Podcast')
        type(new_name)
        type(Key.ENTER)

    def create_feed_folder(self, folder):
        self.open_sidebar_menu()
        self.tl.click('New Folder')
        type(folder)
        type(Key.ENTER)

    def feeds_in_confirmation(self, feeds):
        feed_list = []
        for dialog_text in self._REMOVE_CONFIRMATION_DIALOGS:
            if exists(dialog_text, 2):
                d = getLastMatch().nearby(500)
                break
        else:
            raise ValueError("Did not get the confirmation dialog")
        for feed in feeds:
            if d.exists(feed):
                 feed_list.append(feed) 
        return feed_list

    def remove_confirm(self, action="remove"):
        """If the remove confirmation is displayed, remove or cancel.

        action = (remove_feed, remove_item or cancel)
        """
        if action == "remove":
            type(Key.ENTER)
        elif action == "delete_item":
            if self.sysos == "MAC":
                self.t.click("button_delete_file.png")
            else:
                self.m.click("Delete File")
        elif action == "cancel":
            type(Key.ESC)
        elif action == "keep":
                self.m.click("Keep")
                type(Key.ENTER)
        else:
            self.logger.info('Unrecognized action')

    def download_dialogs(self):
        """Handles and already download(ed / ing) messages

        """
        downloaded = 'undetermined'
        print "in function confirm dl started"
        time.sleep(5)
        mr = Region(self.mtb.above(50).below())
        for status, messages in self._DOWNLOAD_DIALOGS.iteritems():
            for message in messages:
                if mr.exists(message, 1):
                    downloaded = status
                    type(Key.ESC)
        return downloaded



    def edit_item_type(self, new_type, old_type):
        """Change the item's metadata type, assumes item is selected.

        """
        click("Rating")
        f = Region(getLastMatch())
        f.setW(200)
        f.setH(100)
        f.find("Type")
        click(f.getLastMatch().right(50))
        if old_type == "Video" and new_type == "Music":
            type(Key.UP)
        elif old_type == "Video" and new_type == "Misc":
            type(Key.DOWN)
        elif old_type == "Music" and new_type == "Video":
            type(Key.UP)
        else: 
            mouseDown(Button.LEFT)
            mouseMove(new_type)
            mouseUp(Button.LEFT)
        time.sleep(2)
        click("button_ok.png")

    def edit_item_rating(self, rating):
        """Change the item's metadata type, assumes item is selected.

        """
        click("Rating")
        click(getLastMatch().right(50))
        for x in range(0,int(rating)):
            type(Key.DOWN)
        type(Key.ENTER)
        click("button_ok.png")


    def edit_item_general_metadata(self, new_metadata):
        """Given the field and new metadata value, edit a selected item, or multiple items metadata.

        """
        pulldown_menus = ["Rating", "Type", "Video Kind"]
        self.shortcut('i')
        exists(self._EDIT_ITEM_DIALOG, 5)
        metar = Region(getLastMatch()).below(500)
        for meta_field, meta_value in new_metadata:
            metar.find(meta_field)
            if meta_field == 'Name':
                type(Key.BACKSPACE)
            else:
                click(metar.getLastMatch().right(80))
            if meta_field in pulldown_menus:
                metar.click(meta_value)
            elif meta_field == "Art":
                metar.click("Click to")
                type(meta_value)
                type(Key.ENTER)
            else:
                type(meta_value)

        metar.click(self._OK)

    def edit_item_video_metadata_bulk(self,new_metadata_list):
        """Given the field and new metadata value, edit a selected item
           or mulitple items metadata.

        """
        metalist = ["show","episode_id","season_no","episode_no",
                         "video_kind","cancel","ok"]
        self.shortcut('i')
        time.sleep(2)
        find("Rating")
        v = Region(getLastMatch().above(100).left(60))
        v.click("Video")
        if exists("Show"):
            top_tab = getLastMatch().right(200)
            click(top_tab)
            metar = Region(getLastMatch().below())
            metar.setW(metar.getW()+300)
        else:
            print("Can not find show field")
        for meta_field,meta_value,req_id in new_metadata_list:
            print meta_field,meta_value
            for i in (i for i,x in enumerate(metalist) if x == meta_field):
                rep = i
                print rep,meta_field
            for x in range(0,rep): #tab to the correct field
                type(Key.TAB)
                time.sleep(.5)
            if meta_field == "video_kind":
                #need a space bar to open the text entry field
                type(" ")
                metar.click(meta_value)
            else:
                type(meta_value) #enter the new value
                #go back to the top field, Show
            if req_id:
                self.log_result(req_id,"value edited in dialog")
            click(top_tab)
        ok_but = len(metalist)
        for x in range(1,ok_but):
            type(Key.TAB)
            time.sleep(.5)
        type(Key.ENTER) #Save the changes

    def store_item_path(self):
        """Return the items file path from the edit item dialog via clipboard.

        """
        if self.sysos == "MAC":
            self.m.find("Path")
            pr = Region(self.m.getLastMatch()).right(500)
            pr.setX(pr.getX()+15)
            pr.setY(pr.getY()-10)
            pr.setH(pr.getH()+20)
            pr.highlight(5)
            mypath = pr.text()
            print mypath
            filepath = mypath
        else:
            for x in range(0,11):
                type(Key.TAB)
            self.shortcut('c')
            filepath = Env.getClipboard()
            type(Key.ESC) #ESC to close the dialog
        return filepath

    def change_podcast_settings(self, option, setting):
        find("Expire Items")
        p1 = Region(getLastMatch().nearby(800))
        p1.find(option)
        click(p1.getLastMatch().right(100))
        if not p1.exists(setting):
            type(Key.PAGE_DOWN)
        if not p1.exists(setting):
            type(Key.PAGE_UP)
        if setting == "Keep 0":
            type(Key.DOWN)
            time.sleep(1)
            type(Key.ENTER)
        else:
            p1.click(setting)
        time.sleep(2)
        p1.click("button_done.png")

    def new_search_feed(self, term, radio, source, defaults=False, watched=False):
        self.logger.info("Opening the New Search Feed dialog.")
        self.tl.click('idebar')
        self.tl.click("New Search")
        if defaults:
            self.logger.info("Accepting default settings.")
            type(Key.ENTER)
            return
        wait('Create Podcast', 10)
        f = Region(getLastMatch().left(600).above(300))
        if watched:
            self.logger.info('Watched feeds should not be listed.')
            if f.exists(source):
                type(Key.ESC)
                raise ValueError("%s exists when it should not." % source)
            else:
                return True
        self.logger.info("Entering the search term: %s" % term)
        type(term)
        f = Region(getLastMatch().left(600).above(300))
        self.logger.info("Clicking the %s radio button" %radio)
        f.click(radio)
        if radio == "URL":
            click(f.getLastMatch().right(150))
            type(source)
        else:
            self.logger.info('Choosing the feed %s as search source' % source)
            if not f.exists(source, 2):
                click(f.getLastMatch().right(150))
                #f.click(self.OPTION_EXPAND)
                f.click(source)
                time.sleep(1)
        click("Create Podcast")

    def add_watched_folder(self, folder_path, show=True):
        """Add a watched folder via the dialog. """
        self.tl.wait("File", 10)
        self.tl.click("File")
        self.tl.click("Import")
        click("Watch")
        time.sleep(1)
        type(folder_path)
        if not show:
            self.m.click("Show in")
            type(Key.TAB)
            type(Key.TAB)
        type(Key.ENTER)


    def open_file(self, filename):
        self.shortcut('o')
        self.type_a_path(filename)

    def import_opml(self, opml_path):
        self.t.click("idebar")
        self.t.click("Import")
        self.type_a_path(opml_path)
        if exists("imported", 15):
            type(Key.ENTER)

