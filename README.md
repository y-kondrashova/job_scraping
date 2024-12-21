# Job Scraping

This project implements a job scraper for www.work.ua and www.robota.ua to
analyze the top 10 required skills across job listings.

## Features

- Scrapes job listings from www.work.ua and www.robota.ua.
- Extracts and identifies the most frequently requested skills.
- Provides analysis and visualization of the top 10 required skills.

## Installation

Follow these steps to set up and run the scraper:

### 1. Clone the repo

```shell

git clone https://github.com/y-kondrashova/job_scraping.git

```

### 2. Change working directory

```shell

cd job_scraping
```

### 3. Create virtual environment

```shell

python3 -m venv .venv
```

### 4. Activate virtual environment

- On Linux/macOS:
    ```shell
    source .venv/bin/activate
    ```
- On Windows:
    ```shell
  
  .venv\Scripts\activate
  ```

### 5. Install requirements

```shell

pip install -r requirements.txt
```

### 6. Run the scraper

Run the main.py script to start scraping job data. This process may take some
time, depending on the volume of data.

```shell

python main.py
```

### 7. Analyze the results

Open the Jupyter Notebook [main.ipynb](main.ipynb) to view the analysis.
Execute all the cells to generate and explore the statistics.

```shell

jupyter notebook main.ipynb
```

## Notes

- Make sure you have Python 3.7+ installed.
- Ensure that your internet connection is stable during the scraping process.
- Install Jupyter Notebook if it is not already available on your system.

