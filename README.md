# Service Virtualization Platform

## Overview

A comprehensive web-based service virtualization platform designed to streamline API testing and development workflows. This enterprise-grade solution enables development teams to create, manage, and maintain mock API endpoints without dependency on live external services.

## Key Features

- **API Mocking & Virtualization**: Create persistent mock endpoints from real API responses
- **Automated Response Updates**: Scheduled synchronization with source APIs to maintain data freshness
- **Multi-Environment Support**: Segregate mocks across Development, Test, Staging, and Production environments
- **Comprehensive Request Configuration**: Support for headers, authentication, query parameters, and request bodies
- **Real-time API Testing**: Validate APIs before creating mocks with detailed response inspection
- **Centralized Management**: Web-based dashboard for viewing and managing all virtualized services

## Use Cases

- **Development Continuity**: Maintain productivity when external APIs are unavailable or unreliable
- **Offline Development**: Work without internet connectivity using cached API responses
- **Test Automation**: Ensure consistent, predictable responses for automated test suites
- **Edge Case Testing**: Simulate specific scenarios without affecting production systems
- **Performance Testing**: Eliminate external API latency from performance benchmarks

## Architecture

The platform consists of three core components:

### 1. Command Center (`Service_Virtualization.py`)
Web interface for API configuration, testing, and mock creation. Built with Streamlit for rapid development and intuitive user experience.

### 2. Routing Portal (`pages/Routing_Portal.py`)
Administrative dashboard displaying all virtualized services with metadata, timestamps, and management capabilities.

### 3. Scheduler (`scheduler.py`)
Background service that periodically polls source APIs and updates mock responses to maintain data accuracy.

## Technical Requirements

### System Requirements
- **Python**: 3.12 or higher
- **Database**: PostgreSQL 12+
- **Network**: Internet connectivity for API polling
- **Memory**: Minimum 2GB RAM recommended

### Dependencies
```
streamlit - Web application framework
requests - HTTP client library
psycopg2-binary - PostgreSQL database adapter
pandas - Data manipulation and analysis
schedule - Job scheduling library
```

## Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd url_virtualisation
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Configuration
Database credentials are configured in `sql.py`. The application uses a hosted PostgreSQL instance on Retool. Update connection parameters if using a different database:

```python
def connect_to_retool():
    return psycopg2.connect(
        host="your-host",
        database="your-database",
        user="your-username",
        password="your-password",
        sslmode="require"
    )
```

### 4. Initialize Database
The application automatically creates required tables on first run via `create_table()` function in `sql.py`.

## Usage

### Starting the Application

**Launch Web Interface:**
```bash
streamlit run Service_Virtualization.py
```
Access at: `http://localhost:8501`

**Start Background Scheduler:**
```bash
python scheduler.py
```

### Creating a Mock API

1. **Configure Request**
   - Enter API name and description
   - Select HTTP method (GET, POST, PUT, DELETE, PATCH)
   - Provide the source API URL

2. **Set Request Parameters**
   - **Headers Tab**: Add custom HTTP headers
   - **Authorization Tab**: Configure authentication (Bearer Token, Basic Auth, API Key)
   - **Body Tab**: Define request payload for POST/PUT operations
   - **Params Tab**: Add query string parameters
   - **API Details Tab**: Set environment and line of business

3. **Validate API**
   - Click "Validate" to test the source API
   - Review response status, headers, and body
   - Verify response time and data accuracy

4. **Create Mock**
   - Click "Mock API" after successful validation
   - System stores configuration and response in database
   - Routing URL is generated for mock endpoint access

### Accessing Mock APIs

Mock endpoints are accessible via the routing service:
```
https://routing-portal-d3id.vercel.app/route?routing_url=<your-api-path>
```

### Managing Mocks

Navigate to the Routing Portal to:
- View all virtualized services in tabular format
- Monitor creation and update timestamps
- Delete response data for specific mocks
- Access routing URLs for integration

## Database Schema

### `service_virtualisation` Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Unique record identifier |
| name | VARCHAR(255) | NOT NULL | Human-readable service name |
| description | TEXT | - | Detailed service description |
| original_url | TEXT | NOT NULL | Source API endpoint |
| operation | VARCHAR(50) | - | HTTP method |
| routing_url | TEXT | NOT NULL | Mock endpoint path |
| headers | TEXT | - | JSON-encoded request headers |
| parameters | TEXT | - | JSON-encoded query parameters |
| response | JSON | - | Cached API response |
| api_details | TEXT | - | Additional metadata |
| lob | VARCHAR(100) | - | Line of business |
| environment | VARCHAR(50) | - | Deployment environment |
| created_at | TIMESTAMP | DEFAULT NOW() | Record creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last modification timestamp |

## Core Modules

### `sql.py` - Database Layer
**Functions:**
- `connect_to_retool()`: Establishes database connection
- `create_table()`: Initializes database schema
- `insert_url_data()`: Persists new mock configuration
- `get_url_data()`: Retrieves mock records
- `update_mock_data()`: Updates cached responses
- `delete_response()`: Nullifies response data

### `scheduler.py` - Background Processor
**Capabilities:**
- Configurable polling intervals (default: 2 minutes)
- Automatic response synchronization
- Comprehensive error handling and logging
- Support for all HTTP methods
- Request timing and performance tracking

### Configuration Files

**`requirements.txt`**: Python package dependencies

**`.streamlit/config.toml`**: Streamlit server configuration
```toml
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

## Best Practices

### Naming Conventions
- Use descriptive, action-oriented names (e.g., "Get Customer Profile", "Create Order")
- Include API version in name when applicable
- Document purpose and special considerations in description field

### Security
- Avoid storing production credentials in mock configurations
- Use environment variables for sensitive data
- Regularly audit and remove unused mocks
- Implement access controls for production environments

### Maintenance
- Run scheduler continuously to maintain data freshness
- Monitor `scheduler.log` for API failures
- Periodically review and clean up obsolete mocks
- Document mock dependencies and usage

### Organization
- Leverage LOB field to group related services
- Use environment field to segregate mocks by deployment stage
- Maintain consistent naming conventions across teams

## Troubleshooting

### Database Connection Issues
- Verify credentials in `sql.py`
- Check network connectivity to database host
- Ensure PostgreSQL service is running
- Confirm SSL/TLS requirements are met

### API Validation Failures
- Verify source URL accessibility
- Check authentication credentials
- Review request headers and parameters
- Test endpoint using external tools (Postman, curl)

### Scheduler Issues
- Review `scheduler.log` for error details
- Verify source APIs are accessible
- Confirm database connectivity
- Check Python process is running

### Stale Mock Data
- Verify scheduler is running
- Check last update timestamp in Routing Portal
- Manually trigger scheduler for immediate update
- Confirm source API is returning updated data

## Deployment

### Recommended Platforms
- **Streamlit Cloud**: Native Streamlit hosting (recommended)
- **Heroku**: Full application support with worker dynos
- **Railway.app**: Simple deployment with automatic scaling
- **Render.com**: Free tier available for testing
- **AWS EC2/ECS**: Enterprise-grade infrastructure
- **Google Cloud Run**: Containerized deployment
- **Azure App Service**: Microsoft cloud platform

### Deployment Steps (Streamlit Cloud)
1. Push code to GitHub repository
2. Navigate to https://share.streamlit.io
3. Connect GitHub account and select repository
4. Configure environment variables if needed
5. Deploy application

**Note**: Vercel is not suitable for Streamlit applications due to serverless function size limitations (250MB).

## Logging

The scheduler generates detailed logs in `scheduler.log`:
- Request timestamps and durations
- HTTP status codes
- Error messages and stack traces
- Success/failure statistics

## Future Enhancements

- Response templating with dynamic data generation
- GraphQL API support
- Request/response history and versioning
- Performance analytics and monitoring dashboards
- Multi-user collaboration features
- Import/export functionality for mock configurations
- Webhook integration for real-time updates
- API contract testing and validation

## Support

For technical support:
1. Review application logs (`scheduler.log`)
2. Check browser console for frontend errors
3. Verify database connectivity
4. Consult configuration files
5. Contact ValueMomentum development team

## License

This software is proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

**Copyright © 2026 ValueMomentum. All Rights Reserved.**

---

**Developed by ValueMomentum Engineering Team**


