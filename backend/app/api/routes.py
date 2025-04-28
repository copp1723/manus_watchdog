"""
API routes for the Watchdog AI application.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
import uuid
import os
from typing import Optional

from app.api.models import (
    UploadResponse, 
    AnalysisRequest, 
    AnalysisResponse, 
    QuestionRequest, 
    QuestionResponse
)
from app.services.data_loader import load_csv_file
from app.services.data_cleaner import clean_data
from app.services.analyzer import analyze_data
from app.services.insight_engine import generate_insights, answer_question
from app.services.chart_generator import generate_chart
from app.core.config import settings

router = APIRouter()

# In-memory storage for uploaded files (in production, use a database)
uploads = {}


@router.post("/upload", response_model=UploadResponse)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    """
    Upload a CSV file for analysis.
    
    The file will be saved and processed, and an upload ID will be returned
    for use in subsequent analysis requests.
    """
    # Validate file type
    if not file.filename.endswith(('.csv', '.CSV')):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    # Generate unique ID for this upload
    upload_id = str(uuid.uuid4())
    
    # Create file path
    file_path = os.path.join(settings.UPLOAD_DIR, f"{upload_id}.csv")
    
    try:
        # Save file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Load and validate CSV
        df = load_csv_file(file_path)
        
        # Store metadata
        uploads[upload_id] = {
            "file_path": file_path,
            "original_filename": file.filename,
            "row_count": len(df),
            "column_count": len(df.columns),
            "processed": False
        }
        
        # Process data in background
        background_tasks.add_task(process_uploaded_file, upload_id)
        
        return UploadResponse(
            upload_id=upload_id,
            filename=file.filename,
            row_count=len(df),
            column_count=len(df.columns)
        )
    
    except Exception as e:
        # Clean up file if there was an error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


def process_uploaded_file(upload_id: str):
    """
    Process an uploaded file in the background.
    
    This includes cleaning the data and preparing it for analysis.
    """
    try:
        # Get file info
        file_info = uploads.get(upload_id)
        if not file_info:
            return
        
        # Load data
        df = load_csv_file(file_info["file_path"])
        
        # Clean data
        cleaned_df = clean_data(df)
        
        # Save processed data
        processed_path = os.path.join(settings.UPLOAD_DIR, f"{upload_id}_processed.csv")
        cleaned_df.to_csv(processed_path, index=False)
        
        # Update metadata
        uploads[upload_id]["processed"] = True
        uploads[upload_id]["processed_path"] = processed_path
    
    except Exception as e:
        # Log error but don't raise exception (background task)
        print(f"Error processing file {upload_id}: {str(e)}")


@router.post("/analyze/{upload_id}", response_model=AnalysisResponse)
async def analyze(
    upload_id: str,
    request: AnalysisRequest,
):
    """
    Analyze uploaded data based on the specified intent.
    
    Returns insights and optionally a chart URL.
    """
    # Check if upload exists
    if upload_id not in uploads:
        raise HTTPException(status_code=404, detail="Upload not found")
    
    # Get file info
    file_info = uploads[upload_id]
    
    # Check if file has been processed
    if not file_info.get("processed", False):
        raise HTTPException(status_code=400, detail="File is still being processed")
    
    try:
        # Load processed data
        df = load_csv_file(file_info["processed_path"])
        
        # Analyze data based on intent
        analysis_results = analyze_data(df, request.intent)
        
        # Generate insights
        insights = generate_insights(analysis_results, request.intent)
        
        # Generate chart if needed
        chart_url = None
        if analysis_results.get("chart_data"):
            chart_filename = f"{upload_id}_{request.intent}.png"
            chart_url = generate_chart(
                analysis_results["chart_data"],
                chart_filename,
                chart_type=analysis_results.get("chart_type", "bar")
            )
        
        return AnalysisResponse(
            insights=insights,
            chart_url=chart_url
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing data: {str(e)}")


@router.post("/question/{upload_id}", response_model=QuestionResponse)
async def ask_question(
    upload_id: str,
    request: QuestionRequest,
):
    """
    Answer a specific question about the uploaded data.
    
    Returns an answer, insights, and optionally a chart URL.
    """
    # Check if upload exists
    if upload_id not in uploads:
        raise HTTPException(status_code=404, detail="Upload not found")
    
    # Get file info
    file_info = uploads[upload_id]
    
    # Check if file has been processed
    if not file_info.get("processed", False):
        raise HTTPException(status_code=400, detail="File is still being processed")
    
    try:
        # Load processed data
        df = load_csv_file(file_info["processed_path"])
        
        # Process question and generate answer
        answer_data = answer_question(df, request.question)
        
        # Generate chart if needed
        chart_url = None
        if answer_data.get("chart_data"):
            chart_filename = f"{upload_id}_question_{uuid.uuid4().hex[:8]}.png"
            chart_url = generate_chart(
                answer_data["chart_data"],
                chart_filename,
                chart_type=answer_data.get("chart_type", "bar")
            )
        
        return QuestionResponse(
            answer=answer_data["answer"],
            insights=answer_data["insights"],
            chart_url=chart_url
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok"}
