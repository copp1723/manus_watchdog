"""
Module initialization for the API package.
"""
from fastapi import APIRouter

router = APIRouter()

from app.api import routes
