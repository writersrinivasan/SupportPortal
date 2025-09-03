#!/usr/bin/env python3
"""
SupportPortal - FINAL WORKING VERSION
Simplified Flask app without template inheritance issues
"""

import os
import sys
from datetime import datetime

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from flask import Flask, render_template_string, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supportportal-secret-key-2025'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(current_dir, "supportportal.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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

# Create database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>SupportPortal</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { padding-top: 50px; }
        .card { box-shadow: 0 10px 30px rgba(0,0,0,0.3); border: none; }
        .btn-custom { background: #667eea; border: none; }
        .btn-custom:hover { background: #764ba2; }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-body text-center p-5">
                        <h1 class="display-4 mb-4">🎫 SupportPortal</h1>
                        <p class="lead mb-4">Professional Support Ticket Management System</p>
                        
                        {% with messages = get_flashed_messages() %}
                            {% if messages %}
                                {% for message in messages %}
                                    <div class="alert alert-info">{{ message }}</div>
                                {% endfor %}
                            {% endif %}
                        {% endwith %}
                        
                        {% if current_user.is_authenticated %}
                            <div class="alert alert-success">
                                <h5>Welcome back, {{ current_user.username }}!</h5>
                                <p>Role: <strong>{{ current_user.role.title() }}</strong></p>
                            </div>
                            <a href="/dashboard" class="btn btn-primary btn-lg me-3">Dashboard</a>
                            <a href="/submit" class="btn btn-success btn-lg me-3">New Ticket</a>
                            <a href="/logout" class="btn btn-outline-secondary">Logout</a>
                        {% else %}
                            <div class="mb-4">
                                <p>Get started by logging in or creating a new account</p>
                                <a href="/login" class="btn btn-primary btn-lg me-3">Login</a>
                                <a href="/register" class="btn btn-outline-primary btn-lg">Register</a>
                            </div>
                            <div class="row mt-5">
                                <div class="col-md-6">
                                    <h5>For Clients</h5>
                                    <ul class="list-unstyled">
                                        <li>✅ Submit support requests</li>
                                        <li>📊 Track ticket progress</li>
                                        <li>💬 Communicate with support</li>
                                    </ul>
                                </div>
                                <div class="col-md-6">
                                    <h5>For Support Team</h5>
                                    <ul class="list-unstyled">
                                        <li>👥 Manage all tickets</li>
                                        <li>🔄 Update ticket status</li>
                                        <li>📈 Track performance</li>
                                    </ul>
                                </div>
                            </div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
    """)

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
    
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Login - SupportPortal</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding-top: 50px; }</style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h2 class="card-title text-center">Login to SupportPortal</h2>
                        {% with messages = get_flashed_messages() %}
                            {% if messages %}
                                {% for message in messages %}
                                    <div class="alert alert-warning">{{ message }}</div>
                                {% endfor %}
                            {% endif %}
                        {% endwith %}
                        <form method="POST">
                            <div class="mb-3">
                                <label class="form-label">Username</label>
                                <input type="text" name="username" class="form-control" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Password</label>
                                <input type="password" name="password" class="form-control" required>
                            </div>
                            <button type="submit" class="btn btn-primary w-100">Login</button>
                        </form>
                        <div class="text-center mt-3">
                            <p>Don't have an account? <a href="/register">Register here</a></p>
                            <a href="/" class="btn btn-link">← Back to Home</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
    """)

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
    
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Register - SupportPortal</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding-top: 30px; }</style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h2 class="card-title text-center">Create Account</h2>
                        {% with messages = get_flashed_messages() %}
                            {% if messages %}
                                {% for message in messages %}
                                    <div class="alert alert-warning">{{ message }}</div>
                                {% endfor %}
                            {% endif %}
                        {% endwith %}
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
                                    <option value="client">Client (Submit tickets)</option>
                                    <option value="support">Support (Manage tickets)</option>
                                </select>
                            </div>
                            <button type="submit" class="btn btn-primary w-100">Register</button>
                        </form>
                        <div class="text-center mt-3">
                            <p>Already have an account? <a href="/login">Login here</a></p>
                            <a href="/" class="btn btn-link">← Back to Home</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
    """)

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
        tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
        title = "Support Dashboard - All Tickets"
        template = """
        <div class="table-responsive">
            <table class="table table-hover">
                <thead class="table-dark">
                    <tr><th>ID</th><th>Title</th><th>Client</th><th>Status</th><th>Priority</th><th>Created</th><th>Actions</th></tr>
                </thead>
                <tbody>
                    {% for ticket in tickets %}
                    <tr>
                        <td><strong>#{{ ticket.id }}</strong></td>
                        <td>{{ ticket.title }}</td>
                        <td>{{ ticket.user.username }}</td>
                        <td><span class="badge bg-{% if ticket.status=='open' %}danger{% elif ticket.status=='in_progress' %}warning{% else %}success{% endif %}">{{ ticket.status }}</span></td>
                        <td><span class="badge bg-{% if ticket.priority=='high' %}danger{% elif ticket.priority=='medium' %}warning{% else %}secondary{% endif %}">{{ ticket.priority }}</span></td>
                        <td>{{ ticket.created_at.strftime('%Y-%m-%d %H:%M') }}</td>
                        <td><a href="/ticket/{{ ticket.id }}" class="btn btn-sm btn-primary">View</a></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        """
    else:
        tickets = Ticket.query.filter_by(user_id=current_user.id).order_by(Ticket.created_at.desc()).all()
        title = "My Tickets"
        template = """
        <div class="d-flex justify-content-between mb-3">
            <span><strong>{{ tickets|length }}</strong> ticket(s) found</span>
            <a href="/submit" class="btn btn-success">+ New Ticket</a>
        </div>
        {% if tickets %}
            <div class="row">
                {% for ticket in tickets %}
                    <div class="col-md-6 mb-3">
                        <div class="card border-{% if ticket.priority=='high' %}danger{% elif ticket.priority=='medium' %}warning{% else %}secondary{% endif %}">
                            <div class="card-body">
                                <h5 class="card-title">{{ ticket.title }}</h5>
                                <p class="card-text">{{ ticket.description[:150] }}{% if ticket.description|length > 150 %}...{% endif %}</p>
                                <p class="text-muted"><small>
                                    <span class="badge bg-{% if ticket.status=='open' %}danger{% elif ticket.status=='in_progress' %}warning{% else %}success{% endif %}">{{ ticket.status }}</span>
                                    <span class="badge bg-{% if ticket.priority=='high' %}danger{% elif ticket.priority=='medium' %}warning{% else %}secondary{% endif %}">{{ ticket.priority }}</span>
                                    {{ ticket.created_at.strftime('%Y-%m-%d %H:%M') }}
                                </small></p>
                                <a href="/ticket/{{ ticket.id }}" class="btn btn-primary btn-sm">View Details</a>
                            </div>
                        </div>
                    </div>
                {% endfor %}
            </div>
        {% else %}
            <div class="text-center">
                <div class="alert alert-info">
                    <h5>No tickets found</h5>
                    <p>You haven't submitted any tickets yet.</p>
                    <a href="/submit" class="btn btn-primary">Submit Your First Ticket</a>
                </div>
            </div>
        {% endif %}
        """
    
    return render_template_string(f"""
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard - SupportPortal</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">🎫 SupportPortal</a>
            <div class="navbar-nav ms-auto d-flex flex-row">
                <a class="nav-link me-3" href="/dashboard">Dashboard</a>
                <a class="nav-link me-3" href="/submit">New Ticket</a>
                <a class="nav-link" href="/logout">Logout ({{{{ current_user.username }}}})</a>
            </div>
        </div>
    </nav>
    <div class="container mt-4">
        <h2>{title}</h2>
        {{% with messages = get_flashed_messages() %}}
            {{% if messages %}}
                {{% for message in messages %}}
                    <div class="alert alert-info alert-dismissible fade show">
                        {{{{ message }}}}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {{% endfor %}}
            {{% endif %}}
        {{% endwith %}}
        {template}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
    """, tickets=tickets)

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
        flash(f'Ticket "{title}" submitted successfully!')
        return redirect('/dashboard')
    
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Submit Ticket - SupportPortal</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">🎫 SupportPortal</a>
            <div class="navbar-nav ms-auto d-flex flex-row">
                <a class="nav-link me-3" href="/dashboard">Dashboard</a>
                <a class="nav-link me-3" href="/submit">New Ticket</a>
                <a class="nav-link" href="/logout">Logout</a>
            </div>
        </div>
    </nav>
    <div class="container mt-4">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-body">
                        <h2 class="card-title">Submit New Support Ticket</h2>
                        <form method="POST">
                            <div class="mb-3">
                                <label class="form-label">Title <span class="text-danger">*</span></label>
                                <input type="text" name="title" class="form-control" placeholder="Brief description of the issue" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Description <span class="text-danger">*</span></label>
                                <textarea name="description" class="form-control" rows="6" placeholder="Detailed description of the issue, steps to reproduce, etc." required></textarea>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Priority</label>
                                <select name="priority" class="form-control">
                                    <option value="low">Low - General inquiry</option>
                                    <option value="medium" selected>Medium - Standard issue</option>
                                    <option value="high">High - Urgent issue</option>
                                </select>
                            </div>
                            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                                <a href="/dashboard" class="btn btn-secondary me-md-2">Cancel</a>
                                <button type="submit" class="btn btn-primary">Submit Ticket</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
    """)

@app.route('/ticket/<int:ticket_id>')
@login_required
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if current_user.role != 'support' and ticket.user_id != current_user.id:
        flash('Access denied - You can only view your own tickets')
        return redirect('/dashboard')
    
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Ticket #{{ ticket.id }} - SupportPortal</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">🎫 SupportPortal</a>
            <div class="navbar-nav ms-auto d-flex flex-row">
                <a class="nav-link me-3" href="/dashboard">Dashboard</a>
                <a class="nav-link me-3" href="/submit">New Ticket</a>
                <a class="nav-link" href="/logout">Logout</a>
            </div>
        </div>
    </nav>
    <div class="container mt-4">
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <div class="alert alert-success alert-dismissible fade show">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <div class="row">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">
                        <h3>Ticket #{{ ticket.id }}</h3>
                        <h4>{{ ticket.title }}</h4>
                    </div>
                    <div class="card-body">
                        <div class="mb-3">
                            <strong>Description:</strong>
                            <p class="mt-2">{{ ticket.description }}</p>
                        </div>
                        <hr>
                        <div class="row">
                            <div class="col-md-6">
                                <p><strong>Status:</strong> 
                                    <span class="badge bg-{% if ticket.status=='open' %}danger{% elif ticket.status=='in_progress' %}warning{% else %}success{% endif %} fs-6">
                                        {{ ticket.status.replace('_', ' ').title() }}
                                    </span>
                                </p>
                                <p><strong>Priority:</strong> 
                                    <span class="badge bg-{% if ticket.priority=='high' %}danger{% elif ticket.priority=='medium' %}warning{% else %}secondary{% endif %} fs-6">
                                        {{ ticket.priority.title() }}
                                    </span>
                                </p>
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
                    <div class="card-header">
                        <h5>Update Ticket</h5>
                    </div>
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
                            <button type="submit" class="btn btn-primary w-100">Update Status</button>
                        </form>
                    </div>
                </div>
                {% endif %}
                <div class="mt-3">
                    <a href="/dashboard" class="btn btn-secondary w-100">← Back to Dashboard</a>
                </div>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
    """, ticket=ticket)

@app.route('/update/<int:ticket_id>', methods=['POST'])
@login_required
def update_ticket(ticket_id):
    if current_user.role != 'support':
        flash('Access denied - Only support staff can update tickets')
        return redirect('/dashboard')
    
    ticket = Ticket.query.get_or_404(ticket_id)
    old_status = ticket.status
    new_status = request.form['status']
    
    if new_status in ['open', 'in_progress', 'closed']:
        ticket.status = new_status
        db.session.commit()
        flash(f'Ticket #{ticket_id} status updated from "{old_status}" to "{new_status}"')
    
    return redirect(f'/ticket/{ticket_id}')

if __name__ == '__main__':
    print("🚀 SupportPortal Starting...")
    print("📍 URL: http://localhost:3000")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 40)
    
    try:
        app.run(host='127.0.0.1', port=3000, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\n👋 SupportPortal stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
