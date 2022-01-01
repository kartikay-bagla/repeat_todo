import json
from datetime import datetime, timedelta

import pandas as pd
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from repeat_todo.extensions import db
from repeat_todo.models.task_instance import TaskInstance
from repeat_todo.models.task_template import TaskTemplate
from repeat_todo.utils import datetime_to_date, get_dates_from_rrule

task_template_route = Blueprint("task_template", __name__)


@task_template_route.route("/")
@login_required
def task_template():
    user_id = current_user.id
    task_templates = TaskTemplate.query.filter_by(user_id=user_id).all()
    return jsonify([task_template.as_dict for task_template in task_templates])


@task_template_route.route("/", methods=["POST"])
@login_required
def add_task_template():
    data = json.loads(request.data)
    try:
        name = data["name"]
        color = data["color"]
        schedule = data["schedule"]
    except KeyError:
        return jsonify({"error": "Missing name, color or schedule"}), 400

    new_task_template = TaskTemplate(
        name=name, color=color, schedule=schedule, user_id=current_user.id
    )
    db.session.add(new_task_template)
    db.session.commit()

    try:
        start_date = datetime_to_date(datetime.now())
        end_date = start_date + timedelta(days=90)
        dates = get_dates_from_rrule(schedule, end_date)
        task_instance_df = pd.DataFrame(
            {
                "task_template_id": [new_task_template.id] * len(dates),
                "task_scheduled_date": dates,
            }
        )
        task_instance_df.to_sql(
            TaskInstance.__tablename__,
            db.engine,
            if_exists="append",
            index=False,
            chunksize=1000,
        )
        return jsonify({"message": "Task template created successfully."})
    except Exception as e:
        db.session.delete(task_template)
        db.session.commit()
        raise e


@task_template_route.route("/", methods=["DELETE"])
@login_required
def delete_task_template():
    data = json.loads(request.data)
    try:
        task_template_id = data["id"]
    except KeyError:
        return jsonify({"error": "Missing id"}), 400

    task_template = TaskTemplate.query.filter_by(
        id=task_template_id, user_id=current_user.id
    ).first()
    if not task_template:
        return jsonify({"error": "Task template does not exist"}), 400
    db.session.delete(task_template)
    db.session.commit()
    return jsonify({"message": "Task template deleted successfully."})


@task_template_route.route("/", methods=["PUT"])
@login_required
def update_task_template():
    data = json.loads(request.data)
    try:
        task_template_id = data["id"]
    except KeyError:
        return jsonify({"error": "Missing task template id"}), 400

    task_template = TaskTemplate.query.filter_by(
        id=task_template_id, user_id=current_user.id
    ).first()
    if not task_template:
        return jsonify({"error": "Task template does not exist"}), 400
    try:
        name = data["name"]
        color = data["color"]
    except KeyError:
        return jsonify({"error": "Missing name or color"}), 400

    if data.get("schedule"):
        return jsonify({"error": "Cannot update schedule"}), 400

    task_template.name = name
    task_template.color = color
    db.session.commit()
    return jsonify({"message": "Task template updated successfully."})


@task_template_route.route("/<int:task_template_id>/", methods=["GET"])
@login_required
def get_task_template(task_template_id):
    task_template = TaskTemplate.query.filter_by(
        id=task_template_id, user_id=current_user.id
    ).first()
    if not task_template:
        return jsonify({"error": "Task template does not exist"}), 400

    task_instance = TaskInstance.query.filter_by(
        task_template_id=task_template_id
    ).all()
    return jsonify([task_instance.as_dict for task_instance in task_instance])
