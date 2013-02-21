from sikuli.Sikuli import *
import nose
import subprocess
import os
import time
import shutil

class BaseTestCase(object):

    @classmethod
    def setUpClass(cls):
#        Settings.ActionLogs = False
#        Settings.InfoLogs = False
#        Settings.DebugLogs = False
        oses = ['LINUX', 'WINDOWS', 'MAC']
        cls.sysos = [o for o in oses if o in str(Env.getOS())][0]
        cls.reset_db()
        cls.set_image_dirs()
        cls.launch_miro()

        print 'setting up the image regions'
        cls.reg = cls.get_regions()

    @classmethod
    def tearDownClass(cls):
        cls.quit_miro()
        cls.reset_db()

    def tearDown(self):
        try:
            for f in self.feeds:
                if self.sidebar.exists_podcast(f):
                    self.sidebar.delete_podcast(f)
                    self.dialog.remove_confirm()
        except AttributeError:
            pass 

    @classmethod
    def quit_miro(cls):
        os.system("killall -v -I Miro miro.real")


    @classmethod
    def set_image_dirs(cls):
        shared_images = os.path.join('Images', 'SHARED')
        image_dirs = [os.path.join('Images', cls.sysos)]
        for d in os.listdir(shared_images):
            image_dirs.append(os.path.join(shared_images, d))
        [addImagePath(os.path.abspath(x)) for x in image_dirs if x not in list(getImagePath())]


    @classmethod
    def get_regions(cls):
        wait(Pattern("sidebar_top.png").similar(0.6), 15)
        click(Pattern("sidebar_top.png").similar(0.6))
        topx =  int(getLastMatch().getX())-25
        topy = int(getLastMatch().getY())-80
        sidebar_width = 250
        sidex = sidebar_width+topx
        find("BottomCorner.png")
        vbarx =  int(getLastMatch().getX())+30
        vbary = int(getLastMatch().getY())+10
        vbarw = getLastMatch().getW()
        app_height = int(vbary-topy)
        mainwidth = int((vbarx-sidex)+vbarw)

        AppRegions = {"SidebarRegion": Region(topx,topy, sidebar_width,
                      app_height),
                      "MainViewRegion": Region(sidex, topy+110, mainwidth,
                      app_height),
                      "TopHalfRegion":
                      Region(0,0,mainwidth+sidebar_width,app_height/2),
                      "TopLeftRegion": Region(0,0,mainwidth/2,app_height/2),
                      "MainTitleBarRegion": Region(sidex, topy, mainwidth,
                      120),
                      "MainAndHeaderRegion": Region(sidex, topy, mainwidth,
                      app_height+50),
                      "PodcastLowerRegion": Region(sidex, vbary - 80,
                      mainwidth, 70)
                      }
        for regs in AppRegions.itervalues():
            regs.setAutoWaitTimeout(20)
        return AppRegions

    @classmethod
    def get_db(cls):
        if cls.sysos == 'WINDOWS':
            return os.path.join((os.getenv("APPDATA"),
                                 "Participatory Culture Foundation",
                                 "Miro","Support","sqlitedb"))
        if cls.sysos == 'MAC':
            return os.path.join(os.getenv("HOME"), "Library", 
                                "Application Support", "Miro","sqlitedb")
        if cls.sysos == 'LINUX':
            return os.path.join(os.getenv("HOME"),".miro","sqlitedb")

    @classmethod
    def reset_db(cls, db=None):
        if db is None:
            db = os.path.join(os.getcwd(), 'tests.sikuli', 'TestData',
                              'databases', 'empty_db')
        curr_db = cls.get_db()
        shutil.copy(db, curr_db)
        if os.path.exists(db + 'wal'):
            shutil.copy(db+'-wal', curr_db + '-wal')
        else:
            if os.path.exists(curr_db + '-wal'):
                os.unlink(curr_db + '-wal')



    @classmethod
    def launch_miro(cls):
        if cls.sysos == 'LINUX':
            #App.focus('miro')
            subprocess.Popen('miro')
#r'./run.sh', cwd=os.getenv('MIRONIGHTLYDIR'))
            print 'launching Miro on linux'
            time.sleep(10)
            return 
        if cls.sysos == 'WINDOWS':
            app = os.path.join(os.getenv("PROGRAMFILES"),
                               "Participatory Culture Foundation","Miro","Miro.exe")
        if cls.sysos == 'MAC':
            app = '/Applications/Miro.app'
        App.focus(app)


