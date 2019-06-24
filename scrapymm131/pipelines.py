# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
import re

class Scrapymm131Pipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for img_url in item['album_URLs']:
            yield Request(img_url, meta={'albumName': item['album_name']})

    def file_path(self, request, response=None, info=None):
        album_name = request.meta['albumName']
        album_name = re.sub(r'[\\*|“<>:/()0123456789]', '', album_name)
        image_guid = request.url.split('/')[-1]
        filename = u'full/{0}/{1}'.format(album_name, image_guid)

        return filename

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem('Item contains no images')
        # item['image_paths'] = image_path
        item['album_URLs'] = image_path
        return item
