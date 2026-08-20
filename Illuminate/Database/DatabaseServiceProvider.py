from Illuminate.Database.DatabaseManager import DatabaseManager
from Illuminate.Support.ServiceProvider import ServiceProvider


class DatabaseServiceProvider(ServiceProvider):
    def __init__(self, app):
        self.app = app

    def register(self):
        self.app.singleton(
            DatabaseManager,
            lambda app: DatabaseManager(app, app.make("config")),
        )
        self.app.alias(DatabaseManager, "db")

    def boot(self):
        pass
