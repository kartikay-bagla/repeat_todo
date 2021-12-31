from flask_login import UserMixin

from repeat_todo.extensions import db


class User(UserMixin, db.Model):
    """User model."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(120))

    week_start_pref = db.Column(db.String(3), default="mon")

    @property
    def as_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "week_start_pref": self.week_start_pref
        }
