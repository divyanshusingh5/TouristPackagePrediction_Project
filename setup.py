import cssutils
import json

def extract_css_to_json(css_string):
    # Initialize the CSS parser
    parser = cssutils.CSSParser()
    stylesheet = parser.parseString(css_string)
    
    # Dictionary to store the extracted styles
    css_dict = {}

    # Iterate through the CSS rules
    for rule in stylesheet:
        if rule.type == rule.STYLE_RULE:
            selector = rule.selectorText
            styles = {}
            for property in rule.style:
                styles[property.name] = property.value
            css_dict[selector] = styles

    # Convert the dictionary to JSON
    css_json = json.dumps(css_dict, indent=4)
    
    return css_json

# Example usage
css_string = """
body {
    background-color: #f0f0f0;
    color: #333;
}
h1 {
    font-size: 2em;
    margin-bottom: 0.5em;
}
"""

css_json = extract_css_to_json(css_string)
print(css_json)
