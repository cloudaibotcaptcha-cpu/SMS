from flask import Blueprint, request, jsonify
from models import db
from models.sms import SMS
from services.sms_service import sms_service

sms_routes = Blueprint('sms', __name__, url_prefix='/api/sms')


@sms_routes.route('/send', methods=['POST'])
def send_sms():
    """ส่ง SMS ไปยังหมายเลขที่ระบุ"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    recipient = data.get('recipient')
    message = data.get('message')

    if not recipient or not message:
        return jsonify({'error': 'recipient and message are required'}), 400

    # ส่ง SMS ผ่าน Twilio
    result = sms_service.send_sms(recipient, message)

    # บันทึกลง Database
    sms_record = SMS(
        recipient=recipient,
        message=message,
        status=result.get('status', 'pending'),
        twilio_sid=result.get('sid')
    )
    db.session.add(sms_record)
    db.session.commit()

    return jsonify({
        'success': result['success'],
        'message': result['message'],
        'data': sms_record.to_dict()
    }), 201 if result['success'] else 500


@sms_routes.route('/history', methods=['GET'])
def get_history():
    """ดึงประวัติ SMS ทั้งหมด"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    sms_query = SMS.query.order_by(SMS.created_at.desc())
    pagination = sms_query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'success': True,
        'data': [sms.to_dict() for sms in pagination.items],
        'pagination': {
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    })


@sms_routes.route('/stats', methods=['GET'])
def get_stats():
    """ดึงสถิติ SMS"""
    total = SMS.query.count()
    sent = SMS.query.filter_by(status='sent').count()
    failed = SMS.query.filter_by(status='failed').count()
    pending = SMS.query.filter_by(status='pending').count()

    last_sms = SMS.query.order_by(SMS.created_at.desc()).first()

    return jsonify({
        'success': True,
        'data': {
            'total': total,
            'sent': sent,
            'failed': failed,
            'pending': pending,
            'last_sms': last_sms.to_dict() if last_sms else None
        }
    })


@sms_routes.route('/<int:sms_id>', methods=['GET'])
def get_sms(sms_id):
    """ดึงข้อมูล SMS ตาม ID"""
    sms = SMS.query.get_or_404(sms_id)
    return jsonify({
        'success': True,
        'data': sms.to_dict()
    })


@sms_routes.route('/<int:sms_id>', methods=['DELETE'])
def delete_sms(sms_id):
    """ลบ SMS ตาม ID"""
    sms = SMS.query.get_or_404(sms_id)
    db.session.delete(sms)
    db.session.commit()
    return jsonify({
        'success': True,
        'message': f'SMS {sms_id} deleted successfully'
    })
