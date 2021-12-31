from repeat_todo.extensions import db


class TaskInstance(db.Model):
    """Task Instance model."""

    id = db.Column(db.Integer, primary_key=True)
    task_template_id = db.Column(db.Integer, db.ForeignKey("task_template.id"))
    task_scheduled_date = db.Column(db.DateTime)
    task_completed = db.Column(db.Boolean, default=False)
    task_completed_date = db.Column(db.DateTime, nullable=True, default=None)

    @property
    def as_dict(self):
        return {
            "id": self.id,
            "task_template_id": self.task_template_id,
            "task_scheduled_date": self.task_scheduled_date,
            "task_completed": self.task_completed,
            "task_completed_date": self.task_completed_date,
        }
