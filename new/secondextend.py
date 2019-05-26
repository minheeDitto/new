from scrapy import signals
import time
from twisted.internet import task
from scrapy.exceptions import NotConfigured

class Latencies:

    def __init__(self,interval):
        self.interval = interval
        self.latency, self.proc_latency,self.downloader, self.items = 0, 0, 0, 0

    @classmethod
    def from_crawler(cls,crawler):
        interval = crawler.settings.get("LATENTIME")
        if not interval:
            raise NotConfigured
        ext = cls(interval=interval)
        crawler.signals.connect(ext.spider_openned,signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed,signal=signals.spider_closed)
        crawler.signals.connect(ext.request_scheduled,signal=signals.request_scheduled)
        crawler.signals.connect(ext.response_downloaded,signal=signals.response_downloaded)
        crawler.signals.connect(ext.response_received,signal=signals.response_received)
        crawler.signals.connect(ext.item_scraped,signal=signals.item_scraped)
        return ext

    def spider_openned(self,spider):
        self.task = task.LoopingCall(self._log,spider)
        self.task.start(self.interval)

    def spider_closed(self,spider,reason):
        if self.task.running:
            self.task.stop()

    def request_scheduled(self,request,spider):
        request.meta["schedule_time"] = time.time()

    def response_downloaded(self,response,request,spider):
        request.meta["receved_downloader"] = time.time()

    def response_received(self,response,request,spider):
        request.meta["receved_time"] = time.time()

    def item_scraped(self,item,response,spider):
        self.latency += time.time() - response.meta['schedule_time']
        self.proc_latency += time.time() - response.meta['receved_time']
        self.downloader += time.time() -response.meta["receved_downloader"]

        self.items += 1




    def _log(self,spider):
        irate = float(self.items) / self.interval
        latency = self.latency / self.items if self.items else 0
        proc_latency = self.proc_latency / self.items if self.items else 0
        downloader = self.downloader / self.items if self.items else 0

        spider.logger.info(("Scraped %d items at %.1f items/s, avg latency: "
                            "%.2f s and avg time in pipelines: %.2f s %.2f s") %
                           (self.items, irate, latency, proc_latency, downloader))

        self.latency, self.proc_latency, self.items = 0, 0, 0





