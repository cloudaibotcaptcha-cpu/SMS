import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


class SMSService:
    """Service สำหรับส่ง SMS ผ่าน Twilio API"""

    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = os.getenv('TWILIO_PHONE_NUMBER', '+1234567890')
        self.client = None

        if self.account_sid and self.auth_token:
            try:
                self.client = Client(self.account_sid, self.auth_token)
            except Exception as e:
                print(f"[SMSService] Twilio client init error: {e}")

    def send_sms(self, to, body):
        """ส่ง SMS ไปยังหมายเลขที่ระบุ"""
        if not self.client:
            # Demo mode - ไม่มี Twilio credentials
            return {
                'success': True,
                'sid': 'DEMO_' + os.urandom(8).hex(),
                'status': 'sent',
                'message': 'SMS sent (demo mode - no Twilio credentials configured)'
            }

        try:
            message = self.client.messages.create(
                body=body,
                from_=self.from_number,
                to=to
            )
            return {
                'success': True,
                'sid': message.sid,
                'status': message.status,
                'message': 'SMS sent successfully'
            }
        except TwilioRestException as e:
            return {
                'success': False,
                'sid': None,
                'status': 'failed',
                'message': f'Twilio error: {e.msg}'
            }
        except Exception as e:
            return {
                'success': False,
                'sid': None,
                'status': 'failed',
                'message': f'Error: {str(e)}'
            }

    def send_otp(self, to, code):
        """ส่ง OTP code ผ่าน SMS"""
        body = f"Your OTP verification code is: {code}. Valid for 5 minutes."
        return self.send_sms(to, body)


sms_service = SMSService()
