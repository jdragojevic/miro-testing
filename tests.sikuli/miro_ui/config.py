import os
import time
import subprocess


def start_ff_on_linux():
    subprocess.Popen(r'firefox', cwd='/usr/bin/')


def get_video_dir():
    if get_os_name() == "win":
        ver = Env.getOSVersion()
        wv = ver.split('.')[0]
        if int(wv) < 6:
            video_dir = os.path.join(os.getenv("USERPROFILE"),"My Documents","My Videos","Miro")
        else:
            video_dir = os.path.join(os.getenv("USERPROFILE"),"Videos","Miro")
    elif get_os_name() == "lin":
            video_dir = os.path.join(os.getenv("HOME"),"Videos","Miro")
    elif get_os_name() == "osx":
            video_dir = os.path.join(os.getenv("HOME"),"Movies","Miro")

    else:
        print "no clue"
    return video_dir

def reset_preferences():
    if get_os_name() == "lin":
        preffile = os.path.join(datadir,"linux_prefs")
        reset_cmd = ["gconftool-2", "--load", preffile]
        p = subprocess.Popen(reset_cmd).communicate()

    elif get_os_name() == "osx":
        preffile = os.path.join(datadir,"osx.plist")
        plist_file = os.path.join(os.getenv("HOME"),"Library","Preferences","org.participatoryculture.Miro.plist")
        shutil.copy(preffile,plist_file)
    elif get_os_name() == "win":
        preffile = os.path.join(datadir,"win_prefs.bin")
        prefs = os.path.join(get_support_dir(),"preferences.bin")
        shutil.copy(preffile,prefs)
    else:
        print "don't have prefs for this os"

def delete_preferences():
    #completely ditch preferences on linux
    if get_os_name() == "lin":
        unset_cmd = ["gconftool-2", "--recursive-unset", "/apps/miro"]
        p= subprocess.Popen(unset_cmd).communicate()
    #completely ditch preferences on osx
    elif get_os_name() == "osx":
        plist_file = os.path.join(os.getenv("HOME"),"Library","Preferences","org.participatoryculture.Miro.plist")
        if os.path.exists(plist_file):
            os.unlink(plist_file)
    elif get_os_name() == "win":
        miro_support_dir = get_support_dir()
        preffile = os.path.join(miro_support_dir,"preferences.bin")
        if os.path.exists(preffile):
            os.unlink(preffile)
    else:
        print "don't know where preferences are"

def delete_database_and_prefs(dbonly=False):
        """Delete the miro support dir and preferences.

        On Windows, delete the entire Support dir. On OSX delete Support dir + preferences plist.
        On linux, delete Support dir, + unset gconf settings.
        """
        miro_support_dir = get_support_dir()
        if dbonly == True:
            dbfile = os.path.join(miro_support_dir,"sqlitedb")
            if os.path.exists(dbfile):
                os.unlink(dbfile)
        else:
            if os.path.exists(miro_support_dir):
                shutil.rmtree(miro_support_dir)
            else:
                print "***Warning: didn't find support dir***"
            #completely ditch preferences on linux
            if get_os_name() == "lin":
                unset_cmd = ["gconftool-2", "--recursive-unset", "/apps/miro"]
                p = subprocess.Popen(unset_cmd).communicate()
            #completely ditch preferences on osx
            if get_os_name() == "osx":
                plist_file = os.path.join(os.getenv("HOME"),"Library","Preferences","org.participatoryculture.Miro.plist")
                if os.path.exists(plist_file):
                    os.remove(plist_file)


def set_def_db_and_prefs():
    print "resetting db to empty db"
    time.sleep(5)
    db = os.path.join(proj_dir, "features", "terrain", "TestData", "databases", "empty_db")
    replace_database(db)
    reset_preferences()
    time.sleep(5)

def delete_miro_video_storage_dir():
        """Delete the Miro video storage directory.

        """
        #Delete Miro default video storage
        miro_video_dir = get_video_dir()
        if os.path.exists(miro_video_dir):
            shutil.rmtree(miro_video_dir)
        else:
            print "***Warning: didn't find videos dir***"


def delete_miro_downloaded_files():
        """Delete the Miro video storage directory.

        """
        #Delete Miro default video storage
        miro_video_dir = get_video_dir()
        if os.path.exists(miro_video_dir):
            for f in glob.glob(os.path.join(miro_video_dir, '*.*')):
                os.unlink(f)
        else:
            print "***Warning: didn't find videos dir***"

def get_val_from_mirodb(dbtable, dbfield):
    stmt = 'from db_mod import MiroDatabase; MiroDatabase().get_value("%s","%s")' % (dbtable,dbfield)    
    db_cmd = ['python','-c',stmt]
    p = subprocess.Popen(db_cmd).communicate()
    infile = os.path.join(os.getenv("TMPDIR"), "dbval.pkl")
    pkl_file = open(infile, 'rb')
    dbvalue = pickle.load(pkl_file)
    pkl_file.close()
    if os.path.exists(infile):
        os.remove(infile)
    return dbvalue

def set_mirodb_value(dbtable,dbfield,dbval):
    stmt = 'from db_mod import MiroDatabase; MiroDatabase().set_value("%s","%s","%s")' % (dbtable,dbfield,dbval)
    db_cmd = ['python','-c',stmt]
    p = subprocess.Popen(db_cmd).communicate()

def run_db_cmd(db_cmd):
    stmt = 'from db_mod import MiroDatabase; MiroDatabase().run_cmd("%s")' % (db_cmd)
    db_cmd = ['python','-c',stmt]
    p = subprocess.Popen(db_cmd).communicate()    
