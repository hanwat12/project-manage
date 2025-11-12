import os
from app import app

if __name__ == '__main__':
    # Production settings: Use PORT from environment, default to 5000 for Railway
    port = int(os.environ.get('PORT', 5000))

    # Production: Never run in debug mode in production
    # Debug mode is only for local development
    debug = os.environ.get('FLASK_ENV') != 'production' and os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

    app.run(host='0.0.0.0', port=port, debug=debug)
