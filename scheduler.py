import schedule
import time
import requests
import json
import logging
from datetime import datetime
from sql import connect_to_retool, get_url_data, update_mock_data
# from wiremock import update_wiremock

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def hit_original_url(record):
    """Hit the original URL with stored headers and parameters"""
    try:
        url = record['original_url']
        operation = record.get('operation', 'GET')
        
        # Parse headers and parameters from JSON
        headers = {}
        params = {}
        
        if record.get('headers'):
            try:
                if isinstance(record['headers'], str):
                    headers = json.loads(record['headers'])
                else:
                    headers = record['headers']
            except (json.JSONDecodeError, TypeError):
                logging.warning(f"Invalid headers JSON for record {record['id']}")
        
        if record.get('parameters'):
            try:
                if isinstance(record['parameters'], str):
                    params = json.loads(record['parameters'])
                else:
                    params = record['parameters']
            except (json.JSONDecodeError, TypeError):
                logging.warning(f"Invalid parameters JSON for record {record['id']}")
        
        # Make the request
        start_time = datetime.now()
        
        if operation.upper() == 'GET':
            response = requests.get(url, headers=headers, params=params, timeout=30)
        elif operation.upper() == 'POST':
            response = requests.post(url, headers=headers, params=params, timeout=30)
        elif operation.upper() == 'PUT':
            response = requests.put(url, headers=headers, params=params, timeout=30)
        elif operation.upper() == 'DELETE':
            response = requests.delete(url, headers=headers, params=params, timeout=30)
        else:
            response = requests.get(url, headers=headers, params=params, timeout=30)
        
        end_time = datetime.now()
        response_time = (end_time - start_time).total_seconds() * 1000
        
        logging.info(f"Record {record['id']}: {operation} {url} - Status: {response.status_code}, Time: {response_time:.0f}ms")
        
        # Update mock data with new response
        try:
            updated_response = response.json()
        except:
            updated_response = response.text
            
        status = update_mock_data(record['id'], updated_response)
        
        return {
            'id': record['id'],
            'status_code': response.status_code,
            'response_time': response_time,
            'success': 200 <= response.status_code < 300
        }
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Record {record['id']}: Request failed - {str(e)}")
        return {
            'id': record['id'],
            'error': str(e),
            'success': False
        }
    except Exception as e:
        logging.error(f"Record {record['id']}: Unexpected error - {str(e)}")
        return {
            'id': record['id'],
            'error': str(e),
            'success': False
        }

def scheduled_health_check():
    """Main scheduler function to check all URLs"""
    logging.info("Starting scheduled health check...")
    
    try:
        # Get all records from database
        records = get_url_data()
        
        if not records:
            logging.info("No records found in database")
            return
        
        logging.info(f"Found {len(records)} records to check")
        
        results = []
        success_count = 0
        
        for record in records:
            if record.get('original_url'):
                result = hit_original_url(record)
                results.append(result)
                if result.get('success'):
                    success_count += 1
            else:
                logging.warning(f"Record {record['id']}: No original URL found")
        
        logging.info(f"Health check completed: {success_count}/{len(records)} successful")
        
        # Log summary
        failed_records = [r for r in results if not r.get('success')]
        if failed_records:
            logging.warning(f"Failed records: {[r['id'] for r in failed_records]}")
        
    except Exception as e:
        logging.error(f"Scheduler error: {str(e)}")

def start_scheduler(interval_hours=0, interval_minutes=1):
    """Start the scheduler with specified interval"""
    total_minutes = (interval_hours * 60) + interval_minutes
    logging.info(f"Starting scheduler with {interval_hours}h {interval_minutes}m ({total_minutes} minutes) interval")
    
    # Schedule the job
    schedule.every(total_minutes).minutes.do(scheduled_health_check)
    
    # Run immediately on start
    scheduled_health_check()
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    # Default to 1 hour interval
    start_scheduler(interval_hours=0, interval_minutes=2)