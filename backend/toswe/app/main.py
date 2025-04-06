from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.v1.admin import admin_router
from routes.v1.common import common_router
from routes.v1.mobile import mobile_router

app = FastAPI(
    title="E-Commerce Backend API",
    version="1.0.0"
)

# CORS Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prefix versioning
app.include_router(admin_router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(common_router, prefix="/api/v1/common", tags=["Common"])
app.include_router(mobile_router, prefix="/api/v1/mobile", tags=["Mobile"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the E-Commerce API v1"}