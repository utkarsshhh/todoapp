from flask import Flask, render_template, request, jsonify, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import sys

app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:utk%40123@localhost:5432/todoapp'
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer,primary_key = True, autoincrement=True)
    description = db.Column(db.String(),nullable = False)
    completed = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

with app.app_context():
    db.create_all()

@app.route('/todos/create',methods = ['POST'])
def create_todo():

    error = False
    body = {}
    try:
        description = request.get_json()['description']
        todo = Todo(description=description,completed = False)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        db.session.rollback()
        error = True
        print (sys.exc_info())
    finally:
        db.session.close()
    if (error):
        abort(400)
    if (not error):
        return jsonify(body)

@app.route('/todos/<todo_id>/set-completed',methods = ['POST'])
def set_completed(todo_id):
    try:
        completed = request.get_json()['completed']
        print('completed', completed)
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        print ("error in setting completed")
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/delete-todo',methods = ['POST'])
def delete_todo():
    error = False
    try:
        delete_id = request.get_json()['id']
        Todo.query.filter_by(id=delete_id).delete()
        db.session.commit()
    except Exception as e:
        print (e)
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    print ('before return')
    if error:
        abort(400)
    else:
        return '200'



@app.route('/')
def index():
    return render_template('index.html',data = Todo.query.order_by(Todo.id).all())

if __name__ == '__main__':
    app.run(debug=True)