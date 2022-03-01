from crawler import *
from url_list import url_list as urls
import pandas as pd


def main():
    comment_list = []
    for url in urls:
        comments = Crawler(url=url, pages=100).gets_comments()
        comment_list.extend(comments)
    dataframe = Crawler.create_dataframe(comment_list)
    dataframe.to_csv("comments.csv")


if __name__ == '__main__':
    main()
