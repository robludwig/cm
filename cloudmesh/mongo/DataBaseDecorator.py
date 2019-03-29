from datetime import datetime

from cloudmesh.management.configuration.name import Name
from cloudmesh.mongo.CmDatabase import CmDatabase



class DatabaseUpdate:
    """

    The data base decorator utomatically replaces an entry in the database with
    the dictionary returned by a function.

    It is added to a MongoDB collection. The location is determined from the
    values in the dictionary.

    The name of the collection is determined from cloud and kind:

       cloud-kind

    In addition each entry in the collection has a name that must be unique in
    that collection.

    IN most examples it is pest to separate the updload from the actual return
    class. This way we essentially provide two functions one that provide the
    dict and another that is responsible for the upload to the database.





    Example:

    cloudmesh.example.foo contains:

        class Provider(object)

            def entries(self):
                return {
                   "cm": {
                     "cloud": "foo",
                     "kind"": "entries",
                     "name": "test01"
                     "test": "hello"}
                   }
                   "cloud": "foo",
                   "kind"": "entries",
                   "name": "test01"
                   "test": "hello"}


    cloudmesh.example.bar contains:

        class Provider(object)

            def entries(self):
                return {
                   "cloud": "bar",
                   "kind"": "entries",
                   "name": "test01"
                   "test": "hello"}

    cloudmesh.example.provider.foo:

        from cloudmesh.example.foo import Provider as FooProvider
        from cloudmesh.example.foo import Provider as BarProvider

        class Provider(object)

            def __init__(self, provider):
               if provider == "foo":
                  provider = FooProvider()
               elif provider == "bar":
                  provider = BarProvider()

            @DatabaseUpdate
            def entries(self):
                provider.entries()


    Separating the database and the dictionary creation allows the developer to
    implement different providers but only use one class with the same methods
    to interact for all providers with the database.

    In the combined provider a find function to for example search for entries
    by name across collections could be implemented.

    """

    # noinspection PyUnusedLocal
    def __init__(self, **kwargs):
        self.database = CmDatabase()

    def __call__(self, f):
        def wrapper(*args, **kwargs):
            current = f(*args, **kwargs)
            if type(current) == dict:
                current = [current]

            result = self.database.update(current)

            return result

        return wrapper
