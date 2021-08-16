"""
    pypals
    ====================================

    pypals now has a cli interface. check __main__.py for usage

"""

__version__ = "t-1"

class DefaultCommands():
    """ default commands that come with first pypal """

    HELLO = """def run(o):
    print(f"Hello, to you { o.o['friend']}!")
    return True
    """
    
    QUIT = """def run(o):
    import sys
    sys.exit(0)
    """