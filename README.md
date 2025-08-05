# Adaptive Quiz Learning Platform

A comprehensive learning platform with adaptive quiz functionality, built with FastAPI backend and modern web technologies.

## 🚀 Features

- **Adaptive Learning**: Intelligent difficulty adjustment based on user performance
- **User Management**: Complete authentication and authorization system
- **Quiz System**: Dynamic quiz generation with real-time feedback
- **Progress Tracking**: Comprehensive analytics and performance monitoring
- **Admin Dashboard**: Full administrative control panel
- **RESTful API**: Well-documented API with Swagger UI

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework
- **MongoDB** - NoSQL database with Motor async driver
- **JWT** - Secure authentication
- **Pydantic** - Data validation
- **bcrypt** - Password hashing

### Frontend (Coming Soon)
- **React/Next.js** - Modern frontend framework
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework

## 📁 Project Structure

```
project-II/
├── backend/                 # FastAPI backend application
│   ├── main.py             # Application entry point
│   ├── requirements.txt    # Python dependencies
│   ├── models/             # Database models
│   ├── schemas/            # Pydantic schemas
│   ├── routes/             # API route handlers
│   ├── services/           # Business logic
│   ├── database/           # Database utilities
│   ├── utils/              # Utility functions
│   └── README.md           # Backend documentation
├── frontend/               # Frontend application (coming soon)
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- MongoDB
- Git

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd project-II
   ```

2. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Environment setup**
   ```bash
   # Create .env file in backend directory
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run the application**
   ```bash
   python main.py
   # or
   uvicorn main:app --reload
   ```

5. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 📚 API Documentation

The backend provides a comprehensive REST API with the following main endpoints:

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info

### Quiz System
- `POST /quiz/start` - Start a new quiz
- `POST /quiz/answer` - Submit answer
- `GET /quiz/history` - Quiz history
- `GET /quiz/analytics` - Performance analytics

### Question Management
- `GET /questions/` - Get questions
- `POST /questions/` - Create question (Admin)
- `PUT /questions/{id}` - Update question (Admin)

### User Management
- `GET /users/me` - User profile
- `GET /users/` - All users (Admin)
- `GET /users/{id}/stats` - User statistics

## 🔧 Configuration

Create a `.env` file in the backend directory:

```env
# Database
MONGO_URI=mongodb://localhost:27017

# JWT
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API
API_HOST=0.0.0.0
API_PORT=8000
```

## 🧪 Testing

Run the test suite:

```bash
cd backend
python -m pytest
```

## 📊 Features in Detail

### Adaptive Learning Algorithm
- Tracks user performance across topics
- Adjusts difficulty based on success rate
- Provides personalized recommendations
- Monitors learning progress over time

### Quiz System
- Dynamic question generation
- Real-time difficulty adjustment
- Comprehensive analytics
- Progress tracking

### User Management
- Role-based access control (Student, Teacher, Admin)
- Secure authentication with JWT
- Profile management
- Performance analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [API Documentation](http://localhost:8000/docs)
2. Review the backend [README.md](backend/README.md)
3. Open an issue on GitHub

## 🚧 Roadmap

- [ ] Frontend application with React/Next.js
- [ ] Real-time notifications
- [ ] Advanced analytics dashboard
- [ ] Mobile app
- [ ] Integration with external learning platforms
- [ ] AI-powered question generation

---

**Made with ❤️ for better learning experiences** 