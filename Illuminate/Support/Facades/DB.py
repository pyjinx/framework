from Illuminate.Support.Facades.Facade import Facade


class DB(metaclass=Facade):
    @classmethod
    def get_facade_accessor(cls):
        return "db"
