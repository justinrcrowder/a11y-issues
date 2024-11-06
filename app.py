# app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    issues = conn.execute('SELECT * FROM issues').fetchall()
    conn.close()
    return render_template('home.html', issues=issues)

@app.route('/issue/<int:issue_id>')
def issue(issue_id):
    conn = get_db_connection()
    issue = conn.execute('SELECT * FROM issues WHERE id = ?', (issue_id,)).fetchone()
    comments = conn.execute('SELECT * FROM comments WHERE issue_id = ?', (issue_id,)).fetchall()
    reactions = conn.execute('SELECT reaction_type, count FROM reactions WHERE issue_id = ?', (issue_id,)).fetchall()
    conn.close()
    return render_template('issue.html', issue=issue, comments=comments, reactions=reactions)

@app.route('/create_issue', methods=('GET', 'POST'))
def create_issue():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        conn = get_db_connection()
        conn.execute('INSERT INTO issues (title, description) VALUES (?, ?)', (title, description))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))

    return render_template('create_issue.html')

@app.route('/issue/<int:issue_id>/add_comment', methods=('POST',))
def add_comment(issue_id):
    text = request.form['text']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO comments (issue_id, text) VALUES (?, ?)', (issue_id, text))
    conn.commit()
    conn.close()
    
    return redirect(url_for('issue', issue_id=issue_id))

@app.route('/issue/<int:issue_id>/react', methods=('POST',))
def react(issue_id):
    reaction_type = request.form['reaction_type']
    
    conn = get_db_connection()
    # Check if reaction exists
    existing_reaction = conn.execute('SELECT * FROM reactions WHERE issue_id = ? AND reaction_type = ?', 
                                     (issue_id, reaction_type)).fetchone()
    if existing_reaction:
        # If reaction exists, increment count
        conn.execute('UPDATE reactions SET count = count + 1 WHERE id = ?', (existing_reaction['id'],))
    else:
        # Otherwise, create a new reaction entry
        conn.execute('INSERT INTO reactions (issue_id, reaction_type, count) VALUES (?, ?, 1)', 
                     (issue_id, reaction_type))
    conn.commit()
    conn.close()
    
    return redirect(url_for('issue', issue_id=issue_id))

if __name__ == '__main__':
    app.run(debug=True)
