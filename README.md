# TikTok Ads Scraper

## Description
This TikTok Ads Scraper is designed to efficiently gather advertisements information from TikTok, utilizing Selenium for web scraping and BeautifulSoup for parsing the scraped HTML data. It captures various details such as ad ID, advertiser information, first and last shown dates, unique user views, target audience demographics, and more.

## Sample Output

This dataset specifically captures advertisements related to the keyword "fashion" within the UK over the past 7 days. Access the dataset [here](https://github.com/tarxn/tiktok-ads-scrapper/blob/main/output_data/tiktok_ads_data_UK_last7days_fashion.csv).

## Try out yourself

https://colab.research.google.com/drive/1y4CYFRUGo_OVbwFcb86oH7nlBTDSfL43?usp=sharing

------------------------------------------------------------------------------------------------------------------------------------------

## Features
- **Selenium WebDriver**: Automates web browser interaction to scrape dynamic content.
- **BeautifulSoup**: Parses HTML content to extract ad details.
- **Asyncio**: Manages asynchronous tasks for improved performance.
- **Apify SDK Integration**: Stores and manages scraped data on the Apify platform.

## Requirements
- Python 3.6+
- Selenium
- BeautifulSoup4
- Apify Python Client
- A WebDriver (e.g., ChromeDriver) compatible with your browser version

## Setup and Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/tiktok-ads-scraper.git
   cd tiktok-ads-scraper
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **WebDriver Setup:**
   - Download the WebDriver for your browser (e.g., ChromeDriver for Google Chrome) and place it in a known directory.
   - Ensure the path to the WebDriver is correctly set in the script or added to your system's PATH variable.

4. **Apify Setup:**
   - Create an account on [Apify](https://apify.com) and obtain your API token.
   - Update the `actor.json` file with your project details and Apify token.

## Usage
Update the `input_schema.json` with the start URLs and any other parameters you wish to customize for scraping. Then, run the scraper using:

```bash
python main.py
```

## Data Output
Scraped data is stored in the Apify dataset and can be accessed through the Apify platform. You can configure the output format (e.g., JSON, CSV) in the `actor.json` file.

## Contributing
Contributions to improve the TikTok Ads Scraper are welcome. Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

---

Remember to replace placeholders (like `https://github.com/your-username/tiktok-ads-scraper.git`) with actual links or information related to your project. This `README.md` provides a clear overview of your project and guides users through installation, setup, and usage, making your project more accessible and user-friendly.
