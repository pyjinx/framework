from Illuminate.Contracts.Foundation.Application import Application


class Facade(type):
    app: Application | None = None

    def __getattr__(cls, attribute, *args, **kwargs):
        if cls.app is None:
            raise RuntimeError("Facade application has not been set.")

        facade_accessor = cls.get_facade_accessor()
        abstract = cls.app.get_alias(facade_accessor)
        binding = cls.app.make(abstract)
        return getattr(binding, attribute)

    @classmethod
    def set_facade_application(cls, app: Application):
        cls.app = app
