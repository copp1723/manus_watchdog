import pytest
from fastapi.testclient import TestClient
import pandas as pd
import os
import tempfile
from app.main import app

client = TestClient(app)

@pytest.fixture
def sample_csv_file():
    """Create a sample CSV file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
        # Create a simple dataframe
        df = pd.DataFrame({
            'sales_rep_name': ['John Doe', 'Jane Smith', 'John Doe', 'Jane Smith'],
            'lead_source': ['Website', 'Referral', 'Website', 'Walk-in'],
            'vehicle_make': ['Honda', 'Toyota', 'Honda', 'Ford'],
            'vehicle_model': ['Civic', 'Camry', 'Accord', 'F-150'],
            'listing_price': [25000, 28000, 27000, 35000],
            'sold_price': [23500, 26800, 25500, 33000],
            'profit': [2000, 2500, 1800, 3000],
            'sale_date': ['2025-01-15', '2025-01-20', '2025-02-05', '2025-02-10']
        })
        
        # Save to CSV
        df.to_csv(temp.name, index=False)
        
        yield temp.name
    
    # Clean up
    os.unlink(temp.name)

def test_root_endpoint():
    """Test the root endpoint returns correct information."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["name"] == "Watchdog AI API"
    assert response.json()["status"] == "operational"

def test_upload_endpoint(sample_csv_file):
    """Test the file upload endpoint."""
    with open(sample_csv_file, 'rb') as f:
        response = client.post(
            "/v1/upload",
            files={"file": ("test.csv", f, "text/csv")}
        )
    
    assert response.status_code == 200
    assert "upload_id" in response.json()
    assert "row_count" in response.json()
    assert response.json()["row_count"] == 4
    assert response.json()["column_count"] == 8

def test_analyze_endpoint(sample_csv_file):
    """Test the analyze endpoint."""
    # First upload a file
    with open(sample_csv_file, 'rb') as f:
        upload_response = client.post(
            "/v1/upload",
            files={"file": ("test.csv", f, "text/csv")}
        )
    
    upload_id = upload_response.json()["upload_id"]
    
    # Then analyze it
    analyze_response = client.post(
        f"/v1/analyze/{upload_id}",
        json={"intent": "general_analysis"}
    )
    
    assert analyze_response.status_code == 200
    assert "insights" in analyze_response.json()
    assert len(analyze_response.json()["insights"]) > 0

def test_question_endpoint(sample_csv_file):
    """Test the question endpoint."""
    # First upload a file
    with open(sample_csv_file, 'rb') as f:
        upload_response = client.post(
            "/v1/upload",
            files={"file": ("test.csv", f, "text/csv")}
        )
    
    upload_id = upload_response.json()["upload_id"]
    
    # Then ask a question
    question_response = client.post(
        f"/v1/question/{upload_id}",
        json={"question": "Who is my top sales rep?"}
    )
    
    assert question_response.status_code == 200
    assert "answer" in question_response.json()
    assert "insights" in question_response.json()
    assert len(question_response.json()["insights"]) > 0

def test_invalid_file_upload():
    """Test uploading an invalid file type."""
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp:
        temp.write(b"This is not a CSV file")
        temp.flush()
        
        with open(temp.name, 'rb') as f:
            response = client.post(
                "/v1/upload",
                files={"file": ("test.txt", f, "text/plain")}
            )
        
        assert response.status_code == 400
        assert "Only CSV files are supported" in response.json()["detail"]
    
    # Clean up
    os.unlink(temp.name)

def test_nonexistent_upload_id():
    """Test accessing a non-existent upload ID."""
    response = client.post(
        "/v1/analyze/nonexistent-id",
        json={"intent": "general_analysis"}
    )
    
    assert response.status_code == 404
    assert "Upload not found" in response.json()["detail"]
