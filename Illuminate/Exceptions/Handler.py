class Handler:
    def __init__(self, app) -> None:
        self.__app = app

    def handle(self, exception):
        print("handlring exception", exception)
