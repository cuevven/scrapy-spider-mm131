# -*- coding: utf-8 -*-
import scrapy
import uuid
import re
from scrapymm131.items import Scrapymm131Item


class Mm131Spider(scrapy.Spider):
    name = 'mm131'
    allowed_domains = ['www.mm131.net', 'mm131.me']
    start_urls = [
    #     'https://www.mm131.net/xinggan',
        'https://www.mm131.net/qingchun',
    #     'https://www.mm131.net/xiaohua',
    #     'https://www.mm131.net/chemo',
    #     'https://www.mm131.net/qipao',
    #     'https://www.mm131.net/mingxing'
    ]

    def parse(self, response):
        
        albums = response.css('.list-left>dd:not(.page)')
        for album in albums:

            alubm_url = album.css('a').attrib['href']

            yield scrapy.Request(alubm_url, callback=self.content)

        # 读取下一页的图集
        next_url = response.css('.page-en:nth-last-child(2)').attrib['href']
        if next_url is not None:
            yield response.follow(next_url, callback=self.parse)


    def content(self, response):
        item = Scrapymm131Item()
        album_channel = response.url.split('/')[-2]
        album_origin_id = str(int(response.css('.content-pic img').attrib['src'].split('/')[-2]))
        album_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, album_channel + album_origin_id))
        album_name = response.css('.content>h5::text').get()
        album_name = re.sub(r'[\\*|“<>:/()0123456789]', '', album_name)
        item['album_origin_id'] = album_origin_id
        item['album_channel'] = album_channel
        item['uuid'] = album_uuid
        item['album_name'] = album_name
        # 地址必须是一个 list
        item['album_URLs'] = response.css('.content-pic img::attr(src)').getall()
        item['referer'] = response.url
        item['artwork_src_prefix'] = album_channel + '/' + album_origin_id
        # item['artwork_src_prefix'] = album_uuid
        
        yield item

        # 处理下一页的图片
        next_url = response.css('.page-ch:last-child').attrib['href']
        if next_url is not None:
            yield response.follow(next_url, callback=self.content)
