from core import PyWorld
import sys

palname=""
try:
	palname = sys.argv[1]
except Exception:
	pass

# instantiate a world to load the requested pypal
world = PyWorld(palname);