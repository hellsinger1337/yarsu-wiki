from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import example_router, auth, teacher, teacher_rating, comment
from app.init_db import init_db

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(example_router.router)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(teacher.router, prefix="/api", tags=["teachers"])
app.include_router(teacher_rating.router, prefix="/api", tags=["teacher_ratings"])
app.include_router(comment.router, prefix="/api", tags=["comments"])

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}