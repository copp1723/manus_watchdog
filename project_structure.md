# Watchdog AI - Project Structure

## Directory Structure

```
watchdog-manus/
├── backend/                  # Backend Python FastAPI application
│   ├── app/                  # Application code
│   │   ├── api/              # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── routes.py     # API route definitions
│   │   │   └── models.py     # API request/response models
│   │   ├── core/             # Core application code
│   │   │   ├── __init__.py
│   │   │   ├── config.py     # Configuration settings
│   │   │   └── security.py   # Security utilities
│   │   ├── services/         # Business logic services
│   │   │   ├── __init__.py
│   │   │   ├── data_cleaner.py  # Data cleaning utilities
│   │   │   ├── data_loader.py   # CSV loading and parsing
│   │   │   ├── analyzer.py      # Data analysis functions
│   │   │   ├── insight_engine.py # Insight generation
│   │   │   └── chart_generator.py # Visualization generation
│   │   ├── utils/            # Utility functions
│   │   │   ├── __init__.py
│   │   │   ├── file_utils.py # File handling utilities
│   │   │   └── text_utils.py # Text processing utilities
│   │   ├── __init__.py
│   │   └── main.py           # Application entry point
│   ├── tests/                # Backend tests
│   │   ├── __init__.py
│   │   ├── conftest.py       # Test configuration
│   │   ├── test_api.py       # API tests
│   │   ├── test_services.py  # Service tests
│   │   └── test_utils.py     # Utility tests
│   ├── .env.example          # Example environment variables
│   ├── requirements.txt      # Python dependencies
│   ├── requirements-dev.txt  # Development dependencies
│   └── README.md             # Backend documentation
│
├── frontend/                 # Frontend React application
│   ├── public/               # Static assets
│   │   ├── favicon.ico
│   │   └── index.html
│   ├── src/                  # Source code
│   │   ├── components/       # React components
│   │   │   ├── ui/           # UI primitives
│   │   │   │   ├── button.tsx
│   │   │   │   ├── card.tsx
│   │   │   │   ├── input.tsx
│   │   │   │   └── ...
│   │   │   ├── FileUpload.tsx  # File upload component
│   │   │   ├── Chat.tsx        # Chat interface component
│   │   │   ├── InsightCard.tsx # Insight display component
│   │   │   └── ...
│   │   ├── hooks/            # Custom React hooks
│   │   │   ├── useUpload.ts    # File upload hook
│   │   │   ├── useAnalysis.ts  # Data analysis hook
│   │   │   └── useChat.ts      # Chat interaction hook
│   │   ├── lib/              # Utility libraries
│   │   │   ├── api.ts          # API client
│   │   │   ├── utils.ts        # General utilities
│   │   │   └── types.ts        # TypeScript type definitions
│   │   ├── pages/            # Page components
│   │   │   ├── Home.tsx        # Home/upload page
│   │   │   └── Analysis.tsx    # Analysis/chat page
│   │   ├── App.tsx           # Main application component
│   │   ├── index.css         # Global styles
│   │   └── main.tsx          # Application entry point
│   ├── tests/                # Frontend tests
│   │   ├── components/       # Component tests
│   │   ├── hooks/            # Hook tests
│   │   └── utils/            # Utility tests
│   ├── .eslintrc.js          # ESLint configuration
│   ├── tailwind.config.js    # Tailwind CSS configuration
│   ├── tsconfig.json         # TypeScript configuration
│   ├── vite.config.ts        # Vite configuration
│   ├── package.json          # NPM dependencies
│   └── README.md             # Frontend documentation
│
├── scripts/                  # Build and deployment scripts
│   ├── build.sh              # Build script
│   ├── deploy.sh             # Deployment script
│   └── setup.sh              # Setup script
│
├── docs/                     # Documentation
│   ├── architecture.md       # Architecture documentation
│   ├── api.md                # API documentation
│   ├── data_analysis.md      # Data analysis documentation
│   └── user_guide.md         # User guide
│
├── .gitignore                # Git ignore file
├── README.md                 # Project overview
└── docker-compose.yml        # Docker Compose configuration
```

## Key Files and Their Purposes

### Backend

1. **app/main.py**
   - FastAPI application initialization
   - Middleware configuration
   - Route registration

2. **app/api/routes.py**
   - API endpoint definitions
   - Request handling
   - Response formatting

3. **app/services/data_loader.py**
   - CSV file parsing
   - Data validation
   - Initial data structure creation

4. **app/services/data_cleaner.py**
   - Data normalization
   - Type conversion
   - Missing value handling

5. **app/services/analyzer.py**
   - Metric calculation
   - Statistical analysis
   - Data aggregation

6. **app/services/insight_engine.py**
   - Natural language question processing
   - Insight generation
   - Response formatting

7. **app/services/chart_generator.py**
   - Visualization creation
   - Chart rendering
   - Image generation

### Frontend

1. **src/App.tsx**
   - Application routing
   - Global state management
   - Theme configuration

2. **src/components/FileUpload.tsx**
   - File selection interface
   - Upload progress tracking
   - Error handling

3. **src/components/Chat.tsx**
   - Question input interface
   - Message history display
   - Suggestion chips

4. **src/components/InsightCard.tsx**
   - Insight display
   - Data visualization embedding
   - Action item presentation

5. **src/hooks/useUpload.ts**
   - File upload state management
   - Upload API integration
   - Progress tracking

6. **src/hooks/useAnalysis.ts**
   - Analysis request management
   - Result caching
   - Error handling

7. **src/lib/api.ts**
   - API client implementation
   - Request formatting
   - Response parsing

## Development Workflow

1. **Local Development**
   - Backend: `cd backend && python -m app.main`
   - Frontend: `cd frontend && npm run dev`
   - Combined: `docker-compose up`

2. **Testing**
   - Backend: `cd backend && pytest`
   - Frontend: `cd frontend && npm test`

3. **Building**
   - Backend: Docker build
   - Frontend: `npm run build`
   - Combined: `./scripts/build.sh`

4. **Deployment**
   - Package as ZIP: `./scripts/build.sh`
   - Deploy: `./scripts/deploy.sh`

This project structure follows modern best practices for full-stack web applications, with clean separation of concerns and modular organization. The structure is designed to be intuitive and maintainable, while supporting the core "Upload → Ask → Insights" workflow of the Watchdog AI application.
