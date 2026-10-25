"""
Combines all API routes under /api. main.py includes this one router.
"""

from fastapi import APIRouter

from app.api.routes import analysis, health, recommendations

api_router = APIRouter(prefix="/api")
api_router.include_router(health.router)
api_router.include_router(analysis.router)
api_router.include_router(recommendations.router)