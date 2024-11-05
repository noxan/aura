from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv


class OuraDownloader:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        self.base_url = "https://cloud.ouraring.com"

    def setup_driver(self):
        """Setup Chrome driver with custom download preferences"""
        options = webdriver.ChromeOptions()
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)
        return webdriver.Chrome(options=options)

    def login(self, driver):
        """Login to Oura Cloud"""
        driver.get(f"{self.base_url}/user/sign-in")
        
        # Wait for email input and enter credentials
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_input.send_keys(self.email)
        
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(self.password)
        
        # Click login button
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        # Wait for successful login
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(),'Today')]"))
        )
        

    def run(self):
        driver = self.setup_driver()
        self.login(driver)
        driver.get(f"{self.base_url}/account/export/daily-sleep/csv")


if __name__ == "__main__":
    load_dotenv()

    downloader = OuraDownloader(
        email=os.getenv("OURA_EMAIL"),
        password=os.getenv("OURA_PASSWORD")
    )
    downloader.run()