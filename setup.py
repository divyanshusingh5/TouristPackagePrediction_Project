import streamlit as st
import requests

# Set your AiDE API key
aide_key = "<generate_it_from_settings>"
aide_url = "https://aide-sdlc-backend.imagine.tech/api/v1/brownfield"

headers = {
    "Authorization": f"Bearer {aide_key}",
    "Content-Type": "application/json"
}

# Function to read file content in chunks
def read_file_in_chunks(file, chunk_size=4000):
    """Read a file in chunks and decode bytes to string."""
    content = ""
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
        content += chunk.decode('utf-8')  # Decode bytes to string
    return content

# Function to convert CSS to Tailwind CSS using AiDE API
def convert_css_to_tailwind(css_chunk):
    prompt = f"""
    Transform the following traditional CSS into Tailwind CSS utility classes. Ensure the conversion is accurate, preserving visual fidelity and responsiveness.

    CSS Code:
    {css_chunk}

    Instructions:
    - Convert each CSS property to the appropriate Tailwind CSS utility class.
    - For colors, ensure to use the closest Tailwind color.
    - For background images and other properties not directly translatable to Tailwind, indicate how to handle them or suggest a Tailwind equivalent if available.
    """
    
    data = {
        "model": "aide",
        "messages": [
            {"role": "system", "content": "You are an expert in converting CSS to Tailwind CSS."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1500,
        "temperature": 0.5
    }

    try:
        response = requests.post(aide_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.error(f"Error converting CSS: {e}")
        return ""

# Function to apply Tailwind CSS to HTML using AiDE API
def apply_tailwind_to_html(html_chunk, class_mapping):
    class_mapping_str = "\n".join([f"{k} => {v}" for k, v in class_mapping.items()])
    
    prompt = f"""
    Apply the provided Tailwind CSS classes to the existing HTML structure. Ensure that all visual aspects and responsiveness are preserved.

    HTML Code:
    {html_chunk}

    Tailwind CSS Classes Mapping:
    {class_mapping_str}

    Instructions:
    - Replace old CSS class names in the HTML with the corresponding Tailwind utility classes.
    - Ensure that background images, colors, and other CSS properties are handled correctly and visual appearance is preserved.
    """
    
    data = {
        "model": "aide",
        "messages": [
            {"role": "system", "content": "You are an expert in applying Tailwind CSS to HTML."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1500,
        "temperature": 0.5
    }

    try:
        response = requests.post(aide_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.error(f"Error applying Tailwind CSS to HTML: {e}")
        return ""

# Streamlit UI
st.title("CSS to Tailwind CSS Converter")

uploaded_css_file = st.file_uploader("Upload CSS File", type=["css"])
uploaded_html_file = st.file_uploader("Upload HTML File", type=["html"])

if st.button("Convert"):
    if uploaded_css_file is not None and uploaded_html_file is not None:
        st.write("Processing files...")

        # Read CSS and HTML files in chunks
        css = read_file_in_chunks(uploaded_css_file)
        html = read_file_in_chunks(uploaded_html_file)

        # Split CSS into chunks
        chunk_size = 4000
        css_chunks = [css[i:i + chunk_size] for i in range(0, len(css), chunk_size)]
        html_chunks = [html[i:i + chunk_size] for i in range(0, len(html), chunk_size)]

        # Convert CSS chunks to Tailwind classes
        tailwind_mapping = {}
        for css_chunk in css_chunks:
            mapping = convert_css_to_tailwind(css_chunk)
            # Parse and aggregate Tailwind classes mapping
            for line in mapping.split('\n'):
                if '=>' in line:
                    css_class, tailwind_class = map(str.strip, line.split('=>'))
                    tailwind_mapping[css_class] = tailwind_class
        
        # Apply Tailwind CSS to HTML chunks
        converted_html = ""
        for html_chunk in html_chunks:
            converted_html += apply_tailwind_to_html(html_chunk, tailwind_mapping)

        st.write("Converted HTML with Tailwind CSS:")
        st.code(converted_html, language='html')

        # Save the converted HTML
        st.download_button("Download Converted HTML", data=converted_html, file_name="converted.html", mime="text/html")
    else:
        st.warning("Please upload both CSS and HTML files to proceed.")
