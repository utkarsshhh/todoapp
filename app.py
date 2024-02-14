from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',data = [{'description':'TODO 1'},{'description':'TODO 2'},{'description':'TODO 3'},])

if __name__ == '__main__':
    app.run()