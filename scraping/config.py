from selenium.common import NoSuchElementException

TECHNOLOGIES = [
    "Python", "Django", "Web API", "Flask", "FastAPI", "Pyramid", "Tornado",
    "Bottle", "AWS", "RoboDK", "API", "Azure", "Google Cloud Platform",
    "Docker", "Kubernetes", "Terraform", "Ansible", "Celery", "Redis",
    "RabbitMQ", "Apache Kafka", "SQL", "PostgreSQL", "MySQL", "SQLite",
    "MongoDB", "Excel", "Elasticsearch", "SQLAlchemy", "BigQuery", "Peewee",
    "Jenkins", "GitLab CI", "CircleCI", "Travis CI", "Sentry", "New Relic",
    "Grafana", "Prometheus", "pytest", "unittest", "coverage.py", "tox",
    "requests", "httpx", "aiohttp", "BeautifulSoup", "Selenium", "Scrapy",
    "Pytest-Django", "Flask-RESTful", "REST API", "DRF", "Pydantic",
    "Marshmallow", "OpenCV", "TensorFlow", "PyTorch", "scikit-learn", "Keras",
    "NLTK", "spaCy", "Jupyter", "Matplotlib", "Seaborn", "Plotly", "Dash",
    "Pygame", "Pandas", "NumPy", "SciPy", "SymPy", "ML", "CI/CD", "GIT",
    "GitHub", "JavaScript", "React",
]


def safe_extract(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except (AttributeError, NoSuchElementException):
        return None
