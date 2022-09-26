import scrapy
from mdtemplate import Template
from datetime import date
import re

# as per recommendation from @freylis, compile once only
CLEANR = re.compile('<.*?>') 

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

class VulDBSpider(scrapy.Spider):
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

    name = "VulDB"
    max_items = 10
    start_urls = ["https://vuldb.com/?live.recent"]
    block_selector = "table>tr"
    link_selector = "descendant-or-self::td[4]//@href"
    date_selector = "descendant-or-self::td[1]//text()"
    title_selector = "descendant-or-self::td[4]//text()"
    description_selector = ""


    def parse(self, response):
        """
        Parsing the response
        """
        _data = []
        for bulletin in response.css(self.block_selector):
            TITLE = bulletin.xpath(self.title_selector).get()
            LINK = "https://vuldb.com/" +  str(bulletin.xpath(self.link_selector).get())
            DATE = str(date.today()) + " at " + str(bulletin.xpath(self.date_selector).get())
            DESC = "Visit link for details"

            if not TITLE:
                continue

            ITEM = {
                "_title": TITLE,
                "_link": LINK,
                "_date": DATE,
                "_desc": DESC
            }

            _data.append(ITEM)


        _to_write = Template("VULDB", _data)

        with open("docs/VULDB.md", "w") as f:
            f.write(_to_write._fill_table())
            f.close()


        