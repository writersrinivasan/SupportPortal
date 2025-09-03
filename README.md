# 🎫 SupportPortal

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)](https://github.com/writersrinivasan/SupportPortal)

A **professional support ticketing system** built with Flask, inspired by ServiceNow. Streamline your customer support operations with role-based access control, real-time status tracking, and a modern responsive interface.

![SupportPortal Demo](https://via.placeholder.com/800x400/667eea/ffffff?text=SupportPortal+Demo)

## 🌟 Features

### 🎯 **Complete Ticket Management**
- ✅ Submit detailed support tickets with priority levels
- 📊 Real-time status tracking (Open → In Progress → Closed)
- 🎨 Color-coded priority system (Low/Medium/High)
- 📱 Responsive design for all devices

### 🔐 **User Management**
- 👥 Role-based access control (Client/Support)
- 🔒 Secure authentication with password hashing
- 💫 Intuitive registration and login process
- 🎛️ Personalized dashboards by role

### 🚀 **Modern Interface**
- 💎 Bootstrap 5 professional design
- 📱 Mobile-responsive layout
- 🎨 Beautiful gradient themes
- ⚡ Fast, intuitive navigation

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/writersrinivasan/SupportPortal.git
cd SupportPortal
```

2. **Set up virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python final_app.py
```

5. **Access your application**
Open your browser to: **http://localhost:3000**

## 📖 Usage Guide

### For Clients
1. **Register** with "Client" role
2. **Submit tickets** with detailed descriptions
3. **Track progress** in your dashboard
4. **Monitor updates** from support team

### For Support Staff
1. **Register** with "Support" role
2. **View all tickets** in support dashboard
3. **Update ticket status** as work progresses
4. **Manage workload** efficiently

## 🏗️ Architecture

SupportPortal follows a modern MVC architecture pattern:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │    Database     │
│                 │    │                 │    │                 │
│ • Bootstrap 5   │◄──►│ • Flask 2.3.3   │◄──►│ • SQLite        │
│ • Jinja2        │    │ • SQLAlchemy    │    │ • Auto-generated│
│ • JavaScript    │    │ • Flask-Login   │    │ • ACID compliant│
│ • Responsive    │    │ • Security      │    │ • Relationships │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔧 Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| **Backend** | Flask | 2.3.3 |
| **Database** | SQLAlchemy + SQLite | 3.0.5 |
| **Authentication** | Flask-Login | 0.6.3 |
| **Forms** | Flask-WTF | 1.1.1 |
| **Frontend** | Bootstrap | 5.1.3 |
| **Security** | Werkzeug | Latest |

## 📊 Database Schema

```sql
Users                          Tickets
┌─────────────────┐           ┌─────────────────┐
│ id (Primary)    │           │ id (Primary)    │
│ username        │           │ title           │
│ email           │←─────────→│ user_id (FK)    │
│ password_hash   │   1:N     │ description     │
│ role            │           │ status          │
│ created_at      │           │ priority        │
└─────────────────┘           │ created_at      │
                              └─────────────────┘
```

## 🛡️ Security Features

- 🔐 **Password Hashing**: PBKDF2 with salt
- 🛡️ **CSRF Protection**: Flask-WTF tokens
- 🔒 **SQL Injection Prevention**: SQLAlchemy ORM
- 👤 **Session Management**: Flask-Login
- 🎭 **Role-based Access Control**: Client/Support separation

## 📚 Documentation

- **[Complete Documentation](DOCUMENTATION.md)** - Comprehensive guide
- **[Architecture Guide](ARCHITECTURE.md)** - Technical architecture details
- **[API Documentation](docs/API.md)** - API endpoints and usage
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment

## 🚀 Deployment

### Local Development
```bash
python final_app.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 final_app:app
```

### Docker Deployment
```bash
docker build -t supportportal .
docker run -p 3000:3000 supportportal
```

## 🧪 Testing

Create test accounts to explore the system:

**Client Account:**
- Username: `testclient`
- Password: `password123`
- Role: Client

**Support Account:**
- Username: `testsupport`
- Password: `password123`
- Role: Support

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Roadmap

- [ ] 📧 Email notifications for ticket updates
- [ ] 📎 File attachment support
- [ ] 🔍 Advanced search and filtering
- [ ] 📊 Analytics and reporting dashboard
- [ ] 🌐 RESTful API for integrations
- [ ] 🌍 Multi-language support
- [ ] 📱 Mobile application
- [ ] 🔔 Real-time notifications

## 🆘 Support

- 📧 **Email**: [support@supportportal.com](mailto:support@supportportal.com)
- 🐛 **Issues**: [GitHub Issues](https://github.com/writersrinivasan/SupportPortal/issues)
- 📖 **Wiki**: [Documentation Wiki](https://github.com/writersrinivasan/SupportPortal/wiki)

## ⭐ Show Your Support

If you find this project helpful, please consider giving it a star on GitHub!

---

<div align="center">

**[🏠 Home](https://github.com/writersrinivasan/SupportPortal)** • 
**[📚 Docs](DOCUMENTATION.md)** • 
**[🏗️ Architecture](ARCHITECTURE.md)** • 
**[🚀 Deploy](docs/DEPLOYMENT.md)**

Made with ❤️ by [Srinivasan](https://github.com/writersrinivasan)

</div>
