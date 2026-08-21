from Illuminate.Support.Facades.Facade import Facade


class Schema(metaclass=Facade):
    @classmethod
    def get_facade_accessor(cls) -> str:
        return "db.schema"
