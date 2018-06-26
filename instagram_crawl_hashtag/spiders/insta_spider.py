import re
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

#scrapy crawl getHashtag -a search_tag=비온다그램 -a tag_count=10

from instagram_crawl_hashtag.items import InstaHashtagItem
import win_unicode_console

win_unicode_console.enable()

class HadhtagSpider(scrapy.Spider):
    name = "getHashtag"

    def __init__(self, search_tag=None, tag_count=5, *args, **kwargs):
        print("search_tag : ", search_tag)
        super(HadhtagSpider, self).__init__(*args, **kwargs)
        self.search_tag = search_tag
        self.tag_count = tag_count

        self.browser = webdriver.Chrome('C:\PycharmProjects\insta_hashtag\insta_hashtag\spiders/chromedriver')

    def start_requests(self):
        url = "https://www.instagram.com/explore/tags/" + self.search_tag+"/"
        self.browser.get(url)
        # self.contents = ''
        self.identifier = []
        yield scrapy.Request(url, self.parse_insta)

    def parse_insta(self, response):
        print('######크롤링 시작!######')
        element = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]/a/div')
        hover = ActionChains(self.browser).move_to_element(element).click()
        hover.perform()

        #게시글 페이지(?) 뜰 때 까지 기다리기
        list = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li')))
        ActionChains(self.browser).move_to_element(list).perform()

        for c in range(int(self.tag_count)):

            #아직 다음 포스트 안떴을때를 대비
            post = []
            identifier_ = [1, 1, 1]
            while self.identifier == identifier_:
                id1 = self.browser.find_element_by_xpath('//body/div[3]/div/div[2]/div/article').get_attribute('class')
                id2 = self.browser.find_element_by_xpath('//body/div[3]/div/div[2]/div/article/header/div[2]/div[1]/div[1]/a').get_attribute('title')
                post = self.browser.find_elements_by_xpath('//body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li')
                identifier_ = [id1, id2, post]

            id1 = self.browser.find_element_by_xpath('//body/div[3]/div/div[2]/div/article').get_attribute('class')
            print("id1 :", id1)
            id2 = self.browser.find_element_by_xpath('//body/div[3]/div/div[2]/div/article/header/div[2]/div[1]/div[1]/a').get_attribute('title')
            print("id2 :", id2)
            post = self.browser.find_elements_by_xpath('//body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li')
            identifier_ = [id1, id2, post]

            self.identifier = identifier_

            #긁어온 게시글, 댓글 해시태그
            item_ = {}
            for con in post:
                contents = con.find_element_by_xpath('span').text
                tags = re.findall('#[^#^\s]+', contents)

                if len(tags) != 0:
                    item_count = 0
                    for tag in tags:
                        item_name = 'tag'+str(item_count)
                        item_[item_name] = tag.replace('#', '')
                        item_count += 1

            element = self.browser.find_element_by_xpath('//body/div[3]/div/div[1]/div/div/a[2]')
            hover = ActionChains(self.browser).move_to_element(element).click()
            hover.perform()

            #다음 페이지 뜰 때까지 기다리기
            import time
            time.sleep(1)

            if len(item_) != 0:
                item = InstaHashtagItem()
                item['hashtag'] = item_
                yield item


        # divs = self.browser.find_elements_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div')
        #
        # # while len(divs) < 10:
        # #     self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # #     divs = self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div')
        #
        # for div in divs:
        #     posts = div.find_elements_by_xpath('div')
        #
        #     for post in posts:
        #         self.contents = post.find_element_by_xpath('a/div/div/img').get_attribute('alt')
        #         tags = re.findall('#[^#^\s]+', self.contents)
        #         if len(tags) != 0:
        #             count = 1
        #             item_ = {}
        #
        #             for tag in tags:
        #                 item_name = 'tag'+str(count)
        #                 item_[item_name] = tag.replace('#', '')
        #                 count += 1
        #             item = InstaHashtagItem()
        #             item['hashtag'] = item_
        #
        #             yield item
        # self.browser.close()
