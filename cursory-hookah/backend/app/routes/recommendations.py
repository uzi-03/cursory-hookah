from flask import Blueprint, jsonify, request
from app.models.gear import Gear
from app.models.user import UserGear
from app import db
from sqlalchemy import and_

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/', methods=['GET'])
def get_recommendations():
    """Get compatible gear recommendations based on user's collection"""
    try:
        # For MVP, we'll use a demo user ID
        demo_user_id = 1
        
        # Get user's current gear
        user_gear = UserGear.query.filter_by(user_id=demo_user_id).all()
        user_gear_ids = [ug.gear_id for ug in user_gear]
        
        if not user_gear_ids:
            # If user has no gear, return popular items
            recommendations = Gear.query.order_by(Gear.rating.desc()).limit(10).all()
            return jsonify({
                'success': True,
                'data': [gear.to_dict() for gear in recommendations],
                'count': len(recommendations),
                'type': 'popular'
            }), 200
        
        # Get user's gear details
        user_gear_items = Gear.query.filter(Gear.id.in_(user_gear_ids)).all()
        
        # Build compatibility tags from user's gear
        user_compatibility_tags = set()
        for gear in user_gear_items:
            if gear.compatibility_tags:
                user_compatibility_tags.update(gear.compatibility_tags)
        
        # Find compatible gear (gear that shares compatibility tags with user's gear)
        compatible_gear = []
        if user_compatibility_tags:
            # Get all gear that has any of the user's compatibility tags
            compatible_query = Gear.query.filter(
                Gear.compatibility_tags.overlap(list(user_compatibility_tags))
            ).filter(
                ~Gear.id.in_(user_gear_ids)  # Exclude gear user already has
            )
            compatible_gear = compatible_query.order_by(Gear.rating.desc()).limit(20).all()
        
        # If not enough compatible gear, add popular items from different categories
        if len(compatible_gear) < 10:
            user_categories = {gear.category for gear in user_gear_items}
            popular_gear = Gear.query.filter(
                ~Gear.id.in_(user_gear_ids)
            ).filter(
                ~Gear.category.in_(user_categories)
            ).order_by(Gear.rating.desc()).limit(10).all()
            
            compatible_gear.extend(popular_gear)
        
        # Remove duplicates and limit results
        seen_ids = set()
        unique_recommendations = []
        for gear in compatible_gear:
            if gear.id not in seen_ids and len(unique_recommendations) < 15:
                unique_recommendations.append(gear)
                seen_ids.add(gear.id)
        
        return jsonify({
            'success': True,
            'data': [gear.to_dict() for gear in unique_recommendations],
            'count': len(unique_recommendations),
            'type': 'compatible',
            'user_gear_count': len(user_gear_ids)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@recommendations_bp.route('/category/<category>', methods=['GET'])
def get_category_recommendations(category):
    """Get recommendations for a specific category based on user's gear"""
    try:
        # For MVP, we'll use a demo user ID
        demo_user_id = 1
        
        # Get user's current gear
        user_gear = UserGear.query.filter_by(user_id=demo_user_id).all()
        user_gear_ids = [ug.gear_id for ug in user_gear]
        
        # Get user's gear details
        user_gear_items = Gear.query.filter(Gear.id.in_(user_gear_ids)).all()
        
        # Build compatibility tags from user's gear
        user_compatibility_tags = set()
        for gear in user_gear_items:
            if gear.compatibility_tags:
                user_compatibility_tags.update(gear.compatibility_tags)
        
        # Find compatible gear in the specified category
        query = Gear.query.filter(Gear.category == category)
        
        if user_compatibility_tags:
            # Filter by compatibility tags
            query = query.filter(Gear.compatibility_tags.overlap(list(user_compatibility_tags)))
        
        # Exclude gear user already has
        query = query.filter(~Gear.id.in_(user_gear_ids))
        
        # Order by rating and limit results
        recommendations = query.order_by(Gear.rating.desc()).limit(10).all()
        
        return jsonify({
            'success': True,
            'data': [gear.to_dict() for gear in recommendations],
            'count': len(recommendations),
            'category': category
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 