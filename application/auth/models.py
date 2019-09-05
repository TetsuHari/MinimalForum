from application import db
from application.models import Base

from sqlalchemy.sql import text


class User(Base):

    __tablename__ = "account"

    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    @staticmethod
    def get_user_karma(user_id):
        upvote_statement = text("SELECT COUNT(upvote.is_up) FROM upvote"
                                " JOIN comment ON comment.id=upvote.comment_id"
                                " JOIN account on account.id=comment.author_id"
                                " where upvote.is_up=1"
                                " AND account.id=:user_id"
                                ).params(user_id=user_id)
        downvote_statement = text("SELECT COUNT(upvote.is_up) FROM upvote"
                                  " JOIN comment ON comment.id=upvote.comment_id"
                                  " JOIN account on account.id=comment.author_id"
                                  " where upvote.is_up=0"
                                  " AND account.id=:user_id"
                                  ).params(user_id=user_id)
        upvote_res = db.engine.execute(upvote_statement).first()[0]
        downvote_res = db.engine.execute(downvote_statement).first()[0]

        return upvote_res - downvote_res
