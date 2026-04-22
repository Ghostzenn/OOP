from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'task_db'

mysql = MySQL(app)


@app.route('/')
def index():

    q = request.args.get('q')

    cur = mysql.connection.cursor()

    if q:
        cur.execute("""
            SELECT * FROM tasks
            WHERE title LIKE %s OR category LIKE %s
            ORDER BY id DESC
        """, ('%' + q + '%', '%' + q + '%'))
    else:
        cur.execute("SELECT * FROM tasks ORDER BY id DESC")

    rows = cur.fetchall()
    cur.close()

    now = datetime.now()

    ongoing = []
    incomplete = []
    completed = []

    for t in rows:

        deadline = t[3]

        if isinstance(deadline, str):
            deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")

        if t[4] == "completed":
            completed.append(t)

        elif deadline > now:
            ongoing.append(t)

        else:
            incomplete.append(t)

    return render_template(
        'index.html',
        ongoing=ongoing,
        incomplete=incomplete,
        completed=completed,
        q=q
    )


@app.route('/add_or_update', methods=['POST'])
def add_or_update():

    task_id = request.form.get('task_id')
    title = request.form.get('title')
    category = request.form.get('category')
    deadline = request.form.get('deadline')

    cur = mysql.connection.cursor()

    if task_id:
        cur.execute("""
            UPDATE tasks
            SET title=%s, category=%s, deadline=%s
            WHERE id=%s
        """, (title, category, deadline, task_id))
    else:
        cur.execute("""
            INSERT INTO tasks(title, category, deadline, status)
            VALUES(%s, %s, %s, 'ongoing')
        """, (title, category, deadline))

    mysql.connection.commit()
    cur.close()

    return redirect('/')


@app.route('/toggle/<int:id>')
def toggle(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE tasks SET status='completed' WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
