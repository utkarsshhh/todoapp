from flask import Flask, render_template, request, jsonify, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
from flask_migrate import Migrate
import sys

app = Flask(__name__)
# CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:utk%40123@localhost:5432/todoapp'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    name = db.Column(db.String(),nullable= False)
    todos = db.relationship('Todo',backref = 'list',lazy = True)

    def __repr__(self):
        return f'<TodoList {self.id} {self.name}>'


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer,primary_key = True, autoincrement=True)
    description = db.Column(db.String(),nullable = False)
    completed = db.Column(db.Boolean, nullable=False)
    list_id = db.Column(db.Integer,db.ForeignKey('todolists.id'),nullable = True)


    def __repr__(self):
        return f'<Todo {self.id} {self.description}, list {self.list_id}>>'

# with app.app_context():
#     db.create_all()


@app.route('todos/delete_list/<list_id>',methods = ['DELETE'])
def delete_list(list_id):
    error = False




@app.route('/todos/create_list',methods= ['POST'])
def create_list():
    error = False
    body = {}
    try:
        list_name = request.get_json()['list_name']
        list = TodoList(name = list_name)
        db.session.add(list)
        db.session.commit()
        body['list_name'] = list.name
    except:
        db.session.rollback()
        error = True
        print (sys.exc_info())
    finally:
        db.session.close()
    if (error):
        abort(400)
    else:
        return jsonify(body)

@app.route('/todos/create',methods = ['POST'])
def create_todo():

    error = False
    body = {}
    try:
        description = request.get_json()['description']
        list_id = request.get_json()['listId']
        todo = Todo(description=description,list_id = list_id,completed = False)
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


@app.route('/todos/<delete_id>/delete-todo',methods = ['DELETE'])
def delete_todo(delete_id):
    error = False
    try:
        # delete_id = request.get_json()['id']
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
        return redirect(url_for('index'))


@app.route('/todolist/<list_id>')
def get_list(list_id):
    # lists = [list_obj.serialize() for list_obj in TodoList.query.all()]
    lists = [{"id": list_obj.id, "name": list_obj.name} for list_obj in TodoList.query.all()]
    todos = []
    for todo_obj in Todo.query.filter_by(list_id=list_id).order_by(Todo.id).all():
        todo_dict = {
            "id": todo_obj.id,
            "completed": todo_obj.completed,
            "description": todo_obj.description,
            "list_id":todo_obj.list_id
            # Add more attributes as needed
        }
        todos.append(todo_dict)

    return render_template('index.html', data={"list_id": list_id, "lists": lists,
                                               "todos":todos})



@app.route('/')
def index():
    return redirect(url_for('get_list',list_id = 1))

if __name__ == '__main__':
    app.run(debug=True)