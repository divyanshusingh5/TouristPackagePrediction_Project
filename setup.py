Sure, here's a simple Python function that uses regular expressions to extract class names and their content from a CSS file. It reads the CSS file, finds all the class definitions, and stores them in a list named `chunks` with the class name as the key and the content as the value.

```python
import re

def extract_css_classes(file_path):
    chunks = []
    
    # Read the CSS file
    with open(file_path, 'r') as file:
        css_content = file.read()
    
    # Regular expression to match CSS class definitions
    class_pattern = re.compile(r'\.([a-zA-Z0-9_-]+)\s*\{([^}]*)\}')
    
    # Find all matches in the CSS content
    matches = class_pattern.findall(css_content)
    
    # Store the class names and content in chunks
    for match in matches:
        class_name, class_content = match
        chunks.append({class_name: class_content.strip()})
    
    return chunks

# Example usage:
# file_path = 'path/to/your/cssfile.css'
# result = extract_css_classes(file_path)
# print(result)
```

Here's how this function works:
1. It reads the entire content of the CSS file.
2. It uses a regular expression to find all class definitions. The regular expression looks for patterns that start with a dot (`.`) followed by the class name, some optional whitespace, and then curly braces `{}` containing the class content.
3. It finds all matches and extracts the class names and their corresponding content.
4. It stores each class name and its content as a dictionary in the `chunks` list.

You can call this function with the path to your CSS file, and it will return the list of class names and their content.
