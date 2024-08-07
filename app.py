import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = 'API'

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

# Function to convert CSS to Tailwind CSS using OpenAI API
def convert_css_to_tailwind(css_chunk):
    prompt = f"""
    Transform the provided traditional CSS into Tailwind CSS. Ensure a thorough conversion while maintaining visual fidelity and responsiveness.

    *CSS Code:*
    {css_chunk}

    *Instructions:*
    - Convert the provided CSS to Tailwind CSS utility classes.
    - Provide a list of Tailwind CSS classes that correspond to the original CSS classes.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in converting CSS to Tailwind CSS."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.5
    )
    
    return response.choices[0].message['content'].strip()

# Function to apply Tailwind CSS to HTML using OpenAI API
def apply_tailwind_to_html(html_chunk, class_mapping):
    class_mapping_str = "\n".join([f"{k} => {v}" for k, v in class_mapping.items()])
    
    prompt = f"""
    Apply the provided Tailwind CSS classes to the existing HTML structure. Ensure the visual appearance and responsiveness are preserved.

    *HTML Code:*
    {html_chunk}

    *Tailwind CSS Classes Mapping:*
    {class_mapping_str}

    *Instructions:*
    - Replace old CSS class names in the HTML with the corresponding Tailwind utility classes.
    - Ensure that the visual appearance and responsiveness are preserved as closely as possible.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in applying Tailwind CSS to HTML."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.5
    )
    
    return response.choices[0].message['content'].strip()

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
