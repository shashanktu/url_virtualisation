# API Documentation

Complete reference for the Service Virtualization Platform's database functions and routing endpoints.

## Database Functions (sql.py)

### Connection Management

#### `connect_to_retool()`
Establishes a connection to the PostgreSQL database.

**Returns:** `psycopg2.connection` object

**Example:**
```python
from sql import connect_to_retool

conn = connect_to_retool()
# Use the connection
conn.close()
```

**Connection Details:**
- Host: Retool PostgreSQL (SSL required)
- Database: retool
- Auto-commit: Disabled (manual commit required)

---

### Table Management

#### `create_table()`
Creates the `service_virtualisation` table if it doesn't exist. Called automatically when sql.py is imported.

**Returns:** None

**Table Schema:**
```sql
CREATE TABLE service_virtualisation (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    original_url TEXT NOT NULL,
    operation VARCHAR(50),
    routing_url TEXT NOT NULL,
    headers TEXT,
    parameters TEXT,
    response JSON,
    api_details TEXT,
    lob VARCHAR(100),
    environment VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### Data Operations

#### `insert_url_data()`
Inserts a new mock API record into the database.

**Parameters:**
- `name` (str, required): Display name for the API
- `original_url` (str, required): The real API endpoint
- `routing_url` (str, required): Path for the mock API
- `description` (str, optional): Detailed description
- `operation` (str, optional): HTTP method (GET, POST, PUT, DELETE, PATCH)
- `headers` (str, optional): JSON string of request headers
- `parameters` (str, optional): JSON string of query parameters
- `response` (str, optional): The API response to mock
- `api_details` (str, optional): Additional metadata as JSON
- `lob` (str, optional): Line of Business
- `environment` (str, optional): Environment name (Dev, Test, Staging, Prod)

**Returns:** `int` - The ID of the inserted record, or `None` if failed

**Example:**
```python
from sql import insert_url_data
import json

headers = json.dumps({"Content-Type": "application/json"})
params = json.dumps({"userId": "123"})

record_id = insert_url_data(
    name="Get User Profile",
    original_url="https://api.example.com/users/123",
    routing_url="/users/123",
    description="Fetches user profile data",
    operation="GET",
    headers=headers,
    parameters=params,
    response='{"id": 123, "name": "John Doe"}',
    lob="Customer Management",
    environment="Dev"
)

print(f"Created record with ID: {record_id}")
```

---

#### `get_url_data(url_id=None)`
Retrieves mock API records from the database.

**Parameters:**
- `url_id` (int, optional): Specific record ID to retrieve. If None, returns all records.

**Returns:** `list[dict]` - List of records as dictionaries

**Dictionary Keys:**
- `id`: Record ID
- `name`: API name
- `description`: Description
- `original_url`: Real API URL
- `operation`: HTTP method
- `routing_url`: Mock API path
- `headers`: Request headers (JSON string)
- `parameters`: Query parameters (JSON string)
- `response`: Saved response data
- `api_details`: Additional metadata
- `lob`: Line of Business
- `environment`: Environment
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

**Example:**
```python
from sql import get_url_data

# Get all records
all_records = get_url_data()
for record in all_records:
    print(f"{record['name']}: {record['routing_url']}")

# Get specific record
record = get_url_data(url_id=5)
if record:
    print(f"Found: {record[0]['name']}")
```

---

#### `update_mock_data(id, updated_response)`
Updates the response data for an existing mock API.

**Parameters:**
- `id` (int, required): Record ID to update
- `updated_response` (dict/list/str, required): New response data

**Returns:** `bool` - True if successful, False otherwise

**Example:**
```python
from sql import update_mock_data

new_response = {
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com",
    "updated": True
}

success = update_mock_data(5, new_response)
if success:
    print("Mock data updated successfully")
```

**Notes:**
- Automatically converts dict/list to JSON string
- Updates the `updated_at` timestamp
- Commits changes to database

---

#### `delete_response(id)`
Removes the response data for a mock API (sets it to NULL).

**Parameters:**
- `id` (int, required): Record ID to update

**Returns:** `bool` - True if successful, False otherwise

**Example:**
```python
from sql import delete_response

success = delete_response(5)
if success:
    print("Response data deleted")
```

**Notes:**
- Does not delete the entire record, only clears the response field
- Updates the `updated_at` timestamp
- Useful for temporarily disabling a mock without losing configuration

---

## Scheduler Functions (scheduler.py)

### `hit_original_url(record)`
Tests a single API endpoint and updates its mock data.

**Parameters:**
- `record` (dict): Database record containing API configuration

**Returns:** `dict` with keys:
- `id`: Record ID
- `status_code`: HTTP status code (if successful)
- `response_time`: Response time in milliseconds (if successful)
- `success`: Boolean indicating success/failure
- `error`: Error message (if failed)

**Example:**
```python
from sql import get_url_data
from scheduler import hit_original_url

records = get_url_data()
if records:
    result = hit_original_url(records[0])
    print(f"Status: {result['status_code']}, Time: {result['response_time']}ms")
```

---

### `scheduled_health_check()`
Checks all mock APIs and updates their responses.

**Parameters:** None

**Returns:** None

**Behavior:**
- Fetches all records from database
- Calls `hit_original_url()` for each record
- Logs results to scheduler.log
- Continues on errors (doesn't crash)

**Example:**
```python
from scheduler import scheduled_health_check

# Run a manual health check
scheduled_health_check()
```

---

### `start_scheduler(interval_hours=0, interval_minutes=1)`
Starts the background scheduler service.

**Parameters:**
- `interval_hours` (int, optional): Hours between checks (default: 0)
- `interval_minutes` (int, optional): Minutes between checks (default: 1)

**Returns:** None (runs indefinitely)

**Example:**
```python
from scheduler import start_scheduler

# Check every 5 minutes
start_scheduler(interval_hours=0, interval_minutes=5)

# Check every 2 hours
start_scheduler(interval_hours=2, interval_minutes=0)
```

**Notes:**
- Runs immediately on start
- Blocks the current thread (runs forever)
- Logs all activity to scheduler.log
- Use Ctrl+C to stop

---

## Routing Endpoints

### Mock API Routing

**Base URL:** `https://routing-portal-d3id.vercel.app`

#### `GET /route`
Returns the mocked response for a given routing URL.

**Query Parameters:**
- `routing_url` (required): The routing path stored in the database

**Example Request:**
```bash
curl "https://routing-portal-d3id.vercel.app/route?routing_url=/api/users/123"
```

**Response:**
Returns the saved mock response with appropriate headers and status code.

**Example Response:**
```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com"
}
```

---

## Data Formats

### Headers Format
Stored as JSON string in database:
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer token123",
  "X-Custom-Header": "value"
}
```

### Parameters Format
Stored as JSON string in database:
```json
{
  "userId": "123",
  "includeDetails": "true",
  "format": "json"
}
```

### API Details Format
Stored as JSON string in database:
```json
{
  "environment": "Dev",
  "line_of_business": "Customer Management",
  "headers": {...},
  "parameters": {...},
  "body_type": "JSON",
  "body_data": {...},
  "auth_type": "Bearer Token",
  "original_response": "...",
  "created_timestamp": "2024-01-15T10:30:00"
}
```

---

## Error Handling

All database functions include error handling:

**Success:**
```python
result = insert_url_data(name="Test", original_url="...", routing_url="...")
if result:
    print(f"Success! ID: {result}")
```

**Failure:**
```python
result = insert_url_data(name="Test", original_url="...", routing_url="...")
if result is None:
    print("Failed to insert data")
```

**Exceptions:**
- Database connection errors are caught and logged
- Invalid JSON in headers/parameters is handled gracefully
- Network timeouts in scheduler are logged but don't crash the service

---

## Best Practices

**When Inserting Data:**
- Always provide name, original_url, and routing_url
- Use json.dumps() for headers and parameters
- Include environment and LOB for better organization

**When Updating Data:**
- Check if the record exists first
- Verify the new response is valid
- Consider the impact on dependent systems

**When Using the Scheduler:**
- Start with longer intervals (5-10 minutes) to avoid rate limiting
- Monitor scheduler.log for errors
- Ensure original APIs are accessible from the scheduler's network

**Security:**
- Don't store sensitive credentials in mock data
- Use environment variables for database credentials
- Sanitize user input before storing in database

---

## Code Examples

### Complete Mock API Creation
```python
from sql import insert_url_data
import json

# Prepare data
headers = json.dumps({
    "Content-Type": "application/json",
    "Authorization": "Bearer abc123"
})

params = json.dumps({
    "userId": "123"
})

response_data = json.dumps({
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com"
})

api_details = json.dumps({
    "environment": "Dev",
    "line_of_business": "Customer Management",
    "created_timestamp": "2024-01-15T10:30:00"
})

# Insert
record_id = insert_url_data(
    name="Get User Profile",
    description="Retrieves user profile information",
    original_url="https://api.example.com/users/123",
    operation="GET",
    routing_url="/users/123",
    headers=headers,
    parameters=params,
    response=response_data,
    api_details=api_details,
    lob="Customer Management",
    environment="Dev"
)

print(f"Created mock API with ID: {record_id}")
```

### Batch Update All Mocks
```python
from sql import get_url_data
from scheduler import hit_original_url

records = get_url_data()
results = []

for record in records:
    if record.get('original_url'):
        result = hit_original_url(record)
        results.append(result)
        print(f"Updated {record['name']}: {result['success']}")

success_count = sum(1 for r in results if r['success'])
print(f"\nUpdated {success_count}/{len(results)} mocks successfully")
```

---

## Logging

The scheduler logs to `scheduler.log` with the following format:
```
2024-01-15 10:30:00 - INFO - Starting scheduled health check...
2024-01-15 10:30:00 - INFO - Found 5 records to check
2024-01-15 10:30:01 - INFO - Record 1: GET https://api.example.com/users - Status: 200, Time: 150ms
2024-01-15 10:30:02 - ERROR - Record 2: Request failed - Connection timeout
2024-01-15 10:30:03 - INFO - Health check completed: 4/5 successful
```

**Log Levels:**
- `INFO`: Normal operations
- `WARNING`: Non-critical issues (invalid JSON, missing URLs)
- `ERROR`: Failed requests, database errors

---

**Need more help?** Check the main [README.md](README.md) for usage examples and troubleshooting.
