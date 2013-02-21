import os
import sys
from sikuli.Sikuli import *

sys.path.append(os.path.join('/usr', 'local', 'lib', 'python2.7', 'dist-packages'))
sys.path.append(os.path.join('/usr', 'local', 'lib', 'python2.7', 'site-packages'))
sys.path.append(os.getcwd())
import nose 

nose.main()



