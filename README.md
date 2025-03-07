# Flask Login Application

A secure and modern web application built with Flask that features user authentication, a dashboard, and profile management capabilities. This application demonstrates best practices in web security, user experience, and responsive design.

## Features

- **Secure Authentication System**: Robust login and registration with password strength validation
- **Interactive Dashboard**: User-friendly interface for account management
- **Profile Management**: Update personal details and securely change passwords
- **Modern UI**: Responsive design using Tailwind CSS and DaisyUI components
- **Strong Password Policy**: Comprehensive security with visual password strength indicator
- **SEO-Compatible**: Built with search engine optimization in mind

## Technologies Used

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Jinja2 templates with Tailwind CSS and DaisyUI
- **Authentication**: Flask-Login with secure session management
- **Forms**: Flask-WTF with comprehensive validation
- **Security**: 
  - CSRF protection via Flask-WTF
  - Content Security Policy (CSP) via Flask-Talisman
  - Cross-Origin Resource Sharing (CORS) via Flask-CORS
  - Rate limiting via Flask-Limiter
  - Password hashing with Werkzeug's implementation
  - HTTP security headers
  - Secure session cookies

## Installation

### Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

### Setup Instructions

#### Windows

```cmd
# Clone the repository
git clone https://github.com/yourusername/flask-login-app.git
cd flask-login-app

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.sample)
copy .env.sample .env

# Run the application
flask run
```

#### Linux/Mac

```bash
# Clone the repository
git clone https://github.com/yourusername/flask-login-app.git
cd flask-login-app

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.sample)
cp .env.sample .env

# Run the application
flask run
```

## Environment Variables

Create a `.env` file in the root directory with the following variables (see `.env.sample` for reference):

- `FLASK_APP`: Entry point to the application (app.py)
- `FLASK_ENV`: Environment (development/production)
- `SECRET_KEY`: Secret key for session encryption
- `DATABASE_URI`: Database connection URL

## Password Security Features

This application implements stringent password security measures including:

- Minimum length of 12 characters
- Requirement for uppercase and lowercase letters
- Requirement for at least one number
- Requirement for at least one special character
- Visual password strength meter with real-time feedback
- Secure password hashing using Werkzeug's implementation
- Protection against common password patterns
- Account lockout after multiple failed attempts via rate limiting

## Security Features

The application includes several security measures to protect against common web vulnerabilities:

### Content Security Policy (CSP)
- Restricts resources that can be loaded (scripts, styles, fonts, etc.)
- Prevents XSS attacks by controlling which scripts can execute
- Implemented using Flask-Talisman

### Cross-Origin Resource Sharing (CORS)
- Controls which external domains can access the application's resources
- Configurable allowed origins through environment variables
- Implemented using Flask-CORS

### Rate Limiting
- Protects against brute force attacks
- Limits login attempts to 5 per minute
- Limits registration to 3 per hour
- Configurable through environment variables
- Implemented using Flask-Limiter

### CSRF Protection
- Every form includes CSRF token protection
- Prevents cross-site request forgery attacks
- Implemented using Flask-WTF

### HTTP Security Headers
- Strict-Transport-Security (HSTS)
- X-Content-Type-Options
- X-Frame-Options
- Feature-Policy (Permissions-Policy)
- Implemented using Flask-Talisman

## Project Structure

```
flask-login-app/
├── app.py                  # Application entry point
├── models.py               # Database models
├── forms.py                # Form definitions
├── requirements.txt        # Project dependencies
├── .env                    # Environment variables (create from .env.sample)
├── .env.sample             # Sample environment variables
├── README.md               # Project documentation
├── .gitignore              # Git ignore file
├── static/                 # Static files
│   ├── css/                # CSS files
│   └── js/                 # JavaScript files
└── templates/              # Jinja2 templates
    ├── layout.html         # Base template
    ├── index.html          # Home page
    ├── login.html          # Login page
    ├── register.html       # Registration page
    ├── dashboard.html      # User dashboard
    └── profile.html        # User profile page
```

## Development Workflow

1. Create feature branches from the main branch
2. Implement and test new features locally
3. Submit pull requests for code review
4. Merge approved changes back to the main branch

## Deployment to Vercel

This application is configured for deployment to [Vercel](https://vercel.com), a popular platform for hosting web applications.

### Prerequisites for Vercel Deployment

- A Vercel account
- Vercel CLI (optional, for local testing)
- Git repository with your application code

### Deployment Steps

1. **Push your code to a Git repository** (GitHub, GitLab, or Bitbucket)

2. **Connect your repository to Vercel**:
   - Log in to your Vercel account
   - Click "New Project"
   - Import your Git repository
   - Select the repository containing this application

3. **Configure environment variables**:
   - In the Vercel dashboard, go to your project settings
   - Navigate to the "Environment Variables" section
   - Add all the required environment variables from `.env.sample`
   - Ensure you set `FLASK_ENV=production` and `VERCEL_DEPLOYMENT=TRUE`
   - Generate a strong `SECRET_KEY` for production use

4. **Configure build settings** (usually automatic):
   - Vercel will automatically detect the Python application
   - The included `vercel.json` file configures the build process

5. **Deploy your application**:
   - Click "Deploy" in the Vercel dashboard
   - Vercel will build and deploy your application
   - You'll receive a deployment URL (e.g., https://your-app.vercel.app)

### Using the Vercel CLI (Optional)

For local testing or advanced deployment options:

#### Windows

```cmd
# Install Vercel CLI
npm install -g vercel

# Log in to Vercel
vercel login

# Deploy from your project directory
cd your-project-directory
vercel
```

#### Linux/Mac

```bash
# Install Vercel CLI
npm install -g vercel

# Log in to Vercel
vercel login

# Deploy from your project directory
cd your-project-directory
vercel
```

### Notes on Vercel Deployment

- **Serverless functions**: Your Flask app runs as serverless functions on Vercel
- **Static assets**: The `static/` directory contents are served efficiently with proper caching
- **Database**: This application uses SQLite which is not ideal for production. For a production Vercel deployment, consider:
  - Using a managed database service (PostgreSQL, MySQL)
  - Updating the `DATABASE_URI` environment variable accordingly
- **Cold starts**: Serverless functions may experience "cold starts" if not accessed frequently

### Troubleshooting Vercel Deployments

- Check the deployment logs in the Vercel dashboard
- Ensure all required environment variables are set
- Verify your `requirements.txt` includes all dependencies
- For path errors, make sure the paths in `vercel.json` are correct
- For loading issues, check the CSP settings in `app.py` and ensure they're appropriate for production

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask documentation and community
- Tailwind CSS and DaisyUI for the modern UI components
- All open-source packages that made this project possible
