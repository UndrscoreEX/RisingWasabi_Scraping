# -*- coding: utf-8 -*-
from typing import TypeGuard
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

# As there is no consistent layout of the link between Eng - Japanese versions of the articles, this list contains all of the variations I have seen of the English link.
names = ["English Version", "See English", "See English Version", "[English Version]", "English", "[English]", "[See English Version]", "[See English]"]

class RisingspiderSpider(CrawlSpider):
    name = 'RisingSpider'
        # crawl pages: 
    start_urls = [f'https://www.therisingwasabi.com/%e6%97%a5%e6%9c%ac%e8%aa%9e/page/{nums}/' for nums in range(0,13)]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="td_module_10 td_module_wrap td-animation-stack"]/div/a'), callback='parse_item', follow=True),
    )


    # Check for link to English version of the current article and then passes this item into the next function
    def parse_item(self, response):
        urltoEng =""
        for link in response.xpath('//div/p//a'):
            if link.xpath('.//text()').get() in names:
                try:
                    urltoEng = link.xpath('./@href').get()
                    print("-----------we found it----------------------")
                except: 
                    print("something didnt work")
        title = response.xpath('//header/h1/text()').get()
        bodyJP = response.xpath('//div[@class="td-post-content td-pb-padding-side"]/p/text()').getall()
        
        if urltoEng != "":
        
            jpobject = {
                'JP title': title,
                'JP Body text' : "\n".join(bodyJP),
                'Url (JP)' : response.request.url,
                'Url (eng)': urltoEng 
            }
            # if there is an english link, bring all Japanese text into the next function so that both can be printed together
            return response.follow(urltoEng, callback=self.parseEnglish, cb_kwargs= {'Item' : jpobject})
    
    def parseEnglish(self, response, Item):
        title = response.xpath('//header/h1/text()').get()
        bodyEng = response.xpath('//div[@class="td-post-content td-pb-padding-side"]/p/text()').getall()
        print("we made it to the english one")

        Item['English Title'] = title
        Item['English Body'] = "\n".join(bodyEng)
        print(Item)
        yield Item