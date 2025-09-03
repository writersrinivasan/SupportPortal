#!/usr/bin/env python3
"""
SupportPortal - WORKING VERSION
Simple Flask app with all features
"""

import os
import sys
from datetime import datetime

print("Starting SupportPortal setup...")

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import Flask modules
from flask import Flask, render_template_string, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supportportal-secret-key-2025'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(current_dir, "supportportal.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

print("✓ Flask app and extensions initialized")

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='client')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='open')
    priority = db.Column(db.String(20), nullable=False, default='medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    user = db.relationship('User', backref=db.backref('tickets', lazy=True))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

print("✓ Database models defined")

# Create database tables
with app.app_context():
    try:
        db.create_all()
        print("✓ Database tables created successfully")
    except Exception as e:
        print(f"Database error: {e}")

# HTML Templates
BASE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SupportPortal</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .navbar-brand { font-weight: bold; }
        .card { margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .priority-high { border-left: 4px solid #dc3545; }
        .priority-medium { border-left: 4px solid #ffc107; }
        .priority-low { border-left: 4px solid #28a745; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">🎫 SupportPortal</a>
            <div class="navbar-nav ms-auto">
                {% if current_user.is_authenticated %}
                    <a class="nav-link" href="/dashboard">Dashboard</a>
                    <a class="nav-link" href="/submit">New Ticket</a>
                    <a class="nav-link" href="/logout">Logout ({{ current_user.username }})</a>
                {% else %}
                    <a class="nav-link" href="/login">Login</a>
                    <a class="nav-link" href="/register">Register</a>
                {% endif %}
            </div>
        </div>
    </nav>
    <div class="container mt-4">
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <div class="alert alert-info alert-dismissible fade show">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# Routes
@app.route('/')
def index():
    content = """
    {% extends "base.html" %}
    {% block content %}
    <div class="row">
        <div class="col-md-8">
            <h1>Welcome to SupportPortal</h1>
            <p class="lead">Professional ticket management system</p>
            {% if current_user.is_authenticated %}
                <div class="alert alert-success">
                    <h5>Hello, {{ current_user.username }}!</h5>
                    <p>Role: <strong>{{ current_user.role.title() }}</strong></p>
                </div>
                <a href="/dashboard" class="btn btn-primary btn-lg me-2">Go to Dashboard</a>
                <a href="/submit" class="btn btn-success btn-lg">Submit New Ticket</a>
            {% else %}
                <p>Please login or register to access the support portal.</p>
                <a href="/login" class="btn btn-primary btn-lg me-2">Login</a>
                <a href="/register" class="btn btn-outline-primary btn-lg">Register</a>
            {% endif %}
        </div>
        <div class="col-md-4">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Features</h5>
                    <ul class="list-unstyled">
                        <li>✅ Submit support tickets</li>
                        <li>📊 Track ticket status</li>
                        <li>👥 Support team management</li>
                        <li>🔒 Secure and private</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}
    """
    return render_template_string(BASE_HTML.replace("{% block content %}{% endblock %}", content))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!')
            return redirect('/dashboard')
        else:
            flash('Invalid username or password')
    
    content = """
    {% extends "base.html" %}
    {% block content %}
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-body">
                    <h2 class="card-title">Login</h2>
                    <form method="POST">
                        <div class="mb-3">
                            <label class="form-label">Username</label>
                            <input type="text" name="username" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Password</label>
                            <input type="password" name="password" class="form-control" required>
                        </div>
                        <button type="submit" class="btn btn-primary">Login</button>
                    </form>
                    <p class="mt-3">Don't have an account? <a href="/register">Register here</a></p>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}
    """
    return render_template_string(BASE_HTML.replace("{% block content %}{% endblock %}", content))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
        elif User.query.filter_by(email=email).first():
            flash('Email already registered')
        else:
            user = User(username=username, email=email, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please login.')
            return redirect('/login')
    
    content = """
    {% extends "base.html" %}
    {% block content %}
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-body">
                    <h2 class="card-title">Register</h2>
                    <form method="POST">
                        <div class="mb-3">
                            <label class="form-label">Username</label>
                            <input type="text" name="username" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Email</label>
                            <input type="email" name="email" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Password</label>
                            <input type="password" name="password" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Role</label>
                            <select name="role" class="form-control">
                                <option value="client">Client</option>
                                <option value="support">Support</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-primary">Register</button>
                    </form>
                    <p class="mt-3">Already have an account? <a href="/login">Login here</a></p>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}
    """
    return render_template_string(BASE_HTML.replace("{% block content %}{% endblock %}", content))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect('/')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'support':
        tickets = Ticket.query.all()
        content = """
        {% extends "base.html" %}
        {% block content %}
        <h2>Support Dashboard</h2>
        <p class="text-muted">Manage all customer tickets</p>
        {% if tickets %}
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead class="table-dark">
                        <tr><th>ID</th><th>Title</th><th>Client</th><th>Status</th><th>Priority</th><th>Created</th><th>Actions</th></tr>
                    </thead>
                    <tbody>
                        {% for ticket in tickets %}
                        <tr>
                            <td>#{{ ticket.id }}</td>
                            <td>{{ ticket.title }}</td>
                            <td>{{ ticket.user.username }}</td>
                            <td><span class="badge bg-secondary">{{ ticket.status }}</span></td>
                            <td><span class="badge bg-warning">{{ ticket.priority }}</span></td>
                            <td>{{ ticket.created_at.strftime('%Y-%m-%d') }}</td>
                            <td><a href="/ticket/{{ ticket.id }}" class="btn btn-sm btn-primary">View</a></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        {% else %}
            <p>No tickets found.</p>
        {% endif %}
        {% endblock %}
        """
    else:
        tickets = Ticket.query.filter_by(user_id=current_user.id).all()
        content = """
        {% extends "base.html" %}
        {% block content %}
        <h2>My Tickets</h2>
        <div class="d-flex justify-content-between mb-3">
            <span>{{ tickets|length }} ticket(s)</span>
            <a href="/submit" class="btn btn-success">+ New Ticket</a>
        </div>
        {% if tickets %}
            <div class="row">
                {% for ticket in tickets %}
                    <div class="col-md-6 mb-3">
                        <div class="card priority-{{ ticket.priority }}">
                            <div class="card-body">
                                <h5 class="card-title">{{ ticket.title }}</h5>
                                <p class="card-text">{{ ticket.description[:100] }}...</p>
                                <p class="text-muted"><small>
                                    Status: <span class="badge bg-secondary">{{ ticket.status }}</span> |
                                    Priority: <span class="badge bg-warning">{{ ticket.priority }}</span> |
                                    Created: {{ ticket.created_at.strftime('%Y-%m-%d') }}
                                </small></p>
                                <a href="/ticket/{{ ticket.id }}" class="btn btn-primary btn-sm">View Details</a>
                            </div>
                        </div>
                    </div>
                {% endfor %}
            </div>
        {% else %}
            <div class="text-center">
                <p>No tickets found.</p>
                <a href="/submit" class="btn btn-primary">Submit Your First Ticket</a>
            </div>
        {% endif %}
        {% endblock %}
        """
    
    return render_template_string(BASE_HTML.replace("{% block content %}{% endblock %}", content), tickets=tickets)

@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit_ticket():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        
        ticket = Ticket(title=title, description=description, priority=priority, user_id=current_user.id)
        db.session.add(ticket)
        db.session.commit()
        flash('Ticket submitted successfully!')
        return redirect('/dashboard')
    
    content = """
    {% extends "base.html" %}
    {% block content %}
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-body">
                    <h2 class="card-title">Submit New Ticket</h2>
                    <form method="POST">
                        <div class="mb-3">
                            <label class="form-label">Title</label>
                            <input type="text" name="title" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Description</label>
                            <textarea name="description" class="form-control" rows="5" required></textarea>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Priority</label>
                            <select name="priority" class="form-control">
                                <option value="low">Low</option>
                                <option value="medium" selected>Medium</option>
                                <option value="high">High</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-primary">Submit Ticket</button>
                        <a href="/dashboard" class="btn btn-secondary">Cancel</a>
                    </form>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}
    """
    return render_template_string(BASE_HTML.replace("{% block content %}{% endblock %}", content))

@app.route('/ticket/<int:ticket_id>')
@login_required
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if current_user.role != 'support' and ticket.user_id != current_user.id:
        flash('Access denied')
        return redirect('/dashboard')
    
    content = """
    {% extends "base.html" %}
    {% block content %}
    <div class="row">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header">
                    <h3>Ticket #{{ ticket.id }}: {{ ticket.title }}</h3>
                </div>
                <div class="card-body">
                    <p><strong>Description:</strong></p>
                    <p>{{ ticket.description }}</p>
                    <hr>
                    <div class="row">
                        <div class="col-md-6">
                            <p><strong>Status:</strong> <span class="badge bg-secondary">{{ ticket.status }}</span></p>
                            <p><strong>Priority:</strong> <span class="badge bg-warning">{{ ticket.priority }}</span></p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Created:</strong> {{ ticket.created_at.strftime('%Y-%m-%d %H:%M') }}</p>
                            <p><strong>Client:</strong> {{ ticket.user.username }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            {% if current_user.role == 'support' %}
            <div class="card">
                <div class="card-header"><h5>Update Ticket</h5></div>
                <div class="card-body">
                    <form method="POST" action="/update/{{ ticket.id }}">
                        <div class="mb-3">
                            <label class="form-label">Status</label>
                            <select name="status" class="form-control">
                                <option value="open" {% if ticket.status == 'open' %}selected{% endif %}>Open</option>
                                <option value="in_progress" {% if ticket.status == 'in_progress' %}selected{% endif %}>In Progress</option>
                                <option value="closed" {% if ticket.status == 'closed' %}selected{% endif %}>Closed</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-primary">Update</button>
                    </form>
                </div>
            </div>
            {% endif %}
            <div class="mt-3">
                <a href="/dashboard" class="btn btn-secondary">← Back to Dashboard</a>
            </div>
        </div>
    </div>
    {% endblock %}
    """
    return render_template_string(BASE_HTML.replace("{% block content %}{% endblock %}", content), ticket=ticket)

@app.route('/update/<int:ticket_id>', methods=['POST'])
@login_required
def update_ticket(ticket_id):
    if current_user.role != 'support':
        flash('Access denied')
        return redirect('/dashboard')
    
    ticket = Ticket.query.get_or_404(ticket_id)
    status = request.form['status']
    if status in ['open', 'in_progress', 'closed']:
        ticket.status = status
        db.session.commit()
        flash('Ticket updated successfully!')
    
    return redirect(f'/ticket/{ticket_id}')

print("✓ Routes defined")

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 SupportPortal is READY!")
    print("🌐 URL: http://localhost:3000")
    print("🛑 Press Ctrl+C to stop")
    print("="*50)
    
    try:
        app.run(host='127.0.0.1', port=3000, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\n👋 SupportPortal stopped")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
