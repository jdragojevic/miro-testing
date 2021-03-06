from sikuli.Sikuli import *
import nose
import subprocess
import os
import stat
import time
import shutil
import logging

class BaseTestCase(object):

    @classmethod
    def setUpClass(cls):
        cls.logger = logging.getLogger('test_steps')
        cls.logger.setLevel(logging.INFO)
#        Settings.ActionLogs = False
#        Settings.InfoLogs = False
#        Settings.DebugLogs = False
        oses = ['LINUX', 'WINDOWS', 'MAC']
        cls.sysos = [o for o in oses if o in str(Env.getOS())][0]
        cls.set_image_dirs()
        cls.miro_app = cls.launch_miro()
        cls.reg = cls.get_regions()

    @classmethod
    def tearDownClass(cls):
        cls.quit_miro()
        cls.reset_db()

    def tearDown(self):
        type(Key.ESC)

    @classmethod
    def quit_miro(cls):
        cls.miro_app.close()
        time.sleep(3)
        if cls.sysos == 'WINDOWS':
            subprocess.Popen(r'TASKKILL /F /IM Miro.exe')
        elif cls.sysos == 'MAC':
            os.system('killall Miro')
        else:
            os.system("killall miro.real miro")

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
        sidebar_width = 210
        sidex = sidebar_width+topx
        find("BottomCorner.png")
        vbarx =  int(getLastMatch().getX())+30
        vbary = int(getLastMatch().getY())+10
        vbarw = getLastMatch().getW()
        app_height = int(vbary-topy)
        mainwidth = int((vbarx-sidex)+vbarw)

        AppRegions = {"SidebarRegion": Region(topx, topy, sidebar_width,
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
        support_dir = cls.get_support_dir()
        return os.path.abspath(os.path.join(support_dir, 'sqlitedb'))

    @classmethod
    def get_support_dir(cls):
        if cls.sysos == 'WINDOWS':
            appdata = os.getenv("APPDATA")
            return os.path.join(os.path.abspath(appdata),
                                 "Participatory Culture Foundation",
                                 "Miro", "Support")
        if cls.sysos == 'MAC':
            return os.path.join(os.getenv("HOME"), "Library", 
                                "Application Support", "Miro")
        if cls.sysos == 'LINUX':
            return os.path.join(os.getenv("HOME"),".miro")


    @classmethod
    def reset_db(cls, db=None):
        cls.logger.info('Resetting the db to %s' % db)
        if db == None:
            l = os.path.abspath(os.getcwd())
            db = os.path.join(l, 'Data', 'databases', 'empty_db_%s' % cls.sysos)
            cls.logger.info(db)
        curr_db = cls.get_db()
        cls.logger.info(curr_db)
        shutil.copy(db, curr_db)
        currdb_wal = curr_db+'-wal'
        if os.path.exists(db + '-wal'):
            shutil.copy(db+'-wal', currdb_wal)
        else:
            if os.path.exists(currdb_wal):
                os.chmod(currdb_wal, stat.S_IWRITE)
                os.unlink(currdb_wal)
        time.sleep(2)

    @classmethod
    def remove_http_auth_file(cls):
        auth_file = os.path.join(cls.get_support_dir(), "httpauth")
        if os.path.exists(auth_file):
            auth_saved = True
            cls.quit_miro()
            os.remove(auth_file)
            cls.launch_miro()

    @classmethod
    def launch_miro(cls):
        if cls.sysos == 'LINUX':
            #App.focus('miro')
            subprocess.Popen('miro')
            #r'./run.sh', cwd=os.getenv('MIRONIGHTLYDIR'))
            print 'launching Miro on linux'
            time.sleep(10)
            return App('Miro')
        if cls.sysos == 'WINDOWS':
            app = os.path.join(os.getenv("PROGRAMFILES"),
                               "Participatory Culture Foundation","Miro","Miro.exe")
        if cls.sysos == 'MAC':
            app = '/Applications/Miro.app'
        App.focus(app)
        return App('Miro')


