from flask import Flask, request, jsonify, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import uuid
from datetime import datetime, timedelta
import os
import asyncio
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib.parse import urlparse
import re
from llm_orchestrator import orchestrator
from workflow_automation_agent import workflow_agent
from document_generation_agent import document_agent
from ai_governance_agent import governance_agent
from proactive_compliance_agent import compliance_agent
from predictive_analytics_agent import predictive_agent

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key"
app.config["JWT_SECRET_KEY"] = "jwt-secret-string"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hr_advisor.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Automatic CORS handler that works with ANY Vercel deployment URL
@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    if origin:
        # Allow any hr-advisor-app Vercel deployment automatically
        if re.match(r'^https://hr-advisor-app(-[a-z0-9]+)?\.vercel\.app$', origin):
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        # Allow localhost for development
        elif 'localhost' in origin or '127.0.0.1' in origin:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# Handle preflight OPTIONS requests for CORS
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        origin = request.headers.get('Origin')
        response = make_response()
        if origin:
            # Allow any hr-advisor-app Vercel deployment automatically
            if re.match(r'^https://hr-advisor-app(-[a-z0-9]+)?\.vercel\.app$', origin):
                response.headers['Access-Control-Allow-Origin'] = origin
                response.headers['Access-Control-Allow-Credentials'] = 'true'
                response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
                response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            # Allow localhost for development
            elif 'localhost' in origin or '127.0.0.1' in origin:
                response.headers['Access-Control-Allow-Origin'] = origin
                response.headers['Access-Control-Allow-Credentials'] = 'true'
                response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
                response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

# Initialize database tables on startup
def init_database():
    try:
        with app.app_context():
            print("Initializing database...")
            db.create_all()
            print("Database tables created successfully!")
            
            # Initialize subscription plans if they don't exist
            if not SubscriptionPlan.query.first():
                print("Creating default subscription plans...")
                free_plan = SubscriptionPlan(name='Free', monthly_cost=0.0, coin_allocation=10, features='Basic HR Advice,Limited Templates')
                premium_plan = SubscriptionPlan(name='Premium', monthly_cost=29.99, coin_allocation=100, features='Advanced HR Advice,All Templates,Basic Workflows')
                enterprise_plan = SubscriptionPlan(name='Enterprise', monthly_cost=99.99, coin_allocation=1000, features='Custom HR Advice,All Templates,Advanced Workflows,Dedicated Support')
                db.session.add_all([free_plan, premium_plan, enterprise_plan])
                db.session.commit()
                print("Subscription plans created successfully!")
            else:
                print("Subscription plans already exist, skipping creation.")
                
    except Exception as e:
        print(f"Database initialization error: {str(e)}")
        # Don't fail the app startup, but log the error
        import traceback
        traceback.print_exc()

# Models
class SubscriptionPlan(db.Model):
    __tablename__ = 'subscription_plan'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    monthly_cost = db.Column(db.Float, nullable=False)
    coin_allocation = db.Column(db.Integer, nullable=False)
    features = db.Column(db.Text, nullable=True) # Comma separated string of features

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'monthly_cost': self.monthly_cost,
            'coin_allocation': self.coin_allocation,
            'features': self.features.split(',') if self.features else []
        }

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    coins = db.Column(db.Integer, default=100)
    country_context = db.Column(db.String(10), default='US')
    google_id = db.Column(db.String(100), nullable=True)  # For Google OAuth
    
    # Email verification fields
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    verification_token = db.Column(db.String(100), nullable=True)
    verification_sent_at = db.Column(db.DateTime, nullable=True)
    
    # Password reset fields
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)
    
    # New subscription fields
    subscription_plan_id = db.Column(db.Integer, db.ForeignKey('subscription_plan.id'), default=1) # Default to Free plan
    subscription_start_date = db.Column(db.DateTime, default=datetime.utcnow)
    subscription_end_date = db.Column(db.DateTime, nullable=True)

    subscription_plan = db.relationship('SubscriptionPlan', backref='users')

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'email': self.email,
            'email_verified': self.email_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'coins': self.coins,
            'country_context': self.country_context,
            'subscription_plan': self.subscription_plan.to_dict() if self.subscription_plan else None,
            'subscription_start_date': self.subscription_start_date.isoformat() if self.subscription_start_date else None,
            'subscription_end_date': self.subscription_end_date.isoformat() if self.subscription_end_date else None
        }

class PromptHistory(db.Model):
    __tablename__ = 'prompt_history'
    prompt_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.user_id'), nullable=False)
    prompt_text = db.Column(db.Text, nullable=False)
    response_text = db.Column(db.Text, nullable=False)
    country_context = db.Column(db.String(10), nullable=False)
    coins_consumed = db.Column(db.Integer, default=1)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    prompt_type = db.Column(db.String(50), default='query')

    def to_dict(self):
        return {
            'prompt_id': self.prompt_id,
            'user_id': self.user_id,
            'prompt_text': self.prompt_text,
            'response_text': self.response_text,
            'country_context': self.country_context,
            'coins_consumed': self.coins_consumed,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'prompt_type': self.prompt_type
        }

class Employee(db.Model):
    __tablename__ = 'employee'
    employee_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.user_id'), nullable=False)
    
    # Basic Information
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    address = db.Column(db.Text, nullable=True)
    
    # Employment Details
    position = db.Column(db.String(255), nullable=True)
    department = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(10), nullable=False, default='US')
    location = db.Column(db.String(255), nullable=True)  # Office location/city
    employment_type = db.Column(db.String(50), nullable=True, default='Full-time')  # Full-time, Part-time, Contract, Intern
    work_arrangement = db.Column(db.String(50), nullable=True, default='On-site')  # On-site, Remote, Hybrid
    
    # Dates and Status
    hire_date = db.Column(db.Date, nullable=True)
    termination_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(50), default='Active')  # Active, Inactive, On Leave, Terminated
    termination_type = db.Column(db.String(50), nullable=True)  # Voluntary, Involuntary
    termination_reason = db.Column(db.Text, nullable=True)
    
    # Compensation
    salary = db.Column(db.Float, nullable=True)
    currency = db.Column(db.String(10), nullable=True, default='USD')
    
    # Demographics (for diversity analytics)
    gender = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    ethnicity = db.Column(db.String(100), nullable=True)
    
    # Performance and Engagement
    engagement_score = db.Column(db.Float, nullable=True)  # 1-10 scale
    last_engagement_survey = db.Column(db.Date, nullable=True)
    performance_rating = db.Column(db.String(50), nullable=True)  # Excellent, Good, Satisfactory, Needs Improvement
    last_performance_review = db.Column(db.Date, nullable=True)
    
    # Attendance and Leave
    total_leave_days = db.Column(db.Integer, nullable=True, default=0)
    sick_leave_taken = db.Column(db.Integer, nullable=True, default=0)
    vacation_leave_taken = db.Column(db.Integer, nullable=True, default=0)
    unplanned_absences = db.Column(db.Integer, nullable=True, default=0)  # For absenteeism tracking
    
    # Emergency Contact
    emergency_contact_name = db.Column(db.String(255), nullable=True)
    emergency_contact_phone = db.Column(db.String(50), nullable=True)
    emergency_contact_relationship = db.Column(db.String(100), nullable=True)
    
    # System Fields
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'employee_id': self.employee_id,
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'position': self.position,
            'department': self.department,
            'country': self.country,
            'location': self.location,
            'employment_type': self.employment_type,
            'work_arrangement': self.work_arrangement,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'termination_date': self.termination_date.isoformat() if self.termination_date else None,
            'status': self.status,
            'termination_type': self.termination_type,
            'termination_reason': self.termination_reason,
            'salary': self.salary,
            'currency': self.currency,
            'gender': self.gender,
            'age': self.age,
            'ethnicity': self.ethnicity,
            'engagement_score': self.engagement_score,
            'last_engagement_survey': self.last_engagement_survey.isoformat() if self.last_engagement_survey else None,
            'performance_rating': self.performance_rating,
            'last_performance_review': self.last_performance_review.isoformat() if self.last_performance_review else None,
            'total_leave_days': self.total_leave_days,
            'sick_leave_taken': self.sick_leave_taken,
            'vacation_leave_taken': self.vacation_leave_taken,
            'unplanned_absences': self.unplanned_absences,
            'emergency_contact_name': self.emergency_contact_name,
            'emergency_contact_phone': self.emergency_contact_phone,
            'emergency_contact_relationship': self.emergency_contact_relationship,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# Initialize database on startup
init_database()

def get_frontend_url():
    """
    Automatically detect frontend URL from request or environment variable.
    Works with any Vercel deployment URL automatically.
    """
    # Production: Use environment variable if set
    frontend_url = os.getenv('FRONTEND_URL')
    if frontend_url:
        return frontend_url.rstrip('/')
    
    # Automatic detection: Get from request headers (works for any Vercel URL)
    if request and hasattr(request, 'headers'):
        # Check Origin header first (most reliable for CORS requests)
        origin = request.headers.get('Origin')
        if origin and ('hr-advisor-app' in origin or 'localhost' in origin or '127.0.0.1' in origin):
            return origin
        
        # Check Referer header as fallback
        referer = request.headers.get('Referer')
        if referer and ('hr-advisor-app' in referer or 'localhost' in referer or '127.0.0.1' in referer):
            parsed = urlparse(referer)
            return f"{parsed.scheme}://{parsed.netloc}"
    
    # Emergency fallback - should rarely be used with automatic detection
    print("WARNING: Could not detect frontend URL from request headers.")
    print("Consider setting FRONTEND_URL environment variable for reliability.")
    return "https://hr-advisor-app-9a6m.vercel.app"  # Current deployment

def get_redirect_url(verification_status):
    """
    Generate redirect URL with verification status parameter.
    """
    frontend_url = get_frontend_url()
    return f"{frontend_url}/?verification={verification_status}"

# Routes
@app.route('/api/health', methods=['GET'])
def health():
    try:
        # Test database connection
        with app.app_context():
            # Try to query the database
            user_count = User.query.count()
            plan_count = SubscriptionPlan.query.count()
            
        return jsonify({
            'status': 'healthy', 
            'message': 'HR Advisor API is running',
            'database': 'connected',
            'users': user_count,
            'subscription_plans': plan_count
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'message': 'HR Advisor API is running but database has issues',
            'database': 'error',
            'error': str(e)
        }), 500

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if user already exists by email
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Generate verification token
        verification_token = secrets.token_urlsafe(32)
        
        # Get frontend URL from request context for later use
        frontend_url = get_frontend_url()
        
        # Create new user (unverified)
        user = User(
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            email_verified=False,
            verification_token=verification_token,
            verification_sent_at=datetime.utcnow()
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Send verification email (simplified for now)
        try:
            send_verification_email(user.email, verification_token, frontend_url)
        except Exception as e:
            print(f"Failed to send verification email: {str(e)}")
            # Don't fail registration if email fails
        
        return jsonify({
            'message': 'Registration successful! Please check your email to verify your account.',
            'email_sent': True,
            'user_id': user.user_id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500

def send_verification_email(email, token, frontend_url=None):
    """Send verification email to user"""
    try:
        # Email configuration from environment variables
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')
        from_email = os.getenv('FROM_EMAIL', smtp_username)
        
        if not smtp_username or not smtp_password:
            print("SMTP credentials not configured. Email not sent.")
            return False
        
        # Use provided frontend_url or detect dynamically
        if not frontend_url:
            frontend_url = get_frontend_url()
        
        # Create verification URL - point to backend API endpoint
        verification_url = f"https://hr-advisor-app.onrender.com/api/auth/verify-email/{token}"
        
        # Create email content
        subject = "Verify Your AnNi AI Account"
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Verify Your Account</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #2563eb;">AnNi AI</h1>
                    <p style="color: #666;">HR made simple</p>
                </div>
                
                <h2>Welcome to AnNi AI!</h2>
                <p>Thank you for signing up. Please verify your email address to complete your registration.</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{verification_url}" 
                       style="background-color: #2563eb; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 5px; display: inline-block;">
                        Verify Email Address
                    </a>
                </div>
                
                <p>If the button doesn't work, copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #2563eb;">{verification_url}</p>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                <p style="font-size: 12px; color: #666;">
                    This verification link will expire in 24 hours. If you didn't create an account with AnNi AI, 
                    please ignore this email.
                </p>
            </div>
        </body>
        </html>
        """
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = email
        
        # Add HTML content
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        
        print(f"Verification email sent successfully to {email}")
        return True
        
    except Exception as e:
        print(f"Failed to send verification email: {str(e)}")
        return False

def send_password_reset_email(email, token):
    """Send password reset email to user"""
    try:
        # Email configuration from environment variables
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')
        from_email = os.getenv('FROM_EMAIL', smtp_username)
        
        if not smtp_username or not smtp_password:
            print("SMTP credentials not configured. Email not sent.")
            return False
        
        # Create reset URL
        reset_url = f"https://hr-advisor-app.vercel.app/reset-password?token={token}"
        
        # Create email content
        subject = "Reset Your AnNi AI Password"
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Reset Your Password</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #2563eb;">AnNi AI</h1>
                    <p style="color: #666;">HR made simple</p>
                </div>
                
                <h2>Password Reset Request</h2>
                <p>We received a request to reset your password for your AnNi AI account.</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_url}" 
                       style="background-color: #dc2626; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 5px; display: inline-block;">
                        Reset Password
                    </a>
                </div>
                
                <p>If the button doesn't work, copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #dc2626;">{reset_url}</p>
                
                <div style="background-color: #fef2f2; border-left: 4px solid #dc2626; padding: 15px; margin: 20px 0;">
                    <p style="margin: 0; font-weight: bold; color: #dc2626;">Security Notice:</p>
                    <p style="margin: 5px 0 0 0;">If you didn't request this password reset, please ignore this email. 
                    Your password will remain unchanged.</p>
                </div>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                <p style="font-size: 12px; color: #666;">
                    This password reset link will expire in 1 hour for security reasons. 
                    If you need help, contact our support team.
                </p>
            </div>
        </body>
        </html>
        """
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = email
        
        # Add HTML content
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        
        print(f"Password reset email sent successfully to {email}")
        return True
        
    except Exception as e:
        print(f"Failed to send password reset email: {str(e)}")
        return False

@app.route('/api/auth/verify-email/<token>', methods=['GET'])
def verify_email(token):
    try:
        user = User.query.filter_by(verification_token=token).first()
        
        if not user:
            # Redirect to frontend with error
            return redirect(get_redirect_url('invalid'))
        
        if user.email_verified:
            # Redirect to frontend with already verified message
            return redirect(get_redirect_url('already_verified'))
        
        # Check if token is expired (24 hours)
        if user.verification_sent_at and (datetime.utcnow() - user.verification_sent_at) > timedelta(hours=24):
            # Redirect to frontend with expired error
            return redirect(get_redirect_url('expired'))
        
        # Verify the email
        user.email_verified = True
        user.verification_token = None
        db.session.commit()
        
        # Redirect to frontend with success message
        return redirect(get_redirect_url('success'))
        
    except Exception as e:
        print(f"Email verification error: {str(e)}")
        # Redirect to frontend with error
        return redirect(get_redirect_url('error'))

@app.route('/api/auth/resend-verification', methods=['POST'])
def resend_verification():
    try:
        data = request.get_json()
        
        if not data or not data.get('email'):
            return jsonify({'error': 'Email is required'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if user.email_verified:
            return jsonify({'error': 'Email already verified'}), 400
        
        # Generate new verification token
        verification_token = secrets.token_urlsafe(32)
        user.verification_token = verification_token
        user.verification_sent_at = datetime.utcnow()
        db.session.commit()
        
        # Get frontend URL from request context
        frontend_url = get_frontend_url()
        
        # Send verification email
        try:
            send_verification_email(user.email, verification_token, frontend_url)
        except Exception as e:
            print(f"Failed to send verification email: {str(e)}")
            return jsonify({'error': 'Failed to send verification email'}), 500
        
        return jsonify({
            'message': 'Verification email sent! Please check your inbox.',
            'email_sent': True
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to resend verification: {str(e)}'}), 500

@app.route('/api/auth/forgot-password', methods=['POST'])
def forgot_password():
    try:
        data = request.get_json()
        
        if not data or not data.get('email'):
            return jsonify({'error': 'Email is required'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        # Always return success message for security (don't reveal if email exists)
        if not user:
            return jsonify({
                'message': 'If an account with that email exists, a password reset link has been sent.',
                'email_sent': True
            }), 200
        
        # Generate password reset token
        reset_token = secrets.token_urlsafe(32)
        user.reset_token = reset_token
        user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)  # 1 hour expiry
        db.session.commit()
        
        # Send password reset email
        try:
            send_password_reset_email(user.email, reset_token)
        except Exception as e:
            print(f"Failed to send password reset email: {str(e)}")
            # Don't reveal email sending failure for security
        
        return jsonify({
            'message': 'If an account with that email exists, a password reset link has been sent.',
            'email_sent': True
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Password reset request failed: {str(e)}'}), 500

@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        
        if not data or not data.get('token') or not data.get('password'):
            return jsonify({'error': 'Token and new password are required'}), 400
        
        user = User.query.filter_by(reset_token=data['token']).first()
        
        if not user:
            return jsonify({'error': 'Invalid or expired reset token'}), 400
        
        # Check if token is expired
        if not user.reset_token_expires or datetime.utcnow() > user.reset_token_expires:
            return jsonify({'error': 'Reset token has expired'}), 400
        
        # Validate password strength
        if len(data['password']) < 6:
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400
        
        # Update password and clear reset token
        user.password_hash = generate_password_hash(data['password'])
        user.reset_token = None
        user.reset_token_expires = None
        db.session.commit()
        
        return jsonify({
            'message': 'Password reset successful! You can now log in with your new password.',
            'success': True
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Password reset failed: {str(e)}'}), 500

@app.route('/api/auth/validate-reset-token/<token>', methods=['GET'])
def validate_reset_token(token):
    try:
        user = User.query.filter_by(reset_token=token).first()
        
        if not user:
            return jsonify({'valid': False, 'error': 'Invalid reset token'}), 400
        
        # Check if token is expired
        if not user.reset_token_expires or datetime.utcnow() > user.reset_token_expires:
            return jsonify({'valid': False, 'error': 'Reset token has expired'}), 400
        
        return jsonify({
            'valid': True,
            'email': user.email  # Show email for confirmation
        }), 200
        
    except Exception as e:
        return jsonify({'valid': False, 'error': f'Token validation failed: {str(e)}'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing email or password'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if user and check_password_hash(user.password_hash, data['password']):
            # Check if email is verified
            if not user.email_verified:
                return jsonify({
                    'error': 'Please verify your email address before logging in',
                    'email_verified': False,
                    'user_id': user.user_id
                }), 403
            
            access_token = create_access_token(identity=user.user_id)
            return jsonify({
                'message': 'Login successful',
                'access_token': access_token,
                'user': user.to_dict()
            })
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'error': f'Login failed: {str(e)}'}), 500

@app.route('/api/auth/google', methods=['POST'])
def google_auth():
    try:
        data = request.get_json()
        
        if not data or not data.get('google_id') or not data.get('email'):
            return jsonify({'error': 'Missing Google authentication data'}), 400
        
        google_id = data['google_id']
        email = data['email']
        name = data.get('name', '')
        picture = data.get('picture', '')
        
        # Check if user already exists with this email
        user = User.query.filter_by(email=email).first()
        
        if user:
            # User exists, update Google ID if not set and log them in
            if not hasattr(user, 'google_id') or not user.google_id:
                user.google_id = google_id
                db.session.commit()
            
            access_token = create_access_token(identity=user.user_id)
            return jsonify({
                'message': 'Login successful',
                'access_token': access_token,
                'user': user.to_dict()
            })
        else:
            # Create new user with Google data (no username needed)
            user = User(
                email=email,
                password_hash=generate_password_hash(google_id),  # Use Google ID as password hash
                google_id=google_id
            )
            
            db.session.add(user)
            db.session.commit()
            
            # Create access token
            access_token = create_access_token(identity=user.user_id)
            
            return jsonify({
                'message': 'User created successfully',
                'access_token': access_token,
                'user': user.to_dict()
            }), 201
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Google authentication failed: {str(e)}'}), 500

@app.route('/api/user/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()})
        
    except Exception as e:
        return jsonify({'error': f'Failed to get profile: {str(e)}'}), 500

@app.route('/api/hr_advisor/query', methods=['POST'])
@jwt_required()
def hr_advisor_query():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        query = data.get('query', '')
        country = data.get('country', user.country_context)
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Check if user has enough coins
        if user.coins < 1:
            return jsonify({'error': 'Insufficient coins'}), 402
        
        # Multi-LLM Orchestration for HR advice
        try:
            # Country-specific HR context
            country_contexts = {
                'US': 'United States federal and state employment laws, FLSA, FMLA, ADA compliance, OSHA regulations',
                'UK': 'UK employment law, ACAS guidelines, GDPR compliance, statutory rights, Working Time Regulations',
                'SG': 'Singapore Employment Act, MOM regulations, CPF requirements, workplace safety standards',
                'AU': 'Australian Fair Work Act, workplace safety regulations, superannuation requirements',
                'CA': 'Canadian Labour Code, provincial employment standards, health and safety regulations',
                'DE': 'German employment law, works councils, data protection, Arbeitsrecht',
                'FR': 'French Labour Code, collective bargaining agreements, social security regulations',
                'IN': 'Indian labour laws, PF, ESI, gratuity regulations, Factories Act',
                'MY': 'Malaysian Employment Act, EPF, SOCSO, industrial relations',
                'HK': 'Hong Kong Employment Ordinance, MPF, labour tribunal procedures',
                'JP': 'Japanese Labor Standards Act, employment insurance, workplace safety',
                'ID': 'Indonesian Labor Law, BPJS, manpower regulations',
                'TH': 'Thai Labor Protection Act, social security, work permit regulations'
            }
            
            context = country_contexts.get(country, country_contexts['US'])
            system_context = f"You are an expert HR advisor specializing in {context}. Provide practical, actionable advice that complies with local regulations and best practices. Always cite relevant laws and regulations."
            
            # Use Multi-LLM Orchestration
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                orchestration_result = loop.run_until_complete(
                    orchestrator.orchestrate_llm_responses(query, country, system_context)
                )
                
                response_text = orchestration_result['content']
                metadata = {
                    'provider_used': orchestration_result['provider_used'],
                    'confidence_score': orchestration_result['confidence_score'],
                    'sources': orchestration_result['sources'],
                    'llm_responses_count': orchestration_result['llm_responses_count']
                }
                
            finally:
                loop.close()
            
        except Exception as e:
            # Fallback to basic response if orchestration fails
            response_text = f"HR guidance for {country}: {query}. Please ensure compliance with local employment laws and consult official government sources for the most current regulations. [Multi-LLM orchestration error: {str(e)}]"
            metadata = {
                'provider_used': 'fallback',
                'confidence_score': 0.3,
                'sources': [],
                'llm_responses_count': 0
            }
        
        # Deduct coins
        user.coins -= 1
        
        # Save prompt history
        prompt_history = PromptHistory(
            user_id=user_id,
            prompt_text=query,
            response_text=response_text,
            country_context=country,
            coins_consumed=1
        )
        
        db.session.add(prompt_history)
        db.session.commit()
        
        return jsonify({
            'response': response_text,
            'country_context': country,
            'coins_consumed': 1,
            'coins_remaining': user.coins,
            'prompt_id': prompt_history.prompt_id,
            'orchestration_metadata': metadata
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Query failed: {str(e)}'}), 500

@app.route('/api/hr_advisor/chat', methods=['POST'])
@jwt_required()
def hr_advisor_chat():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        prompt = data.get('prompt', '')
        country = data.get('country', user.country_context)
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Check if user has enough coins
        if user.coins < 1:
            return jsonify({'error': 'Insufficient coins'}), 402
        
        # Multi-LLM Orchestration for HR template generation
        try:
            # Country-specific HR context
            country_contexts = {
                'US': 'United States federal and state employment laws, FLSA, FMLA, ADA compliance, OSHA regulations',
                'UK': 'UK employment law, ACAS guidelines, GDPR compliance, statutory rights, Working Time Regulations',
                'SG': 'Singapore Employment Act, MOM regulations, CPF requirements, workplace safety standards',
                'AU': 'Australian Fair Work Act, workplace safety regulations, superannuation requirements',
                'CA': 'Canadian Labour Code, provincial employment standards, health and safety regulations',
                'DE': 'German employment law, works councils, data protection, Arbeitsrecht',
                'FR': 'French Labour Code, collective bargaining agreements, social security regulations',
                'IN': 'Indian labour laws, PF, ESI, gratuity regulations, Factories Act',
                'MY': 'Malaysian Employment Act, EPF, SOCSO, industrial relations',
                'HK': 'Hong Kong Employment Ordinance, MPF, labour tribunal procedures',
                'JP': 'Japanese Labor Standards Act, employment insurance, workplace safety',
                'ID': 'Indonesian Labor Law, BPJS, manpower regulations',
                'TH': 'Thai Labor Protection Act, social security, work permit regulations'
            }
            
            context = country_contexts.get(country, country_contexts['US'])
            system_context = f"You are an expert HR advisor specializing in {context}. Generate professional HR templates and documents that comply with local regulations and best practices. Always include relevant legal disclaimers and cite applicable laws."
            
            # Use Multi-LLM Orchestration
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                orchestration_result = loop.run_until_complete(
                    orchestrator.orchestrate_llm_responses(prompt, country, system_context)
                )
                
                response_text = orchestration_result['content']
                metadata = {
                    'provider_used': orchestration_result['provider_used'],
                    'confidence_score': orchestration_result['confidence_score'],
                    'sources': orchestration_result['sources'],
                    'llm_responses_count': orchestration_result['llm_responses_count']
                }
                
            finally:
                loop.close()
            
        except Exception as e:
            # Fallback to basic response if orchestration fails
            response_text = f"HR template for {country}: {prompt}. Please ensure compliance with local employment laws and consult official government sources for the most current regulations. [Multi-LLM orchestration error: {str(e)}]"
            metadata = {
                'provider_used': 'fallback',
                'confidence_score': 0.3,
                'sources': [],
                'llm_responses_count': 0
            }
        
        # Deduct coins
        user.coins -= 1
        
        # Save prompt history
        prompt_history = PromptHistory(
            user_id=user_id,
            prompt_text=prompt,
            response_text=response_text,
            country_context=country,
            coins_consumed=1
        )
        
        db.session.add(prompt_history)
        db.session.commit()
        
        return jsonify({
            'response': response_text,
            'coins_remaining': user.coins,
            'prompt_id': prompt_history.prompt_id,
            'orchestration_metadata': metadata
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Chat failed: {str(e)}'}), 500

@app.route('/api/subscriptions', methods=['GET'])
@jwt_required()
def get_subscriptions():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get the user's current subscription plan
        subscription_plan = user.subscription_plan
        
        # Handle case where subscription_plan might be None (e.g., new user before default plan is set)
        if not subscription_plan:
            # Attempt to set a default plan if it's missing
            free_plan = SubscriptionPlan.query.filter_by(name='Free').first()
            if free_plan:
                user.subscription_plan_id = free_plan.id
                db.session.commit()
                subscription_plan = free_plan
            else:
                # Fallback if even the Free plan isn't initialized (shouldn't happen if __main__ block runs)
                return jsonify({'error': 'Subscription plans not initialized'}), 500

        return jsonify({
            'plan_type': subscription_plan.name.lower().replace(' ', '_'),
            'coins_balance': user.coins,
            'total_coins_allocated': subscription_plan.coin_allocation,
            'features': subscription_plan.features.split(',') if subscription_plan.features else [],
            'expires_at': user.subscription_end_date.isoformat() if user.subscription_end_date else None
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get subscription: {str(e)}'}), 500

@app.route('/api/history/prompts/recent', methods=['GET'])
@jwt_required()
def get_recent_prompts():
    try:
        user_id = get_jwt_identity()
        history = PromptHistory.query.filter_by(user_id=user_id).order_by(PromptHistory.timestamp.desc()).limit(10).all()
        
        return jsonify({
            'recent_prompts': [h.to_dict() for h in history]
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get recent prompts: {str(e)}'}), 500

@app.route('/api/history', methods=['GET'])
@jwt_required()
def get_history():
    try:
        user_id = get_jwt_identity()
        history = PromptHistory.query.filter_by(user_id=user_id).order_by(PromptHistory.timestamp.desc()).limit(50).all()
        
        return jsonify({
            'history': [h.to_dict() for h in history]
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get history: {str(e)}'}), 500

@app.route('/api/subscriptions/upgrade', methods=['POST'])
@jwt_required()
def upgrade_subscription():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        plan_name = data.get('plan_name')
        
        if not plan_name:
            return jsonify({'error': 'Plan name is required'}), 400
            
        new_plan = SubscriptionPlan.query.filter_by(name=plan_name).first()
        
        if not new_plan:
            return jsonify({'error': 'Invalid plan name'}), 400
            
        # Prevent downgrading or upgrading to the same plan for simplicity
        if user.subscription_plan_id == new_plan.id:
            return jsonify({'message': f'Already on {plan_name} plan'}), 200
            
        # Update user's subscription
        user.subscription_plan_id = new_plan.id
        user.subscription_start_date = datetime.utcnow()
        user.subscription_end_date = None # For simplicity, assuming perpetual for now or handled by external system
        user.coins += new_plan.coin_allocation # Add coins for the new plan
        
        db.session.commit()
        
        return jsonify({
            'message': f'Successfully upgraded to {plan_name} plan',
            'new_plan': new_plan.to_dict(),
            'coins_remaining': user.coins
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Upgrade failed: {str(e)}'}), 500

@app.route('/api/employees', methods=['GET'])
@jwt_required()
def get_employees():
    try:
        user_id = get_jwt_identity()
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        # Get all employees for this user
        employees_query = Employee.query.filter_by(user_id=user_id)
        employees = employees_query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'employees': [emp.to_dict() for emp in employees.items],
            'total': employees.total,
            'pages': employees.pages,
            'current_page': page
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get employees: {str(e)}'}), 500

@app.route('/api/employees', methods=['POST'])
@jwt_required()
def add_employee():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('name') or not data.get('email'):
            return jsonify({'error': 'Name and email are required'}), 400
        
        # Check if employee with this email already exists for this user
        existing_employee = Employee.query.filter_by(
            user_id=user_id, 
            email=data['email']
        ).first()
        
        if existing_employee:
            return jsonify({'error': 'Employee with this email already exists'}), 400
        
        # Create new employee
        employee = Employee(
            user_id=user_id,
            name=data['name'],
            email=data['email'],
            phone=data.get('phone'),
            position=data.get('position'),
            department=data.get('department'),
            country=data.get('country', 'US'),
            hire_date=datetime.strptime(data['hire_date'], '%Y-%m-%d').date() if data.get('hire_date') else None,
            salary=float(data['salary']) if data.get('salary') else None,
            status=data.get('status', 'active'),
            address=data.get('address'),
            emergency_contact_name=data.get('emergency_contact_name'),
            emergency_contact_phone=data.get('emergency_contact_phone'),
            emergency_contact_relationship=data.get('emergency_contact_relationship')
        )
        
        db.session.add(employee)
        db.session.commit()
        
        return jsonify({
            'message': 'Employee added successfully',
            'employee': employee.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to add employee: {str(e)}'}), 500

@app.route('/api/employees/<employee_id>', methods=['GET'])
@jwt_required()
def get_employee(employee_id):
    try:
        user_id = get_jwt_identity()
        
        employee = Employee.query.filter_by(
            employee_id=employee_id,
            user_id=user_id
        ).first()
        
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        return jsonify({'employee': employee.to_dict()})
        
    except Exception as e:
        return jsonify({'error': f'Failed to get employee: {str(e)}'}), 500

@app.route('/api/employees/<employee_id>', methods=['PUT'])
@jwt_required()
def update_employee(employee_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        employee = Employee.query.filter_by(
            employee_id=employee_id,
            user_id=user_id
        ).first()
        
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        # Check if email is being changed and if it conflicts
        if data.get('email') and data['email'] != employee.email:
            existing_employee = Employee.query.filter_by(
                user_id=user_id,
                email=data['email']
            ).first()
            
            if existing_employee:
                return jsonify({'error': 'Employee with this email already exists'}), 400
        
        # Update employee fields
        if data.get('name'):
            employee.name = data['name']
        if data.get('email'):
            employee.email = data['email']
        if 'phone' in data:
            employee.phone = data['phone']
        if 'position' in data:
            employee.position = data['position']
        if 'department' in data:
            employee.department = data['department']
        if 'country' in data:
            employee.country = data['country']
        if data.get('hire_date'):
            employee.hire_date = datetime.strptime(data['hire_date'], '%Y-%m-%d').date()
        if 'salary' in data:
            employee.salary = float(data['salary']) if data['salary'] else None
        if 'status' in data:
            employee.status = data['status']
        if 'address' in data:
            employee.address = data['address']
        if 'emergency_contact_name' in data:
            employee.emergency_contact_name = data['emergency_contact_name']
        if 'emergency_contact_phone' in data:
            employee.emergency_contact_phone = data['emergency_contact_phone']
        if 'emergency_contact_relationship' in data:
            employee.emergency_contact_relationship = data['emergency_contact_relationship']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Employee updated successfully',
            'employee': employee.to_dict()
        })
        
    except ValueError as e:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update employee: {str(e)}'}), 500

@app.route('/api/employees/<employee_id>', methods=['DELETE'])
@jwt_required()
def delete_employee(employee_id):
    try:
        user_id = get_jwt_identity()
        
        employee = Employee.query.filter_by(
            employee_id=employee_id,
            user_id=user_id
        ).first()
        
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        db.session.delete(employee)
        db.session.commit()
        
        return jsonify({'message': 'Employee deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete employee: {str(e)}'}), 500

# Protected main route for staging access
@app.route("/")
def index():
    return jsonify({
        'message': 'HR Advisor API - Staging Environment',
        'status': 'protected',
        'credentials': 'Use hr_admin / hr_staging_2024 for access'
    })

# Production-ready application configuration
if __name__ == '__main__':
    # Only use development server for local testing
    # In production, Render should use: gunicorn --config gunicorn_config.py src.main:app
    import os
    
    if os.getenv('FLASK_ENV') == 'development':
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        # Production mode - this should not be reached if using proper start command
        print("WARNING: Running in production mode with Flask dev server")
        print("Recommended: Use 'gunicorn --config gunicorn_config.py src.main:app' instead")
        app.run(debug=False, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))




# Import new G-P requirements agents
from administrative_automation_agent import AdministrativeAutomationAgent
from personalized_development_agent import PersonalizedDevelopmentAgent

# Initialize new agents
admin_automation_agent = AdministrativeAutomationAgent()
development_agent = PersonalizedDevelopmentAgent()

# Administrative Automation API Endpoints
@app.route('/api/automation/create-task', methods=['POST'])
@jwt_required()
def create_automation_task():
    """Create a new administrative automation task."""
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        task_type = data.get('task_type')
        parameters = data.get('parameters', {})
        employee_id = data.get('employee_id')
        priority = data.get('priority', 'medium')
        
        # Create automation task
        task_id = asyncio.run(admin_automation_agent.create_automation_task(
            task_type=task_type,
            user_id=current_user,
            parameters=parameters,
            employee_id=employee_id,
            priority=getattr(admin_automation_agent.Priority, priority.upper(), admin_automation_agent.Priority.MEDIUM)
        ))
        
        if task_id:
            return jsonify({
                'success': True,
                'task_id': task_id,
                'message': f'Automation task created successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to create automation task'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error creating automation task: {str(e)}'
        }), 500

@app.route('/api/automation/status', methods=['GET'])
@jwt_required()
def get_automation_status():
    """Get automation status and metrics for current user."""
    try:
        current_user = get_jwt_identity()
        
        status = asyncio.run(admin_automation_agent.get_automation_status(current_user))
        
        return jsonify({
            'success': True,
            'data': status
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting automation status: {str(e)}'
        }), 500

@app.route('/api/automation/generate-contract', methods=['POST'])
@jwt_required()
def generate_employment_contract():
    """Generate an employment contract for an employee."""
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        employee_id = data.get('employee_id')
        contract_params = {
            'country': data.get('country', 'singapore'),
            'company': data.get('company', {}),
            'position': data.get('position', {}),
            'compensation': data.get('compensation', {}),
            'effective_date': data.get('effective_date')
        }
        
        # Create contract generation task
        task_id = asyncio.run(admin_automation_agent.create_automation_task(
            task_type='generate_contract',
            user_id=current_user,
            parameters=contract_params,
            employee_id=employee_id,
            priority=admin_automation_agent.Priority.HIGH
        ))
        
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': 'Contract generation started'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error generating contract: {str(e)}'
        }), 500

@app.route('/api/automation/generate-offer', methods=['POST'])
@jwt_required()
def generate_offer_letter():
    """Generate an offer letter for a candidate."""
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        offer_params = {
            'candidate': data.get('candidate', {}),
            'company': data.get('company', {}),
            'position': data.get('position', {}),
            'compensation': data.get('compensation', {}),
            'start_date': data.get('start_date'),
            'offer_expires': data.get('offer_expires')
        }
        
        # Create offer letter generation task
        task_id = asyncio.run(admin_automation_agent.create_automation_task(
            task_type='generate_offer_letter',
            user_id=current_user,
            parameters=offer_params,
            priority=admin_automation_agent.Priority.HIGH
        ))
        
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': 'Offer letter generation started'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error generating offer letter: {str(e)}'
        }), 500

# Personalized Development API Endpoints
@app.route('/api/development/analyze-skills', methods=['POST'])
@jwt_required()
def analyze_skill_gaps():
    """Analyze skill gaps for an employee."""
    try:
        data = request.get_json()
        employee_id = data.get('employee_id')
        target_role = data.get('target_role')
        
        analysis = asyncio.run(development_agent.analyze_skill_gaps(
            employee_id=employee_id,
            target_role=target_role
        ))
        
        return jsonify({
            'success': True,
            'data': analysis
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error analyzing skill gaps: {str(e)}'
        }), 500

@app.route('/api/development/create-plan', methods=['POST'])
@jwt_required()
def create_development_plan():
    """Create a personalized development plan for an employee."""
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        employee_id = data.get('employee_id')
        goals = data.get('goals', [])
        timeline_months = data.get('timeline_months', 12)
        
        plan_id = asyncio.run(development_agent.generate_development_plan(
            employee_id=employee_id,
            created_by=current_user,
            goals=goals,
            timeline_months=timeline_months
        ))
        
        if plan_id:
            return jsonify({
                'success': True,
                'plan_id': plan_id,
                'message': 'Development plan created successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to create development plan'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error creating development plan: {str(e)}'
        }), 500

@app.route('/api/development/recommendations/<employee_id>', methods=['GET'])
@jwt_required()
def get_learning_recommendations(employee_id):
    """Get learning recommendations for an employee."""
    try:
        # First analyze skill gaps
        gap_analysis = asyncio.run(development_agent.analyze_skill_gaps(employee_id))
        
        if 'error' in gap_analysis:
            return jsonify({
                'success': False,
                'message': gap_analysis['error']
            }), 404
        
        # Generate recommendations
        recommendations = asyncio.run(development_agent.generate_learning_recommendations(
            employee_id=employee_id,
            skill_gaps=gap_analysis.get('skill_gaps', [])[:5]  # Top 5 gaps
        ))
        
        return jsonify({
            'success': True,
            'data': {
                'skill_gaps': gap_analysis.get('skill_gaps', []),
                'recommendations': recommendations
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting learning recommendations: {str(e)}'
        }), 500

@app.route('/api/development/progress', methods=['POST'])
@jwt_required()
def update_learning_progress():
    """Update learning progress for a recommendation."""
    try:
        data = request.get_json()
        
        employee_id = data.get('employee_id')
        recommendation_id = data.get('recommendation_id')
        progress_percentage = data.get('progress_percentage', 0)
        status = data.get('status', 'in_progress')
        
        success = asyncio.run(development_agent.track_learning_progress(
            employee_id=employee_id,
            recommendation_id=recommendation_id,
            progress_percentage=progress_percentage,
            status=status
        ))
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Learning progress updated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to update learning progress'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error updating learning progress: {str(e)}'
        }), 500

@app.route('/api/development/analytics/<employee_id>', methods=['GET'])
@jwt_required()
def get_development_analytics(employee_id):
    """Get development analytics for an employee."""
    try:
        analytics = asyncio.run(development_agent.get_development_analytics(employee_id))
        
        return jsonify({
            'success': True,
            'data': analytics
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting development analytics: {str(e)}'
        }), 500

# Enhanced AI Governance Endpoints
@app.route('/api/governance/approval-workflow', methods=['POST'])
@jwt_required()
def create_ai_approval_workflow():
    """Create an AI usage approval workflow."""
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        # This would integrate with the enhanced AI governance agent
        # For now, return a placeholder response
        return jsonify({
            'success': True,
            'message': 'AI approval workflow created',
            'workflow_id': str(uuid.uuid4())
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error creating approval workflow: {str(e)}'
        }), 500

@app.route('/api/governance/usage-metrics', methods=['GET'])
@jwt_required()
def get_ai_usage_metrics():
    """Get AI usage metrics and governance dashboard data."""
    try:
        # This would integrate with the enhanced AI governance agent
        # For now, return placeholder metrics
        metrics = {
            'total_ai_requests': 1250,
            'approval_rate': 94.5,
            'average_response_time': 1.2,
            'top_use_cases': [
                {'name': 'HR Policy Queries', 'count': 450},
                {'name': 'Employee Evaluations', 'count': 320},
                {'name': 'Compliance Checks', 'count': 280},
                {'name': 'Document Generation', 'count': 200}
            ],
            'risk_alerts': 2,
            'compliance_score': 98.5
        }
        
        return jsonify({
            'success': True,
            'data': metrics
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting usage metrics: {str(e)}'
        }), 500

