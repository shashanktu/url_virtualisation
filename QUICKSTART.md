# Quick Start Guide

Get your Service Virtualization Platform running in 5 minutes.

## Prerequisites Check

Before you start, make sure you have:
- [ ] Python 3.7+ installed (`python --version`)
- [ ] pip package manager (`pip --version`)
- [ ] Internet connection

## Installation Steps

### 1. Install Dependencies
```bash
cd url_virtualisation
pip install -r requirements.txt
```

### 2. Verify Database Connection
The database is already configured. To test it:
```bash
python -c "from sql import connect_to_retool; conn = connect_to_retool(); print('✅ Connected!'); conn.close()"
```

### 3. Start the Application
```bash
streamlit run Service_Virtualization.py
```

Your browser should open automatically to `http://localhost:8501`

## Your First Mock API in 60 Seconds

1. **Enter API Details:**
   - Name: "Test API"
   - URL: `https://jsonplaceholder.typicode.com/posts/1`
   - Method: GET

2. **Click "Validate"** - You should see a JSON response

3. **Click "Mock API"** - Your mock is now saved!

4. **Go to "Routing Portal"** (sidebar) to see your mock

## Running the Scheduler (Optional)

To keep your mocks automatically updated:

```bash
python scheduler.py
```

This will:
- Check all your mocked APIs every 2 minutes
- Update responses if they've changed
- Log everything to `scheduler.log`

## Common Commands

**Start the web app:**
```bash
streamlit run Service_Virtualization.py
```

**Start the scheduler:**
```bash
python scheduler.py
```

**Check logs:**
```bash
# Windows
type scheduler.log

# Mac/Linux
tail -f scheduler.log
```

**Test database connection:**
```bash
python sql.py
```

## Project Structure

```
url_virtualisation/
├── Service_Virtualization.py    # Main web app
├── pages/
│   └── Routing_Portal.py        # Mock API dashboard
├── scheduler.py                  # Background updater
├── sql.py                        # Database operations
├── requirements.txt              # Python dependencies
└── src/
    └── ValueMomentum_logo.png   # Logo image
```

## Troubleshooting

**Port already in use?**
```bash
streamlit run Service_Virtualization.py --server.port 8502
```

**Module not found?**
```bash
pip install -r requirements.txt --upgrade
```

**Database connection fails?**
- Check your internet connection
- Verify the credentials in `sql.py` are correct

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the API Details tab for environment and LOB settings
- Try different HTTP methods (POST, PUT, DELETE)
- Set up authentication in the Authorization tab

## Need Help?

Check the main README.md for:
- Detailed feature explanations
- Database schema
- Deployment instructions
- Troubleshooting guide

---

**Happy Mocking! 🚀**
