# Getting Started

<cite>
**Referenced Files in This Document**
- [settings.py](file://config/settings.py)
- [urls.py](file://config/urls.py)
- [manage.py](file://manage.py)
- [wsgi.py](file://config/wsgi.py)
- [asgi.py](file://config/asgi.py)
- [neo4j_docker_compose.yaml](file://docker_files/neo4j_docker_compose.yaml)
- [postgresql_docker_compose.yaml](file://docker_files/postgresql_docker_compose.yaml)
- [document_services.py](file://apps/files/services/document_services.py)
- [models.py](file://apps/users/models.py)
- [0001_initial.py](file://apps/files/migrations/0001_initial.py)
- [0002_initial.py](file://apps/files/migrations/0002_initial.py)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Environment Setup](#environment-setup)
5. [Database Configuration](#database-configuration)
6. [Initial Project Setup](#initial-project-setup)
7. [Running the Local Development Server](#running-the-local-development-server)
8. [Accessing API Endpoints](#accessing-api-endpoints)
9. [Platform-Specific Considerations](#platform-specific-considerations)
10. [Verification Steps](#verification-steps)
11. [Troubleshooting](#troubleshooting)
12. [Next Steps](#next-steps)

## Introduction
This guide helps you set up the Veritas Shield backend locally for development. It covers prerequisites, environment preparation, database configuration, project initialization, running the development server, and verifying your installation. It also includes troubleshooting tips and next steps for ongoing development.

## Prerequisites
Ensure the following before proceeding:
- Python 3.8 or newer
- PostgreSQL database
- Neo4j graph database
- Docker (for containerized databases)
- Git (recommended for version control)

Notes:
- The backend uses Django and Django REST Framework.
- JWT-based authentication is configured.
- PostgreSQL is configured as the default Django database engine.
- Neo4j is referenced in service code for AI-related pipelines.

**Section sources**
- [settings.py:75-84](file://config/settings.py#L75-L84)
- [settings.py:125-137](file://config/settings.py#L125-L137)
- [document_services.py:4-7](file://apps/files/services/document_services.py#L4-L7)

## Installation
Follow these steps to install and prepare the backend:

1. Clone the repository (if not already cloned).
2. Create a virtual environment:
   - On Unix-like systems: python3 -m venv venv && source venv/bin/activate
   - On Windows: py -m venv venv && venv\Scripts\activate
3. Install Python dependencies:
   - pip install django djangorestframework djangorestframework-simplejwt psycopg2-binary python-dotenv
   - If using Docker for databases, install docker-compose or Docker Desktop.

**Section sources**
- [manage.py:10-18](file://manage.py#L10-L18)

## Environment Setup
Set up environment variables and configuration files:

1. Configure Django settings:
   - The settings module is loaded via the manage script and WSGI/ASGI entry points.
   - Default DEBUG is enabled for development.
   - Allowed hosts include localhost and 127.0.0.1.

2. Configure REST Framework and JWT:
   - JWT authentication is enabled with JSON renderer and parser classes.
   - Access tokens expire after 60 minutes; refresh tokens after 7 days.
   - Authentication uses email as the username field.

3. Media and static assets:
   - MEDIA_URL and MEDIA_ROOT are configured for uploaded files.

4. Optional environment variables:
   - You can override defaults using environment variables (e.g., SECRET_KEY, DATABASES).
   - Place sensitive keys in a .env file and load them before running the server.

**Section sources**
- [settings.py:19](file://config/settings.py#L19)
- [settings.py:150](file://config/settings.py#L150)
- [settings.py:125-143](file://config/settings.py#L125-L143)
- [settings.py:121-123](file://config/settings.py#L121-L123)
- [wsgi.py:14](file://config/wsgi.py#L14)
- [asgi.py:14](file://config/asgi.py#L14)

## Database Configuration
The project supports two deployment modes: local databases and Docker containers.

### Option A: Local Databases
1. PostgreSQL:
   - Ensure PostgreSQL is installed and running.
   - Create a database named veritassheild and a user hamza_admin with password hamza.
   - Confirm host=localhost and port=5432 match your local setup.

2. Neo4j:
   - Install Neo4j and start the service.
   - Use the default bolt port 7687 and browser port 7474.
   - Set credentials as neo4j/Ham@za515047.

3. Django database settings:
   - The default DATABASES setting points to PostgreSQL with the above credentials.

**Section sources**
- [settings.py:75-84](file://config/settings.py#L75-L84)
- [neo4j_docker_compose.yaml:11-13](file://docker_files/neo4j_docker_compose.yaml#L11-L13)
- [postgresql_docker_compose.yaml:10-14](file://docker_files/postgresql_docker_compose.yaml#L10-L14)

### Option B: Docker Containers
1. PostgreSQL container:
   - Use the provided compose file to run a Bitnami PostgreSQL image.
   - Exposes port 5432 and persists data to volumes.
   - Sets credentials and optional performance/logging parameters.

2. Neo4j container:
   - Use the provided compose file to run Neo4j 5.x.
   - Exposes ports 7474 (browser) and 7687 (bolt).
   - Persists data/logs/import/plugins to volumes.

3. Start containers:
   - docker-compose -f docker_files/postgresql_docker_compose.yaml up -d
   - docker-compose -f docker_files/neo4j_docker_compose.yaml up -d

4. Verify connectivity:
   - Confirm PostgreSQL responds on localhost:5432.
   - Confirm Neo4j browser on http://localhost:7474 and bolt on localhost:7687.

**Section sources**
- [postgresql_docker_compose.yaml:1-56](file://docker_files/postgresql_docker_compose.yaml#L1-L56)
- [neo4j_docker_compose.yaml:1-25](file://docker_files/neo4j_docker_compose.yaml#L1-L25)

## Initial Project Setup
Complete these steps to initialize the project:

1. Apply database migrations:
   - Run python manage.py migrate to create tables for apps and users.

2. Create a superuser:
   - Run python manage.py createsuperuser to set up admin credentials.

3. Load initial data (optional):
   - Some apps include initial migrations for documents and relationships.

4. Verify models and relationships:
   - The Document model stores uploaded files and metadata.
   - The User model extends AbstractBaseUser with email as the unique identifier.

**Section sources**
- [0001_initial.py:14-27](file://apps/files/migrations/0001_initial.py#L14-L27)
- [0002_initial.py:18-23](file://apps/files/migrations/0002_initial.py#L18-L23)
- [models.py:29-46](file://apps/users/models.py#L29-L46)

## Running the Local Development Server
Start the development server:

- From the project root, run python manage.py runserver.
- The server listens on localhost by default; adjust ALLOWED_HOSTS in settings if needed.

Access the admin interface:
- Navigate to http://127.0.0.1:8000/admin using your superuser credentials.

**Section sources**
- [settings.py:150](file://config/settings.py#L150)
- [manage.py:18](file://manage.py#L18)

## Accessing API Endpoints
- The project defines URL routing in config/urls.py. Add your app URLs there to expose endpoints.
- JWT authentication is enabled; clients should include Authorization: Bearer <token> in requests.
- Default renderers return JSON responses.

Notes:
- Ensure your client sets Content-Type appropriately for JSON or multipart/form-data when uploading files.

**Section sources**
- [urls.py](file://config/urls.py)
- [settings.py:129-137](file://config/settings.py#L129-L137)
- [settings.py:125-143](file://config/settings.py#L125-L143)

## Platform-Specific Considerations
Windows:
- Use Command Prompt or PowerShell; avoid Git Bash for Python commands.
- Ensure Python and pip are added to PATH.
- For Docker, use Docker Desktop or WSL2 backend.

Unix-like (Linux/macOS):
- Use your shell’s activation script for the virtual environment.
- Install system packages for PostgreSQL development headers if needed (e.g., libpq-dev).
- For Docker, ensure docker-compose is installed and the daemon is running.

## Verification Steps
Confirm a successful setup by checking:

- Database connectivity:
  - PostgreSQL: connect to veritassheild with user hamza_admin.
  - Neo4j: access http://localhost:7474 and verify bolt://localhost:7687.

- Django migrations:
  - Run python manage.py showmigrations to list applied/unapplied migrations.

- Server startup:
  - The development server starts without errors on http://127.0.0.1:8000.

- Admin access:
  - Log in to the admin panel using the superuser account.

**Section sources**
- [settings.py:75-84](file://config/settings.py#L75-L84)
- [neo4j_docker_compose.yaml:8-10](file://docker_files/neo4j_docker_compose.yaml#L8-L10)
- [postgresql_docker_compose.yaml:39-40](file://docker_files/postgresql_docker_compose.yaml#L39-L40)
- [manage.py:18](file://manage.py#L18)

## Troubleshooting
Common issues and resolutions:

- Django import error:
  - Symptom: “Couldn’t import Django” during manage.py execution.
  - Fix: Activate your virtual environment and reinstall Django.

- Database connection failures:
  - PostgreSQL: verify host/port/credentials match settings.py and local/remote configuration.
  - Neo4j: ensure the container is running and ports are not blocked.

- Permission denied for PostgreSQL volume (Docker):
  - Bitnami images require proper volume ownership; ensure the mounted directory exists and is writable.

- CORS or host-related errors:
  - Add your domain/IP to ALLOWED_HOSTS in settings.py.

- JWT authentication issues:
  - Ensure clients send Authorization: Bearer <token>.
  - Check SIMPLE_JWT token lifetimes and header types.

**Section sources**
- [manage.py:12-17](file://manage.py#L12-L17)
- [settings.py:75-84](file://config/settings.py#L75-L84)
- [settings.py:150](file://config/settings.py#L150)
- [settings.py:125-143](file://config/settings.py#L125-L143)
- [postgresql_docker_compose.yaml:8](file://docker_files/postgresql_docker_compose.yaml#L8)

## Next Steps
- Define app-specific URLs in config/urls.py to expose API endpoints.
- Implement views and serializers for each app (authentication, analysis, clauses, files, text extractor engine, users).
- Integrate Neo4j pipelines in document services for clause classification and extraction.
- Add environment-specific settings and secrets management (e.g., .env loading).
- Set up automated testing and CI/CD pipelines.
- Deploy to a staging environment using the same settings and Docker configurations.