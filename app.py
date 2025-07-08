# app.py (SQLite Version)
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# ----- DB Setup -----
DB_NAME = 'focus.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        task TEXT NOT NULL,
                        done INTEGER DEFAULT 0,
                        timestamp TEXT NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id))''')

init_db()

# ----- Helper Functions -----
def get_user_id(username):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        row = c.fetchone()
        return row[0] if row else None

def get_tasks(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT id, task, done, timestamp FROM tasks WHERE user_id = ?", (user_id,))
        return [dict(id=row[0], task=row[1], done=bool(row[2]), timestamp=row[3]) for row in c.fetchall()]

# ----- Routes -----
@app.route('/')
def index():
    if 'username' not in session:
        return redirect('/login')
    user_id = get_user_id(session['username'])
    tasks = get_tasks(user_id)
    return render_template('index.html', tasks=tasks, username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
            row = c.fetchone()
            if row and check_password_hash(row[0], password):
                session['username'] = username
                return redirect('/')
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            try:
                c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password))
                conn.commit()
            except sqlite3.IntegrityError:
                return 'Username already taken'
        return redirect('/login')
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/add', methods=['POST'])
def add_task():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    task = request.json.get('task')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    user_id = get_user_id(session['username'])
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO tasks (user_id, task, done, timestamp) VALUES (?, ?, 0, ?)", (user_id, task, timestamp))
        conn.commit()
    return jsonify({'success': True, 'task': task, 'timestamp': timestamp})

@app.route('/toggle/<int:index>', methods=['POST'])
def toggle_task(index):
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    user_id = get_user_id(session['username'])
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT id, done FROM tasks WHERE user_id = ? ORDER BY id", (user_id,))
        tasks = c.fetchall()
        if 0 <= index < len(tasks):
            task_id, done = tasks[index]
            c.execute("UPDATE tasks SET done = ? WHERE id = ?", (0 if done else 1, task_id))
            conn.commit()
    return jsonify({'success': True})

@app.route('/delete/<int:index>', methods=['POST'])
def delete_task(index):
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    user_id = get_user_id(session['username'])
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM tasks WHERE user_id = ? ORDER BY id", (user_id,))
        tasks = c.fetchall()
        if 0 <= index < len(tasks):
            task_id = tasks[index][0]
            c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
