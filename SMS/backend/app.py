import os
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import db
from models.sms import SMS
from models.user import User
from models.otp import OTP
from routes.sms import sms_routes
from routes.users import user_routes
from routes.otp import otp_routes


def create_app():
    app = Flask(__name__,
                static_folder='../../frontend',
                template_folder='../../frontend')

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///sms.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Enable CORS
    CORS(app)

    # Initialize database
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(sms_routes)
    app.register_blueprint(user_routes)
    app.register_blueprint(otp_routes)

    # Serve frontend
    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'dashboard.html')

    @app.route('/clock')
    def clock():
        return send_from_directory(os.path.join(app.static_folder, '..'), 'digital_clock.html')

    @app.route('/statistics')
    def statistics():
        return send_from_directory(os.path.join(app.static_folder, 'pages'), 'statistics.html')

    @app.route('/css/<path:filename>')
    def serve_css(filename):
        return send_from_directory(app.static_folder, filename)

    @app.route('/js/<path:filename>')
    def serve_js(filename):
        return send_from_directory(app.static_folder, filename)

    # Health check
    @app.route('/api/health')
    def health():
        return {'status': 'ok', 'message': 'SMS Dashboard API is running'}

    # Create tables
    with app.app_context():
        db.create_all()
        print("[APP] Database tables created successfully")

    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
