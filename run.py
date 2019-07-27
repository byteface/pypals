from core import PyWorld
import sys

palname = ""
try:
    palname = sys.argv[1]
except Exception:
    pass

world = PyWorld(palname)
