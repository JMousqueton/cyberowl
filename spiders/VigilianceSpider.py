"""
This spider is used to scrape alerts from the following source:
https://vigilance.fr/?action=1135154048&langue=2
"""
import scrapy
from mdtemplate import Template
import re

# as per recommendation from @freylis, compile once only
CLEANR = re.compile('<.*?>') 

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

class VigilanceSpider(scrapy.Spider):
    """
    Spider for the OBS-Vigilance website.

    This spider is used to scrape data from the official website of
    OBS-Vigilance.

    Attributes:
        name : Name of the spider.
        max_items : The maximum number of items to scrape.
        start_url : The website from which to start crawling.
        block_selector : The CSS/XPATH selector of the block containing the data.
        link_selector : The CSS/XPATH selector of the link of the alert.
        title_selector : The CSS/XPATH selector of the title of the alert.
        date_selector : The CSS/XPATH selector of the date of creation of the alert.
        description_selector : The CSS/XPATH selector of the description of the alert.
    """

    name = "Vigilance"
    max_items = 10
    start_urls = ["https://vigilance.fr/?action=1135154048&langue=2"]
    block_selector = "article > table"
    link_selector = "descendant-or-self::tr/td/a/@href"
    date_selector = ""
    title_selector = "descendant-or-self::tr/td/a"
    description_selector = "descendant-or-self::tr/td/font/i/a/text()"

    def parse(self, response):
        """
        Parsing the response
        """
        _data = []
        for bulletin in response.css(self.block_selector):
            TITLE = bulletin.xpath(self.title_selector).get()
            LINK = bulletin.xpath(self.link_selector).get()
            DATE = "Visit link for details"
            DESC = bulletin.xpath(self.description_selector).get()


            ITEM = {
                "_title": cleanhtml(TITLE),
                "_link": cleanhtml(LINK),
                "_date": DATE,
                "_desc": DESC
            }

            _data.append(ITEM)


        _to_write = Template("VIGILANCE", _data)

        with open("docs/VIGILANCE.md", "w") as f:
            f.write(_to_write._fill_table())
            f.close()


        