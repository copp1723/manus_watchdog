"""
API models for request and response validation.
"""
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    """Response model for file upload endpoint."""
    upload_id: str
    filename: str
    row_count: int
    column_count: int


class AnalysisRequest(BaseModel):
    """Request model for data analysis endpoint."""
    intent: str = Field(
        default="general_analysis",
        description="Analysis intent (e.g., 'sales_analysis', 'profit_analysis')"
    )


class InsightItem(BaseModel):
    """Model for a single insight item."""
    title: str
    description: Optional[str] = None
    employee: Optional[str] = None
    employeeTitle: Optional[str] = None
    amount: Optional[str] = None
    percentage: Optional[Union[str, float]] = None
    actionItems: Optional[List[str]] = None


class AnalysisResponse(BaseModel):
    """Response model for data analysis endpoint."""
    insights: List[InsightItem]
    chart_url: Optional[str] = None
    html: Optional[str] = None


class QuestionRequest(BaseModel):
    """Request model for question answering endpoint."""
    question: str


class QuestionResponse(BaseModel):
    """Response model for question answering endpoint."""
    answer: str
    insights: List[InsightItem]
    chart_url: Optional[str] = None


class ErrorResponse(BaseModel):
    """Response model for error responses."""
    detail: str
    code: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
