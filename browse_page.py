import json
import threading
from data_process import Data_Processing
from selen_browser import open_page
from bs4 import BeautifulSoup
import requests
import datetime

text_processing = Data_Processing()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}


def extract_headlines(soup, body_element):
    tag = body_element.get('tag')
    class_name = body_element.get('class')

    headlines = soup.find_all(tag, class_=class_name)
    return headlines


def parse_news(source):
    source_name = source['source']
    url = source['url']
    pattern = source['pattern']

    response = requests.get(url, headers=headers)

    if pattern == 'selenium':
        soup = open_page(url)
    else:
        soup = BeautifulSoup(response.content, 'html.parser')

    body_elements = source['bodyelement']

    for body_element in body_elements:
        headlines = extract_headlines(soup, body_element)
        for headline in headlines:
            link_element = headline.find_next('a')
            link = link_element.get('href')
            domain = source['domain']
            if not link.startswith(domain):
                source_link = domain + link
            else:
                source_link = link
            data = link_element.text
            get_summary = text_processing.summary_parser(source_link)
            clean_headline = text_processing.text_process(data)
            clean_summary = text_processing.text_process(get_summary)
            result = {
                'headline': clean_headline,
                'source': source_name,
                'text': clean_summary,
                'shortDiscription': "",
                'link': source_link,
                'pubDate': "",
                'news_PubDate': "",
                'is_insert': True
            }
            return result


def main():
    with open('json_config.json') as json_file:
        config = json.load(json_file)

    threads = []
    for source in config['website_details']:
        thread = threading.Thread(target=parse_news, args=(source,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
