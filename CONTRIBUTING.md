# Contributing to SupportPortal

We love your input! We want to make contributing to SupportPortal as easy and transparent as possible.

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License

When you submit code changes, your submissions are understood to be under the same [MIT License](LICENSE) that covers the project.

## Report bugs using GitHub's [issue tracker](https://github.com/writersrinivasan/SupportPortal/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/writersrinivasan/SupportPortal/issues/new).

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Development Setup

1. **Fork and Clone**
```bash
git clone https://github.com/YOUR_USERNAME/SupportPortal.git
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
pip install pytest pytest-cov flake8  # For testing and linting
```

4. **Run Tests**
```bash
python -m pytest tests/  # When tests are implemented
```

5. **Run the Application**
```bash
python final_app.py
```

## Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) Python style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions small and focused
- Use type hints where appropriate

## Commit Message Guidelines

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

### Example:
```
Add user profile management feature

- Implement user profile editing
- Add profile picture upload functionality
- Update user settings page
- Add validation for profile data

Fixes #123
```

## Feature Development

### Adding New Features

1. Create a new branch: `git checkout -b feature/amazing-feature`
2. Implement your feature
3. Add tests for your feature
4. Update documentation
5. Submit a pull request

### Feature Categories

- **Authentication**: User login, registration, password reset
- **Ticket Management**: Creating, updating, assigning tickets
- **UI/UX**: Interface improvements, responsive design
- **Admin Features**: User management, system configuration
- **Integrations**: Email notifications, external APIs
- **Performance**: Optimization, caching, database improvements

## Testing Guidelines

### Writing Tests

```python
def test_user_creation():
    """Test that a user can be created successfully."""
    user = User(username='testuser', email='test@example.com', role='client')
    user.set_password('testpassword')
    
    assert user.username == 'testuser'
    assert user.check_password('testpassword')
    assert user.role == 'client'
```

### Test Categories

- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete user workflows
- **Security Tests**: Test authentication and authorization

## Documentation

### Code Documentation

- Add docstrings to all public functions and classes
- Use clear, concise comments for complex logic
- Update README.md for significant changes
- Update ARCHITECTURE.md for structural changes

### Example Docstring:
```python
def create_ticket(title, description, priority='medium', user_id=None):
    """Create a new support ticket.
    
    Args:
        title (str): Brief description of the issue
        description (str): Detailed description of the problem
        priority (str): Priority level ('low', 'medium', 'high')
        user_id (int): ID of the user creating the ticket
    
    Returns:
        Ticket: The created ticket object
    
    Raises:
        ValueError: If required fields are missing
    """
```

## Security Guidelines

- Never commit secrets, passwords, or API keys
- Validate all user input
- Use parameterized queries for database operations
- Implement proper authentication and authorization
- Follow OWASP security guidelines

## Performance Guidelines

- Profile code before optimizing
- Use database indexes for frequently queried fields
- Implement caching for expensive operations
- Optimize database queries (avoid N+1 problems)
- Monitor application performance

## Release Process

1. **Version Numbering**: We use [Semantic Versioning](https://semver.org/)
   - MAJOR.MINOR.PATCH (e.g., 1.2.3)
   - MAJOR: Breaking changes
   - MINOR: New features, backwards compatible
   - PATCH: Bug fixes, backwards compatible

2. **Release Checklist**:
   - [ ] All tests pass
   - [ ] Documentation updated
   - [ ] CHANGELOG.md updated
   - [ ] Version number bumped
   - [ ] Git tag created

## Getting Help

- 📧 Email: [support@supportportal.com](mailto:support@supportportal.com)
- 💬 Discussions: [GitHub Discussions](https://github.com/writersrinivasan/SupportPortal/discussions)
- 🐛 Issues: [GitHub Issues](https://github.com/writersrinivasan/SupportPortal/issues)

## Recognition

Contributors will be recognized in:
- README.md contributors section
- CHANGELOG.md for significant contributions
- GitHub contributors page

Thank you for contributing to SupportPortal! 🎉
