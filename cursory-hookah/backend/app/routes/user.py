from flask import Blueprint, jsonify, request
from app.models.user import User, UserGear
from app.models.gear import Gear
from app import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/gear', methods=['GET'])
def get_user_gear():
    """Get user's gear collection (for now, using a demo user)"""
    try:
        # For MVP, we'll use a demo user ID
        demo_user_id = 1
        
        # Get user's gear collection
        user_gear = UserGear.query.filter_by(user_id=demo_user_id).all()
        
        return jsonify({
            'success': True,
            'data': [ug.to_dict() for ug in user_gear],
            'count': len(user_gear)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@user_bp.route('/gear', methods=['POST'])
def add_gear_to_user():
    """Add gear to user's collection"""
    try:
        data = request.get_json()
        gear_id = data.get('gear_id')
        
        if not gear_id:
            return jsonify({
                'success': False,
                'error': 'gear_id is required'
            }), 400
        
        # For MVP, we'll use a demo user ID
        demo_user_id = 1
        
        # Check if gear exists
        gear = Gear.query.get(gear_id)
        if not gear:
            return jsonify({
                'success': False,
                'error': 'Gear not found'
            }), 404
        
        # Check if user already has this gear
        existing_gear = UserGear.query.filter_by(
            user_id=demo_user_id, 
            gear_id=gear_id
        ).first()
        
        if existing_gear:
            return jsonify({
                'success': False,
                'error': 'Gear already in collection'
            }), 400
        
        # Add gear to user's collection
        user_gear = UserGear(user_id=demo_user_id, gear_id=gear_id)
        db.session.add(user_gear)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': user_gear.to_dict(),
            'message': 'Gear added to collection'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@user_bp.route('/gear/<int:gear_id>', methods=['DELETE'])
def remove_gear_from_user(gear_id):
    """Remove gear from user's collection"""
    try:
        # For MVP, we'll use a demo user ID
        demo_user_id = 1
        
        # Find the user gear entry
        user_gear = UserGear.query.filter_by(
            user_id=demo_user_id, 
            gear_id=gear_id
        ).first()
        
        if not user_gear:
            return jsonify({
                'success': False,
                'error': 'Gear not found in collection'
            }), 404
        
        # Remove from collection
        db.session.delete(user_gear)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Gear removed from collection'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 