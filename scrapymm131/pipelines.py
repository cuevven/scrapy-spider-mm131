# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
from scrapymm131.items import Album, Artwork, create_tables, db
import re
import uuid

class Scrapymm131Pipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for img_url in item['album_URLs']:
            yield Request(img_url, meta={'uuid': item['uuid'], 'artwork_src_prefix':item['artwork_src_prefix']})

    def file_path(self, request, response=None, info=None):
        # folder = request.meta['uuid']
        folder = request.meta['artwork_src_prefix']
        image_guid = request.url.split('/')[-1]
        filename = u'full/{0}/{1}'.format(folder, image_guid)

        return filename

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem('Item contains no images')
        # item['image_paths'] = image_path
        item['album_URLs'] = image_path
        return item

class MySQLStorePipeline(object):
    def __init__(self, database, host, port, user, password, images_store):
        self.database = database
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.charset = 'utf8'
        self.images_store = images_store

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            database = crawler.settings.get('MYSQL_DATABASE'),
            host = crawler.settings.get('MYSQL_HOST'),
            port = crawler.settings.get('MYSQL_PORT'),
            user = crawler.settings.get('MYSQL_USER'),
            password = crawler.settings.get('MYSQL_PASSWORD'),
            images_store = crawler.settings.get('IMAGES_STORE'),
        )

    def open_spider(self, spider):
        self.db = db
        self.db.init(self.database, host=self.host, port=self.port, user=self.user, passwd=self.password, charset=self.charset)
        self.db.connect()
        
        if Album.table_exists() == False:
            create_tables()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        # if Album.table_exists() == False:
            # create_tables()
        try:
            album = Album.create(id=item['uuid'],name=item['album_name'],channel=item['album_channel'],origin_id=item['album_origin_id'])
        except Exception as e:
            if str(e.args[0]) == '1062':
                print('?????????')
            else:
                print(e.args[0], e.args[1])
        finally:
            album = Album.get(Album.id == item['uuid'])
            artwork_src_path = self.images_store[2:] + '/full/' + item['artwork_src_prefix']
            for img_src in item['album_URLs']:
                src = artwork_src_path + '/' + img_src.split('/')[-1]
                Artwork.create(id=str(uuid.uuid5(uuid.NAMESPACE_URL, img_src)), album=album, src=src)

        return item
