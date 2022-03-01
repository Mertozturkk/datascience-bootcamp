import requests
from bs4 import BeautifulSoup
import json
from time import sleep
import logging
import pandas as pd


class Crawler:
    """
    Crawler class for crawling the web.
    """
    def __init__(self, url, pages):
        logging.basicConfig(level=logging.INFO)
        self.url = url
        self.comments = []
        self.pages = pages

    def gets_comments(self):
        """
        Gets comments from the given url

        """
        page_count = 0
        comment_count = 0
        while page_count < self.pages:
            page_count += 1
            sleep(4)
            logging.info(f'{self.url} sayfasının yorumları alınıyor...')  # we use logging, because we want to see the progress
            logging.info("Page: {}".format(page_count))
            response = requests.get(self.url + str(page_count))
            datatext = BeautifulSoup(response.text, 'html.parser').text
            data = json.loads(datatext)
            content_list = data['result']['productReviews']['content']
            for comment in content_list:
                comment_count += 1
                comment_text = comment['comment']  # comment text
                rate = comment['rate']  # comment rate
                self.comments.append(dict(comment=comment_text, rate=rate))  # we add the comment to the list
        logging.info("Total comment count: {}".format(comment_count))
        return self.comments

    @classmethod
    def create_dataframe(cls, data):
        df = pd.DataFrame(data)
        df.columns = ['comment', 'rate']

        return df


