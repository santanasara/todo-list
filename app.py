import os
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///list.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(120), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    creationDate = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id



@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task = Todo(content=request.form['content'])
        
        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/')
        except:
            print("Error.")
    else:
        tasks = Todo.query.all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    taskDelete = Todo.query.get_or_404(id)

    try:
        db.session.delete(taskDelete)
        db.session.commit()
        return redirect('/')
    except:
        return "Unable to delete task"

if __name__ == "__main__":
    app.run(debug=True)
