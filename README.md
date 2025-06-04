## URL Alias Service

URL Alias Service is a REST API service designed to convert long URLs into short, unique links. The service provides creation, management (deactivation, expiration) of short links, redirection from them to the original URLs, as well as collection of access statistics. The primary goal is to simplify working with long URLs and provide a convenient mechanism for their usage and control.

---

## Technical Specification

It is required to develop a REST API service for creating and managing short URLs using one of the popular Python web frameworks (Django DRF / Flask / FastAPI) and a relational database (Postgres / MySQL / SQLite).

### Technology Stack

- Programming Language: Python 3.10+
- Web Framework: Django (DRF) or Flask or FastAPI
- DBMS: Postgres or MySQL or SQLite
- API: REST API following REST principles
- (Optional) API Documentation: Swagger/OpenAPI (e.g., available at `/docs`)
- Authentication: Basic Auth for private endpoints
- (Optional) Makefile for deployment and running the service

### Requirements

#### Functional Requirements

- Creation of a short link that uniquely corresponds to a long URL
- Redirection from the short link to the original URL (public endpoint)
- Link management (private endpoints protected by Basic authentication):
  - Retrieval of the list of created links with filtering by activity status and optional pagination
  - Deactivation of links (without physical deletion from the database, only marking them as inactive)
- Setting an expiration period for short links (e.g., 1 day)
- Blocking access to inactive and expired links with appropriate API rejection
- (Optional) Collection and provision of access statistics for links with breakdowns by the last hour and day, sorted by popularity

#### Technical Requirements

- API implementation must comply with REST standards
- Private endpoints secured by Basic authentication
- User and password creation for authentication implemented via a separate script or built-in framework mechanisms
- Code must be high-quality and readable
- (Optional) Presence of a Makefile for automating deployment and running
- Minimal README.md with step-by-step instructions for local service launch

---

## Technology Stack Selection

### Backend Framework: FastAPI

**Why FastAPI:**
1. **High Performance** – one of the fastest Python frameworks
2. **Automatic Documentation** – generates OpenAPI/Swagger documentation from code
3. **Built-in Validation** – automatic data validation via Pydantic
4. **Asynchronous Support** – native async/await support for high load
5. **Modern Python** – utilizes type hints and modern language features

### Database: PostgreSQL

**Why PostgreSQL:**
1. **ACID Compliance** – guarantees data integrity under high load
2. **Performance** – optimized indexes for fast short URL lookups
3. **Scalability** – supports replication and sharding for load growth
4. **JSON Support** – flexible storage of click metadata and analytics
5. **Reliability** – time-tested stability for production workloads

### Web Server: Uvicorn

**Why Uvicorn:**
1. **ASGI Compatibility** – supports asynchronous FastAPI applications
2. **Performance** – built on uvloop for maximum speed
3. **Auto-reload** – convenient development with hot reload
4. **Lightweight** – minimal resource consumption
5. **Stability** – proven choice for FastAPI apps

### Containerization: Docker

**Why Docker:**
1. **Environment Isolation** – consistent operation across all platforms
2. **Deployment Simplicity** – single `docker-compose up` to start the entire stack
3. **Scalability** – easy horizontal scaling of services
4. **Dependencies** – all dependencies packaged inside the container
5. **CI/CD Ready** – standard for modern deployment pipelines

---

## Local Deployment

### Requirements

- Docker
- Docker Compose

### Step-by-step Installation

1. **Clone the repository**
    ```bash
    git clone <repository-url>
    cd <cloned-repository-dir>
    ```

2. **Configure environment variables**
 
    Copy the environment file `cp .env.example .env` and edit it:

    ```env
    # Application settings
    SECRET_KEY="your-secret-key-change-this"
    TOKEN_EXPIRE_MINUTES=1440

    # Database
    POSTGRES_DB='database'
    POSTGRES_USER='user'
    POSTGRES_PASSWORD='password'
    POSTGRES_HOST=db
    DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:5432/${POSTGRES_DB}"
    ```

3. **Start the services**
   ```bash 
   docker-compose up -d
   ```

### Verifying Operation

1. **Check service status**
   ```bash
   docker-compose ps
   ```

2. **Check API health**
   ```bash
   curl http://localhost/health
   ```

3. **API Documentation**
 
   Open in a browser: http://localhost/docs or http://localhost/redoc or http://localhost/openapi.json

### Management

- **Stop services:** `docker-compose down`
- **Restart services:** `docker-compose restart`
- **View logs:** `docker-compose logs -f`
- **View logs of a specific service:** `docker-compose logs -f app`

### Basic Usage

1. **Create a user**
   ```bash
   curl -X POST "http://localhost/api/users/" \
        -H "Content-Type: application/json" \
        -d '{"username": "admin", "password": "admin"}'
   ```

2. **Create a link**
   ```bash
   curl -X POST "http://localhost/api/links/" \
        -H "Content-Type: application/json" \
        -u "admin:admin" \
        -d '{"original_url": "https://example.com", "expires_in_days": 7}'
   ```

3. **List links**
   ```bash
   curl -X GET "http://localhost/api/links/" -u "admin:admin"
   ```
