from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import sys
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nickyanthony@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean(), nullable=False, default=False)
    list_id = db.Column(db.Integer(), db.ForeignKey('todolists.id'),
                        nullable = False, default = 1)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'


class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean(), nullable=False, default=False)
    todos = db.relationship('Todo', backref='list', lazy=True, cascade="all, delete")

    def __repr__(self):
        return f'<Todo {self.id} {self.name}>'


@app.route('/todos/create', methods=['POST'])
def create_todo():
    new_todo_description = request.get_json()['description']
    new_todo_list_id = request.get_json()['list_id']
    print(request.get_json())
    error_occured = False
    body = {}
    try:
        new_todo = Todo(description=new_todo_description,
                        list_id=new_todo_list_id)
        db.session.add(new_todo)
        db.session.commit()
        body['description'] = new_todo.description
        body['list_id'] = new_todo.list_id
    except:
        db.session.rollback()
        error_occured = True
        print(sys.exec_info())
    finally:
        db.session.close()
    if not error_occured:
        return jsonify(body)


@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    new_completed_state = request.get_json()['completed']
    error_occured = False
    body = {}
    try:
        todo = Todo.query.filter_by(id=todo_id).first()
        if not todo:
            error_occured = True
            raise Exception("Todo with id %s not found in the DB" % todo_id)
        todo.completed = new_completed_state
        db.session.commit()
        body['id'] = todo.id
        body['description'] = todo.description
    except:
        db.session.rollback()
        error_occured = True
        print(sys.exec_info())
    finally:
        db.session.close()
    if not error_occured:
        return redirect(url_for('index'))



@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        todo = Todo.query.filter_by(id=todo_id).first()
        if not todo:
            raise Exception("Todo with id %s not found in the DB" % todo_id)
        db.session.delete(todo)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({ 'success': True })


@app.route('/lists/create', methods=['POST'])
def create_list():
    new_list_name = request.get_json()['name']
    error_occured = False
    body = {}
    try:
        new_list = TodoList(name=new_list_name)
        new_list_id = new_list.id
        db.session.add(new_list)
        db.session.commit()
        body['name'] = new_list.name
    except:
        db.session.rollback()
        error_occured = True
        print(sys.exec_info())
    finally:
        db.session.close()
    if not error_occured:
        return jsonify(body)


@app.route('/lists/<list_id>/set-completed', methods=['POST'])
def set_completed_list(list_id):
    new_completed_state = request.get_json()['completed']
    error_occured = False
    body = {}
    try:
        list = TodoList.query.get(list_id)
        if not list:
            error_occured = True
            raise Exception("List with id %s not found in the DB" % list_id)
        list.completed = new_completed_state
        for todo in list.todos:
            todo.completed = new_completed_state
        db.session.commit()
        body['id'] = list.id
        body['name'] = list.name
    except:
        db.session.rollback()
        error_occured = True
        print(sys.exec_info())
    finally:
        db.session.close()
    if not error_occured:
        return redirect(url_for('index'))



@app.route('/lists/<list_id>', methods=['DELETE'])
def delete_list(list_id):
    try:
        list = TodoList.query.get(list_id)
        if not list:
            raise Exception("List with id %s not found in the DB" % list_id)
        # Because the todo item are marked as "all, delete" or cascade
        # SQLAlchemy will delete them as wel then we delete the associated list.
        db.session.delete(list)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({ 'success': True })


@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template('index.html',
        lists=TodoList.query.order_by('id').all(),
        active_list=TodoList.query.get(list_id),
        todos=Todo.query.filter_by(list_id=list_id).order_by('id').all()
    )


@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))
