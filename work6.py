from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
import time
import datetime
import csv

# Initialize the WebDriver (Make sure to set the path to your WebDriver)
#service_obj = Service("./chromedriver")
#driver = webdriver.Chrome(service=service_obj)



# Initialize the WebDriver in headless mode
service_obj = Service("./chromedriver")
options = webdriver.ChromeOptions()
#options.add_argument('--headless')  # Run in headless mode 
driver = webdriver.Chrome(service=service_obj, options=options)



driver.minimize_window()

# Step 1: Ask the user for a stock number
stock_number = input("Enter stock number (e.g. 00941.hk): ")
print('Initializing... please wait, be patient...')

# Extract the first five digits of the stock code
stock_code_prefix = stock_number[:5]

# Generate the filename based on the current date and stock code prefix
current_date = datetime.datetime.now().strftime("%Y%m%d")
filename = f"{current_date}_{stock_code_prefix}.csv"

# Create or open the CSV file and write the header if it doesn't exist
file_exists = False
try:
    with open(filename, 'r'):
        file_exists = True
except FileNotFoundError:
    pass

with open(filename, 'a', newline='') as file:
    writer = csv.writer(file)
    if not file_exists:
        # Write header
        writer.writerow(["Timestamp", "Label", "Price"])

# not applicable for headless mode

driver.maximize_window()

time.sleep(1)  # Wait for the window to maximize

    # Step 3: Get the screen width
screen_width = driver.execute_script("return window.screen.width;")
screen_height = driver.execute_script("return window.screen.height;")

    # Step 4: Set the desired width and height for the popup
popup_width = 400  # Desired width of the popup
popup_height = 600  # Desired height of the popup

# Step 5: Calculate the position for the right side of the screen
x_position = screen_width - popup_width
y_position = (screen_height - popup_height) // 2  # Center vertically

# Step 6: Open the popup (for demonstration purposes, we can just click a link)
# Replace with the actual action that opens a popup
# Example: driver.find_element(By.LINK_TEXT, "Open Popup").click()

    # Set the size and position of the window
driver.set_window_size(popup_width, popup_height)
driver.set_window_position(x_position, y_position)

time.sleep(1)  # Wait for the window to maximize
    

try:
    while True:
        # Step 2: Visit Google
        driver.get('https://www.google.com')

        # Step 3: Input the stock number into the search box
        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys('https://hk.finance.yahoo.com/quote/'+stock_number)
        search_box.submit()

        # Step 4: Wait for the next page to load and display results
        try:
            first_result = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'h3'))
            )
            first_result.click()  # Click the first search result

        except TimeoutException:
            print("Error: Timeout while waiting for the search results to load.")
            continue  # Retry on error

        # Step 5: Wait for the stock prices to load and extract them
        try:
            stock_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@data-field="regularMarketPrice"]'))
            )

            # Prepare output with specific labels
            stock_prices = []
            #if len(stock_elements) > 0:
            #    stock_prices.append(("Hang Seng Index", stock_elements[0].text))
            if len(stock_elements) > 6:  # Check if there is a 7th item
                stock_prices.append((stock_number, stock_elements[6].text))

            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            # Print and write the specified items with labels
            with open(filename, 'a', newline='') as file:
                writer = csv.writer(file)
                for label, price in stock_prices:
                    output = [now, label, price]
                    print(f"{now} {label}: {price}")
                    writer.writerow(output)

            print('----------------------------------------------------')

        except TimeoutException:
            print("Error: Timeout while waiting for the stock price elements to load.")

        # Wait for a short time before the next iteration
        time.sleep(10)  # Adjust the time as needed

finally:
    # Close the driver
    driver.quit()