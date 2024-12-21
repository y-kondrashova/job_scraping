import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from ..config import safe_extract


class RobotaUAScraper:

    def __init__(self, url: str, technologies: list, delay: int = 1) -> None:
        self.url = url
        self.technologies = technologies
        self.delay = delay
        self.driver = None

    def _get_salary(self) -> str:
        return self.driver.find_element(
            By.CSS_SELECTOR, "[data-id*='salary']"
        ).text.strip()

    def _get_location(self) -> str:
        return self.driver.find_element(
            By.CSS_SELECTOR,
            '[data-id*="vacancy-city"]'
        ).text.strip()

    def _get_company(self) -> str:
        return self.driver.find_element(
            By.CSS_SELECTOR,
            "a[href*='company'] > span"
        ).text.strip()

    def _get_skills(self) -> str:
        description = self.driver.find_element(
            By.CSS_SELECTOR,
            '[id*="description"]'
        ).text
        description = " ".join(description.split())
        skills = {word for word in self.technologies if
                  word in description}
        return ", ".join(skills)

    def _get_details(self, url) -> dict:
        self.driver.execute_script("window.open('');")
        tabs = self.driver.window_handles
        self.driver.switch_to.window(tabs[-1])
        self.driver.get(url)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(self.delay)

            return {
                "company": safe_extract(self._get_company),
                "location": safe_extract(self._get_location),
                "salary": safe_extract(self._get_salary),
                "skills": safe_extract(self._get_skills),
            }

        finally:
            self.driver.close()
            self.driver.switch_to.window(tabs[0])

    def _get_next_page(self) -> None:
        next_button = self.driver.find_element(By.CSS_SELECTOR, "a.next")
        if next_button.is_enabled():
            next_button.click()
            time.sleep(self.delay)


    def get_job_list(self) -> list[dict]:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        service = webdriver.ChromeService(options=chrome_options)
        self.driver = webdriver.Chrome(service=service)
        self.driver.get(self.url)

        job_list = []

        try:
            body = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            while True:
                time.sleep(self.delay)
                body.send_keys(Keys.SPACE)
                jobs_list_container = body.find_element(
                    By.TAG_NAME,
                    "alliance-jobseeker-desktop-vacancies-list"
                )
                for job in jobs_list_container.find_elements(
                    By.CSS_SELECTOR,
                    "a.card"
                ):
                    title = job.find_element(
                        By.CSS_SELECTOR,
                        "h2"
                    ).text.strip()
                    link = job.get_attribute("href")
                    details = self._get_details(link)

                    job_list.append(
                        {
                            "title": title,
                            "link": link,
                            **details,
                        }
                    )

                try:
                    self._get_next_page()
                except NoSuchElementException:
                    break

        finally:
            self.driver.quit()
            return job_list
