def split_css_to_chunks(file_path, max_chunk_size=3500):
    with open(file_path, 'r') as file:
        css_content = file.read()

    chunks = []
    start_index = 0
    
    while start_index < len(css_content):
        # Determine the potential end of the chunk
        end_index = start_index + max_chunk_size
        
        # If end_index goes beyond the content length, adjust it
        if end_index >= len(css_content):
            chunks.append(css_content[start_index:])
            break
        
        # Find the last closing curly brace before or at the 3500th character
        end_index = css_content.rfind('}', start_index, end_index) + 1
        
        # If no closing brace is found, adjust the end index to max_chunk_size
        if end_index == 0:
            end_index = start_index + max_chunk_size

        # Add the chunk to the list
        chunks.append(css_content[start_index:end_index])
        
        # Move the start_index to the end of the current chunk
        start_index = end_index
    
    return chunks

# Example usage:
# chunks = split_css_to_chunks('path/to/your/style.css')
# for idx, chunk in enumerate(chunks):
#     print(f"Chunk {idx+1}:\n{chunk}\n")
