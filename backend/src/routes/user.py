from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User, db
from src.models.subscription import Subscription
from src.models.prompt_history import PromptHistory

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)
        
        # Get subscription info
        subscription = Subscription.query.filter_by(user_id=current_user_id, status='active').first()
        
        profile_data = user.to_dict()
        profile_data['subscription'] = subscription.to_dict() if subscription else None
        
        return jsonify(profile_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/user/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)
        data = request.get_json()
        
        if 'username' in data:
            # Check if username is already taken by another user
            existing = User.query.filter_by(username=data['username']).first()
            if existing and existing.user_id != current_user_id:
                return jsonify({'error': 'Username already taken'}), 400
            user.username = data['username']
        
        if 'email' in data:
            # Check if email is already taken by another user
            existing = User.query.filter_by(email=data['email']).first()
            if existing and existing.user_id != current_user_id:
                return jsonify({'error': 'Email already taken'}), 400
            user.email = data['email']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/history/prompts', methods=['GET'])
@jwt_required()
def get_prompt_history():
    try:
        current_user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        prompts = PromptHistory.query.filter_by(user_id=current_user_id)\
                                   .order_by(PromptHistory.timestamp.desc())\
                                   .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'prompts': [prompt.to_dict() for prompt in prompts.items],
            'total': prompts.total,
            'pages': prompts.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/history/prompts/recent', methods=['GET'])
@jwt_required()
def get_recent_prompts():
    try:
        current_user_id = get_jwt_identity()
        
        recent_prompts = PromptHistory.query.filter_by(user_id=current_user_id)\
                                          .order_by(PromptHistory.timestamp.desc())\
                                          .limit(10).all()
        
        return jsonify([prompt.to_dict() for prompt in recent_prompts]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/subscriptions', methods=['GET'])
@jwt_required()
def get_subscription():
    try:
        current_user_id = get_jwt_identity()
        subscription = Subscription.query.filter_by(user_id=current_user_id, status='active').first()
        
        if not subscription:
            return jsonify({'error': 'No active subscription found'}), 404
        
        return jsonify(subscription.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check endpoint
@user_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200
