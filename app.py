import streamlit as st
import requests
from urllib.parse import quote
import json

# Set page config
st.set_page_config(page_title="NCRA Link Shortener", page_icon="🔗", layout="centered")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem;
        font-size: 1.1rem;
        border-radius: 5px;
        border: none;
        margin-top: 1rem;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🔗 NCRA Link Shortener")

# Add an image in the header (if you have one)
try:
    st.image("images.png", use_container_width=True)
except:
    pass  # Skip if image doesn't exist

# Display "Presented by NCRA-CMS Lab"
st.markdown("<h5 style='text-align: center; color: gray;'>Presented by NCRA-CMS Lab</h5>", unsafe_allow_html=True)
st.markdown("---")

# Description
st.write("""
### Welcome to the Link Shortener! 
This app helps you shorten long URLs into easy-to-share short links.
Just paste your URL below and click **"Shorten URL"** to get started.
""")

# URL input
url = st.text_input("🌐 Enter the URL you want to shorten:", placeholder="https://example.com/very/long/url")

# Function to shorten URL using ShortURL.at (NO PREVIEW PAGE!)
def shorten_url_shorturlat(long_url):
    """Shorten URL using shorturl.at API - Direct redirect, no preview"""
    try:
        api_url = "https://www.shorturl.at/shortener.php"
        response = requests.post(api_url, data={'url': long_url}, timeout=10)
        if response.status_code == 200:
            # The response contains the shortened URL
            result = response.text.strip()
            if result.startswith('http'):
                return result
        return None
    except Exception as e:
        return None

# Function to shorten URL using is.gd (NO PREVIEW PAGE!)
def shorten_url_isgd(long_url):
    """Shorten URL using is.gd API - Direct redirect, no preview"""
    try:
        api_url = f"https://is.gd/create.php?format=simple&url={quote(long_url)}"
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200 and response.text.startswith('http'):
            return response.text.strip()
        return None
    except Exception as e:
        return None

# Function to shorten URL using v.gd (NO PREVIEW PAGE!)
def shorten_url_vgd(long_url):
    """Shorten URL using v.gd API - Direct redirect, no preview"""
    try:
        api_url = f"https://v.gd/create.php?format=simple&url={quote(long_url)}"
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200 and response.text.startswith('http'):
            return response.text.strip()
        return None
    except Exception as e:
        return None

# Function to shorten URL using clck.ru (NO PREVIEW PAGE!)
def shorten_url_clckru(long_url):
    """Shorten URL using clck.ru API - Direct redirect, no preview"""
    try:
        api_url = "https://clck.ru/--"
        response = requests.post(api_url, data={'url': long_url}, timeout=10)
        if response.status_code == 200 and response.text.startswith('http'):
            return response.text.strip()
        return None
    except Exception as e:
        return None

# Function to shorten URL using ulvis.net (NO PREVIEW PAGE!)
def shorten_url_ulvis(long_url):
    """Shorten URL using ulvis.net API - Direct redirect, no preview"""
    try:
        api_url = "https://ulvis.net/api.php"
        params = {'url': long_url}
        response = requests.get(api_url, params=params, timeout=10)
        if response.status_code == 200 and response.text.startswith('http'):
            return response.text.strip()
        return None
    except Exception as e:
        return None

def is_valid_url(url_string):
    """Check if the URL is valid"""
    if not url_string:
        return False
    return url_string.startswith(('http://', 'https://'))

# Add service selector
st.markdown("### Choose a shortening service:")
service = st.radio(
    "Select service (All redirect directly without preview):",
    ["ShortURL.at (Recommended)", "is.gd", "v.gd", "clck.ru", "ulvis.net", "Try All Services"],
    horizontal=False
)

# Info about services
st.info("✅ All these services redirect directly to your destination without preview pages!")

# Shorten URL button
if st.button("🚀 Shorten URL"):
    if url:
        if not is_valid_url(url):
            st.error("❌ Please enter a valid URL starting with http:// or https://")
        else:
            with st.spinner("Shortening your URL..."):
                short_url = None
                service_used = ""
                
                if service == "ShortURL.at (Recommended)":
                    short_url = shorten_url_shorturlat(url)
                    service_used = "ShortURL.at"
                elif service == "is.gd":
                    short_url = shorten_url_isgd(url)
                    service_used = "is.gd"
                elif service == "v.gd":
                    short_url = shorten_url_vgd(url)
                    service_used = "v.gd"
                elif service == "clck.ru":
                    short_url = shorten_url_clckru(url)
                    service_used = "clck.ru"
                elif service == "ulvis.net":
                    short_url = shorten_url_ulvis(url)
                    service_used = "ulvis.net"
                else:  # Try All Services
                    short_url = shorten_url_shorturlat(url)
                    service_used = "ShortURL.at"
                    if not short_url:
                        short_url = shorten_url_isgd(url)
                        service_used = "is.gd"
                    if not short_url:
                        short_url = shorten_url_vgd(url)
                        service_used = "v.gd"
                    if not short_url:
                        short_url = shorten_url_clckru(url)
                        service_used = "clck.ru"
                    if not short_url:
                        short_url = shorten_url_ulvis(url)
                        service_used = "ulvis.net"
                
                if short_url:
                    st.success(f"✅ URL shortened successfully using {service_used}!")
                    
                    # Display the shortened URL in a nice box
                    st.markdown(f"""
                    <div class="success-box">
                        <h4>Your shortened URL:</h4>
                        <h3 style="color: #4CAF50;">{short_url}</h3>
                        <p style="color: #666; font-size: 0.9em;">✅ This link redirects DIRECTLY to your destination (no preview page)</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add copy button functionality
                    col1, col2 = st.columns(2)
                    with col1:
                        st.code(short_url, language=None)
                    with col2:
                        if st.button("📋 Copy to Clipboard"):
                            st.toast("✅ Link copied! (Use Ctrl+C to copy from the code box)", icon="✅")
                    
                    # Test the link
                    st.markdown(f"🔗 [Click here to test your shortened link]({short_url})")
                    
                    # Show original URL
                    with st.expander("📝 View Original URL"):
                        st.write(url)
                else:
                    st.error("❌ Failed to shorten URL. Please try again or choose a different service.")
    else:
        st.error("❌ Please enter a URL first!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 1rem;'>
    <p>💡 <strong>Tip:</strong> Make sure your URL starts with http:// or https://</p>
    <p>✅ <strong>All services provide DIRECT links</strong> - No preview pages!</p>
    <p>📧 For issues or suggestions, contact NCRA-CMS Lab</p>
    <p><a href="https://sahiljatoi744.github.io/Sahil-Ali-Jatoi/" target="_blank">🌐 Visit NCRA-CMS Lab Website</a></p>
</div>
""", unsafe_allow_html=True)

# Sidebar with additional info
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    This Link Shortener tool helps you create compact, 
    shareable URLs for your long links.
    
    **Features:**
    - ✅ Direct redirect (NO preview pages)
    - Multiple shortening services
    - Easy copy functionality
    - Fast and reliable
    - Free to use
    
    **Supported Services:**
    - **ShortURL.at** - Fast & clean
    - **is.gd** - Fast & reliable
    - **v.gd** - Alternative to is.gd
    - **clck.ru** - Russian service
    - **ulvis.net** - Privacy focused
    
    All services redirect directly without 
    showing any preview or interstitial pages!
    """)
    
    st.markdown("---")
    st.markdown("**NCRA-CMS Lab**")
    st.markdown("[Visit our website](https://sahiljatoi744.github.io/Sahil-Ali-Jatoi/)")
    
    st.markdown("---")
    st.markdown("### 🎯 Why No Preview?")
    st.write("""
    Preview pages slow down access and 
    frustrate users. Our selected services 
    provide clean, direct redirects for the 
    best user experience!
    """)
