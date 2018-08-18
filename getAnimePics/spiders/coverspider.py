# import the packages
from getAnimePics.items import GetanimepicsItem
import datetime
import scrapy

class CoverSpider(scrapy.Spider):
    name = "gelbooruSearch"
    allowed_domains = ['gelbooru.com']
    start_urls = ["https://gelbooru.com/index.php?page=post&s=list&tags=solo+tomoe_gozen_%28fate%2Fgrand_order%29+rating%3Asafe&pid=0"]
    custom_settings = {
        "ITEM_PIPELINES": {'scrapy.pipelines.images.ImagesPipeline': 1},
        "IMAGES_STORE": '\Users\KelvinK\Pictures\Tomoe'
    }
    def parse(self, response):
        #For every thumbnail, extract the image link from under the span a attribute
        url = response.css("span a::attr(href)").extract()
        urlList = zip(url)
        #Gets every url in the list and then makes them into a string 
        for item in urlList:
            imageLink = ''.join(item)
            imageLink = "https:" + imageLink
            #Once the link is converted into a string, it uses it as the URL and calls parse_images
            yield scrapy.Request(imageLink, callback=self.parse_images)


    def parse_images(self, response):
        imageUrl = response.css("img::attr(src)").extract()
        realUrl = ''.join(imageUrl)
        #Converts the URL into a string and places it in images_urls, which is used to download the image
        yield GetanimepicsItem(image_urls=[realUrl])


            


