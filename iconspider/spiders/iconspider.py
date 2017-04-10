# Created by Qixun Qu
# quqixun@gmail.com
# 2017/04/09
#


# The whole process is as follows:
# 1. Start from the main page
# 2. Get the page that contains popular icons
# 3. Scan each thumbicon and get the link access
#    to the url of large icon
# 4. Read next page, repeat step 3 until there is
#    no next page or get the maximum number of pages
#    we want to access
# 5. Download all found icons


import scrapy
from iconspider.items import IconSpiderItem


# Set the maximum number of pages that will be
# scanned to download icons
MAX_PAGE_NUM = 3604


class IconSpider(scrapy.Spider):
    # Name the spider
    name = "icon-spider"

    # Indicate the start page
    start_urls = ["http://www.flaticon.com"]

    # Record how many pages has been scanned
    page_num = 0

    # Save the root url of page that contains
    # thumbicons
    root_page = ""

    def parse(self, response):
        # Step 1 & 2
        var = "//a[@id='link-menu-top-icons']/@href"
        url = response.xpath(var).extract_first()

        yield scrapy.Request(url, self.parse_page)

    def parse_page(self, response):
        # Keep the root url, it will be used to form
        # other pages' urls
        self.page_num += 1
        if self.page_num == 1:
            self.root_page = response.url

        # Step 3
        var = "//li[@data-premium='0']//div[@class='overlay']/a/@href"
        urls = response.xpath(var).extract()

        for url in urls:
            yield scrapy.Request(url, self.parse_icon)

        # Step 4
        if self.page_num <= MAX_PAGE_NUM:
            var = "//a[@class='btn pagination-next']/@href"
            next_page = response.xpath(var).extract_first()
            # Form url of thumbicon pages
            no = [(i) for i in next_page.split('/') if i.isdigit()]
            next_page = self.root_page + "/" + no[0]

            yield scrapy.Request(next_page, self.parse_page)

    def parse_icon(self, response):
        # Step 5
        var = "//div[@class='main-icon']/img/@src"
        url = response.xpath(var).extract()

        yield IconSpiderItem(file_urls=url)

# Run this instruction in Terminal
# scrapy crawl icon-spider -o icon_url.json
