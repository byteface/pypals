import json
import os
import configparser
from rich import print


class _meta(object):

    BAK = None  # data recovery for if a user deletes their config file

    def __init__(self, path: str):
        """
        objects check their own root path for a file called _meta.json that contains key value pairs.

        it can also be in any of the following formats:

        - .json file
        - .ini file
        - .txt file
        - .xml file

        # TODO - toml/yaml not supported yet

        """
        self.path = path
        self.filetype = 'json'
        # try to find the config file for the path

        # first try json
        try:
            with open(self.path + "_meta.json") as json_file:
                self.data = json.load(json_file)['object']
        except Exception as e:
            # print('total fail', e)
            self.data = None

        # if that fails, try an ini file
        if self.data == None:
            try:
                config = configparser.ConfigParser()
                config.read(self.path + "_meta.ini")
                self.data = config['default']
                self.filetype = 'ini'
            except Exception as e:
                # print(e)
                self.data = None

        # if that fails, try an xml file
        if self.data == None:
            try:
                import xml.etree.ElementTree as ET
                tree = ET.parse(self.path + "_meta.xml")
                root = tree.getroot()
                self.data = {}
                for child in root:
                    self.data[child.tag] = child.text
                self.filetype = 'xml'
            except:
                self.data = None

        # if that fails try a plain text file of key value pairs separated by an equal sign and parse it to dict
        if self.data == None:
            try:
                self.data = {}
                with open(self.path + "_meta.txt") as txt_file:
                    for line in txt_file:
                        key, value = line.split("=")
                        self.data[key] = value.replace('\n','')
                        self.filetype = 'txt'
            except:
                self.data = None

        # if that fails tell the user
        if self.data == None:
            print("No config file of any type could be found. Trying to create a replacement")
            try:
                # use the current directory as the name
                import os
                # name = os.path.basename(os.path.abspath(os.path.curdir))
                obj = _meta.BAK
                # obj['name'] = _meta.BAK#.get('name')  # name
                obj['friend'] = 'unknown'
                data = {}
                data['object'] = obj
                with open(self.path + '/_meta.json', 'w') as f:
                    json.dump(data, f)
                    self.data = obj#data['object']
                    self.filetype = 'json'
            except Exception as e:
                print("Failed to create replacement config file")


    def save_as(self, filetype='json'):
        """ save the config file as a different filetype """
        self.filetype = filetype
        self.save()


    def save(self):
        """ save the config file """
        # delete any current config file
        for filetype in ['json', 'yml', 'ini', 'toml', 'xml', 'txt']:
            try:
                os.remove(self.path + '/_meta.' + filetype)
            except Exception as e:
                # print(e)
                pass

        # save the new config file
        if self.filetype == 'json':
            with open(self.path + "_meta.json", "w") as json_file:
                obj={'object':dict(self.data)}
                json.dump(obj, json_file)
                return
        # elif self.filetype == 'yml':
        #     with open(self.path + "_meta.yml", "w") as yaml_file:
        #         for key, value in self.data.items():
        #             yaml_file.write(key + ': ' + value + '\n')
        #         return
        elif self.filetype == 'ini':
            with open(self.path + "_meta.ini", "w") as ini_file:
                # format the data for ini and write it with a default section
                ini_file.write('[default]\n')
                for key, value in self.data.items():
                    ini_file.write(key + '=' + value + '\n')
        elif self.filetype == 'txt':
            with open(self.path + "_meta.txt", "w") as txt_file:
                for key, value in self.data.items():
                    txt_file.write(key + "=" + value + '\n')
                return
        elif self.filetype == 'xml':
            with open(self.path + "_meta.xml", "w") as xml_file:
                # fromat the data for xml and write it
                from xml.dom import minidom
                doc = minidom.Document()
                root = doc.createElement('object')
                doc.appendChild(root)
                for key, value in self.data.items():
                    child = doc.createElement(key)
                    root.appendChild(child)
                    text = doc.createTextNode(value)
                    child.appendChild(text)
                xml_file.write(doc.toprettyxml(indent="  "))
                return

    def __getitem__(self, key):
        # print(self.data)
        return self.data[key]
    
    def __setitem__(self, key, value):
        self.data[key] = value
    
    def __delitem__(self, key):
        del self.data[key]
    
    def __iter__(self):
        return iter(self.data)
    
    def __len__(self):
        return len(self.data)

    def __contains__(self, key):
        return key in self.data

    def __str__(self):
        return str(self.data)


    def get(self, meta_type: str):
        """ getter for json nodes """
        return self.data[meta_type]

    def get_property(self, meta_type: str, prop: str):
        """ getter for props on json nodes """
        return self.data[meta_type][prop]
