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
