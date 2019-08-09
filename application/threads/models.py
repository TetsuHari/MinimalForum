from application import database

class Thread(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    date_created = database.Column(database.DateTime, default=database.func.current_timestamp())
    title = database.Column(database.String(144), nullable=False)
    locked = database.Column(database.Boolean, nullable=False, default=False)
    content = database.Column(database.String(144))
    # TODO:
    # content = database.Column( reference to starting comment )
    # modified_on = database.Column(database.DateTime ...)

    def __init__(self, title, content):
        self.title = title
        self.content = content
