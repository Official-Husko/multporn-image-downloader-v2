import os
import json
import atexit

"""
a = {}
a["real_name"] = {}
a["real_name"]["custom_name"] = "custom name"
a["real_name"]["path"] = "custom/ real path"
a["real_name"]["pages"] = [0,1,2,3,4,5,6]

>>> {'real_name': {'custom_name': 'custom name', 'path': 'custom/ real path', 'pages': [0, 1, 2, 3, 4, 5, 6]}}
"""

class Manager():
    """
    Manages database.
    """
    def __init__(self,_dir):
        """
        If database does not exist, it gets created, else its contents are read.
        """
        #self._db_name = "db.dat"
        #__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) +"\\Data"
        #self._dir = os.path.join(__location__, self._db_name)
        self._dir = os.path.join(_dir,"Data\\db.dat")
        if not os.path.exists(self._dir):
            with open(self._dir,"w+"):
                self.data = {}
        else:
            with open(self._dir,"r") as file:
                self.data = json.loads(file.read())
        atexit.register(self._del_)
    def _del_(self):
        """
        Saves the data upon calling "del", or program stop/ crash.
        """
        with open(self._dir,"w") as file:
            file.write(json.dumps(self.data))

    def update_pages(self, comic, lst):
        """
        Updates the databases entry of pages in the given comic.
        """
        if comic not in self.data:
            raise KeyError("Entry not found")
        self.pages = list(set([int(x) for x in set(lst)] + self.data[comic]["pages"]))
        self.comic = comic
        self.data[comic]["pages"] = self.pages

    def update_path(self, comic, new_path):
        """
        Updates the "path" entry of the given comics
        """
        self.data[comic]["path"] = new_path

    def get_data(self, comic):
        """
        Returns all data of the given comics, if it is not found, "None" gets returned. (Possible rework to handle that better)
        """
        self.comic = comic
        if self.comic not in self.data:
            return None, None, None
        else:
            return self.data[comic]["custom_name"], self.data[comic]["path"], self.data[comic]["pages"]

    def create_record(self, comic, custom_name, path, pages):
        """
        Creates a database entry with the given data. (Possible rework with **kwargs)
        """
        if comic in self.data:
            raise KeyError("Entry already exists")
        else:
            self.data[comic] = {}
            self.data[comic]["custom_name"] = custom_name
            self.data[comic]["path"] = path
            self.data[comic]["pages"] = list(set([int(x) for x in pages]))

    def exists(self, comic):
        """
        Returns bool depending on if comic exists in the database
        """
        return comic in self.data

    def force_save(self):
        """
        Should NOT be used, only for edge cases where the program could crash or when debugging/ testing.
        """
        with open(self._dir,"w") as file:
            file.write(json.dumps(self.data))
"""
print(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))))
if __name__ == "__main__":
    test = Manager(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))))
    if not test.exists("oneshot_shadman"):
        test.create_record("oneshot_shadman","my fav comics","c:/Users/agent/OneDrive/Documents/github/mp_downloader/multporn_downloader/",[1,2,3,4,5,6,7,8,9,10])
    else:
        test.update_pages("oneshot_shadman",[1,11,12,13,15,14])
    print(test.get_data("oneshot_shadman"))
"""