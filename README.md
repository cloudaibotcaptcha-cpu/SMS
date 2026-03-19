# SMS Dashboard

A complete SMS Management Dashboard with Flask backend, Twilio integration, OTP verification, and a responsive frontend.

## Features

### SMS Dashboard
- Send SMS via web form
- View SMS history with pagination
- Real-time statistics (Total, Sent, Failed, Pending)
- Delete SMS records

### OTP Verification
- Send OTP codes via SMS
- Verify OTP with attempt limits
- Auto-expiration (5 minutes)
- OTP usage statistics

### User Management
- User registration and login
- Password hashing with Werkzeug
- User CRUD operations

### Digital Clock
- Multi-timezone support
- 12/24 hour format toggle
- Add/remove timezones dynamically
- Real-time updates

### Joke Generator
- Fetch jokes from JokeAPI
- Support for single and setup/delivery formats

## Project Structure

```
SMS/
├── .env.example                 # Environment variable template
├── .gitignore                   # Git ignore rules
├── config.py                    # Flask configuration
├── requirements.txt             # Python dependencies
├── digital_clock.html           # Standalone digital clock
├── joke_generator.py            # Joke API integration
├── frontend/
│   ├── dashboard.html           # Main dashboard page
│   ├── styles.css               # Complete stylesheet
│   ├── script.js                # Dashboard JavaScript
│   └── pages/
│       └── statistics.html      # Statistics page
└── SMS/
    ├── backend/
    │   ├── app.py               # Flask application entry point
    │   ├── models/
    │   │   ├── __init__.py      # Database initialization
    │   │   ├── sms.py           # SMS model
    │   │   ├── user.py          # User model
    │   │   └── otp.py           # OTP model
    │   ├── routes/
    │   │   ├── __init__.py
    │   │   ├── sms.py           # SMS API routes
    │   │   ├── users.py         # User API routes
    │   │   └── otp.py           # OTP API routes
    │   └── services/
    │       ├── __init__.py
    │       └── sms_service.py   # Twilio SMS service
    └── digital_clock/
        ├── index.html           # Digital clock page
        └── script.js            # Clock JavaScript
```

## API Endpoints

### SMS
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/sms/send` | Send an SMS |
| GET | `/api/sms/history` | Get SMS history (paginated) |
| GET | `/api/sms/stats` | Get SMS statistics |
| GET | `/api/sms/<id>` | Get SMS by ID |
| DELETE | `/api/sms/<id>` | Delete SMS by ID |

### OTP
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/otp/send` | Send OTP code |
| POST | `/api/otp/verify` | Verify OTP code |
| GET | `/api/otp/stats` | Get OTP statistics |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/register` | Register new user |
| POST | `/api/users/login` | User login |
| GET | `/api/users/` | List all users |
| GET | `/api/users/<id>` | Get user by ID |
| PUT | `/api/users/<id>` | Update user |
| DELETE | `/api/users/<id>` | Delete user |

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/cloudaibotcaptcha-cpu/SMS.git
   cd SMS
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your Twilio credentials
   ```

4. Run the application:
   ```bash
   cd SMS/backend
   python app.py
   ```

5. Open browser at `http://localhost:5000`

## Demo Mode

The application runs in **demo mode** if Twilio credentials are not configured. SMS will be simulated with demo SIDs.

## Tech Stack

- **Backend**: Flask, Flask-SQLAlchemy, Flask-CORS
- **Database**: SQLite (default), MySQL supported
- **SMS Provider**: Twilio
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Authentication**: Werkzeug password hashing
