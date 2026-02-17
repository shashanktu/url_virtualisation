import streamlit as st
import requests
import json
from datetime import datetime
from urllib.parse import urlparse
from sql import insert_url_data


# Page config
st.set_page_config(
    page_title="Service Virtualization",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set page name for sidebar navigation
if "page_name" not in st.session_state:
    st.session_state.page_name = "Service Virtualization"

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
    .status-code {
        font-weight: bold;
        font-size: 1.2rem;
    }
    .scrollable-json {
        max-height: 300px;
        overflow-y: auto;
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 10px;
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)


st.image("src/ValueMomentum_logo.png", width=100)

st.markdown('<div class="main-header">Command Center(NPE Services Virtualization)</div>', unsafe_allow_html=True)



# Main interface
# st.write(get_routing_url())
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Request Configuration")
    
    # Name and Description fields
    url_name = st.text_input("Name", placeholder="Enter a name for this URL")
    url_description = st.text_area("Description", placeholder="Enter a description for this URL", height=100)
    
    # HTTP Method and URL
    method_col, url_col = st.columns([1, 4])
    with method_col:
        method = st.selectbox("Method", ["GET", "POST", "PUT", "DELETE", "PATCH"])
    with url_col:
        url = st.text_input("Enter API URL", placeholder="https://api.example.com/endpoint", label_visibility="visible")
        st.caption("Note: If mocking JSON directly, enter 'Not Applicable' as URL")
    
    # Tabs for different configurations
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Headers", "Authorization", "Body", "Params", "Mock Response", "API Details"])
    
    with tab1:
        st.write("**Headers**")
        headers = {}
        num_headers = st.number_input("Number of headers", min_value=0, max_value=10, value=1)
        for i in range(num_headers):
            col_key, col_value = st.columns(2)
            with col_key:
                key = st.text_input(f"Header {i+1} Key", key=f"header_key_{i}")
            with col_value:
                value = st.text_input(f"Header {i+1} Value", key=f"header_value_{i}")
            if key and value:
                headers[key] = value
    
    with tab2:
        st.write("**Authorization**")
        auth_type = st.selectbox("Type", ["None", "Bearer Token", "Basic Auth", "API Key"])
        
        auth_headers = {}
        if auth_type == "Bearer Token":
            token = st.text_input("Token", type="password")
            if token:
                auth_headers["Authorization"] = f"Bearer {token}"
        elif auth_type == "Basic Auth":
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if username and password:
                import base64
                credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
                auth_headers["Authorization"] = f"Basic {credentials}"
        elif auth_type == "API Key":
            key_name = st.text_input("Key Name", value="X-API-Key")
            api_key = st.text_input("API Key", type="password")
            if key_name and api_key:
                auth_headers[key_name] = api_key
    
    with tab3:
        st.write("**Request Body**")
        body_type = st.selectbox("Body Type", ["None", "JSON", "Form Data", "Raw Text"])
        
        body_data = None
        if body_type == "JSON":
            body_text = st.text_area("JSON Body", height=150, placeholder='{"key": "value"}')
            if body_text:
                try:
                    body_data = json.loads(body_text)
                    headers["Content-Type"] = "application/json"
                except json.JSONDecodeError:
                    st.error("Invalid JSON format")
        elif body_type == "Form Data":
            num_fields = st.number_input("Number of fields", min_value=0, max_value=10, value=1)
            form_data = {}
            for i in range(num_fields):
                col_key, col_value = st.columns(2)
                with col_key:
                    key = st.text_input(f"Field {i+1} Key", key=f"form_key_{i}")
                with col_value:
                    value = st.text_input(f"Field {i+1} Value", key=f"form_value_{i}")
                if key and value:
                    form_data[key] = value
            if form_data:
                body_data = form_data
        elif body_type == "Raw Text":
            body_data = st.text_area("Raw Body", height=150)
    
    with tab4:
        st.write("**Query Parameters**")
        params = {}
        num_params = st.number_input("Number of parameters", min_value=0, max_value=10, value=0)
        for i in range(num_params):
            col_key, col_value = st.columns(2)
            with col_key:
                key = st.text_input(f"Param {i+1} Key", key=f"param_key_{i}")
            with col_value:
                value = st.text_input(f"Param {i+1} Value", key=f"param_value_{i}")
            if key and value:
                params[key] = value
    with tab5:
        st.write("**Mock Response (Only for 'Not Applicable' URLs)**")
        mock_response_text = None
        if url and url.lower() in ['not applicable', 'na', 'n/a']:
            mock_response_text = st.text_area("Enter Mock JSON Response", height=200, placeholder='{"status": "success", "data": []}', key="mock_response_input")
            if mock_response_text:
                try:
                    mock_response_json = json.loads(mock_response_text)
                    st.success("✓ Valid JSON format")
                except json.JSONDecodeError:
                    st.error("✗ Invalid JSON format")
        else:
            st.info("This tab is only enabled when URL is set to 'Not Applicable'")
    
    with tab6:
        st.write("**API Details**")
        st.text_area("API Documentation", height=150)
        st.write("**Environment**")
        env = st.selectbox("Environment", ["Dev", "Test", "Staging", "Prod"])
        st.write("**LOB**")
        lob = st.selectbox("Line of Business", ["Policy", "Claims", "Small Business"])

with col2:
    st.subheader("Validate")
    
    # Initialize session state for storing validated response
    if 'validated_response' not in st.session_state:
        st.session_state.validated_response = None
    
    # Send button
    if st.button("Validate", type="primary", use_container_width=True):
        if not url:
            st.error("Please enter a URL")
        elif url.lower() in ['not applicable', 'na', 'n/a']:
            # Handle Not Applicable URLs with mock response
            if 'mock_response_input' in st.session_state and st.session_state.mock_response_input:
                try:
                    mock_response_json = json.loads(st.session_state.mock_response_input)
                    st.session_state.validated_response = json.dumps(mock_response_json)
                    
                    st.markdown(f"""
                    <div class="response-success">
                        <span class="status-code">Status: Mock Response Validated</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.json(mock_response_json)
                    
                except json.JSONDecodeError:
                    st.error("Invalid JSON format in Mock Response tab")
            else:
                st.error("Please enter a mock JSON response in the 'Mock Response' tab")
        else:
            try:
                # Combine headers
                all_headers = {**headers, **auth_headers}
                
                # Make request
                start_time = datetime.now()
                
                if method == "GET":
                    response = requests.get(url, headers=all_headers, params=params)
                elif method == "POST":
                    if body_type == "JSON" and body_data:
                        response = requests.post(url, headers=all_headers, params=params, json=body_data)
                    else:
                        response = requests.post(url, headers=all_headers, params=params, data=body_data)
                elif method == "PUT":
                    if body_type == "JSON" and body_data:
                        response = requests.put(url, headers=all_headers, params=params, json=body_data)
                    else:
                        response = requests.put(url, headers=all_headers, params=params, data=body_data)
                elif method == "DELETE":
                    response = requests.delete(url, headers=all_headers, params=params)
                elif method == "PATCH":
                    if body_type == "JSON" and body_data:
                        response = requests.patch(url, headers=all_headers, params=params, json=body_data)
                    else:
                        response = requests.patch(url, headers=all_headers, params=params, data=body_data)
                
                end_time = datetime.now()
                response_time = (end_time - start_time).total_seconds() * 1000
                
                # Store validated response for mock API
                try:
                    st.session_state.validated_response = response.text
                except:
                    st.session_state.validated_response = response.text
                
                # Display response
                status_color = "success" if 200 <= response.status_code < 300 else "error"
                
                st.markdown(f"""
                <div class="response-{status_color}">
                    <span class="status-code">Status: {response.status_code}</span>
                    <span style="float: right;">Time: {response_time:.0f}ms</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Response tabs
                resp_tab1, resp_tab2, resp_tab3 = st.tabs(["Body", "Headers", "Raw"])
                
                with resp_tab1:
                    try:
                        json_response = response.json()
                        with st.container():
                            st.markdown('<div class="scrollable-json">', unsafe_allow_html=True)
                            st.json(json_response)
                            st.markdown('</div>', unsafe_allow_html=True)
                    except:
                        st.text_area("Response", response.text, height=300)
                
                with resp_tab2:
                    with st.container():
                        st.markdown('<div class="scrollable-json">', unsafe_allow_html=True)
                        st.json(dict(response.headers))
                        st.markdown('</div>', unsafe_allow_html=True)
                
                with resp_tab3:
                    st.text(f"Status Code: {response.status_code}")
                    st.text(f"Response Time: {response_time:.0f}ms")
                    st.text(f"Content Length: {len(response.content)} bytes")
                    st.text("Raw Response:")
                    st.code(response.text)
                
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {str(e)}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    
    # Mock API button
    if st.button("Mock API", use_container_width=True):
        if st.session_state.validated_response is None:
            st.error("Please validate an API first to get response data for mocking")
        else:
            try:
                # Handle routing URL based on URL type
                if url.lower() in ['not applicable', 'na', 'n/a']:
                    # Use name as routing URL for Not Applicable
                    mock_path = f"/{url_name.lower().replace(' ', '-')}" if url_name else "/unnamed-api"
                else:
                    # Extract path from URL
                    parsed_url = urlparse(url)
                    mock_path = parsed_url.path
                    if parsed_url.query:
                        mock_path += f"?{parsed_url.query}"
                
                # Prepare API details as JSON
                api_details_data = {
                    "environment": env if 'env' in locals() else "Not specified",
                    "line_of_business": lob if 'lob' in locals() else "Not specified",
                    "headers": {**headers, **auth_headers},
                    "parameters": params,
                    "body_type": body_type if 'body_type' in locals() else "None",
                    "body_data": body_data,
                    "auth_type": auth_type if 'auth_type' in locals() else "None",
                    "original_response": st.session_state.validated_response,
                    "created_timestamp": datetime.now().isoformat()
                }
                
                # Store in database with LOB and Environment
                inserted_id = insert_url_data(
                    name=url_name if url_name else "Unnamed API",
                    original_url=url,
                    routing_url=mock_path,
                    description=url_description if url_description else None,
                    operation=method,
                    headers=json.dumps({**headers, **auth_headers}),
                    parameters=json.dumps(params),
                    response=st.session_state.validated_response,
                    api_details=json.dumps(api_details_data),
                    lob=lob if 'lob' in locals() else None,
                    environment=env if 'env' in locals() else None
                )
                
                if inserted_id:
                    st.success(f"Mock API created and inserted into database with ID: {inserted_id}")
                    
                    # Display routing portal information
                    routing_base_url = "https://routing-portal-d3id.vercel.app"
                    st.info(f"**Routing Portal Base URL:** `{routing_base_url}/route?routing_url={mock_path}`")
                else:
                    st.warning("Failed to insert data into database")
                    
            except Exception as e:
                st.error(f"Mock API error: {str(e)}")
    
    # Request preview
    st.subheader("Request Preview")
    if url:
        preview_headers = {**headers, **auth_headers}
        st.code(f"""
{method} {url}
Headers: {json.dumps(preview_headers, indent=2) if preview_headers else 'None'}
Params: {json.dumps(params, indent=2) if params else 'None'}
Body: {json.dumps(body_data, indent=2) if body_data else 'None'}
        """)
    

# Footer
st.markdown("---")
st.markdown("© 2026 ValueMomentum. All Rights Reserved.")