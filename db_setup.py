# db_setup.py
import sqlite3

def create_tables():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    
    # Table for issues
    c.execute('''CREATE TABLE IF NOT EXISTS issues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL
    )''')
    
    # Table for comments
    c.execute('''CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        issue_id INTEGER,
        text TEXT NOT NULL,
        FOREIGN KEY (issue_id) REFERENCES issues(id)
    )''')
    
    # Table for reactions
    c.execute('''CREATE TABLE IF NOT EXISTS reactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        issue_id INTEGER,
        reaction_type TEXT NOT NULL,
        count INTEGER DEFAULT 1,
        FOREIGN KEY (issue_id) REFERENCES issues(id)
    )''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
