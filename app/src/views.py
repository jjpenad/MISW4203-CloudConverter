import os
from flask import request, jsonify, current_app, Blueprint
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from .models import db, User, Task
from google.cloud import pubsub_v1
from .tasks import convert_video

api = Blueprint('api', __name__)

@api.route('/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password1 = data.get('password1')
    password2 = data.get('password2')
    email = data.get('email')

    # Check if username and email are unique
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'message': 'Username or email already exists'}), 400

    # Check password criteria (implement your own criteria)
    if len(password1) < 8:
        return jsonify({'message': 'Password is too short'}), 400

    if password1 != password2:
        return jsonify({'message': 'Passwords do not match'}), 400

    user = User(username=username, email=email)
    user.set_password(password1)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@api.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=username,expires_delta=False)
    return jsonify(access_token=access_token), 200

@api.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    max_results = request.args.get('max', default=None, type=int)
    order = request.args.get('order', default=0, type=int)

    username = get_jwt_identity()
    user_id = User.query.filter_by(username=username).first()

    if order == 0:
        tasks = Task.query.filter_by(user_id=user_id.id).order_by(Task.id)
    else:
        tasks = Task.query.filter_by(user_id=user_id.id).order_by(Task.id.desc())

    if max_results:
        tasks = tasks.limit(max_results)

    tasks = [task.to_dict() for task in tasks]

    return jsonify(tasks), 200

@api.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    if 'url' not in request.form or 'newFormat' not in request.form:
        return jsonify({'message': 'Missing URL or newFormat field'}), 400

    url = request.form['url']
    new_format = request.form['newFormat']

    username = get_jwt_identity()

    user = User.query.filter_by(username=username).first()

    task = Task(user_id=user.id, url=url, new_format=new_format)
    db.session.add(task)
    db.session.commit()

    publisher = pubsub_v1.PublisherClient()
    topic_name = 'projects/{project_id}/topics/{topic}'.format(
        project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
        topic='worker-topic',  # Set this to something appropriate.
    )
    publisher.create_topic(name=topic_name)
    info = {
        "task_id":task.id,
         "input_url":url, 
         "output_format": new_format
    }
    future = publisher.publish(topic_name, info, spam='eggs')
    future.result()

    return jsonify({'message': 'Task created successfully'}), 201

@api.route('/tasks/<int:id_task>', methods=['GET'])
@jwt_required()
def get_task(id_task):
    task = Task.query.get(id_task)
    if task is None:
        return jsonify({'message': 'Task not found'}), 404
    return jsonify(task.to_dict()), 200


@api.route('/tasks/<int:id_task>', methods=['DELETE'])
@jwt_required()
def delete_task(id_task):
    task = Task.query.get(id_task)
    if task is None:
        return jsonify({'message': 'Task not found'}), 404
    
    if task.status == 'processing':
        return jsonify({'message': 'Task is being processed'}), 400

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'Task deleted successfully'}), 200

