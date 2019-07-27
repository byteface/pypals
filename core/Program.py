from . import _meta

class Program(object):
 
    def __init__(self, path, program):
        self.path = path
        self.program = program
        self.meta = _meta._meta(path)
