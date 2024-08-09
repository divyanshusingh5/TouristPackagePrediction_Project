def merge_json_chunks(json_list, chunk_size=15):
    # Flatten the list of JSON objects into a single list of dictionaries
    merged_list = []
    for json_obj in json_list:
        merged_list.extend(json_obj)  # Assuming each JSON object in the list is a dictionary

    # Create chunks
    chunks = []
    index = 0

    while index < len(merged_list):
        # Take a chunk of the specified size or the remaining items if fewer
        chunk = merged_list[index:index + chunk_size]
        chunks.append(chunk)
        index += chunk_size

    return chunks

# Example usage
json_list = [
    [{"body": {"background-color": "#f0f0f0", "color": "#333"}}],
    [{"h1": {"font-size": "2em", "margin-bottom": "0.5em"}}],
    # Add more JSON objects here
]

chunks = merge_json_chunks(json_list)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i + 1}:")
    print(chunk)
"""

css_json = extract_css_to_json(css_string)
print(css_json)
