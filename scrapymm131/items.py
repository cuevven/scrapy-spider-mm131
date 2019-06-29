# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
from peewee import *


db = MySQLDatabase(None)

class Scrapymm131Item(scrapy.Item):
    # define the fields for your item here like:
    uuid = scrapy.Field()
    album_channel = scrapy.Field()
    album_origin_id = scrapy.Field()
    album_name = scrapy.Field()
    album_URLs = scrapy.Field()
    referer = scrapy.Field()
    artwork_src_prefix = scrapy.Field()
    pass


class BaseModel(Model):
    
    class Meta:
        database = db

class Album(BaseModel):
    id = UUIDField(primary_key = True)
    name = CharField(max_length = 255)
    channel = CharField(max_length = 255)
    origin_id = CharField(max_length = 40)
    deleted_at = DateTimeField(default = None, null = True)
    created_at = DateTimeField(default = datetime.datetime.now, null= True)
    updated_at = DateTimeField(default = None, null = True)

class Artwork(BaseModel):
    id = UUIDField(primary_key = True)
    # title = CharField(max_length = 255)
    # description = TextField(null = True)
    src = CharField(max_length = 255)
    album = ForeignKeyField(Album, backref='albums')
    deleted_at = DateTimeField(default = None, null = True)
    created_at = DateTimeField(default = datetime.datetime.now, null = True)
    updated_at = DateTimeField(default = None, null = True)

def create_tables():
    with db:
        db.create_tables([Album, Artwork])
    return db