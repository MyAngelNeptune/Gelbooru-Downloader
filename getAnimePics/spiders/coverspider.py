# import the packages
from getAnimePics.items import GetanimepicsItem
import datetime
import scrapy

class CoverSpider(scrapy.Spider):
    name = "pyimagesearch-cover-spider"
    allowed_domains = ['gelbooru.com/']
    start_urls = ["https://gelbooru.com/index.php?page=post&s=list&tags=solo+tomoe_gozen_%28fate%2Fgrand_order%29+rating%3Asafe&pid=84"] 

    def parse(self, response):
        #For every thumbnail, extract the image link from under the span a attribute
        #for url in response.xpath("//div[@class='thumbnail-preview']"):
        #    yield scrapy.Request(response.css("span a::attr(href)").extract_first(), self.parse_images)
        url = response.css("span a::attr(href)").extract()
        for item in zip(url):
            imageLink = ''.join(item)
            imageLink = "https:" + imageLink
            yield scrapy.Request(imageLink, self.parse_images)
    def parse_images(self, response):
        imageUrl = response.css("img::attr(src)").extract()
        yield GetanimepicsItem(image_urls=[imageUrl])


            


