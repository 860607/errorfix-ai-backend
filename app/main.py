from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.config import settings
from app.api.v1 import diagnose, search
import os

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="API universelle de diagnostic informatique par IA"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(diagnose.router, prefix="/v1")
app.include_router(search.router, prefix="/v1")

static_path = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def root():
    index = os.path.join(static_path, "index.html")
    if os.path.exists(index):
        return FileResponse(index)
    return {"app": settings.APP_NAME, "version": settings.VERSION, "status": "online"}

@app.get("/health")
async def health():
    return {"status": "healthy"}