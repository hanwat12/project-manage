import os
import logging
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging - INFO level for production, DEBUG for development
log_level = logging.INFO if os.environ.get("FLASK_ENV") == "production" else logging.DEBUG
logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

# Validate required environment variables
def validate_environment():
    """Validate that all required environment variables are set"""
    required_vars = ['SESSION_SECRET', 'DATABASE_URL']

    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)

    if missing_vars:
        logging.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logging.error("Please set all required environment variables before running the application.")
        sys.exit(1)

    logging.info("All required environment variables are set.")

# Validate environment on startup
validate_environment()

# create the app
app = Flask(__name__)

# Require SESSION_SECRET - no fallback for security
session_secret = os.environ.get("f933657c9443fd20332290886265a2a8a5ff900b3341ad61f583fbdfed5627a3")
if not session_secret:
    logging.error("SESSION_SECRET environment variable is required")
    sys.exit(1)
app.secret_key = session_secret

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# configure the database - DATABASE_URL is required
database_url = os.environ.get("postgresql://postgres:ecCQiozFWTZmEEayFNgWHqWGMPYtooZV@postgres.railway.internal:5432/railway")
if not database_url:
    logging.error("DATABASE_URL environment variable is required")
    sys.exit(1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Production settings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logging.info("Database configured successfully.")

# initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# Import and register routes
import routes

# Only create tables if explicitly requested (for initial setup)
if os.environ.get("CREATE_TABLES") == "true":
    with app.app_context():
        import models as models_module
        import models_extensions as models_extensions_module
        db.create_all()
        logging.info("Database tables created/updated.")
        logging.warning("Remember to remove CREATE_TABLES=true from environment variables after initial setup.")
