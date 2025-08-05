# Adaptive Quiz Learning Platform - Backend API

A comprehensive FastAPI backend for an adaptive learning platform with quiz functionality, user management, and analytics.

## Features

- **User Authentication & Authorization**: JWT-based authentication with role-based access control
- **Adaptive Quiz System**: Intelligent difficulty adjustment based on user performance
- **Question Management**: CRUD operations for quiz questions with topic and difficulty categorization
- **Progress Tracking**: Comprehensive analytics and progress monitoring
- **Admin Dashboard**: Administrative functions for managing users, questions, and viewing analytics

## Tech Stack

- **Framework**: FastAPI
- **Database**: MongoDB with Motor (async driver)
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt with passlib
- **Validation**: Pydantic with email validation

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the backend directory with the following variables:

```env
# Database Configuration
MONGO_URI=mongodb://localhost:27017

# JWT Configuration
SECRET_KEY=your-secret-key-here-make-it-long-and-secure
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

### 3. Database Setup

Ensure MongoDB is running on your system. The application will automatically create the necessary collections.

### 4. Run the Application

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Documentation

Once the server is running, you can access:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## API Endpoints

### Authentication (`/auth`)

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access token
- `GET /auth/me` - Get current user information
- `PUT /auth/me` - Update current user information

### Users (`/users`)

- `GET /users/me` - Get current user profile with statistics
- `PUT /users/me` - Update current user profile
- `GET /users/` - Get all users (Admin only)
- `GET /users/{user_id}` - Get user by ID (Admin only)
- `PUT /users/{user_id}` - Update user (Admin only)
- `DELETE /users/{user_id}` - Delete user (Admin only)
- `GET /users/{user_id}/stats` - Get user statistics (Admin only)
- `GET /users/stats/roles` - Get user count by role (Admin only)

### Questions (`/questions`)

- `POST /questions/` - Create a new question (Admin only)
- `GET /questions/` - Get questions with optional filtering
- `GET /questions/{question_id}` - Get question by ID
- `PUT /questions/{question_id}` - Update question (Admin only)
- `DELETE /questions/{question_id}` - Delete question (Admin only)
- `GET /questions/topics/list` - Get available topics
- `GET /questions/stats/overview` - Get question statistics

### Quiz (`/quiz`)

- `POST /quiz/start` - Start a new quiz with adaptive difficulty
- `POST /quiz/answer` - Submit answer for a question
- `GET /quiz/{quiz_id}/progress` - Get quiz progress
- `POST /quiz/{quiz_id}/finish` - Finish quiz and get results
- `GET /quiz/history` - Get user's quiz history
- `GET /quiz/analytics` - Get user's quiz analytics
- `GET /quiz/recommendations` - Get recommended questions for practice
- `GET /quiz/admin/all-attempts` - Get all quiz attempts (Admin only)
- `GET /quiz/admin/analytics` - Get platform analytics (Admin only)

## Usage Examples

### 1. User Registration

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "role": "student"
  }'
```

### 2. User Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john@example.com&password=securepassword123"
```

### 3. Start a Quiz

```bash
curl -X POST "http://localhost:8000/quiz/start" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "mathematics",
    "difficulty": "medium",
    "num_questions": 10
  }'
```

### 4. Submit an Answer

```bash
curl -X POST "http://localhost:8000/quiz/answer" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question_id": "question_id_here",
    "selected_option": "A",
    "time_taken": 30
  }'
```

### 5. Create a Question (Admin)

```bash
curl -X POST "http://localhost:8000/questions/" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "What is 2 + 2?",
    "option_a": "3",
    "option_b": "4",
    "option_c": "5",
    "option_d": "6",
    "correct_option": "B",
    "difficulty": "easy",
    "topic": "mathematics",
    "explanation": "Basic addition: 2 + 2 = 4"
  }'
```

## Database Schema

### Collections

1. **users** - User accounts and profiles
2. **questions** - Quiz questions with options and metadata
3. **quiz_attempts** - Quiz sessions and results
4. **user_answers** - Individual question responses

### Key Fields

- **User Roles**: student, teacher, admin
- **Question Difficulties**: easy, medium, hard
- **Topics**: Custom topics (e.g., mathematics, science, history)

## Adaptive Logic

The system implements intelligent difficulty adjustment:

- **Starting Difficulty**: Based on user's historical performance
- **Adaptive Rules**:
  - 3 consecutive correct answers → Increase difficulty
  - 2 consecutive incorrect answers → Decrease difficulty
- **Performance Tracking**: Monitors accuracy, time taken, and improvement trends

## Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Role-based access control
- Input validation with Pydantic
- CORS middleware for frontend integration

## Development

### Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── models/                 # Database models
├── schemas/               # Pydantic schemas
├── routes/                # API route handlers
├── services/              # Business logic services
├── database/              # Database connection and utilities
├── utils/                 # Utility functions
└── dependencies.py        # FastAPI dependencies
```

### Adding New Features

1. **New Endpoints**: Add to appropriate route file in `routes/`
2. **New Models**: Create in `models/` directory
3. **New Schemas**: Define in `schemas/` directory
4. **Business Logic**: Implement in `services/` directory

## Production Deployment

1. **Environment Variables**: Configure production environment variables
2. **Database**: Use production MongoDB instance
3. **Security**: Update CORS origins and JWT secret
4. **Monitoring**: Add logging and monitoring
5. **SSL**: Configure HTTPS for production

## Contributing

1. Follow the existing code structure
2. Add proper error handling
3. Include input validation
4. Write clear documentation
5. Test thoroughly before submitting

## License

This project is licensed under the MIT License. 