from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"'<Task {self.id!r}>'"


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        # Push it to our database
        try:
            db.session.add(new_task)
            db.session.commit()
            # Redirect to the index
            return redirect('/')
        except Exception as e:
            print(f"There was a problem adding your task. Error: {e}.", file=sys.stderr)

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:identifier>')
def delete(identifier):
    task_to_delete = Todo.query.get_or_404(identifier)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print(f"There was a problem deleting your task. Error: {e}.", file=sys.stderr)


@app.route('/update/<int:identifier>', methods=['GET', 'POST'])
def update(identifier):
    task = Todo.query.get_or_404(identifier)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"There was a problem updating your task. Error: {e}.", file=sys.stderr)
    else:
        return render_template('update.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)
