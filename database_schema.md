# Watchdog AI - Database Schema

While the initial implementation will use file-based storage for simplicity, here's a database schema design that could be implemented in the future for more robust data management:

## Database Tables

### 1. Users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE
);
```

### 2. Uploads
```sql
CREATE TABLE uploads (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_size INTEGER NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    upload_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'processing',
    row_count INTEGER,
    column_count INTEGER
);
```

### 3. DataColumns
```sql
CREATE TABLE data_columns (
    id SERIAL PRIMARY KEY,
    upload_id INTEGER REFERENCES uploads(id) ON DELETE CASCADE,
    column_name VARCHAR(255) NOT NULL,
    column_type VARCHAR(50) NOT NULL,
    has_missing_values BOOLEAN DEFAULT FALSE,
    statistics JSONB,
    UNIQUE (upload_id, column_name)
);
```

### 4. Insights
```sql
CREATE TABLE insights (
    id SERIAL PRIMARY KEY,
    upload_id INTEGER REFERENCES uploads(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    insight_type VARCHAR(50) NOT NULL,
    metrics JSONB NOT NULL,
    chart_url VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### 5. Questions
```sql
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    upload_id INTEGER REFERENCES uploads(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id),
    question_text TEXT NOT NULL,
    answer_text TEXT,
    insight_id INTEGER REFERENCES insights(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### 6. Charts
```sql
CREATE TABLE charts (
    id SERIAL PRIMARY KEY,
    upload_id INTEGER REFERENCES uploads(id) ON DELETE CASCADE,
    chart_type VARCHAR(50) NOT NULL,
    chart_data JSONB NOT NULL,
    chart_options JSONB,
    file_path VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

## Relationships

- A User can have multiple Uploads
- An Upload can have multiple DataColumns
- An Upload can have multiple Insights
- An Upload can have multiple Questions
- A Question can be linked to an Insight
- An Upload can have multiple Charts

## Data Flow

1. User uploads a CSV file
2. System creates an Upload record
3. System processes the file and creates DataColumn records
4. System generates Insights and Charts
5. User asks Questions which are stored with their Answers
6. Insights and Charts are linked to Questions when relevant

## Indexing Strategy

```sql
-- Improve query performance for common operations
CREATE INDEX idx_uploads_user_id ON uploads(user_id);
CREATE INDEX idx_uploads_status ON uploads(status);
CREATE INDEX idx_data_columns_upload_id ON data_columns(upload_id);
CREATE INDEX idx_insights_upload_id ON insights(upload_id);
CREATE INDEX idx_questions_upload_id ON questions(upload_id);
CREATE INDEX idx_charts_upload_id ON charts(upload_id);
```

## Notes on Implementation

For the initial version of Watchdog AI, we'll use a file-based approach where:

1. Uploaded CSV files are stored in a designated directory
2. File metadata and processing status are tracked in memory or simple JSON files
3. Generated insights and charts are stored as files
4. Questions and answers are maintained in the session

This approach simplifies the initial implementation while still providing the core functionality. The database schema above provides a roadmap for future enhancements when more robust data persistence is required.
