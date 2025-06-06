import time
import json
import os
import signal
import sys
import random
import traceback
import socket
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import database
from database import Database

WEBSITES = [
    # websites of your choice
    "https://cse.buet.ac.bd/moodle/",
    "https://google.com",
    "https://prothomalo.com",
]

TRACES_PER_SITE = 1000
FINGERPRINTING_URL = "http://localhost:5000" 
OUTPUT_PATH = "dataset.json"

# Initialize the database to save trace data reliably
database.db = Database(WEBSITES)

""" Signal handler to ensure data is saved before quitting. """
def signal_handler(sig, frame):
    print("\nReceived termination signal. Exiting gracefully...")
    try:
        database.db.export_to_json(OUTPUT_PATH)
    except:
        pass
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


"""
Some helper functions to make your life easier.
"""

def is_server_running(host='127.0.0.1', port=5000):
    """Check if the Flask server is running."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

def setup_webdriver():
    """Set up the Selenium WebDriver with Chrome options."""
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def retrieve_traces_from_backend(driver):
    """Retrieve traces from the backend API."""
    traces = driver.execute_script("""
        return fetch('/api/get_results')
            .then(response => response.ok ? response.json() : {traces: []})
            .then(data => data.traces || [])
            .catch(() => []);
    """)
    
    count = len(traces) if traces else 0
    print(f"  - Retrieved {count} traces from backend API" if count else "  - No traces found in backend storage")
    return traces or []

def clear_trace_results(driver, wait):
    """Clear all results from the backend by pressing the button."""
    clear_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Clear all results')]")
    clear_button.click()

    wait.until(EC.text_to_be_present_in_element(
        (By.XPATH, "//div[@role='alert']"), "Cleared"))
    
def is_collection_complete():
    """Check if target number of traces have been collected."""
    current_counts = database.db.get_traces_collected()
    remaining_counts = {website: max(0, TRACES_PER_SITE - count) 
                      for website, count in current_counts.items()}
    return sum(remaining_counts.values()) == 0

"""
Your implementation starts here.
"""

def collect_single_trace(driver, wait, website_url):
    """ Implement the trace collection logic here. 
    1. Open the fingerprinting website
    2. Click the button to collect trace
    3. Open the target website in a new tab
    4. Interact with the target website (scroll, click, etc.)
    5. Return to the fingerprinting tab and close the target website tab
    6. Wait for the trace to be collected
    7. Return success or failure status
    """
    try:
        # Open the fingerprinting website
        driver.get(FINGERPRINTING_URL)
        time.sleep(1)

        # Verify the fingerprinting page is ready
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Collect trace')]")))
        
        # Click the button to collect trace
        collect_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Collect trace')]")))
        collect_button.click()

        # Open the target website in a new tab
        driver.execute_script(f"window.open('{website_url}', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])
            
        # More comprehensive interaction with the website for 15 seconds
        start_time = time.time()
        
        while time.time() - start_time < 10:  # Extended interaction time for better fingerprinting
            try:                    # Mix of interactions with more emphasis on mouse movement for better fingerprinting
                interactions = ["scroll", "scroll", "scroll", "scroll", "move", "move", "click"]
                interaction_type = random.choice(interactions)
                
                if interaction_type == "scroll":
                    # Random scrolling
                    scroll_distance = random.randint(100, 800)
                    scroll_direction = random.choice([-1, 1])
                    driver.execute_script(f"window.scrollBy(0, {scroll_direction * scroll_distance});")
                
                elif interaction_type == "move":
                    try:
                        # Generate random coordinates
                        x = random.randint(10, 800)
                        y = random.randint(10, 600)
                        
                        # Use JavaScript as a fallback
                        driver.execute_script(f"""
                            var e = new MouseEvent('mousemove', {{
                                'view': window,
                                'bubbles': true,
                                'cancelable': true,
                                'clientX': {x},
                                'clientY': {y}
                            }});
                            document.body.dispatchEvent(e);
                        """)
                    except:
                        pass
                
                elif interaction_type == "click":  # Already weighted in the selection
                    # Try to find clickable elements and click one
                    try:
                        elements = driver.find_elements(By.CSS_SELECTOR, 'a, button, input[type="button"], .btn')
                        if elements:
                            # Don't click links that might navigate away from the page
                            safe_elements = [e for e in elements if not e.get_attribute('href') or 
                                           e.get_attribute('href').startswith('#')]
                            if safe_elements:
                                random_element = random.choice(safe_elements)
                                driver.execute_script("arguments[0].scrollIntoView();", random_element)
                                # Click using JavaScript to avoid issues with element visibility
                                driver.execute_script("arguments[0].click();", random_element)
                    except:
                        pass  # Ignore click errors
                
                time.sleep(random.uniform(0.5, 1.5))  # Varying delay between interactions
            
            except Exception as e:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                return False

        # Return to the fingerprinting tab and close the target website tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        # Wait for the trace to be collected (give the fingerprinting page time to process)
        time.sleep(3)
        
        # Check if trace was collected by looking for confirmation element
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='alert'][contains(text(), 'collected')]")))
            return True
        except:
            print(f"  - No trace collection confirmation for {website_url}")
            return False
            
    except Exception as e:
        print(f"  - Error collecting trace for {website_url}")
        try:
            # If multiple tabs are open, ensure we return to the main tab
            if len(driver.window_handles) > 1:
                driver.close()  # Close current tab
                driver.switch_to.window(driver.window_handles[0])  # Switch to first tab
        except:
            pass
        return False

def collect_fingerprints(driver, target_counts=None):
    """ Implement the main logic to collect fingerprints.
    1. Calculate the number of traces remaining for each website
    2. Open the fingerprinting website
    3. Collect traces for each website until the target number is reached
    4. Save the traces to the database
    5. Return the total number of new traces collected
    """
    if target_counts is None:
        current_counts = database.db.get_traces_collected()
        target_counts = {website: max(0, TRACES_PER_SITE - count) 
                      for website, count in current_counts.items()}

    # Use a longer timeout for page loading operations
    wait = WebDriverWait(driver, 20)
    total_new_traces = 0
    collection_attempts = 0
    max_failed_attempts = 5
    consecutive_failures = 0
    
    # Round-robin collection across websites to distribute failures
    # Create a list of (website, remaining_count) tuples for active collection
    collection_queue = [(website, target_counts[website]) for website in WEBSITES if target_counts[website] > 0]
    
    print(f"Starting collection for {len(collection_queue)} websites with a total of {sum([count for _, count in collection_queue])} traces")
    
    # Collect traces in batches across all websites to maximize efficiency
    while collection_queue:
        # Process the first website in the queue
        website_url, remaining_traces = collection_queue.pop(0)
        
        print(f"Collecting trace for {website_url} ({TRACES_PER_SITE - remaining_traces + 1}/{TRACES_PER_SITE})")
        
        # Try to collect a trace
        success = collect_single_trace(driver, wait, website_url)
        collection_attempts += 1
        
        # Check for trace collection status
        if success:
            consecutive_failures = 0  # Reset consecutive failures counter on success
            remaining_traces -= 1
            
            # Save the newly collected traces
            new_traces = retrieve_traces_from_backend(driver)
            if new_traces:
                site_idx = WEBSITES.index(website_url)
                for trace in new_traces:
                    # Print abbreviated trace info for debugging (first 100 chars)
                    trace_summary = str(trace)[:100] + "..." if len(str(trace)) > 100 else str(trace)
                    print(f"  - Saved trace: {trace_summary}")
                    database.db.save_trace(website_url, site_idx, trace)
                total_new_traces += len(new_traces)
                
                # Clear traces after saving to avoid duplicates
                clear_trace_results(driver, wait)
        else:
            break  # Stop collection if a trace could not be collected
        
        # If we still need more traces for this website, add it back to the queue
        if remaining_traces > 0:
            collection_queue.append((website_url, remaining_traces))
        
    print(f"Collection finished with {total_new_traces} new traces")
    
    if consecutive_failures >= max_failed_attempts:
        print(f"Warning: Stopped collection after {max_failed_attempts} consecutive failures")
    
    return total_new_traces

def main():
    """ Implement the main function to start the collection process.
    1. Check if the Flask server is running
    2. Initialize the database
    3. Set up the WebDriver
    4. Start the collection process, continuing until the target number of traces is reached
    5. Handle any exceptions and ensure the WebDriver is closed at the end
    6. Export the collected data to a JSON file
    7. Retry if the collection is not complete
    """
    max_retries = 3
    retry_count = 0
    driver = None
    
    try:
        # Check if server is running before starting
        if not is_server_running():
            print("Flask server is not running. Please start the server first.")
            return

        # Initialize database
        database.db.init_database()
        print(f"Database initialized. Targeting {TRACES_PER_SITE} traces for each of {len(WEBSITES)} websites.")
        
        # Main collection loop with retries
        while retry_count < max_retries and not is_collection_complete():
            if retry_count > 0:
                print(f"\nRetry attempt {retry_count}/{max_retries}...")
                
            # Setup a fresh webdriver for each retry to avoid stale states
            if driver:
                try:
                    driver.quit()
                except:
                    pass
                    
            driver = setup_webdriver()
            if not driver:
                print("Failed to initialize WebDriver. Retrying...")
                retry_count += 1
                time.sleep(5)
                continue
                
            try:
                # Get current counts to show progress
                current_counts = database.db.get_traces_collected()
                total_collected = sum(current_counts.values())
                total_target = len(WEBSITES) * TRACES_PER_SITE
                print(f"Current progress: {total_collected}/{total_target} traces collected ({total_collected/total_target:.1%})")
                
                # Start collection
                new_traces = collect_fingerprints(driver)
                
                # Check if we need to retry
                if is_collection_complete():
                    print("Target number of traces reached!")
                    break
                elif new_traces == 0:
                    print("No new traces collected in this run. Retrying...")
                    retry_count += 1
                else:
                    print(f"Collection in progress. Continuing...")
                    # Only count as a retry if no progress was made
                    time.sleep(5)  # Brief pause between retries
            
            except Exception as e:
                print(f"Error during collection: {str(e)}")
                retry_count += 1
                time.sleep(10)  # Longer pause after an error
        
        # Final export to ensure all data is saved
        database.db.export_to_json(OUTPUT_PATH)
        
        # Report final status
        if is_collection_complete():
            print(f"\nCollection complete! Data exported to {OUTPUT_PATH}")
        else:
            print(f"\nWarning: Collection incomplete after {retry_count} retries.")
            print(f"Partial data exported to {OUTPUT_PATH}")
            print("You can run the script again to continue collection.")
            
        # Report statistics
        current_counts = database.db.get_traces_collected()
        for website, count in current_counts.items():
            print(f"  - {website}: {count}/{TRACES_PER_SITE} traces collected ({count/TRACES_PER_SITE:.1%})")
            
    except KeyboardInterrupt:
        print("\nCollection interrupted by user.")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        # Ensure data is saved even if interrupted
        try:
            database.db.export_to_json(OUTPUT_PATH)
            print(f"Data saved to {OUTPUT_PATH}")
        except Exception as e:
            print(f"Error saving data: {str(e)}")
    finally:
        # Clean up resources
        if driver:
            try:
                driver.quit()
                print("WebDriver closed.")
            except:
                pass

if __name__ == "__main__":
    main()
