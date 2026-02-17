import psycopg2
import json
from datetime import datetime

def connect_to_retool():
    return psycopg2.connect(
        host="ep-wandering-firefly-afii3dov-pooler.c-2.us-west-2.retooldb.com",
        database="retool",
        user="retool",
        password="npg_Wui0EmLg6xeA",
        sslmode="require"
    )

def list_retool_tables():
    try:
        conn = connect_to_retool()
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        print(tables)
        return tables
    except Exception as e:
        print(f"❌ Error listing tables: {e}")
        if 'conn' in locals():
            if 'cursor' in locals():
                cursor.close()
            conn.close()
        return []

def create_table():
    try:
        conn = connect_to_retool()
        cursor = conn.cursor()
        # Name table as service virtualisation
        create_table_query = """
        CREATE TABLE IF NOT EXISTS service_virtualisation (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            original_url TEXT,
            operation VARCHAR(50),
            routing_url TEXT NOT NULL,
            headers TEXT,
            parameters TEXT,
            response json,
            api_details TEXT,
            lob VARCHAR(100),
            environment VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
          
        cursor.execute(create_table_query)
        conn.commit()

        cursor.close()
        conn.close()
        print("service_virtualisation table created (or already exists)")
    except Exception as e:
        print(f"❌ Error creating table: {e}")
        if 'conn' in locals():
            conn.rollback()
            if 'cursor' in locals():
                cursor.close()
            conn.close()




# create_table()


def insert_url_data(name, original_url, routing_url, description=None, operation=None, headers=None, parameters=None, response=None, api_details=None, lob=None, environment=None):
    """
    Insert data into the service_virtualisation table
    
    Args:
        name (str): Name of the URL (mandatory)
        original_url (str): The original URL (mandatory)
        routing_url (str): The routing URL (mandatory)
        description (str, optional): Description of the URL
        operation (str, optional): The HTTP operation (GET, POST, PUT, DELETE, etc.)
        headers (str, optional): JSON string containing headers
        parameters (str, optional): JSON string containing parameters
        response (str, optional): JSON string containing response
        api_details (str, optional): JSON string or text containing API details
        lob (str, optional): Line of Business
        environment (str, optional): Environment (Dev, Test, Staging, Prod)
    
    Returns:
        int: The ID of the inserted record, or None if insertion failed
    """
    try:
        conn = connect_to_retool()
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO service_virtualisation (name, description, original_url, operation, routing_url, headers, parameters, response, api_details, lob, environment)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        """

        cursor.execute(insert_query, (name, description, original_url, operation, routing_url, headers, parameters, response, api_details, lob, environment))
        inserted_id = cursor.fetchone()[0]
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"Data inserted successfully with ID: {inserted_id}")
        return inserted_id
        
    except Exception as e:
        print(f"❌ Error inserting data: {e}")
        if 'conn' in locals():
            conn.rollback()
            if 'cursor' in locals():
                cursor.close()
            conn.close()
        return None


def get_existing_data():
    try:
        conn = connect_to_retool()
        cursor = conn.cursor()

        select_query = "SELECT id, routing_url, original_url, operation, api_details, lob, environment, headers, parameters, response, created_at, updated_at, name, description FROM service_virtualisation"
        cursor.execute(select_query)
        records = cursor.fetchall()

        cursor.close()
        conn.close()

        return records

    except Exception as e:
        print(f"❌ Error retrieving data: {e}")
        if 'conn' in locals():
            if 'cursor' in locals():
                cursor.close()
            conn.close()
        return []


def get_url_data(url_id=None):
    """
    Retrieve data from the service_virtualisation table
    
    Args:
        url_id (int, optional): Specific ID to retrieve. If None, returns all records.
    
    Returns:
        list: List of dictionaries containing the service virtualisation data
    """
    try:
        conn = connect_to_retool()
        cursor = conn.cursor()

        if url_id:
            query = "SELECT id, name, description, original_url, operation, routing_url, headers, parameters, response, api_details, lob, environment, created_at, updated_at FROM service_virtualisation WHERE id = %s and original_url!= 'Not Applicable';"
            cursor.execute(query, (url_id,))
        else:
            query = "SELECT id, name, description, original_url, operation, routing_url, headers, parameters, response, api_details, lob, environment, created_at, updated_at FROM service_virtualisation WHERE original_url!= 'Not Applicable' ORDER BY created_at DESC;"
            cursor.execute(query)

        rows = cursor.fetchall()
        columns = ['id', 'name', 'description', 'original_url', 'operation', 'routing_url', 'headers', 'parameters', 'response', 'api_details', 'lob', 'environment', 'created_at', 'updated_at']
        
        result = []
        for row in rows:
            result.append(dict(zip(columns, row)))

        cursor.close()
        conn.close()
        
        return result
        
    except Exception as e:
        print(f"❌ Error retrieving data: {e}")
        if 'conn' in locals():
            cursor.close()
            conn.close()
        return []
    


def update_mock_data(id, updated_response):
    """
    Update the mock data for a specific record

    Args:
        id (int): The ID of the record to update
        updated_response: The updated response data (dict, list, or string)
    """
    try:
        conn = connect_to_retool()
        cursor = conn.cursor()

        update_query = """
        UPDATE service_virtualisation
        SET response = %s, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s;
        """
        
        # Convert to JSON string if it's a dict or list
        if isinstance(updated_response, (dict, list)):
            response_data = json.dumps(updated_response)
        else:
            response_data = updated_response

        cursor.execute(update_query, (response_data, id))
        conn.commit()

        cursor.close()
        conn.close()

        print(f"✅ Updated mock data for record ID {id}")
        return True

    except Exception as e:
        print(f" Error updating mock data: {e}")
        if 'conn' in locals():
            conn.rollback()
            cursor.close()
            conn.close()
        return False


def delete_response(id):
    """
    Delete the response data for a specific record by setting it to NULL

    Args:
        id (int): The ID of the record to update
    """
    try:
        conn = connect_to_retool()
        cursor = conn.cursor()

        update_query = """
        UPDATE service_virtualisation
        SET response = NULL, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s;
        """

        cursor.execute(update_query, (id,))
        conn.commit()

        cursor.close()
        conn.close()

        print(f" Deleted response for record ID {id}")
        return True

    except Exception as e:
        print(f" Error deleting response: {e}")
        if 'conn' in locals():
            conn.rollback()
            cursor.close()
            conn.close()
        return False


