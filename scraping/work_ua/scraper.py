import time

import requests
from bs4 import BeautifulSoup

from ..config import safe_extract


class WorkUaScraper:
    BASE_URL = "https://www.work.ua"

    def __init__(self, url: str, technologies: list, delay: int = 2) -> None:
        self.url = url
        self.technologies = technologies
        self.delay = delay
        self.soup = None

    def _fetch_page(self, url: str) -> None:
        try:
            response = requests.get(url, timeout=10)
            self.soup = BeautifulSoup(response.text, "html.parser")
        except requests.RequestException:
            self.soup = None

    def _get_company(self) -> str:
        company_img = self.soup.find("span", title="Дані про компанію")
        company_tag = company_img.find_next_sibling("a")
        return company_tag.find("span").text.strip()

    def _get_location(self) -> str:
        location_label = self.soup.find("span", title="Адреса роботи")
        location = location_label.findParent("li").text.strip()
        return location.split()[0].replace(",", "")

    def _get_salary(self) -> str:
        salary_img = self.soup.find("span", title="Зарплата")
        salary = salary_img.find_next_sibling("span").text.strip()
        return salary.replace("\u2009", " ").replace("\u202F", " ")

    def _get_skills(self) -> str:
        skills = set()
        for skill in self.soup.find_all("li", class_="label-skill"):
            if skill.text.strip() in self.technologies:
                skills.add(skill.text.strip())

        for description in self.soup.find("div", id="job-description"):
            for word in description.text.split():
                if word in self.technologies:
                    skills.add(word)
        return ", ".join(skills)

    def _get_details(self, url: str) -> dict:
        self._fetch_page(url)

        if not self.soup:
            return {}

        return {
            "company": safe_extract(self._get_company),
            "location": safe_extract(self._get_location),
            "salary": safe_extract(self._get_salary),
            "skills": safe_extract(self._get_skills),
        }

    def _get_next_page(self) -> str | None:
        self._fetch_page(self.url)
        pagination = self.soup.find("ul", class_="pagination")
        if pagination:
            next_str = pagination.find(string="Наступна")
            next_page_tag = next_str.findParent(
                "a",
                href=True,
                class_="link-icon"
            )
            if next_page_tag:
                return self.BASE_URL + next_page_tag.get("href")
        return None

    def get_job_list(self) -> list[dict]:
        job_list = []

        while self.url:
            self._fetch_page(self.url)
            for job in self.soup.find_all("div", class_="job-link"):
                title_tag = job.find("h2", class_="my-0")
                title = title_tag.text.strip() if title_tag else None

                link_tag = job.find("a", href=True)
                link = link_tag.get("href")

                if link:
                    link = self.BASE_URL + link
                    additional_info = self._get_details(link)
                    job_list.append(
                        {
                            "title": title,
                            "link": link,
                            **additional_info,
                        }
                    )
                time.sleep(self.delay)
            self.url = self._get_next_page()

        return job_list
