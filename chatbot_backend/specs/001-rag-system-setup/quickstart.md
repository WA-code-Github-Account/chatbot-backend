# Quickstart Guide: RAG System Setup

## Prerequisites

- Python 3.11+
- PostgreSQL (Neon) account and credentials
- Qdrant Cloud account and credentials
- Groq API key
- Git

## Installation Steps

### 1. Clone the Repository
```bash
git clone <repository-url>
cd rag-system
```

### 2. Set up Virtual Environment
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your credentials
nano .env
```

Required environment variables:
- `POSTGRES_USER`: PostgreSQL username
- `POSTGRES_PASSWORD`: PostgreSQL password
- `POSTGRES_HOST`: PostgreSQL host
- `POSTGRES_PORT`: PostgreSQL port
- `POSTGRES_DB`: PostgreSQL database name
- `QDRANT_HOST`: Qdrant server URL
- `QDRANT_API_KEY`: Qdrant API key
- `GROQ_API_KEY`: Groq API key
- `SECRET_KEY`: Secret key for JWT tokens
- `ALGORITHM`: Algorithm for JWT (default: "HS256")
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiry time in minutes

### 5. Run Database Migrations
```bash
# Install Alembic if not already installed
pip install alembic

# Run the database migrations
alembic upgrade head
```

### 6. Start the Qdrant Service
If using a local Qdrant instance:
```bash
# Using Docker
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

For this project, we'll use the cloud Qdrant instance specified in your environment variables.

### 7. Initialize Vector Collections
```bash
# Run the initialization script to create required collections in Qdrant
python scripts/init_qdrant.py
```

## Running the Application

### Development Mode
```bash
# Using uvicorn
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
# Using gunicorn (for synchronous) or uvicorn with multiple workers (for async)
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Usage Examples

### Authentication
```bash
# Get an access token
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=your_username&password=your_password"
```

### Upload a Document
```bash
# Upload a PDF document
curl -X POST "http://localhost:8000/documents/upload" \
  -H "Authorization: Bearer your_access_token" \
  -F "file=@path_to_your_document.pdf" \
  -F "title=Document Title"
```

### Query the RAG System
```bash
# Submit a query
curl -X POST "http://localhost:8000/rag/query" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_access_token" \
  -d '{
    "query": "Your question here",
    "language": "en"
  }'
```

## Testing

### Running Unit Tests
```bash
# Run all tests
python -m pytest tests/unit/

# Run with coverage
python -m pytest tests/unit/ --cov=src/
```

### Running Integration Tests
```bash
# Run integration tests
python -m pytest tests/integration/
```

## Docker Deployment (Optional)

### Build the Docker Image
```bash
docker build -t rag-system .
```

### Run with Docker
```bash
docker run -d --name rag-system -p 8000:8000 \
  -v ./data:/app/data \
  --env-file .env \
  rag-system
```

## Troubleshooting

### Common Issues

1. **Database Connection Issues**:
   - Verify your PostgreSQL credentials in `.env`
   - Check that your PostgreSQL instance is accessible
   - Confirm that your IP is whitelisted in Neon console

2. **Qdrant Connection Issues**:
   - Verify QDRANT_HOST and QDRANT_API_KEY in `.env`
   - Check that your Qdrant instance is running
   - Confirm that your API key has the necessary permissions

3. **API Rate Limits**:
   - Monitor your Groq API usage
   - Implement caching if encountering rate limits
   - Consider request queuing mechanisms

4. **Memory Issues**:
   - Monitor application memory usage
   - Adjust chunk sizes if processing large documents
   - Implement proper resource cleanup

## Performance Tuning

### For High Concurrency (1000 concurrent queries):
- Adjust uvicorn worker count: `--workers 8` or more based on CPU cores
- Tune PostgreSQL connection pool: `asyncpg.create_pool(max_size=20)`
- Implement Redis caching for frequent queries
- Use CDN for static assets if applicable

### For Cost Optimization:
- Optimize embedding size and chunk length
- Implement smart caching to reduce API calls
- Use appropriate vector quantization in Qdrant
- Monitor and optimize token usage in Groq API calls