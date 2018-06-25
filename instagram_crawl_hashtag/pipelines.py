# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class instagramCrawlHashtagPipeline(object):
    def __init__(self):
        self.count = 1

    def open_spider(self, spider):
        file_name = 'hashtag_' + str(spider.search_tag) + '.json'
        self.file = open(file_name, 'w', encoding='utf-8')
        self.file.write('{\n')

    def process_item(self, item, spider):
        line = '\t"tag' + str(self.count) + '":' + json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.file.write(line)
        self.count += 1
        return item

    def close_spider(self, spider):
        print('######크롤링 끝!######')
        self.file.seek(self.file.tell() - 3)
        self.file.write("\n}")  # 파일에 기록
        self.file.close()