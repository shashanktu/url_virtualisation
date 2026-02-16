# Service Virtualization Platform

A powerful web-based tool for creating and managing mock APIs, designed to help development teams test their applications without relying on live external services.

## What Does This Do?

Think of this as your personal API simulator. Instead of hitting real APIs during development or testing, you can:
- Test an API once to see what it returns
- Save that response as a "mock" version
- Use the mock version whenever you need it
- Keep your mocks updated automatically with a scheduler

This is incredibly useful when:
- The real API is slow or unreliable
- You're working offline
- You want to test edge cases without affecting production data
- You need consistent responses for automated testing

## The Big Picture

The platform has three main components working together:

1. **Command Center** - A friendly web interface where you configure and test APIs
2. **Routing Portal** - A dashboard showing all your saved mock APIs
3. **Scheduler** - A background worker that keeps your mocks fresh by periodically checking the real APIs

## Getting Started

### What You'll Need

- Python 3.7 or newer
- A PostgreSQL database (we're using Retool's hosted database)
- Internet connection for testing real APIs

### Installation

1. Clone or download this project to your computer

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

3. Make sure your database credentials are set up in `sql.py` (they're already configured for the Retool database)

### Running the Application

Start the web interface:
```bash
streamlit run Service_Virtualization.py
```

The app will open in your browser at `http://localhost:8501`

To run the scheduler (keeps mocks updated):
```bash
python scheduler.py
```

## How to Use It

### Creating Your First Mock API

1. **Open the Command Center** - This is the main page when you start the app

2. **Fill in the basics:**
   - Give your API a name (like "Get User Profile")
   - Add a description so you remember what it does later
   - Choose the HTTP method (GET, POST, etc.)
   - Enter the real API URL

3. **Configure the request:**
   - **Headers tab**: Add any custom headers the API needs
   - **Authorization tab**: Set up authentication (Bearer token, API key, etc.)
   - **Body tab**: For POST/PUT requests, add the request body
   - **Params tab**: Add query parameters
   - **API Details tab**: Specify environment (Dev/Test/Prod) and line of business

4. **Test it first:**
   - Click "Validate" to test the real API
   - You'll see the response, status code, and how long it took
   - Make sure it works before creating the mock

5. **Create the mock:**
   - Once validated, click "Mock API"
   - The system saves everything to the database
   - You get a routing URL you can use instead of the real API

### Viewing Your Mocks

Navigate to the "Routing Portal" page (in the sidebar) to see:
- All your saved mock APIs in a table
- When each was created and last updated
- The routing URL for each mock
- Options to delete mocks you no longer need

### Using Your Mock APIs

Instead of calling the real API, use the routing URL:
```
https://routing-portal-d3id.vercel.app/route?routing_url=/your/api/path
```

The routing service will return the saved mock response instantly.

## Understanding the Code

### Service_Virtualization.py
The main application file. It's a Streamlit app that provides the user interface for:
- Configuring API requests with all the bells and whistles
- Testing APIs to see if they work
- Saving successful responses as mocks
- Displaying responses in a clean, readable format

Key features:
- Custom CSS for a polished look
- Tabbed interface for organizing request configuration
- Real-time API testing with response preview
- Automatic database insertion when creating mocks

### Routing_Portal.py
A separate page that shows all your saved mocks in a table format. It:
- Fetches all records from the database
- Displays them in an organized table
- Converts timestamps to IST (Indian Standard Time)
- Provides delete functionality for each record
- Shows tooltips with descriptions when you hover over names

### sql.py
The database layer that handles all PostgreSQL operations:

- `connect_to_retool()` - Establishes database connection
- `create_table()` - Sets up the service_virtualisation table if it doesn't exist
- `insert_url_data()` - Saves a new mock API to the database
- `get_url_data()` - Retrieves mock APIs (all or by ID)
- `update_mock_data()` - Updates the response for an existing mock
- `delete_response()` - Removes the response data for a mock

The database schema includes:
- Basic info (name, description)
- URLs (original and routing)
- Request details (method, headers, parameters)
- Response data
- Metadata (LOB, environment, timestamps)

### scheduler.py
A background service that keeps your mocks up-to-date:

- Runs on a configurable schedule (default: every 2 minutes)
- Fetches all mock APIs from the database
- Hits each original URL with the saved configuration
- Updates the mock response if the real API returns new data
- Logs everything for troubleshooting

The scheduler is smart about:
- Handling different HTTP methods (GET, POST, PUT, DELETE)
- Parsing JSON headers and parameters
- Timing requests to track performance
- Gracefully handling failures without crashing

## Configuration Files

### requirements.txt
Lists all Python dependencies:
- `streamlit` - Web framework for the UI
- `requests` - HTTP library for calling APIs
- `psycopg2-binary` - PostgreSQL database driver
- `pandas` - Data manipulation for displaying tables
- `schedule` - Task scheduling for the background worker

### .streamlit/config.toml
Streamlit configuration:
- Runs in headless mode (no browser auto-open)
- Disables CORS for easier deployment
- Disables XSRF protection for API testing
- Turns off usage statistics

### vercel.json
Deployment configuration for Vercel hosting:
- Specifies Python runtime
- Routes all traffic to the main app
- Enables serverless deployment

## Database Schema

The `service_virtualisation` table stores:

| Column | Type | Purpose |
|--------|------|---------|
| id | SERIAL | Unique identifier |
| name | VARCHAR(255) | Human-readable name |
| description | TEXT | Detailed description |
| original_url | TEXT | The real API endpoint |
| operation | VARCHAR(50) | HTTP method (GET, POST, etc.) |
| routing_url | TEXT | Path for the mock API |
| headers | TEXT | JSON string of request headers |
| parameters | TEXT | JSON string of query parameters |
| response | JSON | The saved API response |
| api_details | TEXT | Additional metadata |
| lob | VARCHAR(100) | Line of business |
| environment | VARCHAR(50) | Environment (Dev/Test/Prod) |
| created_at | TIMESTAMP | When the mock was created |
| updated_at | TIMESTAMP | Last update time |

## Tips and Best Practices

**Naming Your Mocks**
- Use descriptive names like "Get Customer by ID" instead of "API 1"
- Add descriptions to explain what the API does and any special considerations

**Testing Before Mocking**
- Always validate the API first to ensure it works
- Check the response to make sure it's what you expect
- Verify authentication is working correctly

**Organizing Your Mocks**
- Use the LOB (Line of Business) field to group related APIs
- Set the environment to keep Dev/Test/Prod mocks separate
- Add meaningful descriptions for complex APIs

**Keeping Mocks Fresh**
- Run the scheduler regularly to update responses
- Check the logs (scheduler.log) to see if any APIs are failing
- Delete old mocks you're no longer using

**Security Considerations**
- Don't store sensitive API keys in the mock data
- Use environment variables for credentials when possible
- Be careful about what data you save in mock responses

## Troubleshooting

**Can't connect to database**
- Check the credentials in sql.py
- Make sure your network allows connections to Retool's database
- Verify the database exists and the table is created

**API validation fails**
- Check if the URL is correct and accessible
- Verify authentication credentials are valid
- Look at the error message for specific details
- Try the API in a tool like Postman first

**Scheduler not updating mocks**
- Check scheduler.log for error messages
- Verify the original URLs are still accessible
- Make sure the scheduler process is running
- Check if the database connection is working

**Mock API returns old data**
- Run the scheduler manually to force an update
- Check when the mock was last updated in the Routing Portal
- Verify the original API is returning new data

## Deployment

The app is configured for deployment on Vercel:

1. Push your code to a Git repository
2. Connect the repository to Vercel
3. Vercel will automatically detect the configuration
4. The app will be deployed and accessible via a public URL

For the scheduler, you'll need to run it separately on a server or use a service like:
- AWS Lambda with CloudWatch Events
- Google Cloud Functions with Cloud Scheduler
- A simple VPS running the Python script

## Future Enhancements

Some ideas for extending this platform:
- Add response templating for dynamic mock data
- Support for GraphQL APIs
- Request/response history tracking
- API performance analytics
- Team collaboration features
- Import/export mock configurations
- Webhook support for real-time updates

## Support

If you run into issues:
1. Check the logs (scheduler.log for the scheduler)
2. Look at the browser console for frontend errors
3. Verify database connectivity
4. Review the configuration files

## License

This project is proprietary software owned by ValueMomentum.

---

**Built with ❤️ by the ValueMomentum Team**

*Making API testing easier, one mock at a time.*
