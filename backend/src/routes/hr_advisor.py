from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User
from src.models.subscription import Subscription, CountryHRData
from src.models.prompt_history import PromptHistory
from datetime import datetime, date
from openai import OpenAI
import os

hr_advisor_bp = Blueprint('hr_advisor', __name__)

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_API_BASE')
)

def check_subscription_and_coins(user_id, coins_needed=1):
    """Check if user has valid subscription and enough coins (for free trial)"""
    subscription = Subscription.query.filter_by(user_id=user_id, status='active').first()
    
    if not subscription:
        return False, "No active subscription found"
    
    if subscription.plan_type == 'free_trial':
        # Check if coins need to be refreshed (daily refresh)
        if subscription.last_coin_refresh != date.today():
            subscription.coins_balance = 100  # Daily refresh
            subscription.last_coin_refresh = date.today()
            db.session.commit()
        
        if subscription.coins_balance < coins_needed:
            return False, f"Insufficient coins. You need {coins_needed} coins but have {subscription.coins_balance}"
        
        # Deduct coins
        subscription.coins_balance -= coins_needed
        db.session.commit()
    
    return True, subscription

def get_country_context(country_code):
    """Get country-specific HR data"""
    country_data = CountryHRData.query.filter_by(country_code=country_code.upper()).all()
    
    context = ""
    if country_data:
        context = f"Country-specific HR information for {country_code}:\n"
        for data in country_data:
            context += f"- {data.category}: {data.title}\n{data.content[:500]}...\n\n"
    
    return context

def generate_ai_response(prompt, country_context="", response_type="query"):
    """Generate AI response using OpenAI"""
    try:
        system_prompt = f"""You are an expert HR advisor specializing in country-specific labor laws and HR practices. 
        You provide accurate, practical advice for startups and companies with lean HR teams.
        
        {country_context}
        
        Always provide:
        1. Clear, actionable advice
        2. Relevant legal considerations
        3. Best practices
        4. Potential risks to consider
        
        Response type: {response_type}
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"I apologize, but I'm currently unable to process your request. Please try again later. Error: {str(e)}"

@hr_advisor_bp.route('/query', methods=['POST'])
@jwt_required()
def hr_query():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('query'):
            return jsonify({'error': 'Query is required'}), 400
        
        country = data.get('country', 'US')
        query = data['query']
        
        # Check subscription and coins
        coins_needed = len(query.split()) // 10 + 1  # Variable coin consumption based on query length
        valid, result = check_subscription_and_coins(current_user_id, coins_needed)
        
        if not valid:
            return jsonify({'error': result}), 403
        
        # Get country-specific context
        country_context = get_country_context(country)
        
        # Generate AI response
        ai_response = generate_ai_response(query, country_context, "query")
        
        # Save to prompt history
        prompt_history = PromptHistory(
            user_id=current_user_id,
            prompt_text=query,
            response_text=ai_response,
            country_context=country,
            resource_links=[],  # TODO: Add relevant resource links
            coins_consumed=coins_needed
        )
        
        db.session.add(prompt_history)
        db.session.commit()
        
        return jsonify({
            'response': ai_response,
            'country_context': country,
            'coins_consumed': coins_needed,
            'resources': []  # TODO: Add relevant resources
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@hr_advisor_bp.route('/template', methods=['POST'])
@jwt_required()
def generate_template():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        required_fields = ['type', 'country']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        template_type = data['type']
        country = data['country']
        details = data.get('details', {})
        
        # Check subscription and coins
        coins_needed = 3  # Templates cost more coins
        valid, result = check_subscription_and_coins(current_user_id, coins_needed)
        
        if not valid:
            return jsonify({'error': result}), 403
        
        # Get country-specific context
        country_context = get_country_context(country)
        
        # Create template generation prompt
        prompt = f"""Generate a professional {template_type} template for {country}. 
        
        Template details: {details}
        
        Please provide a complete, ready-to-use template that follows local laws and best practices."""
        
        # Generate AI response
        template_content = generate_ai_response(prompt, country_context, "template")
        
        # Save to prompt history
        prompt_history = PromptHistory(
            user_id=current_user_id,
            prompt_text=f"Template request: {template_type} for {country}",
            response_text=template_content,
            country_context=country,
            resource_links=[],
            coins_consumed=coins_needed
        )
        
        db.session.add(prompt_history)
        db.session.commit()
        
        return jsonify({
            'template_content': template_content,
            'template_type': template_type,
            'country_context': country,
            'coins_consumed': coins_needed
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@hr_advisor_bp.route('/workflow', methods=['POST'])
@jwt_required()
def create_workflow():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        required_fields = ['type', 'country']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        workflow_type = data['type']
        country = data['country']
        details = data.get('details', {})
        
        # Check subscription and coins
        coins_needed = 2
        valid, result = check_subscription_and_coins(current_user_id, coins_needed)
        
        if not valid:
            return jsonify({'error': result}), 403
        
        # Get country-specific context
        country_context = get_country_context(country)
        
        # Create workflow generation prompt
        prompt = f"""Create a detailed {workflow_type} workflow for a company in {country}.
        
        Workflow details: {details}
        
        Please provide:
        1. Step-by-step process
        2. Responsible parties
        3. Timeline/deadlines
        4. Required documents
        5. Legal compliance checkpoints
        
        Format as a clear, actionable workflow."""
        
        # Generate AI response
        workflow_content = generate_ai_response(prompt, country_context, "workflow")
        
        # Parse workflow into steps (simple parsing)
        workflow_steps = [step.strip() for step in workflow_content.split('\n') if step.strip() and (step.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '-', '•')))]
        
        # Save to prompt history
        prompt_history = PromptHistory(
            user_id=current_user_id,
            prompt_text=f"Workflow request: {workflow_type} for {country}",
            response_text=workflow_content,
            country_context=country,
            resource_links=[],
            coins_consumed=coins_needed
        )
        
        db.session.add(prompt_history)
        db.session.commit()
        
        return jsonify({
            'workflow_content': workflow_content,
            'workflow_steps': workflow_steps,
            'workflow_type': workflow_type,
            'country_context': country,
            'coins_consumed': coins_needed
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@hr_advisor_bp.route('/countries', methods=['GET'])
@jwt_required()
def get_supported_countries():
    """Get list of countries with available HR data"""
    try:
        countries = db.session.query(CountryHRData.country_code).distinct().all()
        country_list = [country[0] for country in countries]
        
        # Add some default countries if none in database
        if not country_list:
            country_list = ['US', 'GB', 'SG', 'AU', 'CA', 'DE', 'FR', 'IN', 'JP']
        
        return jsonify({
            'supported_countries': country_list,
            'total_countries': len(country_list)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

