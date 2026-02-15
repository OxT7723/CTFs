from flask import Flask, request, render_template_string, session, redirect, url_for, g, make_response
import sqlite3
import hashlib
import os
import unicodedata
import json
import re

app = Flask(__name__)
app.secret_key = os.urandom(32)

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def filter_security_input(tags):
    if not tags:
        return tags
    
    regex = re.compile(
        r"^(?!.*['\";\-#=<>|&])"
        r"(?!.*(/\*|\*/))"
        r"(?!.*(union|select|insert|update|delete|drop|create|alter|exec|execute|where|from|join|order|group|having|limit|offset|into|values|set|table|database|column|index|view|trigger|procedure|function|declare|cast|convert|char|concat|substring|ascii|hex|unhex|sleep|benchmark|waitfor|delay|information_schema|sysobjects|syscolumns))"
        r".+$",
        re.IGNORECASE
    )
    
    if not regex.match(tags):
        return None
    
    normalized = unicodedata.normalize('NFKC', tags)
    
    return normalized

BASE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>NoteShare</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0f0f23;
            color: #e8eaed;
            min-height: 100vh;
            padding: 0;
            line-height: 1.6;
        }
        .header {
            background: #1a1a2e;
            border-bottom: 1px solid #2d2d44;
            padding: 18px 0;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        .header-content {
            max-width: 1280px;
            margin: 0 auto;
            padding: 0 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo {
            font-size: 22px;
            font-weight: 600;
            color: #4a9eff;
            letter-spacing: 0.5px;
        }
        .nav {
            display: flex;
            gap: 8px;
            align-items: center;
        }
        .nav a {
            color: #9ca3af;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            padding: 8px 16px;
            border-radius: 6px;
            transition: all 0.2s;
        }
        .nav a:hover { 
            color: #fff;
            background: #2d2d44;
        }
        .nav .active { 
            color: #fff;
            background: #2d2d44;
        }
        .container {
            max-width: 1280px;
            margin: 0 auto;
            padding: 40px;
        }
        .main-content {
            background: #1a1a2e;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        }
        h1 { 
            color: #fff;
            margin-bottom: 12px;
            font-size: 32px;
            font-weight: 600;
        }
        h2 { 
            color: #fff;
            margin-bottom: 20px;
            margin-top: 40px;
            font-size: 20px;
            font-weight: 600;
            padding-bottom: 12px;
            border-bottom: 1px solid #2d2d44;
        }
        .subtitle {
            color: #9ca3af;
            margin-bottom: 32px;
            font-size: 15px;
        }
        input[type="text"], input[type="password"], input[type="file"], textarea {
            width: 100%;
            padding: 12px 16px;
            margin: 10px 0;
            border: 1px solid #2d2d44;
            border-radius: 8px;
            font-size: 14px;
            font-family: inherit;
            background: #0f0f23;
            color: #e8eaed;
            transition: border 0.2s;
        }
        input:focus, textarea:focus {
            outline: none;
            border-color: #4a9eff;
        }
        button, .btn {
            background: #4a9eff;
            color: #fff;
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.2s;
            text-decoration: none;
            display: inline-block;
        }
        button:hover, .btn:hover { 
            background: #3d8ae6;
            transform: translateY(-1px);
        }
        .btn-secondary {
            background: #2d2d44;
            color: #e8eaed;
        }
        .btn-secondary:hover { 
            background: #3d3d54;
        }
        .error { 
            background: #3d1a1a;
            color: #ff6b6b;
            padding: 14px 18px;
            border-radius: 8px;
            margin: 12px 0;
            border: 1px solid #5d2a2a;
            font-size: 14px;
        }
        .success { 
            background: #1a3d1a;
            color: #6bff6b;
            padding: 14px 18px;
            border-radius: 8px;
            margin: 12px 0;
            border: 1px solid #2a5d2a;
            font-size: 14px;
        }
        .note-card {
            background: #16162a;
            padding: 24px;
            margin: 16px 0;
            border-radius: 10px;
            border: 1px solid #2d2d44;
            transition: all 0.3s;
        }
        .note-card:hover {
            transform: translateY(-2px);
            border-color: #4a9eff;
            box-shadow: 0 4px 16px rgba(74, 158, 255, 0.1);
        }
        .note-card h3 {
            margin-bottom: 12px;
            color: #fff;
            font-size: 18px;
            font-weight: 600;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .note-card p {
            color: #9ca3af;
            font-size: 14px;
            line-height: 1.7;
        }
        .note-meta {
            color: #6b7280;
            font-size: 12px;
            margin-top: 16px;
            padding-top: 16px;
            border-top: 1px solid #2d2d44;
        }
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .badge-user { background: #1e3a8a; color: #93c5fd; }
        .badge-editor { background: #78350f; color: #fbbf24; }
        .badge-admin { background: #7f1d1d; color: #fca5a5; }
        .badge-shared { background: #14532d; color: #86efac; }
        .badge-private { background: #374151; color: #9ca3af; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: #16162a;
            border-radius: 8px;
            overflow: hidden;
        }
        th, td {
            padding: 14px 16px;
            text-align: left;
            border-bottom: 1px solid #2d2d44;
            font-size: 14px;
        }
        th { 
            background: #1a1a2e;
            color: #4a9eff;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 0.5px;
        }
        tr:hover { background: #1a1a2e; }
        tr:last-child td { border-bottom: none; }
        code {
            background: #16162a;
            padding: 3px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            color: #4a9eff;
            border: 1px solid #2d2d44;
        }
        a { color: #4a9eff; transition: color 0.2s; }
        a:hover { color: #3d8ae6; }
        .checkbox-label {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 16px 0;
            cursor: pointer;
            color: #e8eaed;
            font-size: 14px;
        }
        input[type="checkbox"] {
            width: 18px;
            height: 18px;
            cursor: pointer;
            accent-color: #4a9eff;
        }
        .auth-container {
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            background: radial-gradient(ellipse at bottom, #1a1a2e 0%, #0f0f23 100%);
        }
        .auth-box {
            background: #1a1a2e;
            padding: 48px;
            border-radius: 16px;
            border: 1px solid #2d2d44;
            max-width: 420px;
            width: 100%;
            box-shadow: 0 8px 32px rgba(0,0,0,0.5);
        }
        .auth-box h1 {
            text-align: center;
            color: #4a9eff;
            font-size: 28px;
            margin-bottom: 8px;
        }
        .auth-box .subtitle {
            text-align: center;
            color: #9ca3af;
            font-size: 14px;
            margin-bottom: 32px;
        }
        .auth-box input {
            background: #16162a;
            border: 1px solid #2d2d44;
        }
        .auth-box button {
            width: 100%;
            padding: 14px;
            font-size: 15px;
            margin-top: 8px;
        }
        .auth-footer {
            margin-top: 24px;
            text-align: center;
            font-size: 13px;
            color: #6b7280;
        }
        .auth-footer a {
            color: #4a9eff;
            font-weight: 600;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin-top: 32px;
        }
        .stat-card {
            background: #16162a;
            padding: 28px;
            border-radius: 12px;
            border: 1px solid #2d2d44;
            transition: all 0.3s;
        }
        .stat-card:hover {
            transform: translateY(-4px);
            border-color: #4a9eff;
            box-shadow: 0 6px 20px rgba(74, 158, 255, 0.15);
        }
        .stat-value {
            font-size: 36px;
            font-weight: 700;
            margin-top: 12px;
            color: #4a9eff;
        }
        .stat-label {
            font-size: 13px;
            color: #9ca3af;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .warning-banner {
            background: #3d2a1a;
            border: 1px solid #5d4a2a;
            color: #fbbf24;
            padding: 12px 16px;
            border-radius: 8px;
            margin: 16px 0;
            font-size: 13px;
        }
    </style>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
'''

LOGIN_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
    <div class="auth-container">
        <div class="auth-box">
            <h1>NoteShare</h1>
            <p class="subtitle">Secure collaborative note platform</p>
            {% if error %}
            <div class="error">{{ error }}</div>
            {% endif %}
            <form method="POST">
                <input type="text" name="username" placeholder="Username" required autofocus>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Sign in</button>
            </form>
            <div class="auth-footer">
                Don't have an account? <a href="/register">Create one</a>
            </div>
        </div>
    </div>
''')

REGISTER_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
    <div class="auth-container">
        <div class="auth-box">
            <h1>Create Account</h1>
            <p class="subtitle">Join NoteShare today</p>
            {% if error %}
            <div class="error">{{ error }}</div>
            {% endif %}
            {% if success %}
            <div class="success">{{ success }}</div>
            {% endif %}
            <form method="POST">
                <input type="text" name="username" placeholder="Username" required autofocus>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Create Account</button>
            </form>
            <div class="auth-footer">
                Already have an account? <a href="/">Sign in</a>
            </div>
        </div>
    </div>
''')

DASHBOARD_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
    <div class="header">
        <div class="header-content">
            <div class="logo">NoteShare</div>
            <div class="nav">
                <a href="/dashboard" class="active">Dashboard</a>
                <a href="/notes">My Notes</a>
                <a href="/shared">Shared Notes</a>
                {% if role == 'editor' or role == 'admin' %}
                <a href="/settings">Settings</a>
                {% endif %}
                {% if role == 'admin' %}
                <a href="/admin">Admin</a>
                {% endif %}
                <span class="badge badge-{{ role }}">{{ role }}</span>
                <a href="/logout">Logout</a>
            </div>
        </div>
    </div>
    <div class="container">
        <div class="main-content">
            <h1>Welcome back, {{ username }}</h1>
            <p class="subtitle">Manage your notes and collaborate with others</p>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Your Notes</div>
                    <div class="stat-value" style="color: #58a6ff;">{{ note_count }}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Shared Notes</div>
                    <div class="stat-value" style="color: #56d364;">{{ shared_count }}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Account Type</div>
                    <div class="stat-value" style="font-size: 20px; text-transform: uppercase;">{{ role }}</div>
                </div>
            </div>
        </div>
    </div>
''')

NOTES_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
    <div class="header">
        <div class="header-content">
            <div class="logo">NoteShare</div>
            <div class="nav">
                <a href="/dashboard">Dashboard</a>
                <a href="/notes" class="active">My Notes</a>
                <a href="/shared">Shared Notes</a>
                {% if role == 'editor' or role == 'admin' %}
                <a href="/settings">Settings</a>
                {% endif %}
                {% if role == 'admin' %}
                <a href="/admin">Admin</a>
                {% endif %}
                <span class="badge badge-{{ role }}">{{ role }}</span>
                <a href="/logout">Logout</a>
            </div>
        </div>
    </div>
    <div class="container">
        <div class="main-content">
            <h1>My Notes</h1>
            <p class="subtitle">Create and manage your personal notes</p>
            
            <h2>Create New Note</h2>
            <form method="POST" action="/notes/create">
                <input type="text" name="title" placeholder="Note title" required>
                <textarea name="content" placeholder="Note content..." rows="5" required></textarea>
                <input type="text" name="tags" placeholder="Tags (comma separated, e.g: work,ideas,project)">
                <label class="checkbox-label">
                    <input type="checkbox" name="shared" value="1">
                    <span>Share this note publicly</span>
                </label>
                <button type="submit">Create Note</button>
            </form>
            
            <h2>Your Notes</h2>
            {% if notes %}
            {% for note in notes %}
            <div class="note-card">
                <h3>
                    {{ note.title }}
                    {% if note.shared %}
                    <span class="badge badge-shared">Shared</span>
                    {% else %}
                    <span class="badge badge-private">Private</span>
                    {% endif %}
                </h3>
                <p>{{ note.content }}</p>
                {% if note.tags %}
                <div class="note-meta">
                    Tags: <code>{{ note.tags }}</code>
                    {% if note.shared %}
                    | <a href="/shared/{{ note.id }}">View Public Link</a>
                    {% endif %}
                </div>
                {% endif %}
            </div>
            {% endfor %}
            {% else %}
            <p style="color: #8b949e; margin-top: 16px;">No notes yet. Create your first note above.</p>
            {% endif %}
        </div>
    </div>
''')

SHARED_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
    <div class="header">
        <div class="header-content">
            <div class="logo">NoteShare</div>
            <div class="nav">
                <a href="/dashboard">Dashboard</a>
                <a href="/notes">My Notes</a>
                <a href="/shared" class="active">Shared Notes</a>
                {% if role == 'editor' or role == 'admin' %}
                <a href="/settings">Settings</a>
                {% endif %}
                {% if role == 'admin' %}
                <a href="/admin">Admin</a>
                {% endif %}
                <span class="badge badge-{{ role }}">{{ role }}</span>
                <a href="/logout">Logout</a>
            </div>
        </div>
    </div>
    <div class="container">
        <div class="main-content">
            <h1>Shared Notes</h1>
            <p class="subtitle">Browse notes shared by other users</p>
            
            <h2>Public Notes</h2>
            {% if notes %}
            {% for note in notes %}
            <div class="note-card">
                <h3>{{ note.title }}</h3>
                <p>{{ note.content }}</p>
                <div class="note-meta">
                    Shared by <strong style="color: #58a6ff;">{{ note.author }}</strong>
                    {% if note.tags %}
                    | Tags: <code>{{ note.tags }}</code>
                    {% endif %}
                    | <a href="/shared/{{ note.id }}">Permalink</a>
                </div>
            </div>
            {% endfor %}
            {% else %}
            <p style="color: #8b949e; margin-top: 16px;">No shared notes found.</p>
            {% endif %}
        </div>
    </div>
''')

SHARED_NOTE_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
    <div class="header">
        <div class="header-content">
            <div class="logo">NoteShare</div>
            <div class="nav">
                <a href="/dashboard">Dashboard</a>
                <a href="/notes">My Notes</a>
                <a href="/shared" class="active">Shared Notes</a>
                {% if role == 'editor' or role == 'admin' %}
                <a href="/settings">Settings</a>
                {% endif %}
                {% if role == 'admin' %}
                <a href="/admin">Admin</a>
                {% endif %}
                <span class="badge badge-{{ role }}">{{ role }}</span>
                <a href="/logout">Logout</a>
            </div>
        </div>
    </div>
    <div class="container">
        <div class="main-content">
            {% if error %}
            <div class="error">{{ error }}</div>
            <p style="margin-top: 20px;"><a href="/shared">← Back to Shared Notes</a></p>
            {% elif note %}
            <h1>{{ note.title }}</h1>
            <p class="subtitle">Shared by <strong style="color: #58a6ff;">{{ note.author }}</strong> • Total Views: <strong>{{ view_count|default(0) }}</strong></p>
            
            <div class="note-card">
                <p style="white-space: pre-wrap;">{{ note.content }}</p>
                {% if note.tags %}
                <div class="note-meta">
                    Tags: <code>{{ note.tags }}</code>
                </div>
                {% endif %}
            </div>
            
            {% if tag_stats %}
            <h2>View Statistics by Tag</h2>
            <table>
                <tr>
                    <th>Action Type</th>
                    <th>View Count</th>
                </tr>
                {% for stat in tag_stats %}
                <tr>
                    <td>{{ stat.action }}</td>
                    <td><strong style="color: #56d364;">{{ stat.count }}</strong></td>
                </tr>
                {% endfor %}
            </table>
            {% endif %}
            
            <p style="margin-top: 24px;"><a href="/shared">← Back to Shared Notes</a></p>
            {% endif %}
        </div>
    </div>
''')

SETTINGS_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
    <div class="header">
        <div class="header-content">
            <div class="logo">NoteShare</div>
            <div class="nav">
                <a href="/dashboard">Dashboard</a>
                <a href="/notes">My Notes</a>
                <a href="/shared">Shared Notes</a>
                <a href="/settings" class="active">Settings</a>
                {% if role == 'admin' %}
                <a href="/admin">Admin</a>
                {% endif %}
                <span class="badge badge-{{ role }}">{{ role }}</span>
                <a href="/logout">Logout</a>
            </div>
        </div>
    </div>
    <div class="container">
        <div class="main-content">
            <h1>User Settings</h1>
            <p class="subtitle">Customize your preferences</p>
            
            {% if error %}
            <div class="error">{{ error }}</div>
            {% endif %}
            {% if success %}
            <div class="success">{{ success }}</div>
            {% endif %}
            
            <h2>Profile</h2>
            <form method="POST" action="/settings/profile">
                <input type="text" name="display_name" placeholder="Display Name" value="{{ profile.get('display_name', '') }}">
                <input type="text" name="bio" placeholder="Bio" value="{{ profile.get('bio', '') }}">
                <input type="text" name="website" placeholder="Website" value="{{ profile.get('website', '') }}">
                <button type="submit">Update Profile</button>
            </form>
            
            <h2>Import/Export Settings</h2>
            <form method="POST" action="/settings/import" enctype="multipart/form-data">
                <p style="color: #8b949e; font-size: 13px; margin-bottom: 12px;">Import preferences from a JSON file</p>
                <input type="file" name="config_file" accept=".json">
                <button type="submit" style="margin-top: 12px;">Import Configuration</button>
            </form>
            
            <form method="POST" action="/settings/export" style="margin-top: 20px;">
                <button type="submit" class="btn-secondary">Export Current Settings</button>
            </form>
            
            <p style="margin-top: 16px; color: #6e7681; font-size: 13px;">
                JSON format supports nested objects for advanced configuration
            </p>
        </div>
    </div>
''')

ADMIN_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
    <div class="header">
        <div class="header-content">
            <div class="logo">NoteShare</div>
            <div class="nav">
                <a href="/dashboard">Dashboard</a>
                <a href="/notes">My Notes</a>
                <a href="/shared">Shared Notes</a>
                <a href="/settings">Settings</a>
                <a href="/admin" class="active">Admin</a>
                <span class="badge badge-{{ role }}">{{ role }}</span>
                <a href="/logout">Logout</a>
            </div>
        </div>
    </div>
    <div class="container">
        <div class="main-content">
            <h1>System Administration</h1>
            <p class="subtitle">Monitor system activity and logs</p>
            
            {% if error %}
            <div class="error">{{ error }}</div>
            {% endif %}
            {% if success %}
            <div class="success">{{ success }}</div>
            {% endif %}
            
            <h2>Activity Logs</h2>
            <table>
                <tr>
                    <th>ID</th>
                    <th>User</th>
                    <th>Action</th>
                    <th>Metadata</th>
                    <th>Timestamp</th>
                </tr>
                {% for log in logs %}
                <tr>
                    <td><strong>#{{ log.id }}</strong></td>
                    <td><span class="badge badge-user">{{ log.username }}</span></td>
                    <td>{{ log.action }}</td>
                    <td><code>{{ log.metadata if log.metadata else '-' }}</code></td>
                    <td>{{ log.timestamp }}</td>
                </tr>
                {% endfor %}
            </table>
            
            <h2>Export Logs</h2>
            <form method="POST" action="/admin/export">
                <input type="text" name="filename" placeholder="Export filename (e.g., audit_2024-01-15.log)" required>
                <input type="text" name="format" placeholder="Format (log, csv, json)" value="log">
                <button type="submit">Export Logs</button>
            </form>
            <p style="margin-top: 16px; color: #6e7681; font-size: 13px;">
                Logs will be saved to <code>/var/log/noteshare/exports/</code>
            </p>
        </div>
    </div>
''')


class Config:
    def __init__(self):
        self.__class__.__name__ = 'Config'


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                         (username, hashlib.md5(password.encode()).hexdigest())).fetchone()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            
            db.execute('INSERT INTO logs (user_id, action, metadata) VALUES (?, ?, ?)', 
                      (user['id'], 'User logged in', f'ip={request.remote_addr}'))
            db.commit()
            
            return redirect(url_for('dashboard'))
        else:
            return render_template_string(LOGIN_TEMPLATE, error='Invalid credentials')
    
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        if not username or not password:
            return render_template_string(REGISTER_TEMPLATE, error='All fields are required')
        
        db = get_db()
        try:
            db.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                      (username, hashlib.md5(password.encode()).hexdigest(), 'user'))
            db.commit()
            return render_template_string(REGISTER_TEMPLATE, success='Account created! You can now login.')
        except sqlite3.IntegrityError:
            return render_template_string(REGISTER_TEMPLATE, error='Username already exists')
    
    return render_template_string(REGISTER_TEMPLATE)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    note_count = db.execute('SELECT COUNT(*) as count FROM notes WHERE user_id = ?', 
                           (session['user_id'],)).fetchone()['count']
    shared_count = db.execute('SELECT COUNT(*) as count FROM notes WHERE shared = 1').fetchone()['count']
    
    return render_template_string(DASHBOARD_TEMPLATE, 
                                 username=session['username'],
                                 role=session['role'],
                                 note_count=note_count,
                                 shared_count=shared_count)

@app.route('/notes', methods=['GET'])
def notes():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    notes = db.execute('SELECT * FROM notes WHERE user_id = ? ORDER BY id DESC', 
                      (session['user_id'],)).fetchall()
    
    return render_template_string(NOTES_TEMPLATE, 
                                 notes=notes,
                                 role=session['role'])

@app.route('/notes/create', methods=['POST'])
def create_note():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    title = request.form.get('title', '')
    content = request.form.get('content', '')
    tags = request.form.get('tags', '')
    shared = 1 if request.form.get('shared') else 0
    
    tags_filtered = filter_security_input(tags) if tags else ''
    
    if tags and not tags_filtered:
        db = get_db()
        notes = db.execute('SELECT * FROM notes WHERE user_id = ? ORDER BY id DESC', 
                          (session['user_id'],)).fetchall()
        return render_template_string(NOTES_TEMPLATE + 
                                     '<script>alert("Security filter: Invalid characters or patterns detected in tags");</script>',
                                     notes=notes,
                                     role=session['role'])
    
    db = get_db()
    db.execute('INSERT INTO notes (user_id, title, content, shared, tags) VALUES (?, ?, ?, ?, ?)',
              (session['user_id'], title, content, shared, tags_filtered))
    
    action = f"Created note: {title}"
    metadata = f"shared={shared}, tags={tags_filtered}"
    db.execute('INSERT INTO logs (user_id, action, metadata) VALUES (?, ?, ?)', 
              (session['user_id'], action, metadata))
    db.commit()
    
    return redirect(url_for('notes'))

@app.route('/shared')
def shared():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    notes = db.execute('''SELECT notes.id, notes.title, notes.content, notes.tags, users.username as author 
                         FROM notes 
                         JOIN users ON notes.user_id = users.id 
                         WHERE notes.shared = 1 
                         ORDER BY notes.id DESC''').fetchall()
    
    return render_template_string(SHARED_TEMPLATE, 
                                 notes=notes,
                                 role=session['role'])

@app.route('/shared/<note_id>')
def view_shared_note(note_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if not note_id.isdigit():
        return render_template_string(SHARED_NOTE_TEMPLATE, 
                                     error='Invalid note ID format',
                                     role=session['role'])
    
    db = get_db()
    try:
        note = db.execute('''SELECT notes.id, notes.title, notes.content, notes.tags, users.username as author 
                            FROM notes 
                            JOIN users ON notes.user_id = users.id 
                            WHERE notes.id = ? AND notes.shared = 1''', (note_id,)).fetchone()
        
        if not note:
            return render_template_string(SHARED_NOTE_TEMPLATE,
                                         error='Note not found or not shared',
                                         role=session['role'])
        
        tags = note['tags'] if note['tags'] else ''
        
        db.execute('INSERT INTO logs (user_id, action, metadata) VALUES (?, ?, ?)', 
                  (session['user_id'], f'Viewed shared note: {note["title"]}', f'tags={tags}'))
        db.commit()
        
        view_count = 0
        tag_stats = []
        
        if tags:
            stats_query = f"SELECT action, COUNT(*) as count FROM logs WHERE metadata LIKE '%{tags}%' GROUP BY action"
            try:
                results = db.execute(stats_query).fetchall()
                for row in results:
                    tag_stats.append({
                        'action': row['action'],
                        'count': row['count']
                    })
                view_count = sum([stat['count'] for stat in tag_stats])
            except Exception as sqli_error:
                view_count = 0
                tag_stats = [{'action': f'SQL Error: {str(sqli_error)}', 'count': 0}]
        
        return render_template_string(SHARED_NOTE_TEMPLATE,
                                     note=note,
                                     role=session['role'],
                                     view_count=view_count,
                                     tag_stats=tag_stats)
    except Exception as e:
        return render_template_string(SHARED_NOTE_TEMPLATE,
                                     error=f'Error loading note: {str(e)}',
                                     role=session['role'])


@app.route('/settings', methods=['GET'])
def settings():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session['role'] not in ['editor', 'admin']:
        return redirect(url_for('dashboard'))
    
    if 'profile' not in session:
        session['profile'] = {'display_name': '', 'bio': '', 'website': ''}
    
    return render_template_string(SETTINGS_TEMPLATE,
                                 role=session['role'],
                                 profile=session.get('profile', {}))

@app.route('/settings/profile', methods=['POST'])
def settings_profile():
    if 'user_id' not in session or session['role'] not in ['editor', 'admin']:
        return redirect(url_for('dashboard'))
    
    if 'profile' not in session:
        session['profile'] = {}
    
    session['profile']['display_name'] = request.form.get('display_name', '')
    session['profile']['bio'] = request.form.get('bio', '')
    session['profile']['website'] = request.form.get('website', '')
    session.modified = True
    
    return redirect(url_for('settings'))

@app.route('/settings/import', methods=['POST'])
def settings_import():
    if 'user_id' not in session or session['role'] not in ['editor', 'admin']:
        return redirect(url_for('dashboard'))
    
    if 'config_file' not in request.files:
        return render_template_string(SETTINGS_TEMPLATE,
                                     role=session['role'],
                                     profile=session.get('profile', {}),
                                     error='No file uploaded')
    
    file = request.files['config_file']
    
    if file.filename == '':
        return render_template_string(SETTINGS_TEMPLATE,
                                     role=session['role'],
                                     profile=session.get('profile', {}),
                                     error='No file selected')
    
    try:
        content = file.read().decode('utf-8')
        
        dangerous_patterns = ['__class__', '__globals__', '__builtins__', '__init__', 
                              '__dict__', 'role', 'user_id', 'username']
        
        for pattern in dangerous_patterns:
            if pattern in content.lower():
                raise ValueError(f'Potentially dangerous configuration detected: {pattern}')
        
        config_data = json.loads(content)
        
        if not isinstance(config_data, dict):
            raise ValueError('Invalid JSON structure')
        
        if 'profile' in config_data and isinstance(config_data['profile'], dict):
            if 'profile' not in session:
                session['profile'] = {}
            session['profile'].update(config_data['profile'])
        
        for key, value in config_data.items():
            if key == 'profile':
                continue
            
            if key in ['user_id', 'username', '_sa_instance_state']:
                continue
            
            if isinstance(value, dict):
                if key in session and isinstance(session[key], dict):
                    session[key].update(value)
                else:
                    session[key] = value
            elif isinstance(value, (str, int, float, bool, list, type(None))):
                session[key] = value
        
        session.modified = True
        
        db = get_db()
        db.execute('INSERT INTO logs (user_id, action, metadata) VALUES (?, ?, ?)', 
                  (session['user_id'], 'Imported configuration', f'filename={file.filename}'))
        db.commit()
        
        return render_template_string(SETTINGS_TEMPLATE,
                                     role=session['role'],
                                     profile=session.get('profile', {}),
                                     success='Configuration imported successfully')
    except ValueError as ve:
        if 'profile' not in session or not isinstance(session.get('profile'), dict):
            session['profile'] = {}
        return render_template_string(SETTINGS_TEMPLATE,
                                     role=session['role'],
                                     profile=session.get('profile', {}),
                                     error=f'Validation error: {str(ve)}')
    except Exception as e:
        if 'profile' not in session or not isinstance(session.get('profile'), dict):
            session['profile'] = {}
        
        return render_template_string(SETTINGS_TEMPLATE,
                                     role=session['role'],
                                     profile=session.get('profile', {}),
                                     error=f'Import failed: {str(e)}')


@app.route('/settings/export', methods=['POST'])
def settings_export():
    if 'user_id' not in session or session['role'] not in ['editor', 'admin']:
        return redirect(url_for('dashboard'))
    
    export_data = {
        'profile': session.get('profile', {})
    }
    
    response = make_response(json.dumps(export_data, indent=2))
    response.headers['Content-Type'] = 'application/json'
    response.headers['Content-Disposition'] = 'attachment; filename=config.json'
    
    return response

@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session['role'] != 'admin':
        return redirect(url_for('dashboard'))
    
    db = get_db()
    logs = db.execute('''SELECT logs.id, logs.action, logs.metadata, logs.timestamp, users.username 
                        FROM logs 
                        JOIN users ON logs.user_id = users.id 
                        ORDER BY logs.id DESC LIMIT 100''').fetchall()
    
    return render_template_string(ADMIN_TEMPLATE,
                                 role=session['role'],
                                 logs=logs)

@app.route('/admin/export', methods=['POST'])
def export_logs():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    filename = request.form.get('filename', 'audit.log')
    format_type = request.form.get('format', 'log')
    
    allowed_formats = ['log', 'csv', 'json']
    if format_type not in allowed_formats:
        format_type = 'log'
    
    blacklist = [';', '|', '&', '`', '$', ' ', ',', '{', '}']
    for char in blacklist:
        if char in filename or char in format_type:
            return render_template_string(ADMIN_TEMPLATE,
                                        role=session['role'],
                                        logs=get_db().execute('''SELECT logs.id, logs.action, logs.metadata, logs.timestamp, users.username 
                                                                FROM logs JOIN users ON logs.user_id = users.id 
                                                                ORDER BY logs.id DESC LIMIT 100''').fetchall(),
                                        error='Invalid characters detected in filename')
    
    safe_filename = filename.replace('..', '')
    
    export_dir = '/var/log/noteshare/exports'
    os.makedirs(export_dir, exist_ok=True)
    
    filepath = f"{export_dir}/{safe_filename}"
    
    db = get_db()
    logs = db.execute('''SELECT logs.id, logs.action, logs.metadata, logs.timestamp, users.username 
                        FROM logs 
                        JOIN users ON logs.user_id = users.id 
                        ORDER BY logs.id DESC''').fetchall()
    
    try:
        content = ""
        if format_type == 'log':
            for log in logs:
                metadata_str = f" | {log['metadata']}" if log['metadata'] else ""
                content += f"[{log['timestamp']}] {log['username']}: {log['action']}{metadata_str}\n"
        elif format_type == 'csv':
            content = "ID,Username,Action,Metadata,Timestamp\n"
            for log in logs:
                metadata = log['metadata'] if log['metadata'] else ''
                content += f"{log['id']},{log['username']},{log['action']},{metadata},{log['timestamp']}\n"
        elif format_type == 'json':
            log_list = [dict(log) for log in logs]
            content = json.dumps(log_list, indent=2)
        
        import tempfile
        temp = tempfile.NamedTemporaryFile(mode='w', delete=False)
        temp.write(content)
        temp.close()
        
        os.system(f"cat {temp.name} > {filepath} && chmod 644 {filepath}")
        os.unlink(temp.name)
        
        return render_template_string(ADMIN_TEMPLATE,
                                    role=session['role'],
                                    logs=db.execute('''SELECT logs.id, logs.action, logs.metadata, logs.timestamp, users.username 
                                                      FROM logs JOIN users ON logs.user_id = users.id 
                                                      ORDER BY logs.id DESC LIMIT 100''').fetchall(),
                                    success=f'Logs exported successfully to {filepath}')
    except Exception as e:
        return render_template_string(ADMIN_TEMPLATE,
                                    role=session['role'],
                                    logs=db.execute('''SELECT logs.id, logs.action, logs.metadata, logs.timestamp, users.username 
                                                      FROM logs JOIN users ON logs.user_id = users.id 
                                                      ORDER BY logs.id DESC LIMIT 100''').fetchall(),
                                    error=f'Export failed: {str(e)}')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
