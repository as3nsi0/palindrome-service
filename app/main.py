from fastapi import FastAPI
from app.routes import detection

app = FastAPI(title="Palindrome Detection Service")
app.include_router(detection.router)