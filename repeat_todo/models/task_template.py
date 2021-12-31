from repeat_todo.extensions import db


class TaskTemplate(db.Model):
    """Task template model."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(120))
    color = db.Column(db.String(120))
    schedule = db.Column(db.String(120))

    @property
    def as_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "color": self.color,
            "schedule": self.schedule
        }
