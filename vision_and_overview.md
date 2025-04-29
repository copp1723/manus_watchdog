# Manus Watchdog AI: Vision & Project Overview

## Executive Summary

Manus Watchdog AI is a pioneering dealership analytics platform that transforms raw automotive sales data into actionable business intelligence. With an intuitive interface built around simplicity and clarity, Watchdog AI empowers dealership decision-makers to extract valuable insights without requiring technical expertise.

**Our mission:** To be the simplest interface for dealership intelligence, delivering friction-free insights that drive better business decisions.

![Manus Watchdog Dashboard](docs/images/dashboard_preview.png)

---

## Product Vision

### Core Philosophy

Watchdog AI is built on three fundamental principles:

1. **Clarity Over Clutter**  
   We eliminate dashboard complexity and information overload to focus on what matters.

2. **Zero-Friction Insights**  
   Built for decision-makers, not just analysts, with minimal barriers to valuable information.

3. **Conversational Intelligence**  
   Natural language interaction replaces complex querying, making data accessible to everyone.

### The User Experience

Our streamlined workflow makes data analysis effortless:

1. **Upload** → Drop any dealership report (CSV, Excel, PDF) into the browser
2. **Ask** → Pose questions in natural language about your business
3. **Insights** → Receive clear, actionable intelligence with supporting visualizations

---

## Technical Architecture

Manus Watchdog is built on a modern, scalable technology stack:

| Layer | Technology |
|-------|------------|
| **Frontend** | React 19, Next.js 15.x, Tailwind CSS, Radix UI |
| **Backend** | Python 3.12, FastAPI |
| **Transport** | tRPC (typed API calls) |
| **Data Processing** | Pandas, Pydantic |
| **AI Integration** | LlamaIndex → OpenAI o3 |
| **Database** | PostgreSQL (via Supabase) |
| **Storage** | Supabase Buckets |
| **Authentication** | Supabase Auth (JWT) |
| **Deployment** | Heroku |
| **Observability** | Sentry, OpenTelemetry, Grafana Loki |
| **CI/CD** | GitHub Actions |

### System Architecture Diagram

```
┌───────────────────┐      ┌───────────────────┐      ┌───────────────────┐
│                   │      │                   │      │                   │
│  Next.js Frontend │◄────►│  Backend API      │◄────►│  Analysis Engine  │
│  (React)          │      │  (FastAPI)        │      │  (Python/Pandas)  │
│                   │      │                   │      │                   │
└───────────────────┘      └───────────────────┘      └───────────────────┘
                                    ▲                          ▲
                                    │                          │
                                    ▼                          │
                           ┌───────────────────┐      ┌───────────────────┐
                           │                   │      │                   │
                           │  Database         │      │  AI Model (LLM)   │
                           │  (PostgreSQL)     │      │  (OpenAI o3)      │
                           │                   │      │                   │
                           └───────────────────┘      └───────────────────┘
```

### Repository Structure

```
watchdog-core/
├── api/          # FastAPI backend code
├── ui/           # React frontend (Lovable + shadcn-ui)
├── interfaces/   # Service wrappers (Uploader, LLM, etc.)
├── infra/        # Infrastructure as Code
├── scripts/      # Utility scripts
├── tests/        # Unit & integration tests
└── .github/      # CI/CD workflows
```

---

## Core Capabilities

### Data Analysis

The system analyzes dealership data across multiple dimensions:

- **Sales Analysis**: Total sales, average sale price, top-selling vehicles, sales trends
- **Profit Analysis**: Total profit, profit margins, most profitable vehicles/sources
- **Rep Performance**: Sales team metrics, leaderboards, individual performance
- **Lead Source Analysis**: Marketing channel effectiveness, ROI calculations
- **Vehicle Analysis**: Make/model performance, days-to-sell metrics, inventory insights

### AI-Powered Insights

Watchdog transforms raw data into actionable business intelligence:

- Automatically identifies key performance indicators
- Highlights top performers and underperforming areas
- Provides contextual recommendations for business improvement
- Presents insights in a readily actionable format

### Natural Language Interaction

Ask questions in plain English to get instant answers:

- "Who is my top sales representative by profit this month?"
- "What is my most profitable vehicle model?"
- "How effective are my different lead sources?"
- "What was my total sales last quarter compared to this quarter?"

---

## Current Scope & Future Roadmap

### Current Implementation (Phase 1)

The initial release focuses on core analytics capabilities:

- **Upload Service**: Drag-and-drop CSV file intake
- **Backend API**: Data validation, cleaning, and processing
- **AI Integration**: OpenAI-powered analysis guidance
- **Insight Engine**: Python/Pandas computations
- **Frontend Interface**: Clean, conversational UI
- **Observability**: Basic error tracking and logging
- **Quality Gates**: Continuous integration checks

### Future Enhancements (Phase 2+)

Planned additions to the platform include:

- **Enhanced Data Sources**: PDF parsing, inventory data, lead data
- **Advanced Analytics**: Predictive insights, trend forecasting
- **Enriched NLP**: Compound questions, causality analysis, hypotheticals
- **Performance Optimizations**: Caching, asynchronous processing
- **Architecture Improvements**: Factory patterns, dependency injection
- **Extended Testing**: Comprehensive integration tests, QA corpus

---

## Value Proposition

Manus Watchdog AI delivers unparalleled business value through:

- **Time Efficiency**: Instant answers without complex report building
- **Democratized Insights**: Making data accessible to all stakeholders, not just analysts
- **Better Decisions**: Clear, actionable information when and where it's needed
- **Focus on Action**: Less time analyzing data, more time implementing solutions

> "Watchdog AI is a clean, fast, and smart interface for dealership data. No dashboards. No noise. Just answers."

