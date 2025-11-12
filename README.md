# SLRDX Project Management System

A comprehensive Flask-based project management application with user authentication, task tracking, file uploads, and approval workflows.

## Features

- **User Management**: Role-based access control (Admin, Manager, User)
- **Project Management**: Create, edit, and track projects with progress monitoring
- **Task Management**: Assign tasks, track deadlines, and manage dependencies
- **File Uploads**: Secure document management with version control
- **Approval Workflows**: Multi-level approval system for tasks and projects
- **Dashboard Analytics**: Real-time statistics and reporting
- **Team Collaboration**: Comments, mentions, and notifications

## Production Deployment

This application is configured for production deployment on Railway with:

- ✅ Secure environment variable validation
- ✅ Production-ready logging
- ✅ PostgreSQL database support
- ✅ Gunicorn WSGI server
- ✅ Automatic debug mode disabling in production

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL database (provided by Railway)

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set environment variables:
   ```bash
   export SESSION_SECRET="your-secure-secret-here"
   export DATABASE_URL="postgresql://user:password@host:port/database"
   ```

4. Run the application:
   ```bash
   python main.py
   ```

## Deployment to Railway

1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard:
   - `SESSION_SECRET`: Generate with `python -c "import secrets; print(secrets.token_hex(32))"`
   - `CREATE_TABLES=true` (remove after first deployment)
3. Railway will automatically build and deploy using the provided configuration

## Project Structure

```
├── app.py                 # Main Flask application
├── main.py               # Application entry point
├── models.py             # Database models
├── models_extensions.py  # Extended models (outcomes, approvals)
├── routes.py             # All application routes
├── requirements.txt      # Python dependencies
├── Procfile             # Railway deployment configuration
├── railway.json         # Railway build configuration
├── runtime.txt          # Python version specification
├── static/              # Static assets (CSS, JS, images)
├── templates/           # Jinja2 templates
├── uploads/             # File upload directory
└── instance/            # SQLite database (development only)
```

## Security Features

- Password hashing with Werkzeug
- Session management with secure secrets
- CSRF protection
- Input validation and sanitization
- Role-based permissions system

## Database Schema

The application uses SQLAlchemy ORM with the following main entities:

- **Users**: Authentication and authorization
- **Projects**: Project management with progress tracking
- **Tasks**: Task assignment and tracking
- **Comments**: Discussion threads
- **Documents**: File management with versions
- **Milestones**: Project milestones
- **Approvals**: Workflow approvals

## API Endpoints

The application provides several API endpoints for dynamic data loading:

- `/api/dashboard/<task_type>` - Dashboard data
- `/api/project/<id>/tasks` - Project tasks
- `/api/tasks/all` - All accessible tasks
- `/api/team_members` - Team member data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue on GitHub.
