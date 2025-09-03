#!/usr/bin/env python3
"""
SupportPortal - Working Flask Application
Fixed version with proper imports and error handling
"""

import os
import sys
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

# Configuration
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-supportportal-2025'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{current_dir}/supportportal.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

def create_app():
    from flask import Flask, render_template, request, redirect, url_for, flash
    from flask_sqlalchemy import SQLAlchemy
    from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
    from flask_wtf import FlaskForm
    from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField
    from wtforms.validators import DataRequired, Email, Length, EqualTo
    from werkzeug.security import generate_password_hash, check_password_hash
    from datetime import datetime
    
    # Create Flask app
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db = SQLAlchemy(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page.'
    
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
        assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
        
        user = db.relationship('User', foreign_keys=[user_id], backref='tickets')
        assignee = db.relationship('User', foreign_keys=[assigned_to])
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Forms
    class LoginForm(FlaskForm):
        username = StringField('Username', validators=[DataRequired()])
        password = PasswordField('Password', validators=[DataRequired()])
        submit = SubmitField('Login')
    
    class RegistrationForm(FlaskForm):
        username = StringField('Username', validators=[DataRequired(), Length(min=2, max=64)])
        email = StringField('Email', validators=[DataRequired(), Email()])
        password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
        password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
        role = SelectField('Role', choices=[('client', 'Client'), ('support', 'Support')], default='client')
        submit = SubmitField('Register')
    
    class TicketForm(FlaskForm):
        title = StringField('Title', validators=[DataRequired(), Length(max=100)])
        description = TextAreaField('Description', validators=[DataRequired()])
        priority = SelectField('Priority', choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')
        submit = SubmitField('Submit Ticket')
    
    # Routes
    @app.route('/')
    def index():
        return render_template_string(INDEX_TEMPLATE)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
            flash('Invalid username or password')
        return render_template_string(LOGIN_TEMPLATE, form=form)
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = RegistrationForm()
        if form.validate_on_submit():
            if User.query.filter_by(username=form.username.data).first():
                flash('Username already exists')
                return render_template_string(REGISTER_TEMPLATE, form=form)
            if User.query.filter_by(email=form.email.data).first():
                flash('Email already registered')
                return render_template_string(REGISTER_TEMPLATE, form=form)
            
            user = User(username=form.username.data, email=form.email.data, role=form.role.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        return render_template_string(REGISTER_TEMPLATE, form=form)
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        if current_user.role == 'support':
            tickets = Ticket.query.all()
            return render_template_string(SUPPORT_DASHBOARD_TEMPLATE, tickets=tickets)
        else:
            tickets = Ticket.query.filter_by(user_id=current_user.id).all()
            return render_template_string(CLIENT_DASHBOARD_TEMPLATE, tickets=tickets)
    
    @app.route('/submit_ticket', methods=['GET', 'POST'])
    @login_required
    def submit_ticket():
        form = TicketForm()
        if form.validate_on_submit():
            ticket = Ticket(
                title=form.title.data,
                description=form.description.data,
                priority=form.priority.data,
                user_id=current_user.id
            )
            db.session.add(ticket)
            db.session.commit()
            flash('Ticket submitted successfully!')
            return redirect(url_for('dashboard'))
        return render_template_string(SUBMIT_TICKET_TEMPLATE, form=form)
    
    @app.route('/ticket/<int:ticket_id>')
    @login_required
    def view_ticket(ticket_id):
        ticket = Ticket.query.get_or_404(ticket_id)
        if current_user.role != 'support' and ticket.user_id != current_user.id:
            flash('Access denied')
            return redirect(url_for('dashboard'))
        return render_template_string(TICKET_DETAIL_TEMPLATE, ticket=ticket)
    
    @app.route('/update_ticket/<int:ticket_id>', methods=['POST'])
    @login_required
    def update_ticket(ticket_id):
        if current_user.role != 'support':
            flash('Access denied')
            return redirect(url_for('dashboard'))
        
        ticket = Ticket.query.get_or_404(ticket_id)
        status = request.form.get('status')
        if status in ['open', 'in_progress', 'closed']:
            ticket.status = status
            db.session.commit()
            flash('Ticket updated successfully!')
        return redirect(url_for('view_ticket', ticket_id=ticket_id))
    
    # Create tables
    with app.app_context():
        db.create_all()
        print("✓ Database tables created")
    
    return app

# Templates (embedded for simplicity)
BASE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>SupportPortal</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .navbar-brand { font-weight: bold; }
        .ticket-priority-high { border-left: 5px solid #dc3545; }
        .ticket-priority-medium { border-left: 5px solid #ffc107; }
        .ticket-priority-low { border-left: 5px solid #28a745; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('index') }}">🎫 SupportPortal</a>
            <div class="navbar-nav ms-auto">
                {% if current_user.is_authenticated %}
                    <a class="nav-link" href="{{ url_for('dashboard') }}">Dashboard</a>
                    <a class="nav-link" href="{{ url_for('submit_ticket') }}">New Ticket</a>
                    <a class="nav-link" href="{{ url_for('logout') }}">Logout ({{ current_user.username }})</a>
                {% else %}
                    <a class="nav-link" href="{{ url_for('login') }}">Login</a>
                    <a class="nav-link" href="{{ url_for('register') }}">Register</a>
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
'''

INDEX_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
<div class="row">
    <div class="col-md-8">
        <h1>Welcome to SupportPortal</h1>
        <p class="lead">Professional support ticket management system</p>
        {% if current_user.is_authenticated %}
            <p>Hello, <strong>{{ current_user.username }}</strong>! ({{ current_user.role }})</p>
            <a href="{{ url_for('dashboard') }}" class="btn btn-primary">Go to Dashboard</a>
            <a href="{{ url_for('submit_ticket') }}" class="btn btn-success">Submit New Ticket</a>
        {% else %}
            <p>Please login or register to access the support portal.</p>
            <a href="{{ url_for('login') }}" class="btn btn-primary">Login</a>
            <a href="{{ url_for('register') }}" class="btn btn-outline-primary">Register</a>
        {% endif %}
    </div>
    <div class="col-md-4">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Quick Help</h5>
                <ul class="list-unstyled">
                    <li>✅ Submit tickets for technical issues</li>
                    <li>📊 Track ticket status in real-time</li>
                    <li>👥 Support team assistance</li>
                    <li>🔒 Secure and private</li>
                </ul>
            </div>
        </div>
    </div>
</div>
''')

LOGIN_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-body">
                <h2 class="card-title">Login</h2>
                <form method="POST">
                    {{ form.hidden_tag() }}
                    <div class="mb-3">
                        {{ form.username.label(class="form-label") }}
                        {{ form.username(class="form-control") }}
                    </div>
                    <div class="mb-3">
                        {{ form.password.label(class="form-label") }}
                        {{ form.password(class="form-control") }}
                    </div>
                    {{ form.submit(class="btn btn-primary") }}
                </form>
                <p class="mt-3">Don't have an account? <a href="{{ url_for('register') }}">Register here</a></p>
            </div>
        </div>
    </div>
</div>
''')

REGISTER_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-body">
                <h2 class="card-title">Register</h2>
                <form method="POST">
                    {{ form.hidden_tag() }}
                    <div class="mb-3">
                        {{ form.username.label(class="form-label") }}
                        {{ form.username(class="form-control") }}
                    </div>
                    <div class="mb-3">
                        {{ form.email.label(class="form-label") }}
                        {{ form.email(class="form-control") }}
                    </div>
                    <div class="mb-3">
                        {{ form.password.label(class="form-label") }}
                        {{ form.password(class="form-control") }}
                    </div>
                    <div class="mb-3">
                        {{ form.password2.label(class="form-label") }}
                        {{ form.password2(class="form-control") }}
                    </div>
                    <div class="mb-3">
                        {{ form.role.label(class="form-label") }}
                        {{ form.role(class="form-control") }}
                    </div>
                    {{ form.submit(class="btn btn-primary") }}
                </form>
                <p class="mt-3">Already have an account? <a href="{{ url_for('login') }}">Login here</a></p>
            </div>
        </div>
    </div>
</div>
''')

SUBMIT_TICKET_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card">
            <div class="card-body">
                <h2 class="card-title">Submit New Ticket</h2>
                <form method="POST">
                    {{ form.hidden_tag() }}
                    <div class="mb-3">
                        {{ form.title.label(class="form-label") }}
                        {{ form.title(class="form-control") }}
                    </div>
                    <div class="mb-3">
                        {{ form.description.label(class="form-label") }}
                        {{ form.description(class="form-control", rows=5) }}
                    </div>
                    <div class="mb-3">
                        {{ form.priority.label(class="form-label") }}
                        {{ form.priority(class="form-control") }}
                    </div>
                    {{ form.submit(class="btn btn-primary") }}
                    <a href="{{ url_for('dashboard') }}" class="btn btn-secondary">Cancel</a>
                </form>
            </div>
        </div>
    </div>
</div>
''')

CLIENT_DASHBOARD_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
<h2>My Tickets</h2>
<div class="d-flex justify-content-between align-items-center mb-3">
    <span>{{ tickets|length }} ticket(s) found</span>
    <a href="{{ url_for('submit_ticket') }}" class="btn btn-success">+ New Ticket</a>
</div>
{% if tickets %}
    <div class="row">
        {% for ticket in tickets %}
            <div class="col-md-6 mb-3">
                <div class="card ticket-priority-{{ ticket.priority }}">
                    <div class="card-body">
                        <h5 class="card-title">{{ ticket.title }}</h5>
                        <p class="card-text">{{ ticket.description[:100] }}...</p>
                        <p class="text-muted">
                            <small>
                                Status: <span class="badge bg-secondary">{{ ticket.status }}</span> |
                                Priority: <span class="badge bg-warning">{{ ticket.priority }}</span> |
                                Created: {{ ticket.created_at.strftime('%Y-%m-%d') }}
                            </small>
                        </p>
                        <a href="{{ url_for('view_ticket', ticket_id=ticket.id) }}" class="btn btn-primary btn-sm">View Details</a>
                    </div>
                </div>
            </div>
        {% endfor %}
    </div>
{% else %}
    <div class="text-center">
        <p>No tickets found.</p>
        <a href="{{ url_for('submit_ticket') }}" class="btn btn-primary">Submit Your First Ticket</a>
    </div>
{% endif %}
''')

SUPPORT_DASHBOARD_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
<h2>Support Dashboard</h2>
<p class="text-muted">Manage all customer tickets</p>
{% if tickets %}
    <div class="table-responsive">
        <table class="table table-hover">
            <thead class="table-dark">
                <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Client</th>
                    <th>Status</th>
                    <th>Priority</th>
                    <th>Created</th>
                    <th>Actions</th>
                </tr>
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
                    <td>
                        <a href="{{ url_for('view_ticket', ticket_id=ticket.id) }}" class="btn btn-sm btn-primary">View</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
{% else %}
    <p>No tickets in the system.</p>
{% endif %}
''')

TICKET_DETAIL_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
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
            <div class="card-header">
                <h5>Update Ticket</h5>
            </div>
            <div class="card-body">
                <form method="POST" action="{{ url_for('update_ticket', ticket_id=ticket.id) }}">
                    <div class="mb-3">
                        <label for="status" class="form-label">Status</label>
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
            <a href="{{ url_for('dashboard') }}" class="btn btn-secondary">← Back to Dashboard</a>
        </div>
    </div>
</div>
''')

if __name__ == '__main__':
    print("🚀 Starting SupportPortal...")
    app = create_app()
    
    print("✅ SupportPortal is ready!")
    print("🌐 Open your browser to: http://localhost:3000")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    app.run(host='127.0.0.1', port=3000, debug=True, use_reloader=False)
