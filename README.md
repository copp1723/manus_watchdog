# Manus Watchdog

> A comprehensive dealership analytics and insight generation platform for automotive sales data.

## 🚀 Overview

Manus Watchdog is an intelligent analytics platform designed specifically for automotive dealerships. It processes sales data to generate actionable insights and answer business questions through natural language queries. 

For a detailed overview of our vision, architecture, and capabilities, see the [Vision & Project Overview](vision_and_overview.md) document.

### Key Features

- **Data Analysis Engine**: Processes dealership sales data to extract meaningful metrics and patterns
- **Insight Generation**: Creates actionable business insights across multiple domains
- **Natural Language Q&A**: Answers business questions in plain English about dealership performance
- **Interactive Visualizations**: Presents data through charts and dynamic dashboards
- **Multi-Domain Analytics**: Covers sales, profits, personnel, marketing, and inventory

## 🏗️ Architecture

Manus Watchdog follows a modern web application architecture:

```
┌───────────────────┐      ┌───────────────────┐      ┌───────────────────┐
│                   │      │                   │      │                   │
│  Next.js Frontend │◄────►│  Backend API      │◄────►│  Analysis Engine  │
│  (React)          │      │  (Python)         │      │  (Python)         │
│                   │      │                   │      │                   │
└───────────────────┘      └───────────────────┘      └───────────────────┘
                                    ▲                          ▲
                                    │                          │
                                    ▼                          │
                           ┌───────────────────┐              │
                           │                   │              │
                           │  Database         │◄─────────────┘
                           │  (PostgreSQL)     │
                           │                   │
                           └───────────────────┘
```

### Technology Stack

- **Frontend**: Next.js 15.x, React 19, Tailwind CSS, Radix UI
- **Backend**: Python, FastAPI
- **Database**: PostgreSQL
- **Deployment**: Heroku, Cloudflare Workers
- **Data Processing**: Pandas, NumPy
- **Visualization**: Recharts

## 📊 Features in Detail

### Data Analysis

The system analyzes dealership data across multiple dimensions:

- **Sales Analysis**: Total sales, average sale price, top-selling vehicles, sales trends
- **Profit Analysis**: Total profit, profit margins, most profitable vehicles/sources
- **Rep Performance**: Sales team metrics, leaderboards, individual performance
- **Lead Source Analysis**: Marketing channel effectiveness, ROI calculations
- **Vehicle Analysis**: Make/model performance, days-to-sell metrics, inventory insights

### Insight Generation

The insight engine transforms raw data into actionable business intelligence:

- Automatically identifies key performance indicators
- Highlights top performers and underperforming areas
- Provides actionable recommendations for improvement
- Presents insights in an easily digestible format

### Question Answering

Users can ask natural language questions about their business data:

- "Who is my top sales representative by profit?"
- "What is my most profitable vehicle model?"
- "How effective are my different lead sources?"
- "What was my total sales last month?"

## 🚦 Getting Started

### Prerequisites

- Node.js 18+
- Python 3.8+
- PostgreSQL 13+
- pnpm 8+

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/copp1723/manus_watchdog.git
   cd manus_watchdog
   ```

2. Install frontend dependencies:
   ```bash
   pnpm install
   ```

3. Set up Python environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and other settings
   ```

5. Run database migrations:
   ```bash
   cd migrations
   python run_migrations.py
   ```

6. Start the development servers:
   ```bash
   # In one terminal (backend)
   cd backend
   python -m app.main

   # In another terminal (frontend)
   cd ..  # Back to root directory
   pnpm dev
   ```

7. Access the application at http://localhost:3000

### Deployment

The application can be deployed using Heroku Git:

```bash
# Make sure you're logged in to Heroku CLI
heroku login

# Create a new Heroku app if you don't have one
heroku create your-app-name

# Add PostgreSQL add-on
heroku addons:create heroku-postgresql:hobby-dev

# Set up Heroku Git remote (if not already done)
heroku git:remote -a your-app-name

# Push to Heroku
git push heroku main
```

## 📝 API Documentation

The backend API provides the following main endpoints:

- `POST /api/analyze`: Analyze a dataset and return insights
- `POST /api/question`: Answer a specific question about the data
- `GET /api/charts/{chart_type}`: Get chart data for visualization

For detailed API documentation, see the [API Reference](docs/api_reference.md).

## 🔮 Future Enhancements

The following enhancements are planned for future releases:

### Data Processing & Quality
- Data validation and cleaning
- Outlier detection
- Completeness checks
- Performance optimization through caching

### Insight Generation
- Trend analysis over time
- Comparative period-over-period analysis
- Industry benchmarking
- Predictive insights
- New analyzers for customer behavior, inventory optimization

### Question Answering
- Advanced NLP with spaCy
- Support for compound and follow-up questions
- Causal ("why") analysis
- Hypothetical scenario modeling
- Confidence scores for answers

### Technical Architecture
- Factory pattern for analyzers
- Better error handling and recovery
- Dependency injection for testing
- Comprehensive logging and monitoring

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [Pandas](https://pandas.pydata.org/) - Data analysis library
- [Next.js](https://nextjs.org/) - React framework
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework
- [Radix UI](https://www.radix-ui.com/) - UI component library
- [Recharts](https://recharts.org/) - Charting library

## Development

### Testing

Run the test suite to ensure your changes don't break existing functionality:

```bash
# Run backend tests
cd backend
python -m pytest

# Run frontend tests
cd ..
pnpm test
```

### Code Quality

Before submitting contributions, ensure your code meets the project's quality standards:

```bash
# Backend linting
cd backend
flake8 app

# Frontend linting
cd ..
pnpm lint
```

## Additional Resources

- [Vision & Project Overview](vision_and_overview.md) - Detailed project vision, technical architecture, and roadmap
- [API Reference](docs/api_reference.md) - Comprehensive API documentation
- [Development Guide](docs/development_guide.md) - Detailed guide for developers
