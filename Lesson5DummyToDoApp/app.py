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

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

db.create_all()



@app.route('/todos/create', methods=['POST'])
def create_todo():
    new_todo_description = request.get_json()['description']
    error_occured = False
    body = {}
    try:
        new_todo = Todo(description=new_todo_description)
        db.session.add(new_todo)
        db.session.commit()
        body['description'] = new_todo.description
    except:
        db.session.rollback()
        error_occured = True
        print(sys.exec_info())
    finally:
        db.session.close()
    if not error_occured:
        return jsonify(body)

@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())
