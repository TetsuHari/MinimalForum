from application import db
from application.models import Base


class Comment(Base):

    author_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                          nullable=False)
    author = db.relationship("User", backref="comments_created", lazy=True)

    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'),
                          nullable=False)
    thread = db.relationship("Thread", backref="thread_comments", lazy=True)

    content = db.Column(db.Text, nullable=False)

    def __init__(self, content, author, thread):
        self.content = content
        self.author = author
        self.thread = thread


class Upvote(Base):
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'),
                           nullable=False)
    comment = db.relationship("Comment", backref="upvotes", lazy=True)

    author_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                          nullable=False)
    author = db.relationship("User", backref="votes_given", lazy=True)

    is_up = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, author, comment, is_up):
        self.author = author
        self.comment = comment
        self.is_up = is_up
