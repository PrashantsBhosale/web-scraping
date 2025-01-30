import requests
from bs4 import BeautifulSoup
import re
import json
import datetime

class Data_Processing:

    def summary_parser(self, link):
        response = requests.get(link)
        print(link)

        soup = BeautifulSoup(response.text, 'html.parser')

        with open('json_config.json') as json_file:
            config = json.load(json_file)

            for site_config in config['website_details']:
                summary_text = []

                summary_tags = site_config['summary_tags']

                for body_element in summary_tags:
                    tag = body_element.get('sum_tag')
                    class_name = body_element.get('sum_class')

                    try:
                        full_text = soup.find_all(tag, class_=class_name)
                        for data in full_text:
                            summary_t = data.text
                            summary_text.append(summary_t)
                    except:
                        pass
                    finally:
                        try:
                            summary = soup.find(tag, class_=class_name).text
                            summary_text.append(summary)
                        except:
                            pass

                full_summary = "".join(summary_text)

                return full_summary

    def text_process(self,headline=None):

        if headline is not None:
            clean_string = re.sub('[^a-zA-Z0-9\s?,."@$%!&]+', '', headline)

            return clean_string
