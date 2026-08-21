from Illuminate.Database.DatabaseManager import DatabaseManager
from Illuminate.Database.Schema.Builder import SchemaBuilder
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
        
        self.app.singleton(
            SchemaBuilder,
            lambda app: SchemaBuilder(app.make("db")),
        )
        self.app.alias(SchemaBuilder, "db.schema")
    def boot(self):
        pass
