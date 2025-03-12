import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select

# Path to your ChromeDriver
driver_path = r'C:\Users\20353979\Downloads\chromedriver-win64\chromedriver.exe'

# Directory to store extracted data
output_directory = r"C:\Users\20353979\Desktop\Intern Rohit\DEFPROC_SEL\output_bids_gem"
os.makedirs(output_directory, exist_ok=True)

# Path to the CSV file for saving bid data
csv_file_path = os.path.join(output_directory, 'bid_data_gem_portal.csv')

# Function to initialize the CSV file with headers
def initialize_csv():
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Bid Number", "Link", "Information", "Start Date", "End Date"])

# Function to load existing bid numbers from the CSV file
def load_existing_bids():
    if os.path.exists(csv_file_path):
        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header row
            return {row[0] for row in reader}  # Collect bid numbers from the first column
    return set()

# Function to save bid data to the CSV file
def save_bid_data_to_csv(bid_data):
    with open(csv_file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(bid_data)

# Configure Chrome options
options = webdriver.ChromeOptions()

# Initialize WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    # Initialize CSV file and load existing bids
    initialize_csv()
    processed_bids = load_existing_bids()

    # Open the website
    driver.get("https://bidplus.gem.gov.in/advance-search")

    # Wait for the "Search by Ministry / Organization" tab to be clickable and click on it
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "ministry-tab"))
    ).click()

    # Wait for the Ministry dropdown to be visible
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ministry"))
    )

    # Select "Ministry of Defence" from the dropdown
    ministry_dropdown = Select(driver.find_element(By.ID, "ministry"))
    ministry_dropdown.select_by_visible_text("MINISTRY OF DEFENCE")

    # Find the search button and click it
    search_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//a[@id="searchByBid" and @onclick="searchBid(\'ministry-search\')"]'))
    )
    driver.execute_script("arguments[0].click();", search_button)

    # Wait for the results to load
    time.sleep(5)

    # Pagination loop
    while True:
        # Process bid cards on the current page (from div[2] to div[11])
        for index in range(2, 12):  # Bid card indexes
            try:
                bid_number_xpath = f'//*[@id="bidCard"]/div[{index}]/div[1]/p[1]/a'
                primary_information_xpath = f'//*[@id="bidCard"]/div[{index}]/div[3]/div/div[1]'
                secondary_information_xpath = f'//*[@id="bidCard"]/div[{index}]/div[3]/div/div[1]/div[1]/a'
                start_date_xpath = f'//*[@id="bidCard"]/div[{index}]/div[3]/div/div[3]/div[1]/span'
                end_date_xpath = f'//*[@id="bidCard"]/div[{index}]/div[3]/div/div[3]/div[2]/span'

                # Extract bid number and link
                bid_number_element = driver.find_element(By.XPATH, bid_number_xpath)
                bid_number = bid_number_element.text.strip()
                link = bid_number_element.get_attribute('href')

                # Skip already processed bids
                if bid_number in processed_bids:
                    continue

                # Check for secondary XPath; if present, use it; otherwise, use the primary XPath
                information = ""
                try:
                    information_element = driver.find_element(By.XPATH, secondary_information_xpath)
                    information = information_element.get_attribute('data-content').strip()
                except:
                    try:
                        information_element = driver.find_element(By.XPATH, primary_information_xpath)
                        information = information_element.text.strip()
                    except:
                        print(f"No information found for bid card index {index}")

                # Extract start date and end date
                start_date_element = driver.find_element(By.XPATH, start_date_xpath)
                start_date = start_date_element.text.strip()

                end_date_element = driver.find_element(By.XPATH, end_date_xpath)
                end_date = end_date_element.text.strip()

                # Save the extracted data to the CSV file
                save_bid_data_to_csv([bid_number, link, information, start_date, end_date])

                # Mark bid as processed
                processed_bids.add(bid_number)

            except Exception as e:
                print(f"Error extracting data for card index {index}: {e}")

        # Find and click the "Next" button in pagination
        try:
            next_button = driver.find_element(By.XPATH, '//a[contains(@class, "page-link next")]')
            if "disabled" in next_button.get_attribute("class"):
                print("Reached the last page.")
                break
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(5)  # Adjust as necessary to allow the page to load
        except Exception as e:
            print(f"Error navigating to next page: {e}")
            break

finally:
    # Close the browser
    driver.quit()
