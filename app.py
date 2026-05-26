from flask import Flask, render_template, redirect
import sqlite3

app = Flask(__name__)

# CREATE DATABASE
def init_db():

    conn = sqlite3.connect('team.db')

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT,
            available INTEGER
        )
    ''')

    # CHECK IF DATA EXISTS
    cursor.execute('SELECT COUNT(*) FROM members')

    count = cursor.fetchone()[0]

    # INSERT DEFAULT USERS
    if count == 0:

        users = [

            ('Alex Rivers', 'Senior Developer', 1),
            ('Samantha Chen', 'UX Designer', 0),
            ('Jordan Taylor', 'Project Manager', 1),
            ('Maria Garcia', 'Marketing Lead', 0),
            ('David Kim', 'Backend Engineer', 1)

        ]

        cursor.executemany(
            'INSERT INTO members (name, role, available) VALUES (?, ?, ?)',
            users
        )

    conn.commit()
    conn.close()

init_db()


# HOME PAGE
@app.route('/')
def home():

    conn = sqlite3.connect('team.db')

    cursor = conn.cursor()

    cursor.execute('SELECT * FROM members')

    members = cursor.fetchall()

    conn.close()

    return render_template(
        'index.html',
        members=members
    )


# TOGGLE AVAILABILITY
@app.route('/toggle/<int:id>')
def toggle(id):

    conn = sqlite3.connect('team.db')

    cursor = conn.cursor()

    # GET CURRENT STATUS
    cursor.execute(
        'SELECT available FROM members WHERE id=?',
        (id,)
    )

    current = cursor.fetchone()[0]

    # TOGGLE VALUE
    new_value = 0 if current == 1 else 1

    # UPDATE DATABASE
    cursor.execute(
        'UPDATE members SET available=? WHERE id=?',
        (new_value, id)
    )

    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)