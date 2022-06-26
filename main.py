from spiders.CISASpider import CisaSpider
from spiders.CertFrAvisSpider import CertFrAvisSpider
from spiders.CertFrAlerteSpider import CertFrAlerteSpider
from scrapy.crawler import CrawlerProcess
from datetime import datetime

def main():
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    item = f"""## CyberOwl \n> Last Updated {now} \n\n
A daily updated summary of the most frequent types of security incidents currently being reported from different sources.\n\n"""

    with open("docs/README.md", "w") as f:
        f.write(item)
        f.close()

    try:
        process = CrawlerProcess()
        process.crawl(CertFrAvisSpider)
        process.crawl(CertFrAlerteSpider)
        process.crawl(CisaSpider)
        process.start()

    except Exception:
        raise ValueError("Error in the spiders!")

if __name__ == "__main__":
    main()
