# instagram_crawl_hashtag
특정 해시태그를 포함한 게시글의 해시태그를 가져오는 크롤러<br>

설치
----------
scrapy <br>
selenium <br>
cromedrive <br>
win_unicode_console <br>

사용 방법
----------
1. 'insta_spider.py'의 'self.browser = webdriver.Chrome(path)'에 cromedriver의 경로를 path 자리에 넣는다.
2. 터미널에서 아래의 명령어를 입력하면 코드가 동작한다.<br>

    scrapy crawl getHashtag -a search_tag=[검색하고자 하는 해시태그] -a tag_count=[가져온 게시글 개수]
    EX) scrapy crawl getHashtag -a search_tag=멍스타그램 -a tag_count=10
    
