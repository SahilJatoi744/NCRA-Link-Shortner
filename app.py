import streamlit as st
import requests
from urllib.parse import quote
import json
import time
from datetime import datetime
import qrcode
from io import BytesIO
import base64
import pandas as pd

# Set page config
st.set_page_config(
    page_title="NCRA Link Shortener Pro", 
    page_icon="🔗", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'stats' not in st.session_state:
    st.session_state.stats = {'total_shortened': 0, 'successful': 0, 'failed': 0}

# Custom CSS for premium styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        padding: 1rem 2rem;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.75rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        margin-top: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .link-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        transition: transform 0.3s ease;
    }
    
    .link-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    }
    
    .success-badge {
        background: #10b981;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .failed-badge {
        background: #ef4444;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .speed-badge {
        background: #3b82f6;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        display: inline-block;
        margin-left: 0.5rem;
    }
    
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6b7280;
        margin-top: 0.5rem;
    }
    
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem !important;
    }
    
    .header-subtitle {
        color: #6b7280;
        font-size: 1.2rem;
        margin-top: -1rem;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🔗 NCRA Link Shortener Pro")
    st.markdown('<p class="header-subtitle">The World\'s Most Advanced URL Shortener</p>', unsafe_allow_html=True)

try:
    st.image("images.jpg", use_container_width=True)
except:
    pass

st.markdown("---")

# Shortening functions with timing
def shorten_url_shorturlat(long_url):
    try:
        start = time.time()
        api_url = "https://www.shorturl.at/shortener.php"
        response = requests.post(api_url, data={'url': long_url}, timeout=10)
        elapsed = round((time.time() - start) * 1000, 2)
        if response.status_code == 200:
            result = response.text.strip()
            if result.startswith('http'):
                return result, elapsed, True
        return None, elapsed, False
    except Exception as e:
        return None, 0, False

def shorten_url_isgd(long_url):
    try:
        start = time.time()
        api_url = f"https://is.gd/create.php?format=simple&url={quote(long_url)}"
        response = requests.get(api_url, timeout=10)
        elapsed = round((time.time() - start) * 1000, 2)
        if response.status_code == 200 and response.text.startswith('http'):
            return response.text.strip(), elapsed, True
        return None, elapsed, False
    except Exception as e:
        return None, 0, False

def shorten_url_vgd(long_url):
    try:
        start = time.time()
        api_url = f"https://v.gd/create.php?format=simple&url={quote(long_url)}"
        response = requests.get(api_url, timeout=10)
        elapsed = round((time.time() - start) * 1000, 2)
        if response.status_code == 200 and response.text.startswith('http'):
            return response.text.strip(), elapsed, True
        return None, elapsed, False
    except Exception as e:
        return None, 0, False

def shorten_url_clckru(long_url):
    try:
        start = time.time()
        api_url = "https://clck.ru/--"
        response = requests.post(api_url, data={'url': long_url}, timeout=10)
        elapsed = round((time.time() - start) * 1000, 2)
        if response.status_code == 200 and response.text.startswith('http'):
            return response.text.strip(), elapsed, True
        return None, elapsed, False
    except Exception as e:
        return None, 0, False

def shorten_url_ulvis(long_url):
    try:
        start = time.time()
        api_url = "https://ulvis.net/api.php"
        params = {'url': long_url}
        response = requests.get(api_url, params=params, timeout=10)
        elapsed = round((time.time() - start) * 1000, 2)
        if response.status_code == 200 and response.text.startswith('http'):
            return response.text.strip(), elapsed, True
        return None, elapsed, False
    except Exception as e:
        return None, 0, False

def test_short_url(short_url):
    """Test if shortened URL works and get redirect destination"""
    try:
        response = requests.head(short_url, allow_redirects=True, timeout=5)
        return response.status_code == 200, response.url
    except:
        return False, None

def generate_qr_code(url):
    """Generate QR code for URL"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def is_valid_url(url_string):
    if not url_string:
        return False
    return url_string.startswith(('http://', 'https://'))

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Shorten URLs", "📊 Analytics", "📜 History", "⚙️ Batch Processing"])

with tab1:
    # Display stats at top
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{st.session_state.stats['total_shortened']}</div>
            <div class="metric-label">Total Shortened</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{st.session_state.stats['successful']}</div>
            <div class="metric-label">Successful</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{st.session_state.stats['failed']}</div>
            <div class="metric-label">Failed</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        success_rate = round((st.session_state.stats['successful'] / max(st.session_state.stats['total_shortened'], 1)) * 100, 1)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{success_rate}%</div>
            <div class="metric-label">Success Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # URL input
    url = st.text_input("🌐 Enter URL to shorten:", placeholder="https://example.com/very/long/url/that/needs/shortening", key="main_url")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        show_qr = st.checkbox("📱 Generate QR Codes", value=True)
    with col2:
        test_links = st.checkbox("🔍 Test Links", value=True)
    
    if st.button("🚀 Generate All Short Links", type="primary"):
        if url and is_valid_url(url):
            st.session_state.stats['total_shortened'] += 1
            
            services = {
                'ShortURL.at': shorten_url_shorturlat,
                'is.gd': shorten_url_isgd,
                'v.gd': shorten_url_vgd,
                'clck.ru': shorten_url_clckru,
                'ulvis.net': shorten_url_ulvis
            }
            
            results = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, (service_name, service_func) in enumerate(services.items()):
                status_text.text(f"Shortening with {service_name}...")
                short_url, elapsed, success = service_func(url)
                
                if success and short_url:
                    # Test the link if enabled
                    working = True
                    redirect_url = url
                    if test_links:
                        working, redirect_url = test_short_url(short_url)
                    
                    results.append({
                        'service': service_name,
                        'short_url': short_url,
                        'elapsed': elapsed,
                        'success': success,
                        'working': working,
                        'redirect_url': redirect_url
                    })
                    st.session_state.stats['successful'] += 1
                else:
                    results.append({
                        'service': service_name,
                        'short_url': None,
                        'elapsed': elapsed,
                        'success': False,
                        'working': False,
                        'redirect_url': None
                    })
                    st.session_state.stats['failed'] += 1
                
                progress_bar.progress((idx + 1) / len(services))
            
            status_text.empty()
            progress_bar.empty()
            
            # Sort by speed
            results.sort(key=lambda x: x['elapsed'] if x['success'] else float('inf'))
            
            # Save to history
            st.session_state.history.insert(0, {
                'original_url': url,
                'results': results,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # Display results
            st.success(f"✅ Generated {len([r for r in results if r['success']])} shortened links!")
            
            for idx, result in enumerate(results):
                if result['success']:
                    with st.container():
                        st.markdown(f"""
                        <div class="link-card">
                            <h3>🏆 {result['service']} {'⚡ FASTEST' if idx == 0 else ''}</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.code(result['short_url'], language=None)
                            
                            subcol1, subcol2, subcol3 = st.columns(3)
                            with subcol1:
                                st.markdown(f'<span class="success-badge">✓ Working</span>' if result['working'] else '<span class="failed-badge">✗ Failed Test</span>', unsafe_allow_html=True)
                            with subcol2:
                                st.markdown(f'<span class="speed-badge">⚡ {result["elapsed"]}ms</span>', unsafe_allow_html=True)
                            with subcol3:
                                if st.button(f"🔗 Test Link", key=f"test_{result['service']}"):
                                    st.markdown(f"[Click to test]({result['short_url']})")
                            
                            if result['redirect_url'] and result['redirect_url'] != url:
                                with st.expander("🔍 Redirect Chain"):
                                    st.text(f"Final URL: {result['redirect_url']}")
                        
                        with col2:
                            if show_qr:
                                qr_img = generate_qr_code(result['short_url'])
                                st.markdown(f'<img src="data:image/png;base64,{qr_img}" width="150"/>', unsafe_allow_html=True)
                                st.markdown(f'<a href="data:image/png;base64,{qr_img}" download="{result["service"]}_qr.png">📥 Download QR</a>', unsafe_allow_html=True)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.warning(f"❌ {result['service']} - Failed to generate link")
            
            # Show original URL
            with st.expander("📝 Original URL"):
                st.code(url)
        else:
            st.error("❌ Please enter a valid URL starting with http:// or https://")

with tab2:
    st.header("📊 Performance Analytics")
    
    if st.session_state.history:
        # Collect all service performance data
        service_stats = {}
        
        for entry in st.session_state.history:
            for result in entry['results']:
                service = result['service']
                if service not in service_stats:
                    service_stats[service] = {'successes': 0, 'failures': 0, 'total_time': 0, 'count': 0}
                
                if result['success']:
                    service_stats[service]['successes'] += 1
                    service_stats[service]['total_time'] += result['elapsed']
                    service_stats[service]['count'] += 1
                else:
                    service_stats[service]['failures'] += 1
        
        # Create dataframe
        df_data = []
        for service, stats in service_stats.items():
            avg_time = stats['total_time'] / max(stats['count'], 1)
            success_rate = (stats['successes'] / max(stats['successes'] + stats['failures'], 1)) * 100
            df_data.append({
                'Service': service,
                'Successes': stats['successes'],
                'Failures': stats['failures'],
                'Avg Speed (ms)': round(avg_time, 2),
                'Success Rate (%)': round(success_rate, 1)
            })
        
        df = pd.DataFrame(df_data)
        df = df.sort_values('Avg Speed (ms)')
        
        st.dataframe(df, use_container_width=True)
        
        # Best service recommendation
        best_service = df.iloc[0]['Service']
        st.success(f"🏆 **Recommended Service:** {best_service} (Fastest average speed)")
    else:
        st.info("📊 No data yet. Shorten some URLs to see analytics!")

with tab3:
    st.header("📜 Link History")
    
    if st.session_state.history:
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()
        
        for entry in st.session_state.history[:10]:  # Show last 10
            with st.expander(f"🔗 {entry['original_url'][:50]}... - {entry['timestamp']}"):
                st.text(f"Original: {entry['original_url']}")
                st.markdown("**Shortened URLs:**")
                for result in entry['results']:
                    if result['success']:
                        st.text(f"• {result['service']}: {result['short_url']} ({result['elapsed']}ms)")
        
        # Export option
        if st.button("📥 Export History as CSV"):
            export_data = []
            for entry in st.session_state.history:
                for result in entry['results']:
                    if result['success']:
                        export_data.append({
                            'Original URL': entry['original_url'],
                            'Service': result['service'],
                            'Short URL': result['short_url'],
                            'Speed (ms)': result['elapsed'],
                            'Timestamp': entry['timestamp']
                        })
            
            df_export = pd.DataFrame(export_data)
            csv = df_export.to_csv(index=False)
            st.download_button("Download CSV", csv, "link_history.csv", "text/csv")
    else:
        st.info("📜 No history yet. Start shortening URLs!")

with tab4:
    st.header("⚙️ Batch URL Processing")
    st.write("Shorten multiple URLs at once!")
    
    batch_urls = st.text_area("Enter URLs (one per line):", height=200, placeholder="https://example.com/url1\nhttps://example.com/url2\nhttps://example.com/url3")
    
    batch_service = st.selectbox("Choose service for batch:", ['ShortURL.at', 'is.gd', 'v.gd', 'clck.ru', 'ulvis.net'])
    
    if st.button("🚀 Process Batch"):
        urls = [url.strip() for url in batch_urls.split('\n') if url.strip()]
        valid_urls = [url for url in urls if is_valid_url(url)]
        
        if valid_urls:
            service_map = {
                'ShortURL.at': shorten_url_shorturlat,
                'is.gd': shorten_url_isgd,
                'v.gd': shorten_url_vgd,
                'clck.ru': shorten_url_clckru,
                'ulvis.net': shorten_url_ulvis
            }
            
            service_func = service_map[batch_service]
            progress = st.progress(0)
            results_container = st.container()
            
            batch_results = []
            for idx, url in enumerate(valid_urls):
                short_url, elapsed, success = service_func(url)
                batch_results.append({
                    'original': url,
                    'short': short_url if success else 'Failed',
                    'success': success
                })
                progress.progress((idx + 1) / len(valid_urls))
                time.sleep(0.5)  # Rate limiting
            
            with results_container:
                df_batch = pd.DataFrame(batch_results)
                st.dataframe(df_batch, use_container_width=True)
                
                # Download results
                csv_batch = df_batch.to_csv(index=False)
                st.download_button("📥 Download Results", csv_batch, "batch_results.csv", "text/csv")
        else:
            st.error("❌ No valid URLs found!")

# Sidebar
with st.sidebar:
    st.header("ℹ️ About Link Shortener Pro")
    
    st.markdown("""
    ### 🌟 Premium Features
    
    ✅ **Multi-Service Generation**
    - Get 5 different short links instantly
    - Compare speeds and reliability
    
    ✅ **Smart Testing**
    - Auto-verify each link works
    - See redirect chains
    
    ✅ **QR Code Generation**
    - Instant QR codes for all links
    - Download as PNG
    
    ✅ **Performance Analytics**
    - Track success rates
    - Find fastest services
    
    ✅ **Batch Processing**
    - Shorten multiple URLs
    - Export results
    
    ✅ **Link History**
    - Save all shortened links
    - Export as CSV
    """)
    
    st.markdown("---")
    st.markdown("**Presented by NCRA-CMS Lab**")
    
    st.markdown("---")
    st.info("💡 **Pro Tip:** The fastest service changes based on your location and current server load!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 1rem;'>
    <p><strong>🔗 NCRA Link Shortener Pro</strong> - The World's Most Advanced URL Shortener</p>
    <p>✨ Features: Multi-service generation • Live testing • QR codes • Analytics • Batch processing</p>
    <p>💼 Professional tool by NCRA-CMS Lab</p>
</div>
""", unsafe_allow_html=True)
