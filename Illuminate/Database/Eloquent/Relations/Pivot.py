from Illuminate.Database.Eloquent.Model import Model


class Pivot(Model):
    """Dynamic model representing an intermediate many-to-many row."""

    guarded = []
    incrementing = False
    timestamps = False

    def __init__(self, table, attributes=None, exists=True):
        self.table = table
        super().__init__(attributes, exists=exists)
