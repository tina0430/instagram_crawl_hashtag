import re
import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#scrapy crawl getHashtag -a search_tag=비온다그램

from instagram_crawl_hashtag.items import InstaHashtagItem
import win_unicode_console

win_unicode_console.enable()

class HadhtagSpider(scrapy.Spider):
    name = "getHashtag"

    def __init__(self, search_tag=None, *args, **kwargs):
        print("search_tag : ", search_tag)
        super(HadhtagSpider, self).__init__(*args, **kwargs)
        self.search_tag = search_tag
        self.browser = webdriver.Chrome('C:\PycharmProjects\insta_hashtag\insta_hashtag\spiders/chromedriver')

    def start_requests(self):
        url = "https://www.instagram.com/explore/tags/" + self.search_tag+"/"
        self.browser.get(url)
        self.contents = ''
        yield scrapy.Request(url, self.parse_insta)

    def parse_insta(self, response):
        print('######크롤링 시작!######')
        divs = self.browser.find_elements_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div')

        c = 0
        # while len(divs) < 10:
        #     self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     divs = self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div')

        for div in divs:
            posts = div.find_elements_by_xpath('div')
            print('######크롤링 중간1######')

            for post in posts:
                self.contents = post.find_element_by_xpath('a/div/div/img').get_attribute('alt')
                print('contents')
                print(self.contents)
                print('######크롤링 중간2######')
                tags = re.findall('#[^#^\s]+', self.contents)
                if len(tags) != 0:
                    count = 1
                    item_ = {}

                    for tag in tags:
                        print(tag)
                        item_name = 'tag'+str(count)
                        item_[item_name] = tag.replace('#', '')
                        count += 1
                    print('='*100)
                    print(c)
                    c+= 1
                    print(item_)
                    item = InstaHashtagItem()
                    item['hashtag'] = item_

                    yield item

        self.browser.close()
