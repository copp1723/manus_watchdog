# Watchdog AI - Architecture Design

## System Overview

Watchdog AI is designed as a modern web application with a clean separation between frontend and backend components. The architecture follows the user's vision of simplicity and clarity, focusing on the core workflow: "Upload → Ask → Insights."

## Architecture Diagram

```
┌─────────────────┐     ┌─────────────────────────────────────┐
│                 │     │                                     │
│    Frontend     │     │               Backend               │
│  (React + Vite) │     │             (FastAPI)              │
│                 │     │                                     │
└────────┬────────┘     └─────────────────┬───────────────────┘
         │                                │
         │  HTTP/REST                     │
         │  Requests                      │
         ▼                                ▼
┌─────────────────┐     ┌─────────────────────────────────────┐
│                 │     │                                     │
│   API Gateway   │◄────┤         Data Processing             │
│                 │     │                                     │
└─────────────────┘     └─────────────────┬───────────────────┘
                                          │
                                          │
                                          ▼
                        ┌─────────────────────────────────────┐
                        │                                     │
                        │        Analysis Engine              │
                        │                                     │
                        └─────────────────┬───────────────────┘
                                          │
                                          │
                                          ▼
                        ┌─────────────────────────────────────┐
                        │                                     │
                        │      Storage (File System)          │
                        │                                     │
                        └─────────────────────────────────────┘
```

## Backend Architecture

### Technology Stack
- **Framework**: FastAPI (Python)
- **Data Processing**: Pandas, NumPy
- **Storage**: File system for uploaded files and generated charts
- **API**: RESTful endpoints

### Components

1. **API Layer**
   - File upload endpoint
   - Analysis request endpoint
   - Question answering endpoint
   - Health check endpoint

2. **Data Processing Service**
   - CSV parsing and validation
   - Data cleaning and normalization
   - Data transformation

3. **Analysis Engine**
   - Metric calculation
   - Insight generation
   - Natural language processing for question understanding
   - Chart generation

4. **Storage Service**
   - File storage management
   - Temporary data caching
   - Session management

### API Endpoints

| Endpoint | Method | Description | Request | Response |
|----------|--------|-------------|---------|----------|
| `/v1/upload` | POST | Upload CSV file | Multipart form with file | `{ "upload_id": "string" }` |
| `/v1/analyze/{upload_id}` | POST | Analyze uploaded data | `{ "intent": "string" }` | `{ "insights": [...], "chart_url": "string" }` |
| `/v1/question/{upload_id}` | POST | Answer specific question | `{ "question": "string" }` | `{ "answer": "string", "insights": [...], "chart_url": "string" }` |
| `/v1/health` | GET | Check service health | None | `{ "status": "string" }` |

## Frontend Architecture

### Technology Stack
- **Framework**: React with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **UI Components**: Custom components with Radix UI primitives
- **State Management**: React Query for API state

### Components

1. **Core Pages**
   - Home/Upload Page
   - Analysis/Chat Page

2. **UI Components**
   - File Upload Zone
   - Chat Interface
   - Insight Cards
   - Charts and Visualizations
   - Loading States and Error Handling

3. **Services**
   - API Client
   - File Upload Service
   - Question Processing Service

### State Management

- **Upload State**: Tracks file upload progress and status
- **Analysis State**: Manages analysis results and insights
- **Chat State**: Handles user questions and system responses
- **UI State**: Controls loading indicators, error messages, and UI interactions

## Data Flow

1. **File Upload Flow**
   - User selects CSV file
   - Frontend validates file format
   - File is uploaded to backend
   - Backend validates and processes file
   - Upload ID is returned to frontend

2. **Analysis Flow**
   - Frontend requests analysis with upload ID
   - Backend processes data and generates insights
   - Insights and visualizations are returned to frontend
   - Frontend displays results in Insight Cards

3. **Question Flow**
   - User enters question in chat interface
   - Question is sent to backend with upload ID
   - Backend interprets question and generates answer
   - Answer and supporting insights are returned
   - Frontend displays response with appropriate visualizations

## Error Handling

1. **Frontend Error Handling**
   - Input validation
   - Network error handling
   - Graceful degradation
   - User-friendly error messages

2. **Backend Error Handling**
   - Request validation
   - Data processing error handling
   - Detailed error responses
   - Logging for debugging

## Security Considerations

1. **File Upload Security**
   - File type validation
   - Size limits
   - Content scanning

2. **API Security**
   - Rate limiting
   - Input sanitization
   - CORS configuration

## Performance Optimization

1. **Frontend Optimization**
   - Code splitting
   - Lazy loading
   - Optimized assets

2. **Backend Optimization**
   - Efficient data processing
   - Caching where appropriate
   - Asynchronous processing for long-running tasks

## Development and Deployment

1. **Development Environment**
   - Local development setup
   - Hot reloading
   - Development tools

2. **Deployment**
   - Docker containerization
   - Environment configuration
   - Build process

This architecture is designed to be simple yet scalable, focusing on the core functionality while maintaining clean separation of concerns. The system prioritizes user experience and performance, ensuring that the "Upload → Ask → Insights" workflow is as frictionless as possible.
