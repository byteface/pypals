__version__ = "0.0.1"

import sys
from pypals.PyWorld import PyWorld

name = ""
if len(sys.argv)>1:
    name = sys.argv[1]

PyWorld(name)