# instagram_crawl_hashtag
특정 해시태그를 포함한 게시글의 해시태그를 가져오는 크롤러 (최근 게시물 순으로 가져옴)<br><br>

설치
----------
scrapy <br>
selenium <br>
cromedrive <br>
win_unicode_console <br>

사용 방법
----------
1. `insta_spider.py`의 `self.browser = webdriver.Chrome(path)`에 path 자리에 cromedriver의 경로를 넣는다.  
2. 터미널에서 아래의 명령어를 입력하면 코드가 동작한다.
```
scrapy crawl getHashtag -a search_tag=[검색하고자 하는 해시태그] -a tag_count=[가져올 게시글 개수]<br>
EX) scrapy crawl getHashtag -a search_tag=멍스타그램 -a tag_count=10
```    

결과
----------
```
{
  "tag1":{"hashtag": {"tag1" : "선팔하면 맞팔", "tag2":"멈뭄미", "tag3":"멍스타그램"}, "date" : "2018-06-27T06:12:54.000Z"},
  "tag2":{"hashtag": {"tag1" : "귀여워", "tag2":"멍스타그램"}, "date" : "2018-06-27T06:10:38.000Z"},
  "tag3":{"hashtag": {"tag1": "시바견", "tag2": "산책", "tag3":"멍스타그램", "tag4":"개스타그램"}, "date": "2018-06-27T06:10:23.000Z"},
    .
    .
    .
  "tag10":{"hashtag": {"tag1": "멍스타그램", "tag2": "행복이", "tag3": "만복이", "tag4" : "가족"}, "date": "2018-06-27T06:08:48.000Z"}
}
```
