from Illuminate.Support.Facades.Facade import Facade


class Redirect(metaclass=Facade):
    @classmethod
    def get_facade_accessor(cls):
        return "redirect"
