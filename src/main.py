import requests
import csv
import time
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from apify import Actor


async def main():
    async with Actor() as actor:
        input_data = await actor.get_input() or {}
        start_urls = input_data.get('start_urls', [])
        max_depth = input_data.get('max_depth', 1)

        dataset = await actor.open_dataset(name='tiktok-ads-data')

        for url_obj in start_urls:
            start_url = url_obj.get('url')
            if not start_url:
                continue
        # start_url="https://library.tiktok.com/ads?region=FR&start_time=1712082600000&end_time=1712169000000&adv_name=fashion&adv_biz_ids=&query_type=1&sort_type=last_shown_date,desc"

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')


        # Instantiate WebDriver
        driver = webdriver.Chrome(chrome_options)
        driver.get(start_url)

        try:
            driver.get(start_url)
            wait = WebDriverWait(driver, 10)  # Creating WebDriverWait instance
            while True:
                # Try clicking the "View More" button
                view_more_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".loading_more")))
                driver.execute_script("arguments[0].scrollIntoView();", view_more_button)  # Scroll to the button
                driver.execute_script("window.scrollBy(0, -100);")
                driver.execute_script("arguments[0].click();", view_more_button)
                # Optional: Wait for the content to load
                WebDriverWait(driver, 2).until(lambda d: d.find_element(By.CSS_SELECTOR, ".ad_card"))

        except (TimeoutException, NoSuchElementException):
            actor.log.info("All content loaded or button not found.")

        html= driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, 'html.parser')
        ad_links = soup.find_all('a', class_='link')
        # print(ad_links)

        ad_ids = [link['href'].split('=')[-1] for link in ad_links]
        # print(ad_ids)



        base_url = 'https://library.tiktok.com/ads/detail/?ad_id='
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
       
        for ad_id in ad_ids:
            ad_url = base_url + ad_id
            driver = webdriver.Chrome(chrome_options)
            driver.get(ad_url)

            time.sleep(2)
            ad_html = driver.page_source
            ad_soup = BeautifulSoup(ad_html, 'html.parser')
            details_tags = ad_soup.find_all('span', {'class': 'item_value'})

            advertiser = ad_soup.find('div', {'class': 'ad_advertiser_value'})
            if advertiser is None:
                advertiser = f"no advertiser available for ad_id: {ad_id}"
            else:
                advertiser = advertiser.text

            video_link_tag = ad_soup.find('video')
            if video_link_tag is None:
                video_link = f"no video available for ad_id: {ad_id}"
            else:
                video_link = video_link_tag['src']

            target_audience = ad_soup.find('span', {'class': 'ad_target_audience_size_value'})
            if target_audience is None:
                target_audience = f"no views available for ad_id: {ad_id}"
            else:
                target_audience = target_audience.text

            details_list = []
            for detail in details_tags:
                details_list.append(detail.text)

            rows = ad_soup.find_all('tbody', class_='byted-Table-Body')

            gender = []
            age = []
            country_list = []
            addn_parameters = []

            countries = rows[0].find_all('tr')
            for c in countries:
                cells = c.find_all('td')
                country = cells[1].text.strip()
                country_list.append(country)
                male, female, unknown = True, True, True
                if cells[2].find('path')['d'] == "M6 23a1 1 0 0 1 1-1h34a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1v-2Z":
                    male = False
                if cells[3].find('path')['d'] == "M6 23a1 1 0 0 1 1-1h34a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1v-2Z":
                    female = False
                if cells[4].find('path')['d'] == "M6 23a1 1 0 0 1 1-1h34a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1v-2Z":
                    unknown = False

                entry = {
                    'country': country,
                    'gender': {
                        'Male': male,
                        'Female': female,
                        'Unknown': unknown
                    }
                }
                gender.append(entry)

            countries = rows[1].find_all('tr')
            for c in countries:
                cells = c.find_all('td')
                country = cells[1].text.strip()
                ages = [True] * 6
                for i in range(6):
                    if cells[2 + i].find('path')['d'] == "M6 23a1 1 0 0 1 1-1h34a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1v-2Z":
                        ages[i] = False

                entry = {
                    'country': country,
                    'ages': {
                        '13-17': ages[0],
                        '18-24': ages[1],
                        '25-34': ages[2],
                        '35-44': ages[3],
                        '45-54': ages[4],
                        '55+': ages[5],
                    }
                }
                age.append(entry)

            param_rows = ad_soup.find_all('tr', class_="targeting_additional_parameters_table_row")

            entry = {}
            for p in param_rows:
                param = p.find('td', class_="targeting_additional_parameters_table_first_col")
                status = p.find('td', class_='')
                if status is not None:
                    entry[param.text] = status.text
                else:
                    entry[param.text] = 'None'

            addn_parameters.append(entry)
            writer.writerow([ad_id, advertiser, details_list[0], details_list[1],details_list[2],target_audience,country_list,gender,age,addn_parameters, video_link])
            await dataset.push_data({'ad_id':ad_id,'ad_advertiser': advertiser, 'first_shown':details_list[0], 'last_shown':details_list[1], 'unique_user_views':details_list[2], 'target_audience':target_audience,
                    'country_list':country_list,'gender': gender, 'age':age, 'additional_parameters':addn_parameters, 'video_link':video_link})
            
            driver.quit()


    # Disable urllib3 warnings

    # Export the data as CSV and JSON
    await dataset.export_to_csv('data.csv', to_key_value_store_name='my-key-value-store')

    # Print the exported records
    store = await actor.open_key_value_store(name='my-key-value-store')
    print(await store.get_value('data.csv'))
    # print(csv_data)
    # print(await store.get_value('data.json'))
    actor.log.info(f"Ad IDs: {ad_ids}")


def download_video(url, ad_id):
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        filename = f"{str(ad_id)}.mp4"
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        actor.log.info(f"{filename} downloaded successfully.")
    else:
        actor.log.info(f"Failed to download video from {url}. Status code: {response.status_code}")


if __name__ == "__main__":
    asyncio.run(main())

        # Example usage:
        # url = 'https://library.tiktok.com/api/v1/cdn/1712151504/video/aHR0cHM6Ly92NzcudGlrdG9rY2RuLmNvbS8zZjJiOWU5YmNhOGRlMGJjZjA3YmIwYWRiN2E3ZjE4Yi82NjBkYjAzOS92aWRlby90b3MvdXNlYXN0MmEvdG9zLXVzZWFzdDJhLXZlLTAwNjgtZXV0dHAvb01JRUtGbWVzQkM2RFVEOUVmeFJRUFFRRVd3aWdDaWRzNEpBUnQv/7cd4caab-916d-44c8-b3b9-34c155a810e1?a=475769&bti=PDU2NmYwMy86&ch=0&cr=0&dr=1&cd=0%7C0%7C0%7C0&cv=1&br=3876&bt=1938&cs=0&ds=6&ft=.NpOcInz7Th4FkErXq8Zmo&mime_type=video_mp4&qs=0&rc=aGg7ZmY3NTdnNDxnOzNoZ0BpM3RsO2s5cnFmcjMzZjczM0BjLmJiLTUxXjQxNDUxXy9hYSNkbWZjMmRjMTJgLS1kMWNzcw%3D%3D&vvpl=1&l=20240403133823D8EDE6F40EAE406831A7&btag=e00088000&cc=13'
        # ad_id = 123
        # download_video(url, ad_id)

