import streamlit as st
import requests
from PIL import Image
from typing import Optional, Dict, Any

# Configuration
API_BASE_URL = "http://35.154.225.172:8003"  # Update this to match your API server

# Page configuration
st.set_page_config(
    page_title="Face Recognition System",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .error-box {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .info-box {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def check_api_health() -> Dict[str, Any]:
    """Check if the API is running and healthy"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return {
            "status": "healthy" if response.status_code == 200 else "unhealthy",
            "data": response.json() if response.status_code == 200 else None
        }
    except requests.exceptions.RequestException:
        return {"status": "offline", "data": None}

def get_collection_info() -> Optional[Dict[str, Any]]:
    """Get collection information from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/collection/info", timeout=10)
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException:
        return None

def enroll_employee(image_bytes: bytes, filename: str, phone: Optional[str] = None) -> Dict[str, Any]:
    """Enroll an employee via API"""
    try:
        files = {"file": (filename, image_bytes, "image/jpeg")}
        data = {"phone": phone} if phone else {}
        
        response = requests.post(f"{API_BASE_URL}/enroll", files=files, data=data, timeout=30)
        return {
            "success": response.status_code == 200,
            "data": response.json(),
            "status_code": response.status_code
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "data": {"detail": f"Request failed: {str(e)}"},
            "status_code": 500
        }

def login_employee(image_bytes: bytes, filename: str) -> Dict[str, Any]:
    """Login an employee via API"""
    try:
        files = {"file": (filename, image_bytes, "image/jpeg")}
        
        response = requests.post(f"{API_BASE_URL}/login", files=files, timeout=30)
        return {
            "success": response.status_code == 200,
            "data": response.json(),
            "status_code": response.status_code
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "data": {"detail": f"Request failed: {str(e)}"},
            "status_code": 500
        }

def search_faces(image_bytes: bytes, filename: str, limit: int = 5) -> Dict[str, Any]:
    """Search for face matches via API"""
    try:
        files = {"file": (filename, image_bytes, "image/jpeg")}
        data = {"limit": limit}
        
        response = requests.post(f"{API_BASE_URL}/search", files=files, data=data, timeout=30)
        return {
            "success": response.status_code == 200,
            "data": response.json(),
            "status_code": response.status_code
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "data": {"detail": f"Request failed: {str(e)}"},
            "status_code": 500
        }

def list_enrolled_phones() -> Optional[Dict[str, Any]]:
    """Get list of enrolled phone numbers"""
    try:
        response = requests.get(f"{API_BASE_URL}/collection/list", timeout=10)
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException:
        return None

def remove_enrollment(phone: str) -> Dict[str, Any]:
    """Remove an enrollment"""
    try:
        response = requests.delete(f"{API_BASE_URL}/enroll/{phone}", timeout=10)
        return {
            "success": response.status_code == 200,
            "data": response.json(),
            "status_code": response.status_code
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "data": {"detail": f"Request failed: {str(e)}"},
            "status_code": 500
        }

def clear_collection() -> Dict[str, Any]:
    """Clear all data from collection"""
    try:
        response = requests.delete(f"{API_BASE_URL}/collection/clear", timeout=30)
        return {
            "success": response.status_code == 200,
            "data": response.json(),
            "status_code": response.status_code
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "data": {"detail": f"Request failed: {str(e)}"},
            "status_code": 500
        }

def display_image_with_info(uploaded_file, max_width: int = 300):
    """Display uploaded image with information"""
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption=f"Uploaded: {uploaded_file.name}", width=max_width)
        
        # Display image info
        st.write(f"**File Name:** {uploaded_file.name}")
        st.write(f"**File Size:** {uploaded_file.size:,} bytes")
        st.write(f"**Image Size:** {image.size[0]} x {image.size[1]} pixels")
        return image
    return None

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>👤 Face Recognition System</h1>
        <p>AI-Powered Employee Authentication & Management</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar for navigation
    st.sidebar.title("🔧 System Control")
    
    # API Status check
    with st.sidebar:
        st.subheader("📊 System Status")
        health_status = check_api_health()
        
        if health_status["status"] == "healthy":
            st.success("✅ API Online")
        elif health_status["status"] == "unhealthy":
            st.warning("⚠️ API Issues")
        else:
            st.error("❌ API Offline")
        
        # Collection info
        if health_status["status"] == "healthy":
            collection_info = get_collection_info()
            if collection_info:
                st.metric("Total Faces", collection_info.get("total_faces", 0))

    # Navigation
    page = st.sidebar.selectbox(
        "Choose Action",
        ["🏠 Home", "📝 Enroll Employee", "🔐 Employee Login", "🔍 Face Search", "👥 Manage Employees", "⚙️ System Admin"]
    )

    if page == "🏠 Home":
        show_home_page()
    elif page == "📝 Enroll Employee":
        show_enrollment_page()
    elif page == "🔐 Employee Login":
        show_login_page()
    elif page == "🔍 Face Search":
        show_search_page()
    elif page == "👥 Manage Employees":
        show_management_page()
    elif page == "⚙️ System Admin":
        show_admin_page()

def show_home_page():
    """Home page with system overview"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 System Features
        - **Face Enrollment**: Register employees with their photos
        - **Face Authentication**: Secure login using facial recognition
        - **Multi-Match Search**: Advanced face similarity analysis
        - **Employee Management**: View and manage enrolled users
        - **Real-time Analytics**: Live confidence scores and match quality
        """)
    
    with col2:
        st.markdown("""
        ### 📈 How It Works
        1. **Enroll**: Upload employee photo with phone number
        2. **Authenticate**: Login by taking/uploading a photo
        3. **Analyze**: Get detailed match analysis and confidence scores
        4. **Manage**: Add, remove, or update employee records
        """)
    
    # System Statistics
    st.subheader("📊 System Statistics")
    
    health_status = check_api_health()
    if health_status["status"] == "healthy":
        collection_info = get_collection_info()
        enrolled_list = list_enrolled_phones()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🎭 Total Faces", collection_info.get("total_faces", 0) if collection_info else 0)
        with col2:
            st.metric("📱 Enrolled Users", enrolled_list.get("total_count", 0) if enrolled_list else 0)
        with col3:
            st.metric("🟢 System Status", "Online")
    else:
        st.error("❌ Cannot connect to Face Recognition API. Please ensure the server is running.")

def show_enrollment_page():
    """Employee enrollment page"""
    st.header("📝 Enroll New Employee")
    
    st.markdown("""
    <div class="info-box">
        <strong>💡 Enrollment Tips:</strong>
        <ul>
            <li>Use clear, well-lit photos</li>
            <li>Ensure face is clearly visible and not obscured</li>
            <li>Phone number can be in filename (name_1234567890.jpg) or entered manually</li>
            <li>Supported formats: JPG, JPEG, PNG</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose employee photo",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear photo of the employee's face"
    )
    
    if uploaded_file is not None:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            display_image_with_info(uploaded_file)
        
        with col2:
            st.subheader("📋 Enrollment Details")
            
            # Phone number input
            phone = st.text_input(
                "📱 Phone Number (optional if in filename)",
                placeholder="1234567890",
                help="Enter phone number if not included in filename"
            )
            
            # Validate phone if provided
            phone_valid = True
            if phone:
                if not phone.isdigit() or len(phone) < 10:
                    st.error("❌ Phone number must be at least 10 digits and contain only numbers")
                    phone_valid = False
                else:
                    st.success(f"✅ Phone number: {phone}")
            
            # Enrollment button
            if st.button("🚀 Enroll Employee", type="primary", disabled=not phone_valid):
                with st.spinner("Processing enrollment..."):
                    image_bytes = uploaded_file.getvalue()
                    result = enroll_employee(image_bytes, uploaded_file.name, phone if phone else None)
                
                if result["success"]:
                    st.markdown(f"""
                    <div class="success-box">
                        <h4>✅ Enrollment Successful!</h4>
                        <p><strong>Phone:</strong> {result['data']['phone']}</p>
                        <p><strong>Message:</strong> {result['data']['message']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
                else:
                    st.markdown(f"""
                    <div class="error-box">
                        <h4>❌ Enrollment Failed</h4>
                        <p>{result['data'].get('detail', 'Unknown error occurred')}</p>
                    </div>
                    """, unsafe_allow_html=True)

def show_login_page():
    """Employee login page"""
    st.header("🔐 Employee Login")
    
    st.markdown("""
    <div class="info-box">
        <strong>🔒 Authentication Process:</strong>
        The system will find the closest face match and provide detailed confidence scores.
        Authentication is based on match quality and similarity threshold.
    </div>
    """, unsafe_allow_html=True)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload photo for authentication",
        type=['jpg', 'jpeg', 'png'],
        help="Take or upload a photo for face recognition login"
    )
    
    if uploaded_file is not None:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            display_image_with_info(uploaded_file)
        
        with col2:
            if st.button("🔍 Authenticate", type="primary"):
                with st.spinner("Analyzing face..."):
                    image_bytes = uploaded_file.getvalue()
                    result = login_employee(image_bytes, uploaded_file.name)
                
                if result["success"]:
                    data = result["data"]
                    
                    # Display authentication result
                    if data["is_authenticated"]:
                        st.markdown(f"""
                        <div class="success-box">
                            <h4>✅ Authentication Successful!</h4>
                            <p><strong>Phone:</strong> {data['phone']}</p>
                            <p><strong>Match Quality:</strong> {data['match_quality'].title()}</p>
                            <p><strong>Confidence:</strong> {data['confidence_score']:.1f}%</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.success("🎉 Welcome! Login successful.")
                    else:
                        st.markdown(f"""
                        <div class="error-box">
                            <h4>❌ Authentication Failed</h4>
                            <p><strong>Reason:</strong> Face match quality too low</p>
                            <p><strong>Nearest Match:</strong> {data.get('phone', 'None found')}</p>
                            <p><strong>Confidence:</strong> {data.get('confidence_score', 0):.1f}%</p>
                            <p><strong>Match Quality:</strong> {data.get('match_quality', 'Unknown').title()}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Display detailed metrics
                    st.subheader("📊 Authentication Metrics")
                    col3, col4, col5 = st.columns(3)
                    with col3:
                        st.metric("Distance Score", f"{data.get('distance', 0):.2f}")
                    with col4:
                        st.metric("Confidence", f"{data.get('confidence_score', 0):.1f}%")
                    with col5:
                        st.metric("Quality", data.get('match_quality', 'Unknown').title())
                
                else:
                    st.markdown(f"""
                    <div class="error-box">
                        <h4>❌ Authentication Error</h4>
                        <p>{result['data'].get('detail', 'Unknown error occurred')}</p>
                    </div>
                    """, unsafe_allow_html=True)

def show_search_page():
    """Face search and analysis page"""
    st.header("🔍 Face Search & Analysis")
    
    st.markdown("""
    <div class="info-box">
        <strong>🎯 Advanced Search:</strong>
        Find the top matching faces in the database with detailed similarity analysis.
        Useful for debugging and detailed face recognition analysis.
    </div>
    """, unsafe_allow_html=True)
    
    # Search parameters
    col1, col2 = st.columns([2, 1])
    with col2:
        limit = st.slider("Number of matches to return", 1, 10, 5)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload photo for face search",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a photo to find similar faces in the database"
    )
    
    if uploaded_file is not None:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            display_image_with_info(uploaded_file)
        
        with col2:
            if st.button("🔎 Search Faces", type="primary"):
                with st.spinner("Searching database..."):
                    image_bytes = uploaded_file.getvalue()
                    result = search_faces(image_bytes, uploaded_file.name, limit)
                
                if result["success"]:
                    data = result["data"]
                    
                    st.subheader(f"📋 Search Results ({data.get('total_matches', 0)} matches)")
                    
                    if data.get('matches'):
                        for i, match in enumerate(data['matches'], 1):
                            with st.expander(f"Match #{i}: {match['phone']} - {match['match_quality'].title()}"):
                                col3, col4, col5, col6 = st.columns(4)
                                with col3:
                                    st.metric("📱 Phone", match['phone'])
                                with col4:
                                    st.metric("📏 Distance", f"{match['distance']:.3f}")
                                with col5:
                                    st.metric("🎯 Confidence", f"{match['confidence_score']:.1f}%")
                                with col6:
                                    quality_emoji = {"excellent": "🟢", "good": "🟡", "fair": "🟠", "poor": "🔴", "very poor": "⚫"}.get(match['match_quality'], "❓")
                                    st.metric("⭐ Quality", f"{quality_emoji} {match['match_quality'].title()}")
                    else:
                        st.info("No matches found in database.")
                
                else:
                    st.error(f"Search failed: {result['data'].get('detail', 'Unknown error')}")

def show_management_page():
    """Employee management page"""
    st.header("👥 Employee Management")
    
    # Get enrolled employees
    enrolled_data = list_enrolled_phones()
    
    if enrolled_data:
        st.subheader(f"📊 Enrolled Employees ({enrolled_data['total_count']})")
        
        if enrolled_data['phones']:
            # Display as a table
            phones_df = [{"Phone Number": phone, "Status": "✅ Active"} for phone in enrolled_data['phones']]
            st.dataframe(phones_df, use_container_width=True)
            
            # Remove employee section
            st.subheader("❌ Remove Employee")
            col1, col2 = st.columns([2, 1])
            
            with col1:
                phone_to_remove = st.selectbox(
                    "Select phone number to remove",
                    [""] + enrolled_data['phones']
                )
            
            with col2:
                st.write("")  # Spacing
                st.write("")  # Spacing
                if st.button("🗑️ Remove", type="secondary", disabled=not phone_to_remove):
                    if st.session_state.get('confirm_removal', False):
                        with st.spinner("Removing employee..."):
                            result = remove_enrollment(phone_to_remove)
                        
                        if result["success"]:
                            st.success(f"✅ Successfully removed {phone_to_remove}")
                            st.session_state['confirm_removal'] = False
                            st.rerun()
                        else:
                            st.error(f"❌ Failed to remove: {result['data'].get('detail', 'Unknown error')}")
                    else:
                        st.warning(f"⚠️ Click again to confirm removal of {phone_to_remove}")
                        st.session_state['confirm_removal'] = True
        else:
            st.info("📭 No employees enrolled yet.")
    else:
        st.error("❌ Could not retrieve employee list. Check API connection.")

def show_admin_page():
    """System administration page"""
    st.header("⚙️ System Administration")
    
    st.warning("🚨 **Warning:** Administrative actions are irreversible!")
    
    # System health
    st.subheader("🏥 System Health Check")
    health_status = check_api_health()
    
    if health_status["status"] == "healthy" and health_status["data"]:
        data = health_status["data"]
        
        col1, col2 = st.columns(2)
        with col1:
            st.success("✅ API Status: Healthy")
            st.info(f"🗄️ Collections: {', '.join(data.get('collections', []))}")
        with col2:
            st.success(f"🤖 Face Model: {data.get('face_model', 'Unknown')}")
            st.info(f"📊 Collection Loaded: {'Yes' if data.get('collection_loaded') else 'No'}")
    
    # Database operations
    st.subheader("🗄️ Database Operations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Collection Statistics")
        collection_info = get_collection_info()
        if collection_info:
            st.metric("Total Faces", collection_info.get("total_faces", 0))
            st.metric("Collection Name", collection_info.get("collection_name", "Unknown"))
            st.metric("Status", collection_info.get("status", "Unknown"))
    
    with col2:
        st.markdown("### 🧹 Maintenance")
        
        if st.button("🔄 Refresh Data", help="Reload collection information"):
            st.rerun()
        
        st.markdown("---")
        
        # Danger zone
        st.markdown("### ⚠️ Danger Zone")
        
        if st.button("🗑️ Clear All Data", type="secondary", help="Remove all enrolled faces"):
            if st.session_state.get('confirm_clear', False):
                with st.spinner("Clearing all data..."):
                    result = clear_collection()
                
                if result["success"]:
                    st.success("✅ All data cleared successfully")
                    st.session_state['confirm_clear'] = False
                    st.rerun()
                else:
                    st.error(f"❌ Failed to clear data: {result['data'].get('detail', 'Unknown error')}")
            else:
                st.error("⚠️ **DANGER!** Click again to confirm - this will delete ALL enrolled faces!")
                st.session_state['confirm_clear'] = True

if __name__ == "__main__":
    main()