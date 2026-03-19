from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sms.db'
db = SQLAlchemy(app)

from routes.sms import sms_routes
from routes.users import user_routes
from routes.otp import otp_routes

app.register_blueprint(sms_routes)
app.register_blueprint(user_routes)
app.register_blueprint(otp_routes)

if __name__ == '__main__':
    app.run(debug=True)