from application import db


class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    title = db.Column(db.String(144), nullable=False)
    locked = db.Column(db.Boolean, default=False, nullable=False)
    content = db.Column(db.Text, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    author = db.relationship("User", backref="threads_created")

    def __init__(self, title, content, auth_id):
        self.title = title
        self.content = content
        self.author_id = auth_id
