from flask import Flask, request
import sqlite3

app = Flask(__name__)

# 🔧 Setup (creates table and inserts one dummy user)
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return '''
        <form action="/login">
            Username: <input name="username"><br>
            Password: <input name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # 🚨 VULNERABLE: user inputs directly embedded in SQL query (NO parameterization)
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print("[DEBUG] Executing:", query)
    cursor.execute(query)

    result = cursor.fetchone()
    conn.close()

    if result:
        return "<h2>✅ Login Successful!</h2>"
    else:
        return "<h2>❌ Login Failed!</h2>"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
