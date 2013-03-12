import os
import sys
from sikuli.Sikuli import *

testos = str(Env.getOS())

if 'LINUX' in testos:
    sys.path.append(os.path.join('/usr', 'local', 'lib', 'python2.7', 'dist-packages'))
    sys.path.append(os.path.join('/usr', 'local', 'lib', 'python2.7', 'site-packages'))
elif 'WINDOWS' in testos:
    pkg_path = os.path.join(os.getcwd(), '..', 'env-miro', 'Lib', 'site-packages')
    sys.path.append(pkg_path)
elif 'MAC' in testos:
    pkg_path = os.path.join(os.getenv('VIRTUAL_ENV'), 'lib', 'python2.7', 'site-packages')
    print pkg_path
    sys.path.append(pkg_path)
else:
    print 'no idea the os'

import nose 

nose.main()

