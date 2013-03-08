import os
import sys
from sikuli.Sikuli import *

sys.path.append(os.path.join('/usr', 'local', 'lib', 'python2.7', 'dist-packages'))
sys.path.append(os.path.join('/usr', 'local', 'lib', 'python2.7', 'site-packages'))
if 'WINDOWS' in str(Env.getOS()):
    pkg_path = os.path.join(os.getcwd(), '..', 'env-miro', 'Lib', 'site-packages')
    print pkg_path
    sys.path.append(pkg_path)
sys.path.append(os.getcwd())
import nose 

nose.main()

