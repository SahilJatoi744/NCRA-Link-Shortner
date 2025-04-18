import streamlit as st
import pyshorteners

# Set up the Streamlit app
st.title("Link Shortener")

# Add an image in the header
image_url = "images.png"  # Replace with your image URL
st.image(image_url, use_column_width=True)

# Display "Presented by NCRA-CMS Lab"
st.markdown("<h5 style='text-align: center; color: gray;'>Presented by NCRA-CMS Lab</h5>", unsafe_allow_html=True)

# Adding a description
st.write("""
This app helps you shorten long URLs into easy-to-share short links.
Just paste the URL below and click on "Shorten URL!"
""")

# Ask the user to input a URL
url = st.text_input("Enter the URL you want to shorten:")

# Initialize the URL shortener
s = pyshorteners.Shortener()

# Create a button to shorten the URL
if st.button("Shorten URL"):
    if url:
        try:
            # Shorten the URL using TinyURL
            short_url = s.tinyurl.short(url)
            st.success(f"Your shortened URL: {short_url}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please enter a valid URL.")
