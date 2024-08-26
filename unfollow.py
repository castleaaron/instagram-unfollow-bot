from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Load the list of usernames from ITY.html
def load_usernames(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        usernames = [tag.text.strip() for tag in soup.find_all('a')]  # Extract text from <a> tags
    return usernames

# Set up Chrome options to add a user-agent
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# Initialize the web driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get('https://www.instagram.com/accounts/login/')

# Log in to Instagram
time.sleep(2)  # Wait for the page to load

username_input = driver.find_element(By.NAME, 'username')
password_input = driver.find_element(By.NAME, 'password')

username_input.send_keys('')  # Replace with your Instagram username
password_input.send_keys('')  # Replace with your Instagram password
password_input.send_keys(Keys.RETURN)


for i in range(20):
    print(i)
    time.sleep(1)

# Load usernames from ITY.html
usernames = load_usernames('ITY.html')

# Unfollow users starting from the bottom of the list
for username in reversed(usernames):
    driver.get(f'https://www.instagram.com/{username}/')
    time.sleep(2)  # Wait for the page to load

    try:
        unfollow_button = driver.find_element(By.XPATH, "//button[contains(., 'Following')]")
        unfollow_button.click()
        time.sleep(2)  # Wait for the unfollow confirmation dialog

        confirm_button = driver.find_element(By.XPATH, "//span[contains(., 'Unfollow')]")
        confirm_button.click()
        time.sleep(2)  # Wait for the unfollow action to complete
    except Exception as e:
        print(f'Failed to unfollow {username}')

driver.quit()