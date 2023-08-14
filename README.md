## Web Scraping Real Estate Data from alonhadat.com.vn

This repository contains a Python script for scraping real estate data from the alonhadat.com.vn website. The script utilizes the `requests` library for making HTTP requests, `BeautifulSoup` for HTML parsing, and `pandas` for data manipulation. It allows users to extract information about properties available for sale or rent and stores the data in CSV files.

### Prerequisites

- Python 3.x
- Required Python libraries: `requests`, `bs4` (BeautifulSoup), `pandas`

You can install the required libraries using the following command:

```
pip install requests beautifulsoup4 pandas
```

### How to Use

1. Clone this repository to your local machine.

2. Navigate to the repository's directory.

3. Open the `scraper.py` file in your preferred text editor or IDE.

4. Customize the parameters within the script's main section according to your preferences:
   - `options`: List of options to scrape ("can-ban" for sale, "cho-thue" for rent)
   - `fol_names`: Corresponding folder names for each option
   - `min_page_no`: Minimum page number to start scraping
   - `max_page_no`: Maximum page number to stop scraping

5. Run the script using the following command:

```
python scraper.py
```

The script will create folders and CSV files to store the scraped data. It will iterate through the specified options, pages, and property types, scraping information about each property. The data will be saved in separate CSV files for each page and merged into a final CSV file for each property type.

### Note

- The script simulates a user-agent to make requests appear like they come from a web browser.
- The time between requests is randomized to avoid overwhelming the server.
- If no data is found for a particular option, a `readme.txt` file will be created indicating the absence of information.

Please use this script responsibly and in compliance with the website's terms of use.
