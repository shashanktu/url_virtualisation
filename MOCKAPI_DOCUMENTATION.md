# Service Virtualization - MockAPI Documentation

## Overview
This project provides a service virtualization solution that routes API requests to either actual URLs or mock APIs based on a virtualization flag. The system validates APIs, creates mocks, and manages them through a centralized portal.

---

## MockAPI URLs

### Base URL
```
https://r1j4l.wiremockapi.cloud/
```

### WireMock API Management URL
```
https://api.wiremock.cloud/v1/mock-apis/r1j4l/mappings
```

### Authentication
- **Username**: `pshmockapi`
- **Password**: `mock@api123`
- **Authorization Token**: `wmcp_7l0od_a86e9838fdc8c8a48bdb0d95d3c706c9_b2437e2f`

---

## Core Functionality

### 1. API Validation & Mock Creation
**File**: `Service_Virtualization.py`

#### Process Flow:
1. **Configure Request**: User enters API details (URL, method, headers, auth, body, params)
2. **Validate**: System hits the actual API endpoint and captures the response
3. **Create Mock**: After validation, user clicks "Mock API" to create a mock endpoint

#### Features:
- **HTTP Methods Supported**: GET, POST, PUT, DELETE, PATCH
- **Authentication Types**: Bearer Token, Basic Auth, API Key
- **Body Types**: JSON, Form Data, Raw Text
- **Request Configuration**:
  - Custom headers
  - Query parameters
  - Authorization
  - Request body
  - API metadata (Environment, LOB)

#### Mock Creation:
```python
# Mock endpoint format
mock_endpoint = f"{base_url}service-virtualisation{original_path}"

# Example:
# Original: https://api.example.com/users/123
# Mock: https://r1j4l.wiremockapi.cloud/service-virtualisation/users/123
```

### 2. Routing Algorithm
**Concept**: The system provides a routing mechanism that directs requests to either:
- **Actual URL**: When virtualization is disabled
- **Mock URL**: When virtualization is enabled

**Implementation**:
- Routing URLs are stored in the database
- Each API mapping contains both original_url and mock_url
- The routing decision is based on the virtualization flag
- Client receives the appropriate URL based on configuration

### 3. Database Management
**File**: `sql.py`

#### Database Schema (wiremock table):
```sql
- id: SERIAL PRIMARY KEY
- routing_url: TEXT NOT NULL
- original_url: TEXT (nullable)
- operation: VARCHAR(50) (nullable)
- api_details: TEXT
- mock_url: TEXT (nullable)
- wiremock_id: VARCHAR(100)
- lob: VARCHAR(100)
- environment: VARCHAR(50)
- headers: TEXT (JSON)
- parameters: TEXT (JSON)
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

#### Key Functions:
- `insert_wiremock_data()`: Store new API mappings
- `get_wiremock_data()`: Retrieve API mappings
- `update_wiremock_by_routing_url()`: Update existing mappings
- `delete_record()`: Soft delete mock mappings
- `get_routing_url()`: Fetch all routing URLs

### 4. Mock API Management
**File**: `wiremock.py`

#### Operations:
- **Update Mock**: `update_wiremock(wiremock_id, url, response)`
  - Updates existing mock with new response data
  - Preserves authentication and path structure

- **Delete Mock**: `delete_wiremock_data(id)`
  - Removes mock from WireMock cloud
  - Updates database record status
  - Soft delete approach (marks as deleted)

### 5. API Data Portal
**File**: `pages/Routing_Portal.py`

#### Features:
- **View All Mocks**: Display all registered mock APIs in table format
- **Mock Details**:
  - ID, Method, Original URL, Mock URL
  - WireMock ID, LOB, Environment
  - Creation timestamp
- **Actions**:
  - View mock endpoint (opens in browser with auth)
  - Delete mock (removes from WireMock and updates DB)
- **Real-time Updates**: Auto-refresh after delete operations

### 6. Automated Health Check & Sync
**File**: `scheduler.py`

#### Functionality:
- **Scheduled Execution**: Runs every configurable interval (default: 2 minutes)
- **Health Check Process**:
  1. Fetches all records from database
  2. Hits original URLs with stored headers/parameters
  3. Captures fresh responses
  4. Updates mock APIs with new response data
  5. Updates database timestamps

#### Benefits:
- Keeps mocks synchronized with actual APIs
- Automatic response updates
- Monitors API availability
- Logs all operations for audit

---

## API Workflow

### Creating a Mock API:
```
1. User enters API details in Service Virtualization page
   ↓
2. User clicks "Validate" button
   ↓
3. System hits actual API and stores response
   ↓
4. User clicks "Mock API" button
   ↓
5. System creates WireMock mapping with:
   - Path: /service-virtualisation{original_path}
   - Auth: Basic Auth (pshmockapi/mock@api123)
   - Response: Validated response body
   ↓
6. System stores mapping in database with:
   - Routing URL
   - Original URL
   - Mock URL
   - WireMock ID
   - Metadata (LOB, Environment, Headers, Params)
   ↓
7. Mock API is ready for use
```

### Using the Routing Algorithm:
```
1. Client requests routing URL from system
   ↓
2. System checks virtualization flag
   ↓
3. If virtualization enabled:
   - Return mock_url
   Else:
   - Return original_url
   ↓
4. Client uses provided URL for API calls
```

### Automated Sync Process:
```
1. Scheduler runs at configured interval
   ↓
2. Fetches all API mappings from database
   ↓
3. For each mapping:
   - Hits original_url with stored headers/params
   - Captures response
   - Updates WireMock mapping via API
   - Updates database timestamp
   ↓
4. Logs success/failure for each operation
```

---

## Configuration

### Database Connection:
```python
Host: ep-wandering-firefly-afii3dov-pooler.c-2.us-west-2.retooldb.com
Database: retool
User: retool
Password: npg_Wui0EmLg6xeA
SSL Mode: require
```

### WireMock Configuration:
```python
Base URL: https://r1j4l.wiremockapi.cloud/
API URL: https://api.wiremock.cloud/v1/mock-apis/r1j4l/mappings
Token: wmcp_7l0od_a86e9838fdc8c8a48bdb0d95d3c706c9_b2437e2f
```

### Scheduler Configuration:
```python
Default Interval: 2 minutes
Log File: scheduler.log
Timeout: 30 seconds per request
```

---

## Supported Features

### Line of Business (LOB):
- Policy
- Claims
- Small Business

### Environments:
- Dev
- Test
- Staging
- Prod

### HTTP Methods:
- GET
- POST
- PUT
- DELETE
- PATCH

### Authentication Types:
- None
- Bearer Token
- Basic Auth
- API Key

---

## API Endpoints Structure

### Mock API Path Format:
```
{base_url}/service-virtualisation{original_path}
```

### Examples:
```
Original: https://api.example.com/v1/users
Mock: https://r1j4l.wiremockapi.cloud/service-virtualisation/v1/users

Original: https://api.example.com/orders?status=active
Mock: https://r1j4l.wiremockapi.cloud/service-virtualisation/orders?status=active
```

---

## Key Benefits

1. **Service Virtualization**: Test without depending on actual services
2. **Automated Sync**: Mocks stay updated with real API responses
3. **Centralized Management**: Single portal for all mock APIs
4. **Routing Flexibility**: Easy switch between real and mock endpoints
5. **Audit Trail**: Complete logging and timestamp tracking
6. **Multi-Environment Support**: Separate mocks for Dev/Test/Staging/Prod
7. **LOB Segregation**: Organize mocks by business unit

---

## Files Overview

| File | Purpose |
|------|---------|
| `Service_Virtualization.py` | Main UI for API validation and mock creation |
| `pages/Routing_Portal.py` | View and manage all mock APIs |
| `sql.py` | Database operations and schema management |
| `wiremock.py` | WireMock API integration (create, update, delete) |
| `scheduler.py` | Automated health checks and mock synchronization |
| `main.py` | Application entry point |

---

## Usage Notes

1. **Always validate before mocking**: Ensures mock has valid response data
2. **Routing URL is mandatory**: Required for routing algorithm to work
3. **Soft deletes**: Deleted mocks are marked in DB but can be tracked
4. **Automatic timestamps**: created_at and updated_at tracked automatically
5. **Scheduler runs continuously**: Keeps mocks fresh with latest responses
6. **Basic Auth required**: All mock endpoints require authentication

---

© 2026 ValueMomentum. All Rights Reserved.
