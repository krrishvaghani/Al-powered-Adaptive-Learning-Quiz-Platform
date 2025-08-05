from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, quiz, user, question

# Create FastAPI app
app = FastAPI(
    title="AI-Powered Adaptive Learning & Quiz Platform",
    description="A comprehensive learning platform with adaptive quizzes, AI integration, and user management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(quiz.router, prefix="/quiz", tags=["Quiz"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(question.router, prefix="/questions", tags=["Questions"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to AI-Powered Adaptive Learning & Quiz Platform",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)