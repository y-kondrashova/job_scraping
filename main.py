from scraping import WorkUaScraper, save_data_to_csv, RobotaUAScraper
from scraping.config import TECHNOLOGIES
search_work_ua_url = "https://www.work.ua/jobs-python/"
search_robota_ua_url = "https://robota.ua/zapros/python/ukraine"

if __name__ == '__main__':
    scraper_1 = WorkUaScraper(search_work_ua_url, TECHNOLOGIES)
    data_1 = scraper_1.get_job_list()
    save_data_to_csv(data_1, "jobs")
    scraper_2 = RobotaUAScraper(search_robota_ua_url, TECHNOLOGIES)
    data_2 = scraper_2.get_job_list()
    save_data_to_csv(data_2, "jobs")
