#!/usr/bin/env python

import sys
from core.PyWorld import PyWorld

palname = ""
try:
    palname = sys.argv[1]
except Exception as e:
    pass

world = PyWorld(palname)
