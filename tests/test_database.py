# nosetest -v --nopature
# nosetests -v --nocapture tests/test_database.py
#############
from cloudmesh.common.util import HEADING

from cloudmesh.mongo.CmDatabase import CmDatabase
from cloudmesh.common.Printer import Printer
#from cloudmesh.mongo import MongoDBController

#from cloudmesh.mongo import DatabaseUpdate
#from cloudmesh.management.debug import HEADING, myself
from pprint import pprint

from cloudmesh.management.configuration.name import Name

class TestMongo:

    def setup(self):
        self.database = CmDatabase()

        self.name = Name(experiment="exp",
                       group="grp",
                       user="gregor",
                       kind="vm",
                       counter=1)

    def test_10_find_in_collection(self):
        HEADING()
        r = self.database.find_name("CC-CentOS7")
        pprint(r)

    def test_11_find_in_collections(self):
        HEADING()
        r = self.database.find_names("CC-CentOS7,CC-CentOS7-1811")
        pprint(r)

    def test_12_find_in_collection(self):
        HEADING()
        r = self.database.name_count("CC-CentOS7")
        pprint(r)


class t:
    def test_00_status(self):
        HEADING()

        #print(self.name)
        #print(self.name.counter)
        #print(self.name.id(counter=100))

        self.database.clear()

        r = self.database.find()
        pprint(r)

        assert len(r) == 0

    def test_01_status(self):
        HEADING()
        r = self.database.status()
        # pprint(r)
        assert "Connection refused" not in r

        d = {}
        for field in ['uptime', 'pid', 'version', 'host']:
            d[field]=r[field]

        print (Printer.attribute(d))

        assert d is not None

    def test_02_update(self):
        HEADING()

        entries = [{"name" : "Gregor"},
                   {"name" : "Laszewski"}]

        for entry in entries:
            entry["cmid"] = str(self.name)
            entry["cmcounter"] = self.name.counter
            self.name.incr()
        self.database.update(entries)

        r = self.database.find()

        pprint(r)
        assert len(r) == 2


    def test_03_update(self):
        HEADING()

        r = self.database.find(name="Gregor")
        pprint (r)

        assert r[0]['name'] == "Gregor"

    def test_04_update(self):
        HEADING()
        entries = [{"cmcounter" : 1, "name" : "gregor"},
                   {"cmcounter" : 2, "name" : "laszewski"}]
        pprint(entries)
        for entry in entries:
            counter = entry["cmcounter"]
            print("Counter:", counter)
            entry["cmid"] = self.name.id(counter=counter)
        self.database.update(entries, replace=False)
        r = self.database.find()
        pprint(r)


    def test_05_update(self):
        HEADING()
        r = self.database.find(name="gregor")
        pprint (r)
        assert r[0]["name"] == "gregor"


    def test_06_find_by_counter(self):
        HEADING()
        r = self.database.find_by_counter(1)
        pprint (r)
        assert r[0]["name"] == "gregor"

        r = self.database.find_by_counter(2)
        pprint (r)
        assert r[0]["name"] == "laszewski"


    def test_07_decorator_update(self):
        HEADING()

        @DatabaseUpdate(collection="cloudmesh")
        def entry():
            name = Name()
            print (name)
            print ("OOOO", str(name), name.counter)
            d = {"cmid": str(name), "cmcounter" : name.counter, "name" : "albert"}
            name.incr()
            pprint (d)
            return d

        a = entry()

        r = self.database.find_by_counter(3)

        pprint (r)

    def test_08_decorator_add(self):
        HEADING()

        @DatabaseAdd(collection="cloudmesh")
        def entry():
            d = {"name" : "zweistein"}
            return d

        a = entry()

        r = self.database.find()

        pprint (r)

        assert len(r) == 4



    def test_09_overwrite(self):
        HEADING()
        r = self.database.find(name="gregor")[0]
        pprint (r)
        r["color"] = "red"


        self.database.update([r], replace=True)

        r = self.database.find(color="red")

        pprint (r)

        assert len(r) == 1


    def test_10_fancy(self):
        HEADING()

        counter = 1

        n = Name(experiment="exp",
                 group="grp",
                 user="gregor",
                 kind="vm",
                 counter=counter)

        print (n)

        entries = [{
              "cmcounter" : counter,
              "cmid": str(n),
              "name" : "gregor",
              "phone": "android"
        }]
        self.database.update(entries, replace=True)

        r = self.database.find()

        pprint (r)

        assert len(r) == 4

