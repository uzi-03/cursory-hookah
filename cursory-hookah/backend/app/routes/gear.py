from flask import Blueprint, jsonify, request
from app.models.gear import Gear
from app import db

gear_bp = Blueprint('gear', __name__)

@gear_bp.route('/', methods=['GET'])
def get_all_gear():
    """Get all available gear with optional filtering"""
    try:
        # Get query parameters for filtering
        category = request.args.get('category')
        brand = request.args.get('brand')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        
        # Build query
        query = Gear.query
        
        if category:
            query = query.filter(Gear.category == category)
        if brand:
            query = query.filter(Gear.brand == brand)
        if min_price is not None:
            query = query.filter(Gear.price >= min_price)
        if max_price is not None:
            query = query.filter(Gear.price <= max_price)
        
        # Execute query
        gear_list = query.all()
        
        return jsonify({
            'success': True,
            'data': [gear.to_dict() for gear in gear_list],
            'count': len(gear_list)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gear_bp.route('/<int:gear_id>', methods=['GET'])
def get_gear_by_id(gear_id):
    """Get specific gear by ID"""
    try:
        gear = Gear.query.get_or_404(gear_id)
        return jsonify({
            'success': True,
            'data': gear.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gear_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all available gear categories"""
    try:
        categories = db.session.query(Gear.category).distinct().all()
        category_list = [cat[0] for cat in categories]
        
        return jsonify({
            'success': True,
            'data': category_list
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gear_bp.route('/brands', methods=['GET'])
def get_brands():
    """Get all available brands"""
    try:
        brands = db.session.query(Gear.brand).distinct().all()
        brand_list = [brand[0] for brand in brands]
        
        return jsonify({
            'success': True,
            'data': brand_list
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 