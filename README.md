# Django Real-Time Chat App 

A real-time chat application built with Django Channels and WebSockets. Features include instant messaging, online user status, and a beautiful responsive interface.

## Features

### Core Functionality
- **Real-time messaging** - Instant message delivery via WebSockets
- **User authentication** - Secure login/registration system
- **Private chat rooms** - One-on-one conversations
- **Message persistence** - Chat history saved to database
- **Online status** - See who's currently active

### Modern Interface
- **Instagram-inspired design** - Clean, minimal UI
- **Split-screen layout** - User list + chat interface
- **Responsive design** - Works on desktop and mobile

### Security Features
- **User authentication** - Login required for chat access
- **Session management** - Proper logout functionality

## Tech Stack
- **Backend**: Django 4.2+, Django Channels
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **WebSockets**: Django Channels with ASGI
- **Database**: SQLite (development) 
- **Server**: Daphne (ASGI server)



<img width="1680" height="1050" alt="Screenshot 2025-09-28 at 6 25 05 PM" src="https://github.com/user-attachments/assets/fbf580be-0a72-4e38-9ed8-da65ddf3edcb" />





## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
pip
virtualenv (recommended)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/django-realtime-chat.git
cd django-realtime-chat
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install django channels daphne
```

4. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Start the server**
```bash
daphne -p 8000 chat.asgi:application
```

7. **Open your browser**
```
http://localhost:8000
```

## How to Use

### Getting Started
1. **Register** a new account or **login** with existing credentials
2. **View user list** in the left sidebar
3. **Click any user** to start a conversation
4. **Type your message** and press Enter or click Send
5. **Real-time updates** - messages appear instantly!

## Key Components Explained

### WebSocket Consumer (`consumers.py`)
Handles real-time communication:
- `connect()` - User joins chat room
- `disconnect()` - User leaves chat room  
- `receive()` - Process and broadcast messages

### Models (`models.py`)
- **ChatRoom** - Private conversations between two users
- **Message** - Individual chat messages with timestamps
- **OnlineUser** - Track which users are currently online

### Frontend JavaScript
- WebSocket connection management
- Real-time message sending/receiving
- Enter key support for sending

### HTTP Routes
```
/                    # Redirect to lobby (login required)
/login/             # User login page
/register/          # User registration page  
/logout/            # User logout (POST only)
/lobby/             # Main user list page
/chat/<user_id>/    # Start chat with specific user
/room/<room_id>/    # Chat room interface
```
