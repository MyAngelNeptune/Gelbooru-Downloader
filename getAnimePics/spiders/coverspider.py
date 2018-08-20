# import the packages
from getAnimePics.items import GetanimepicsItem
import datetime
import scrapy

pageNumber = 0

class CoverSpider(scrapy.Spider):
    name = "gelbooruSearch"
    allowed_domains = ['gelbooru.com']
    start_urls = ["https://gelbooru.com/index.php?page=post&s=list&tags=dengeki&pid=0"]
    custom_settings = {
        "ITEM_PIPELINES": {'scrapy.pipelines.images.ImagesPipeline': 1},
        "IMAGES_STORE": 'D:\Cute anime girls\Test'
    }

    def request(self, url, callback):
        request = scrapy.Request(url=url, callback=callback)
        request.cookies['resize-original'] = "1"
        request.cookies['resize-notification'] = "1"
        request.headers['User-Agent'] = ('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, '
            'like Gecko) Chrome/45.0.2454.85 Safari/537.36')
        return request

    def parse(self, response):
        parsing = False
        #Starts on first page and increases the page number once every image is downloaded
        imagesPerPage = 42
        #For every thumbnail, extract the image link from under the span a attribute
        url = response.css("span a::attr(href)").extract()
        urlList = zip(url)
        #Gets every url in the list and then makes them into a string 
        for item in urlList:
            parsing = True
            imageLink = ''.join(item)
            imageLink = "https:" + imageLink
            #Once the link is converted into a string, it uses it as the URL and calls parse_images
            yield self.request(imageLink, callback=self.parse_images)
     
        nextUrl = response.url.split("&pid=")
        global pageNumber
        pageNumber += 1
        nextPage = nextUrl[0] + "&pid=" + str(pageNumber * imagesPerPage)
        if parsing:
            yield self.request(nextPage, callback=self.parse)
        else:
            raise CloseSpider('Done looking')
        
    def parse_images(self, response):
        #this is real bad
        imageUrl = response.css("img::attr(src)").extract_first()
        tempUrl = ''.join(imageUrl)
        #hard code found the xpath on gelbooru seems to be the same for every image though
        list = response.xpath("/html/body/div[4]/div[5]/script[2]/text()").extract()
        tempString = ''.join(list)
        #extracts part of the hd image url, not sample
        tempString = tempString[(tempString.index('\'img\'')):(tempString.index('\', \'base_dir'))]
        image = tempString.split('\'img\':\'')
        image = ''.join(image[1])
        #replaces the imageurl if it is a sample
        realUrl = tempUrl.replace("samples", "images")
        realUrl = realUrl.split("sample_")
        finalUrl = realUrl[0] + image
        #Converts the URL into a string and places it in images_urls, which is used to download the image
        yield GetanimepicsItem(image_urls=[finalUrl])


            


