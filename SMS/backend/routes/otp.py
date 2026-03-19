import random
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from models import db
from models.otp import OTP
from services.sms_service import sms_service

otp_routes = Blueprint('otp', __name__, url_prefix='/api/otp')


def generate_otp_code(length=6):
    """สร้างรหัส OTP แบบสุ่ม"""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


@otp_routes.route('/send', methods=['POST'])
def send_otp():
    """ส่ง OTP ไปยังหมายเลขโทรศัพท์"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    phone = data.get('phone')

    if not phone:
        return jsonify({'error': 'phone is required'}), 400

    # สร้าง OTP code
    code = generate_otp_code()
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    # บันทึก OTP ลง Database
    otp = OTP(
        phone=phone,
        code=code,
        expires_at=expires_at
    )
    db.session.add(otp)
    db.session.commit()

    # ส่ง OTP ผ่าน SMS
    result = sms_service.send_otp(phone, code)

    return jsonify({
        'success': result['success'],
        'message': 'OTP sent successfully' if result['success'] else 'Failed to send OTP',
        'data': {
            'otp_id': otp.id,
            'phone': phone,
            'expires_at': expires_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    }), 201 if result['success'] else 500


@otp_routes.route('/verify', methods=['POST'])
def verify_otp():
    """ตรวจสอบ OTP code"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    phone = data.get('phone')
    code = data.get('code')

    if not phone or not code:
        return jsonify({'error': 'phone and code are required'}), 400

    # ค้นหา OTP ล่าสุดที่ยังไม่ verified
    otp = OTP.query.filter_by(
        phone=phone,
        is_verified=False
    ).order_by(OTP.created_at.desc()).first()

    if not otp:
        return jsonify({'error': 'No OTP found for this phone number'}), 404

    # ตรวจสอบว่าหมดอายุหรือไม่
    if otp.is_expired():
        return jsonify({'error': 'OTP has expired'}), 410

    # ตรวจสอบจำนวนครั้งที่พยายาม
    if otp.is_max_attempts():
        return jsonify({'error': 'Maximum verification attempts exceeded'}), 429

    # เพิ่มจำนวนครั้งที่พยายาม
    otp.attempts += 1

    # ตรวจสอบ code
    if otp.code != code:
        db.session.commit()
        remaining = otp.max_attempts - otp.attempts
        return jsonify({
            'error': 'Invalid OTP code',
            'remaining_attempts': remaining
        }), 400

    # OTP ถูกต้อง
    otp.is_verified = True
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'OTP verified successfully',
        'data': otp.to_dict()
    })


@otp_routes.route('/stats', methods=['GET'])
def otp_stats():
    """ดึงสถิติ OTP"""
    total = OTP.query.count()
    verified = OTP.query.filter_by(is_verified=True).count()
    failed = OTP.query.filter_by(is_verified=False).count()

    return jsonify({
        'success': True,
        'data': {
            'total_requests': total,
            'verified': verified,
            'failed': failed,
            'success_rate': round((verified / total * 100), 2) if total > 0 else 0
        }
    })
