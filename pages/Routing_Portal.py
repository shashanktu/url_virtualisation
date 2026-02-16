import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import sys
import os
import base64

# Add parent directory to path to import from sql.py
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sql import get_url_data, connect_to_retool, delete_response
# from wiremock import delete_wiremock_data


# Page config
st.set_page_config(
    page_title="Update API Data - Command Center",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6C37;
        text-align: center;
        margin-bottom: 2rem;
    }
    .response-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    .response-error {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header with Logo
# col_logo, col_title = st.columns([1, 4])
# with col_logo:
#     try:
st.image("src/ValueMomentum_logo.png", width=100)
    
st.write("")

st.markdown('<div class="main-header">API Data</div>', unsafe_allow_html=True)


# Main content
st.subheader(" Mock API Database Records")

# Add refresh button

# Fetch data from database




try:
    with st.spinner("Loading data from database..."):
        url_data = get_url_data()

    if url_data:
        st.success(f"Found {len(url_data)} records in the database")

        # Convert to DataFrame for better display
        df = pd.DataFrame(url_data)

        # Format the created_at column to IST
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at']).dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata').dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Format the updated_at column to IST
        if 'updated_at' in df.columns:
            df['updated_at'] = pd.to_datetime(df['updated_at']).dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata').dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Display records as table with delete buttons
        st.subheader("All Records - Table View")
        
        # Create table headers
        header_cols = st.columns([1, 2, 1, 2, 3, 2, 2, 1, 1])
        with header_cols[0]:
            st.write("**ID**")
        with header_cols[1]:
            st.write("**Name**")
        with header_cols[2]:
            st.write("**Method**")
        with header_cols[3]:
            st.write("**Routing URL**")
        with header_cols[4]:
            st.write("**Original URL**")
        with header_cols[5]:
            st.write("**LOB**")
        with header_cols[6]:
            st.write("**Environment**")
        with header_cols[7]:
            st.write("**Created At**")
        with header_cols[8]:
            st.write("**Action**")
        
        st.markdown("---")
        
        # Display data rows
        for index, row in df.iterrows():
            data_cols = st.columns([1, 2, 1, 2, 3, 2, 2, 1, 1])
            
            with data_cols[0]:
                st.write(row['id'])
            with data_cols[1]:
                name = row.get('name', 'N/A')
                description = row.get('description', '')
                if description:
                    st.markdown(f'<span title="{description}" style="cursor:help;border-bottom:1px dotted #666;">{name}</span>', unsafe_allow_html=True)
                else:
                    st.write(name)
            with data_cols[2]:
                st.write(row.get('operation', 'N/A'))
            with data_cols[3]:
                routing_url = f"https://routing-portal-d3id.vercel.app/route?routing_url={row.get('routing_url', '')}"
                st.write(routing_url)
            with data_cols[4]:
                st.write(row['original_url'])
            with data_cols[5]:
                st.write(row.get('lob', 'N/A'))
            with data_cols[6]:
                st.write(row.get('environment', 'N/A'))
            with data_cols[7]:
                st.write(row.get('created_at', 'N/A'))
            with data_cols[8]:
                if st.button("Delete", key=f"delete_{row['id']}", type="secondary"):
                    if delete_response(row['id']):
                        st.success(f"Response deleted for record {row['id']}")
                        st.rerun()
                    else:
                        st.error(f"Failed to delete response for record {row['id']}")

        # st.markdown("---")  # Separator line

        # Display options
    else:
        st.info("No records found in the service_virtualisation database")
        st.write("Register the APIs to create mock APIs first.")

except Exception as e:
    st.error(f"Error connecting to database: {str(e)}")
    st.write("Please check your database connection in sql.py")
    
    # Show connection test button
    if st.button("Test Database Connection"):
        try:
            conn = connect_to_retool()
            conn.close()
            st.success("Database connection successful!")
        except Exception as conn_error:
            st.error(f"Database connection failed: {str(conn_error)}")


# Footer
st.markdown("---")
st.markdown("© 2026 ValueMomentum. All Rights Reserved.")