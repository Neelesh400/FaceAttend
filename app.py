import os
import datetime
from flask import Flask, render_template, session, redirect, url_for, flash
from config import Config
from database.db import close_db, init_db, query_db
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.user import user_bp
from routes.api import api_bp

def create_app(config_class=Config):
    """Application factory for FaceAttend."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure required directories exist
    os.makedirs(os.path.join(app.config['BASE_DIR'], 'database', 'faces'), exist_ok=True)
    os.makedirs(os.path.join(app.config['BASE_DIR'], 'face_recognition', 'models'), exist_ok=True)

    # Register database teardown
    app.teardown_appcontext(close_db)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(api_bp)

    # Global template context processor
    @app.context_processor
    def inject_global_vars():
        settings = query_db("SELECT institute_name, academic_term FROM settings WHERE id = 1", one=True)
        institute_name = settings['institute_name'] if settings else 'FaceAttend Academy'
        academic_term = settings['academic_term'] if settings else '2026 Term'
        
        now = datetime.datetime.now()
        return {
            'system_name': 'FaceAttend',
            'institute_name': institute_name,
            'academic_term': academic_term,
            'current_year': now.year,
            'current_date_formatted': now.strftime("%A, %d %B %Y"),
            'current_time_formatted': now.strftime("%I:%M %p"),
            'session_user': session
        }

    # Custom error handlers
    @app.errorhandler(403)
    def forbidden(e):
        flash("Access Denied: You do not have permission to view this resource.", "danger")
        if session.get('role') == 'ADMIN':
            return redirect(url_for('admin.dashboard'))
        elif session.get('role') == 'USER':
            return redirect(url_for('user.dashboard'))
        return redirect(url_for('auth.login'))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('base.html', error_code=404, error_message="Page Not Found"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('base.html', error_code=500, error_message="Internal Server Error"), 500

    return app

app = create_app()

if __name__ == '__main__':
    # Initialize DB tables if not present
    with app.app_context():
        init_db()
    print("=====================================================")
    print("   FaceAttend: Face Recognition Attendance System     ")
    print("   Admin Portal:   http://127.0.0.1:5000/login       ")
    print("   Admin Login:    admin / admin123                  ")
    print("   Student Login:  student / student123              ")
    print("=====================================================")
    app.run(host='127.0.0.1', port=5000, debug=True)
