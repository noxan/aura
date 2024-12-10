from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
import os
from environs import Env
import logging

env = Env()
env.read_env()


class OuraDownloader:
    def __init__(self, email: str, password: str) -> None:
        self.base_url: str = "https://cloud.ouraring.com"
        self.email: str = email
        self.password: str = password
        self.download_dir: str = os.path.join(os.path.dirname(__file__), "downloads")
        os.makedirs(self.download_dir, exist_ok=True)
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info("OuraDownloader initialized")

    def setup_driver(self) -> WebDriver:
        """Setup Chrome driver with custom download preferences"""
        self.logger.info("Setting up Chrome driver")
        options = webdriver.ChromeOptions()
        prefs: dict[str, str | bool] = {
            "download.default_directory": os.path.abspath(self.download_dir),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        }
        options.add_experimental_option("prefs", prefs)
        return webdriver.Chrome(options=options)

    def login(self, driver: WebDriver) -> None:
        """Login to Oura Cloud"""
        self.logger.info("Logging in to Oura Cloud")
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
        self.logger.info("Login successful")

    def download_csv_files(self, driver: WebDriver) -> None:
        """Download all CSV files from the profile page"""
        self.logger.info("Downloading CSV files from profile page")
        driver.get(f"{self.base_url}/profile/")

        # Wait for CSV links to be present
        csv_links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "a[download][type='text/csv']")
            )
        )

        for link in csv_links:
            href = link.get_attribute("href")
            if href:
                self.logger.info(f"Downloading CSV from: {href}")
                driver.get(href)
                # Add small delay to ensure download starts
                driver.implicitly_wait(1)

    def run(self) -> None:
        self.logger.info("Running OuraDownloader")
        driver = self.setup_driver()
        try:
            self.login(driver)
            self.download_csv_files(driver)
            self.logger.info("All downloads complete")
        finally:
            driver.quit()


if __name__ == "__main__":
    downloader = OuraDownloader(
        email=env.str("OURA_EMAIL"),
        password=env.str("OURA_PASSWORD"),
    )
    downloader.run()
