from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from models.user import User

user_routes = Blueprint('users', __name__, url_prefix='/api/users')


@user_routes.route('/register', methods=['POST'])
def register():
    """สร้างผู้ใช้ใหม่"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')

    if not username or not email or not password:
        return jsonify({'error': 'username, email, and password are required'}), 400

    # ตรวจสอบว่ามีผู้ใช้ซ้ำหรือไม่
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 409

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 409

    user = User(
        username=username,
        email=email,
        phone=phone,
        password_hash=generate_password_hash(password)
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'User registered successfully',
        'data': user.to_dict()
    }), 201


@user_routes.route('/login', methods=['POST'])
def login():
    """เข้าสู่ระบบ"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'username and password are required'}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify({
        'success': True,
        'message': 'Login successful',
        'data': user.to_dict()
    })


@user_routes.route('/', methods=['GET'])
def get_users():
    """ดึงรายชื่อผู้ใช้ทั้งหมด"""
    users = User.query.all()
    return jsonify({
        'success': True,
        'data': [user.to_dict() for user in users]
    })


@user_routes.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """ดึงข้อมูลผู้ใช้ตาม ID"""
    user = User.query.get_or_404(user_id)
    return jsonify({
        'success': True,
        'data': user.to_dict()
    })


@user_routes.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """อัปเดตข้อมูลผู้ใช้"""
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if data.get('email'):
        user.email = data['email']
    if data.get('phone'):
        user.phone = data['phone']
    if data.get('is_active') is not None:
        user.is_active = data['is_active']

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'User updated successfully',
        'data': user.to_dict()
    })


@user_routes.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ลบผู้ใช้"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({
        'success': True,
        'message': f'User {user_id} deleted successfully'
    })
