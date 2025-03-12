import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Keywords to search
keywords = [
    "Ship","Weapon","Launcher", "Torpedo", "Rocket", "Sonar", "Fin Stabilizer",
    "Low Frequency Variable Depth Sonar", "Winch System", "Fire Control System",
    "Mast Hoisting Gear", "Future Combat System", "Helicopter Traversing system", "Gun",
    "Waterjet Propulsion System", "Submarine", "Sonar Dome", "Degaussing system",
    "Electric Propulsion", "Gear Box", "Hangar Shutter", "Radar Mast",
    "Controllable Pitch propeller", "Shafting", "Propulsion",
    "Radar", "Modular Bridge", "Hangar Door"
]

# Path to ChromeDriver
driver_path = r'C:\Users\20353979\Downloads\chromedriver-win64\chromedriver.exe'

# Directory to store extracted data
output_directory = r"C:\Users\20353979\Desktop\Intern Rohit\DEFPROC_SEL\output_bids"
os.makedirs(output_directory, exist_ok=True)

# Configure Chrome options
options = webdriver.ChromeOptions()

# Initialize WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Output CSV file
output_file = os.path.join(output_directory, "hindustan_data.csv")

# Write CSV headers
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Keyword", "e-Published Date", "Closing Date", "Opening Date", "Title", "Link", "Tender Reference Number", "Tender ID", "Organisation Chain"])

# Iterate through keywords
for keyword in keywords:
    try:
        # Open the website
        driver.get("https://eprocurehsl.nic.in/nicgep/app")
        time.sleep(2)  # Allow page to load

        # Find the search input field and enter the keyword
        search_box = driver.find_element(By.XPATH, '//*[@id="SearchDescription"]')
        search_box.clear()
        search_box.send_keys(keyword)

        # Click the search button
        search_button = driver.find_element(By.XPATH, '//*[@id="Go"]')
        search_button.click()
        time.sleep(5)  # Allow results to load

        # Extract all rows dynamically
        row_index = 0
        while True:
            try:
                # Dynamically generate xpaths for each field
                e_published_date_xpath = f'//*[@id="informal"]/td[2]' if row_index == 0 else f'//*[@id="informal_{row_index - 1}"]/td[2]'
                closing_date_xpath = f'//*[@id="informal"]/td[3]' if row_index == 0 else f'//*[@id="informal_{row_index - 1}"]/td[3]'
                opening_date_xpath = f'//*[@id="informal"]/td[4]' if row_index == 0 else f'//*[@id="informal_{row_index - 1}"]/td[4]'
                link_xpath = f'//*[@id="DirectLink_0"]' if row_index == 0 else f'//*[@id="DirectLink_0_{row_index - 1}"]'
                tender_info_xpath = f'//*[@id="informal"]/td[5]' if row_index == 0 else f'//*[@id="informal_{row_index - 1}"]/td[5]'
                organisation_chain_xpath = f'//*[@id="informal"]/td[6]' if row_index == 0 else f'//*[@id="informal_{row_index - 1}"]/td[6]'

                # Extract data using the xpaths
                e_published_date = driver.find_element(By.XPATH, e_published_date_xpath).text
                closing_date = driver.find_element(By.XPATH, closing_date_xpath).text
                opening_date = driver.find_element(By.XPATH, opening_date_xpath).text
                title = driver.find_element(By.XPATH, link_xpath).text  # Get text from <a></a>
                link = driver.find_element(By.XPATH, link_xpath).get_attribute("href")
                tender_info = driver.find_element(By.XPATH, tender_info_xpath).text
                organisation_chain = driver.find_element(By.XPATH, organisation_chain_xpath).text

                # Parse tender information
                tender_info_parts = tender_info.split("][")
                tender_reference_number = f"[{tender_info_parts[0].strip('[')}]"  # First bracket content
                tender_id = tender_info_parts[1].strip("]")  # Second bracket content

                # Remove title from Tender Reference Number if present
                if title in tender_reference_number:
                    tender_reference_number = tender_reference_number.replace(title, "").strip()

                # Append data to CSV
                with open(output_file, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([keyword, e_published_date, closing_date, opening_date, title, link, tender_reference_number, tender_id, organisation_chain])

                row_index += 1
            except Exception as e:
                # Break when no more rows are found
                print(f"No more rows to process for keyword '{keyword}'. Error: {e}")
                break
    except Exception as e:
        print(f"Error processing keyword '{keyword}': {e}")

# Close the driver
driver.quit()
print(f"Data extraction complete. Saved to {output_file}.")
