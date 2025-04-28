# Watchdog AI - Project Documentation

## Overview
Watchdog AI is a clean, fast, and smart interface for dealership data analysis. It follows a simple workflow:
1. **Upload** - Users upload dealership CSV files
2. **Ask** - Users ask questions in natural language
3. **Insights** - Users get valuable, tangible, and practical insights

## Project Structure
The project consists of two main components:

### Backend (Python/FastAPI)
- Data processing and analysis engine
- RESTful API for file upload, analysis, and question answering
- Comprehensive data cleaning and insight generation

### Frontend (Next.js)
- Clean, modern user interface
- Responsive design for all devices
- Simple file upload zone
- Natural language question interface
- Clear insight cards with actionable recommendations

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- pnpm (for frontend package management)

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m app.main
```

The backend server will start at http://localhost:8000

### Frontend Setup
```bash
cd frontend/watchdog-ui
pnpm install
pnpm dev
```

The frontend development server will start at http://localhost:3000

## API Documentation

### Upload Endpoint
`POST /v1/upload`
- Accepts CSV files
- Returns upload ID, filename, and data statistics

### Analysis Endpoint
`POST /v1/analyze/{upload_id}`
- Analyzes uploaded data based on specified intent
- Returns insights and optional chart URL

### Question Endpoint
`POST /v1/question/{upload_id}`
- Answers specific questions about the data
- Returns answer, insights, and optional chart URL

## Features

### Data Analysis
- Sales performance analysis
- Profit analysis
- Sales representative performance
- Lead source effectiveness
- Vehicle sales analysis

### Insights
- Clear, actionable insights
- Performance metrics
- Trend identification
- Recommendations

### Visualizations
- Automatically generated charts
- Visual representation of key metrics
- Support for various chart types

## Testing
Both backend and frontend include comprehensive test suites:

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend/watchdog-ui
pnpm test
```

## Deployment
The application can be deployed in various environments:

### Backend Deployment
- Can be deployed as a standalone FastAPI application
- Supports containerization with Docker
- Works with various WSGI servers (Uvicorn, Gunicorn)

### Frontend Deployment
- Static export for simple hosting
- Supports Vercel, Netlify, and other Next.js-compatible platforms
- Cloudflare Workers integration for edge deployment

## License
This project is proprietary and confidential.

## Contact
For support or inquiries, please contact the development team.
