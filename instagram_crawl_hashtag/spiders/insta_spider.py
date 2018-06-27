#     <<Instagram hashtag crawler>>
#     leejihee950430@gmail.com
#
#     Copyright (c) 2018, Jihee Lee
#     All rights reserved.
#
#     Redistribution and use in source and binary forms, with or without
#     modification, are permitted provided that the following conditions are
#     met:
#
#         * Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#         * Redistributions in binary form must reproduce the above copyright
#         notice, this list of conditions and the following disclaimer in the
#         documentation and/or other materials provided with the distribution.
#         * Neither the name of the <ORGANIZATION> nor the names of its
#         contributors may be used to endorse or promote products derived from
#         this software without specific prior written permission.
#
#     THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#     IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
#     TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#     PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
#     OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#     EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#     PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#     PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#     LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#     NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#     SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import re
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

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
        ActionChains(self.browser).move_to_element(element).click().perform()

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
            id2 = self.browser.find_element_by_xpath('//body/div[3]/div/div[2]/div/article/header/div[2]/div[1]/div[1]/a').get_attribute('title')
            post = self.browser.find_elements_by_xpath('//body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li')
            identifier_ = [id1, id2, post]

            self.identifier = identifier_

            #긁어온 게시글, 댓글 해시태그
            item_ = {}
            date = ''
            for con in post:
                contents = con.find_elements_by_xpath('span')
                tags = ''
                if len(contents) != 0:
                    contents = contents[0].text
                    tags = re.findall('#[^#^ \s]+', contents)

                if len(tags) != 0:
                    item_count = 1
                    for tag in tags:
                        item_name = 'tag'+str(item_count)
                        item_[item_name] = tag.replace('#', '')
                        item_count += 1
                    date = self.browser.find_element_by_xpath('//body/div[3]/div/div[2]/div/article/div[2]/div[2]/a/time').get_attribute('datetime')


            #다음 게시글로 넘어가는 버튼 누르기
            element = self.browser.find_element_by_xpath('//body/div[3]/div/div[1]/div/div/a[2]')
            ActionChains(self.browser).move_to_element(element).click().perform()

            #다음 페이지 뜰 때까지 기다리기
            import time
            time.sleep(1)

            #아이템 쌓기
            if len(item_) != 0:
                item = InstaHashtagItem()
                item['hashtag'] = item_
                item['date'] = date
                yield item