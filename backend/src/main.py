from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import uuid
from datetime import datetime
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key"
app.config["JWT_SECRET_KEY"] = "jwt-secret-string"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hr_advisor.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

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
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    coins = db.Column(db.Integer, default=100)
    country_context = db.Column(db.String(10), default='US')
    google_id = db.Column(db.String(100), nullable=True)  # For Google OAuth
    
    # New subscription fields
    subscription_plan_id = db.Column(db.Integer, db.ForeignKey('subscription_plan.id'), default=1) # Default to Free plan
    subscription_start_date = db.Column(db.DateTime, default=datetime.utcnow)
    subscription_end_date = db.Column(db.DateTime, nullable=True)

    subscription_plan = db.relationship('SubscriptionPlan', backref='users')

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
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
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    position = db.Column(db.String(255), nullable=True)
    department = db.Column(db.String(255), nullable=True)
    hire_date = db.Column(db.Date, nullable=True)
    salary = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(50), default='active')
    address = db.Column(db.Text, nullable=True)
    emergency_contact = db.Column(db.String(255), nullable=True)
    emergency_phone = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'employee_id': self.employee_id,
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'position': self.position,
            'department': self.department,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'salary': self.salary,
            'status': self.status,
            'address': self.address,
            'emergency_contact': self.emergency_contact,
            'emergency_phone': self.emergency_phone,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Initialize database on startup
init_database()

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
        
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=generate_password_hash(data['password'])
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
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Missing username or password'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if user and check_password_hash(user.password_hash, data['password']):
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
            # Create new user with Google data
            # Generate username from email or name
            username = email.split('@')[0]
            counter = 1
            original_username = username
            
            # Ensure username is unique
            while User.query.filter_by(username=username).first():
                username = f"{original_username}{counter}"
                counter += 1
            
            user = User(
                username=username,
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
        
        # OpenAI integration for HR advice
        try:
            import openai
            
            # Country-specific HR context
            country_contexts = {
                'US': 'United States federal and state employment laws, FLSA, FMLA, ADA compliance',
                'UK': 'UK employment law, ACAS guidelines, GDPR compliance, statutory rights',
                'SG': 'Singapore Employment Act, MOM regulations, CPF requirements',
                'AU': 'Australian Fair Work Act, workplace safety regulations',
                'CA': 'Canadian Labour Code, provincial employment standards',
                'DE': 'German employment law, works councils, data protection',
                'FR': 'French Labour Code, collective bargaining agreements',
                'IN': 'Indian labour laws, PF, ESI, gratuity regulations'
            }
            
            context = country_contexts.get(country, country_contexts['US'])
            
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gemini-2.5-flash",
                messages=[
                    {"role": "system", "content": f"You are an expert HR advisor specializing in {context}. Provide practical, actionable advice that complies with local regulations and best practices."},
                    {"role": "user", "content": query}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            response_text = response.choices[0].message.content
            
        except Exception as e:
            # Fallback to mock response if OpenAI fails
            response_text = f"HR Advisor response for {country}: {query[:50]}... [OpenAI integration error: {str(e)}. This is a mock response.]"
        
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
            'prompt_id': prompt_history.prompt_id
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
        
        # OpenAI integration for HR advice
        try:
            import openai
            
            # Country-specific HR context
            country_contexts = {
                'US': 'United States federal and state employment laws, FLSA, FMLA, ADA compliance',
                'UK': 'UK employment law, ACAS guidelines, GDPR compliance, statutory rights',
                'SG': 'Singapore Employment Act, MOM regulations, CPF requirements',
                'AU': 'Australian Fair Work Act, workplace safety regulations',
                'CA': 'Canadian Labour Code, provincial employment standards',
                'DE': 'German employment law, works councils, data protection',
                'FR': 'French Labour Code, collective bargaining agreements',
                'IN': 'Indian labour laws, PF, ESI, gratuity regulations'
            }
            
            context = country_contexts.get(country, country_contexts['US'])
            
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gemini-2.5-flash",
                messages=[
                    {"role": "system", "content": f"You are an expert HR advisor specializing in {context}. Provide practical, actionable advice that complies with local regulations and best practices."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            response_text = response.choices[0].message.content
            
        except Exception as e:
            # Fallback to mock response if OpenAI fails
            response_text = f"HR Advisor response for {country}: {prompt[:50]}... [OpenAI integration error: {str(e)}. This is a mock response.]"
        
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
            'prompt_id': prompt_history.prompt_id
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
            hire_date=datetime.strptime(data['hire_date'], '%Y-%m-%d').date() if data.get('hire_date') else None,
            salary=float(data['salary']) if data.get('salary') else None,
            status=data.get('status', 'active'),
            address=data.get('address'),
            emergency_contact=data.get('emergency_contact'),
            emergency_phone=data.get('emergency_phone')
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
        if data.get('hire_date'):
            employee.hire_date = datetime.strptime(data['hire_date'], '%Y-%m-%d').date()
        if 'salary' in data:
            employee.salary = float(data['salary']) if data['salary'] else None
        if 'status' in data:
            employee.status = data['status']
        if 'address' in data:
            employee.address = data['address']
        if 'emergency_contact' in data:
            employee.emergency_contact = data['emergency_contact']
        if 'emergency_phone' in data:
            employee.emergency_phone = data['emergency_phone']
        
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


