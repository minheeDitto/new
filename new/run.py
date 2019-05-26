from scrapy.crawler import CrawlerProcess
from new.spiders.ad import AdSpider
from scrapy.utils.project import get_project_settings

spider = get_project_settings()
m = CrawlerProcess(spider)
m.crawl(AdSpider)
m.start()
