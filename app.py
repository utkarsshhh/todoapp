from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:utk%40123@localhost:5432/todoapp'
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer,primary_key = True)
    description = db.Column(db.String(),nullable = False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html',data = Todo.query.all())

if __name__ == '__main__':
    app.run()