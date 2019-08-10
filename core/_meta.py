class _meta(object):

    def __init__(self, path: str):
        """ meta for each object. initialised by Program passes the path """
        self.path = path
        import json
        with open(self.path + "/_meta.json") as json_file:
            self.data = json.load(json_file)

    def get(self, meta_type: str):
        """ getter for json nodes """
        return self.data[meta_type]

    def get_property(self, meta_type: str, prop: str):
        """ getter for props on json nodes """
        return self.data[meta_type][prop]
