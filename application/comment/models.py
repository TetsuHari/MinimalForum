from application import db


class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    author_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    author = db.relationship("User", backref="comments_created", lazy=True)

    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'),
                          nullable=False)
    thread = db.relationship("Thread", backref="thread_comments", lazy=True)

    parent_comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'),
                                  nullable=True)
    comments = db.relationship("Comment",
                               backref=db.backref('parent', remote_side=[id]))

    content = db.Column(db.Text, nullable=False)

    def __init__(self, content, author, thread):
        self.content = content
        self.author = author
        self.thread = thread
