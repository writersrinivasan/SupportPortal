# 🎫 SupportPortal - Complete Documentation

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Features](#features)
4. [Installation & Setup](#installation--setup)
5. [Usage Guide](#usage-guide)
6. [API Documentation](#api-documentation)
7. [Database Schema](#database-schema)
8. [Security](#security)
9. [Deployment](#deployment)
10. [Contributing](#contributing)

---

## Overview

**SupportPortal** is a professional support ticket management system built with Flask, inspired by ServiceNow. It provides a complete solution for organizations to manage customer support requests efficiently with role-based access control and real-time status tracking.

### Key Highlights
- 🎯 **ServiceNow-inspired** design and functionality
- 🔐 **Role-based access control** (Client/Support)
- 📱 **Responsive design** with Bootstrap 5
- 🚀 **Real-time updates** and notifications
- 💾 **SQLite database** with SQLAlchemy ORM
- 🔒 **Secure authentication** with password hashing

---

## Architecture

### System Architecture Diagram

```mermaid
graph TB
    A[Web Browser] --> B[Flask Application]
    B --> C[Authentication Layer]
    C --> D[Role-Based Access Control]
    D --> E[Route Handlers]
    E --> F[Business Logic]
    F --> G[SQLAlchemy ORM]
    G --> H[SQLite Database]
    
    subgraph "Frontend Layer"
        I[Bootstrap 5 CSS]
        J[Jinja2 Templates]
        K[JavaScript]
    end
    
    subgraph "Backend Layer"
        L[Flask-Login]
        M[Flask-WTF]
        N[Werkzeug Security]
    end
    
    B --> I
    B --> J
    B --> K
    C --> L
    E --> M
    C --> N
```

### Application Structure

```
SupportPortal/
├── final_app.py              # Main application file
├── requirements.txt          # Python dependencies
├── supportportal.db          # SQLite database (auto-generated)
├── README.md                 # Project documentation
├── docs/                     # Documentation files
│   ├── ARCHITECTURE.md       # Detailed architecture
│   ├── API.md               # API documentation
│   └── DEPLOYMENT.md        # Deployment guide
├── .gitignore               # Git ignore file
└── static/                  # Static assets (if needed)
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend Framework** | Flask 2.3.3 | Web application framework |
| **Database ORM** | SQLAlchemy 3.0.5 | Database abstraction layer |
| **Authentication** | Flask-Login 0.6.3 | User session management |
| **Forms** | Flask-WTF 1.1.1 | Form handling and validation |
| **Database** | SQLite | Lightweight database |
| **Frontend** | Bootstrap 5 | Responsive UI framework |
| **Templating** | Jinja2 | Server-side templating |
| **Security** | Werkzeug | Password hashing |

---

## Features

### 🔐 Authentication & Authorization
- User registration with role selection
- Secure login/logout functionality
- Password hashing with Werkzeug
- Session management with Flask-Login
- Role-based access control (Client/Support)

### 🎫 Ticket Management
- **Create Tickets**: Submit detailed support requests
- **Priority Levels**: Low, Medium, High priority classification
- **Status Tracking**: Open → In Progress → Closed workflow
- **Real-time Updates**: Instant status change notifications
- **Rich Descriptions**: Detailed problem descriptions

### 👥 User Roles

#### Client Users
- Submit new support tickets
- View personal ticket history
- Track ticket status and progress
- Update ticket descriptions

#### Support Staff
- View all tickets across the system
- Update ticket status and assignments
- Manage ticket priorities
- Support dashboard with analytics

### 🎨 User Interface
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Bootstrap 5 with custom styling
- **Color-coded Priority**: Visual priority indicators
- **Status Badges**: Clear status visualization
- **Intuitive Navigation**: Easy-to-use interface

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Quick Setup

1. **Clone the Repository**
```bash
git clone https://github.com/writersrinivasan/SupportPortal.git
cd SupportPortal
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the Application**
```bash
python final_app.py
```

5. **Access the Application**
Open your browser to: `http://localhost:3000`

### Environment Variables (Optional)
```bash
export SECRET_KEY="your-secret-key-here"
export DATABASE_URL="sqlite:///supportportal.db"
```

---

## Usage Guide

### For End Users (Clients)

1. **Registration**
   - Visit `http://localhost:3000`
   - Click "Register"
   - Fill in username, email, password
   - Select "Client" role
   - Submit registration

2. **Submitting Tickets**
   - Login to your account
   - Click "New Ticket" or "Submit Ticket"
   - Enter ticket title and detailed description
   - Select priority level (Low/Medium/High)
   - Submit the ticket

3. **Tracking Tickets**
   - Access your dashboard to view all tickets
   - Click on any ticket to view details
   - Monitor status changes from support team

### For Support Staff

1. **Registration & Setup**
   - Register with "Support" role
   - Access support dashboard after login

2. **Managing Tickets**
   - View all tickets in the system
   - Click on tickets to view full details
   - Update ticket status as work progresses
   - Communicate with clients through status updates

3. **Dashboard Features**
   - View tickets by status and priority
   - Quick actions for common operations
   - Real-time ticket statistics

---

## API Documentation

### Authentication Endpoints

#### POST `/register`
Register a new user account.

**Request Body:**
```json
{
    "username": "string",
    "email": "string",
    "password": "string",
    "role": "client" | "support"
}
```

**Response:**
- `302 Redirect` to login page on success
- `400 Bad Request` if validation fails

#### POST `/login`
Authenticate user and create session.

**Request Body:**
```json
{
    "username": "string",
    "password": "string"
}
```

**Response:**
- `302 Redirect` to dashboard on success
- `401 Unauthorized` for invalid credentials

#### GET `/logout`
End user session and logout.

**Response:**
- `302 Redirect` to home page

### Ticket Management Endpoints

#### GET `/dashboard`
Access role-based dashboard.

**Authentication:** Required
**Response:** Dashboard HTML with user's tickets (client) or all tickets (support)

#### POST `/submit`
Create a new support ticket.

**Authentication:** Required (Client role)
**Request Body:**
```json
{
    "title": "string",
    "description": "string",
    "priority": "low" | "medium" | "high"
}
```

#### GET `/ticket/<int:ticket_id>`
View specific ticket details.

**Authentication:** Required
**Access Control:** Ticket owner or support staff only

#### POST `/update/<int:ticket_id>`
Update ticket status.

**Authentication:** Required (Support role only)
**Request Body:**
```json
{
    "status": "open" | "in_progress" | "closed"
}
```

---

## Database Schema

### User Table
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(64) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'client'
);
```

### Ticket Table
```sql
CREATE TABLE ticket (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'open',
    priority VARCHAR(20) NOT NULL DEFAULT 'medium',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```

### Relationships
- **One-to-Many**: User → Tickets (One user can have multiple tickets)
- **Foreign Key**: ticket.user_id → user.id

### Data Model Diagram
```mermaid
erDiagram
    User ||--o{ Ticket : creates
    User {
        int id PK
        string username UK
        string email UK
        string password_hash
        string role
    }
    Ticket {
        int id PK
        string title
        text description
        string status
        string priority
        datetime created_at
        int user_id FK
    }
```

---

## Security

### Authentication Security
- **Password Hashing**: Uses Werkzeug's PBKDF2 with salt
- **Session Management**: Flask-Login handles secure sessions
- **CSRF Protection**: Flask-WTF provides CSRF tokens
- **SQL Injection Prevention**: SQLAlchemy ORM parameterized queries

### Access Control
- **Role-based Authorization**: Client/Support role separation
- **Route Protection**: Login required decorators
- **Data Isolation**: Users can only access their own tickets
- **Admin Privileges**: Support staff can view/modify all tickets

### Best Practices Implemented
- Secure session cookies
- Password complexity requirements
- Input validation and sanitization
- SQL injection prevention
- XSS protection through template escaping

---

## Deployment

### Production Deployment

#### Using Gunicorn (Recommended)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 final_app:app
```

#### Using Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 3000
CMD ["python", "final_app.py"]
```

#### Environment Configuration
```bash
# Production environment variables
export FLASK_ENV=production
export SECRET_KEY="your-production-secret-key"
export DATABASE_URL="postgresql://user:pass@host:port/db"
```

### Cloud Deployment Options
- **Heroku**: Easy deployment with git push
- **AWS EC2**: Full control over server environment
- **Google Cloud Run**: Serverless container deployment
- **DigitalOcean App Platform**: Simple PaaS deployment

---

## Performance Considerations

### Database Optimization
- Implement database indexing for frequently queried fields
- Use connection pooling for multiple concurrent users
- Consider PostgreSQL for production use

### Caching
- Implement Redis for session storage
- Cache frequently accessed ticket data
- Use CDN for static assets

### Scaling
- Horizontal scaling with load balancers
- Database read replicas for heavy read workloads
- Microservices architecture for large deployments

---

## Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Submit a pull request

### Code Standards
- Follow PEP 8 Python style guide
- Add docstrings to all functions
- Include unit tests for new features
- Update documentation for changes

### Testing
```bash
# Run tests (when implemented)
python -m pytest tests/
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Support

For support and questions:
- Create an issue on GitHub
- Email: support@supportportal.com
- Documentation: [GitHub Wiki](https://github.com/writersrinivasan/SupportPortal/wiki)

---

## Changelog

### Version 1.0.0 (Current)
- Initial release
- User authentication and authorization
- Ticket creation and management
- Role-based dashboards
- Responsive UI design
- SQLite database support

### Roadmap
- [ ] Email notifications
- [ ] File attachments
- [ ] Advanced search and filtering
- [ ] Reporting and analytics
- [ ] API endpoints for integrations
- [ ] Multi-language support
