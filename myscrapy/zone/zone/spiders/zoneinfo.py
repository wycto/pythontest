# -*- coding: utf-8 -*-
import scrapy


class ZoneinfoSpider(scrapy.Spider):
    name = 'zoneinfo'
    allowed_domains = ['www.stats.gov.cn']
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html']

    domain = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/"

    # 此方法用于抓取省份信息
    def parse(self, response):
        provinces = response.xpath("//tr[@class='provincetr']/td/a")
        for province in provinces:
            name = province.xpath("./text()").extract_first()
            href = province.xpath("./@href").extract_first()
            url = self.domain + href
            print(1,name,href[0:2],url)
            yield scrapy.Request(url,callback=self.parse_prefecture)

    #此方法用于抓取地州信息
    def parse_prefecture(self, response):
        prefectures = response.xpath("//tr[@class='citytr']")
        for prefecture in prefectures:
            code = prefecture.xpath("./td[1]/a/text()").extract_first()
            name = prefecture.xpath("./td[2]/a/text()").extract_first()
            href = prefecture.xpath("./td[2]/a/@href").extract_first()
            if href != None:
                url = self.domain + href
                print(2, name,code, url)
                yield scrapy.Request(url, callback=self.parse_county)
            # yield {
            #     'code':code,
            #     'name':name,
            #     'href':href
            # }
        pass

    # 此方法用于抓取县级市信息
    def parse_county(self, response):
        countys = response.xpath("//tr[@class='countytr']")
        for county in countys:
            code = county.xpath("./td[1]/a/text()").extract_first()
            name = county.xpath("./td[2]/a/text()").extract_first()
            href = county.xpath("./td[2]/a/@href").extract_first()
            if href!=None:
                url = self.domain + code[0:2] + "/" + href
                print(3, name,code, url)
                yield scrapy.Request(url, callback=self.parse_town)
        pass

    # 此方法用于抓取乡镇信息
    def parse_town(self, response):
        towns = response.xpath("//tr[@class='towntr']")
        for town in towns:
            code = town.xpath("./td[1]/a/text()").extract_first()
            name = town.xpath("./td[2]/a/text()").extract_first()
            href = town.xpath("./td[2]/a/@href").extract_first()
            if href != None:
                url = self.domain + code[0:2] + "/" + code[2:4] + "/" + href
                print(4, name, code, url)
                yield scrapy.Request(url, callback=self.parse_town)
        pass

    # 此方法用于抓取村信息
    def parse_town(self, response):
        towns = response.xpath("//tr[@class='villagetr']")
        for town in towns:
            code = town.xpath("./td[1]/text()").extract_first()
            vcode = town.xpath("./td[2]/text()").extract_first()
            name = town.xpath("./td[3]/text()").extract_first()
            print(5, name, code)
        pass
