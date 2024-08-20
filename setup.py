from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Selenium options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless Chrome (optional)
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional)
chrome_options.add_argument("--no-sandbox")  # Disable sandboxing (optional)

# Initialize the WebDriver using webdriver_manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def extract_code_from_link(link):
    """Extracts code from the provided link."""
    driver.get(link)
    wait = WebDriverWait(driver, 10)
    
    try:
        # Wait for the content with class 'my-4' to be present
        content_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.my-4"))
        )
        
        # Extract pre and code elements
        pre_elements = content_element.find_elements(By.CSS_SELECTOR, "pre.language-html")
        code_elements = content_element.find_elements(By.CSS_SELECTOR, "code.language-html")
        
        code_snippets = []
        for pre in pre_elements:
            code_snippets.append(pre.text)
        for code in code_elements:
            code_snippets.append(code.text)
        
        return code_snippets

    except TimeoutException:
        return [f"Timed out waiting for code snippets on {link}"]
    except NoSuchElementException as e:
        return [f"Element not found on {link}: {e}"]
    except ElementClickInterceptedException as e:
        return [f"Error clicking on element at {link}: {e}"]
    except StaleElementReferenceException as e:
        return [f"Stale element reference on {link}: {e}"]

# Define output file
output_file = 'output.txt'

# Base URL
base_url = 'https://bootstrapshuffle.com/classes'

# Initialize WebDriver (e.g., Chrome)
driver.get(base_url)  # Navigate to the base URL

# Create a WebDriverWait instance
wait = WebDriverWait(driver, 10)

# Counter for tracking card index
card_index_counter = 0

with open(output_file, 'w') as file:
    while True:
        try:
            # Wait for card elements to be present
            card_elements = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.card"))
            )

            if not card_elements:
                break

            # Process cards starting from the current counter index
            for card_index in range(card_index_counter, len(card_elements)):
                try:
                    # Re-locate card header to avoid StaleElementReferenceException
                    card_element = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, f"div.card:nth-of-type({card_index + 1})"))
                    )
                    card_header = card_element.find_element(By.CSS_SELECTOR, "h5.card-header").text

                    # Extract list group items
                    list_group_elements = card_element.find_elements(By.CSS_SELECTOR, "div.list-group.list-group-flush a")
                    
                    # Check if there are list group items
                    if list_group_elements:
                        list_group_items = [(item.text, item.get_attribute('href')) for item in list_group_elements]
                    else:
                        list_group_items = []

                    file.write(f"Card Header: {card_header}\n")
                    file.write("List Group Items:\n")
                    for item_text, item_link in list_group_items:
                        file.write(f"- {item_text}\n")
                        if item_link:
                            file.write(f"  - Extracting code from: {item_link}\n")
                            code_snippets = extract_code_from_link(item_link)
                            for snippet in code_snippets:
                                file.write(f"    Code snippet:\n{snippet}\n")

                    # Update the card index counter after successful processing
                    card_index_counter = card_index + 1

                except (NoSuchElementException, ElementClickInterceptedException) as e:
                    file.write(f"Error processing card at index {card_index}: {e}\n")
                    # Move to the next card after an error
                    card_index_counter = card_index + 1
                    break

                # Wait a bit before processing the next card
                time.sleep(1)

            # Break the loop if all cards have been processed
            if card_index_counter >= len(card_elements):
                break

        except Exception as e:
            # Log exception and navigate back to the base URL
            file.write(f"Exception occurred: {e}. Navigating back to base URL.\n")
            driver.get(base_url)
            time.sleep(5)  # Wait a bit before retrying

# Close the WebDriver
driver.quit()
