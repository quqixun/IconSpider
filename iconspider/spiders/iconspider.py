import scrapy
from iconspider.items import IconSpiderItem


class IconSpider(scrapy.Spider):
    name = "icon-spider"
    start_urls = ["http://www.flaticon.com"]

    page_num = 1
    MAX_PAGE_NUM = 11
    ROOT_PAGE = ""

    def parse(self, response):
        var = "//a[@id='link-menu-top-icons']/@href"
        url = response.xpath(var).extract_first()

        yield scrapy.Request(url, self.parse_page)

    def parse_page(self, response):
        if self.page_num == 1:
            self.ROOT_PAGE = response.url

        var = "//li[@data-premium='0']//div[@class='overlay']/a/@href"
        urls = response.xpath(var).extract()

        for url in urls:
            yield scrapy.Request(url, self.parse_icon)

        self.page_num += 1

        if self.page_num <= self.MAX_PAGE_NUM:
            var = "//a[@class='btn pagination-next']/@href"
            next_page = response.xpath(var).extract_first()
            no = [(int(i)) for i in next_page.split('/') if i.isdigit()]
            next_page = self.ROOT_PAGE + "/" + str(no[0])

            yield scrapy.Request(next_page, self.parse_page)

    def parse_icon(self, response):
        var = "//div[@class='main-icon']/img/@src"
        url = response.xpath(var).extract()

        yield IconSpiderItem(file_urls=url)

# scrapy crawl icon-spider -o icon_url.json
