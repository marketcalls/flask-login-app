from flask import Flask, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf import CSRFProtect
from models import db, User
from forms import LoginForm, RegistrationForm, ProfileForm
from config import get_config
from datetime import datetime

# Create Flask app
app = Flask(__name__)
app.config.from_object(get_config())

# Initialize extensions
db.init_app(app)
csrf = CSRFProtect(app)

# Add CSRF token to all templates
@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=csrf._get_csrf_token())

# Add current year to template context
@app.context_processor
def inject_template_globals():
    return {'current_year': datetime.now().year}

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Initialize security features in production only
def init_security_for_production():
    if app.config.get('FLASK_ENV') == 'production':
        try:
            from flask_talisman import Talisman
            # In production, use strict CSP
            talisman = Talisman(
                app,
                content_security_policy=app.config['CSP'],
                content_security_policy_nonce_in=['script-src', 'style-src'],
                feature_policy='geolocation \'none\'; microphone \'none\'; camera \'none\'',
                force_https=app.config.get('FORCE_HTTPS', True),
                session_cookie_secure=app.config.get('SECURE_COOKIES', True),
                session_cookie_http_only=True,
                frame_options='DENY',
            )
            app.logger.info("Talisman initialized in production mode with CSP")
        except ImportError:
            app.logger.warning("Flask-Talisman not available, running without CSP")

# Don't initialize Talisman in development mode
if app.config.get('FLASK_ENV') != 'development':
    init_security_for_production()

# Initialize Flask-CORS
allowed_origins = app.config.get('ALLOWED_ORIGINS', '*')
origins = [origin.strip() for origin in allowed_origins.split(',')] if allowed_origins != '*' else '*'
CORS(app, resources={r"/*": {
    "origins": origins, 
    "methods": app.config.get('ALLOWED_METHODS', ['GET', 'POST', 'OPTIONS']),
    "supports_credentials": app.config.get('ALLOW_CREDENTIALS', True)
}})

# Initialize Flask-Limiter
default_day_limit = app.config.get('DEFAULT_RATE_LIMIT_DAY', '200')
default_hour_limit = app.config.get('DEFAULT_RATE_LIMIT_HOUR', '50')
default_limits = [f"{default_day_limit} per day", f"{default_hour_limit} per hour"]

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=default_limits,
    storage_uri="memory://",
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit(app.config.get('LOGIN_RATE_LIMIT', '5/minute'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page if next_page else url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit(app.config.get('REGISTER_RATE_LIMIT', '3/hour'))
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        
        if form.password.data:
            current_user.password = form.password.data
            
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('profile.html', form=form)

# Create database tables within app context
def create_tables():
    with app.app_context():
        db.create_all()

# Vercel serverless function entry point
def handler(request, context):
    # Create WSGI handler for Vercel
    return app(request, context)

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
