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