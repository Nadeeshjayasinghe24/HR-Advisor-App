from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db
from src.models.prompt_history import PromptHistory
from datetime import datetime, timedelta

history_bp = Blueprint('history', __name__)

@history_bp.route('/prompts', methods=['GET'])
@jwt_required()
def get_prompt_history():
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        prompt_type = request.args.get('type')  # query, template, workflow
        
        query = PromptHistory.query.filter_by(user_id=user_id)
        
        if prompt_type:
            query = query.filter_by(prompt_type=prompt_type)
        
        query = query.order_by(PromptHistory.timestamp.desc())
        
        paginated = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'prompts': [prompt.to_dict() for prompt in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page,
            'per_page': per_page
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@history_bp.route('/prompts/recent', methods=['GET'])
@jwt_required()
def get_recent_prompts():
    try:
        user_id = get_jwt_identity()
        limit = request.args.get('limit', 10, type=int)
        
        prompts = PromptHistory.query.filter_by(user_id=user_id)\
            .order_by(PromptHistory.timestamp.desc())\
            .limit(limit)\
            .all()
        
        return jsonify([prompt.to_dict() for prompt in prompts])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@history_bp.route('/prompts/<prompt_id>', methods=['GET'])
@jwt_required()
def get_prompt_detail(prompt_id):
    try:
        user_id = get_jwt_identity()
        
        prompt = PromptHistory.query.filter_by(
            prompt_id=prompt_id, 
            user_id=user_id
        ).first()
        
        if not prompt:
            return jsonify({'error': 'Prompt not found'}), 404
        
        return jsonify(prompt.to_dict())
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@history_bp.route('/prompts/<prompt_id>', methods=['DELETE'])
@jwt_required()
def delete_prompt(prompt_id):
    try:
        user_id = get_jwt_identity()
        
        prompt = PromptHistory.query.filter_by(
            prompt_id=prompt_id, 
            user_id=user_id
        ).first()
        
        if not prompt:
            return jsonify({'error': 'Prompt not found'}), 404
        
        db.session.delete(prompt)
        db.session.commit()
        
        return jsonify({'message': 'Prompt deleted successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@history_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_usage_stats():
    try:
        user_id = get_jwt_identity()
        
        # Get stats for the last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        total_prompts = PromptHistory.query.filter_by(user_id=user_id).count()
        
        recent_prompts = PromptHistory.query.filter(
            PromptHistory.user_id == user_id,
            PromptHistory.timestamp >= thirty_days_ago
        ).count()
        
        total_coins_used = db.session.query(
            db.func.sum(PromptHistory.coins_consumed)
        ).filter_by(user_id=user_id).scalar() or 0
        
        recent_coins_used = db.session.query(
            db.func.sum(PromptHistory.coins_consumed)
        ).filter(
            PromptHistory.user_id == user_id,
            PromptHistory.timestamp >= thirty_days_ago
        ).scalar() or 0
        
        # Get breakdown by prompt type
        type_breakdown = db.session.query(
            PromptHistory.prompt_type,
            db.func.count(PromptHistory.prompt_id)
        ).filter_by(user_id=user_id).group_by(PromptHistory.prompt_type).all()
        
        return jsonify({
            'total_prompts': total_prompts,
            'recent_prompts': recent_prompts,
            'total_coins_used': total_coins_used,
            'recent_coins_used': recent_coins_used,
            'type_breakdown': dict(type_breakdown)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

