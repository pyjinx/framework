import sys
import importlib


class RouteLoader:
    @classmethod
    def load_routes(cls, loader: str):
        try:
            if loader in sys.modules:
                importlib.reload(sys.modules[loader])
            else:
                importlib.import_module(loader)
        except ImportError as e:
            print("RouteLoader.ImportError", e)
            raise e
        except ModuleNotFoundError as e:
            print("RouteLoader.ModuleNotFoundError", e)
            raise e
