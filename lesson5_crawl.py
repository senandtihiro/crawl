import requests
from print_log import log
from lxml import html


__author__ = 'ahe'


class Model(object):
    def __str__(self):
        class_name = self.__class__.__name__
        properties = (u'{0} = ({1})'.format(k, v) for k, v in self.__dict__.items())
        r = u'\n<{0}:\n  {1}\n>'.format(class_name, u'\n  '.join(properties))
        return r


class Book(Model):
    def __init__(self):
        super(Book, self).__init__()
        # self.cover_url = ''
        self.bookname = ''
        self.author = ''
        self.publish_info = ''
        self.rating = 0.0
        self.number_of_comments = 0
        self.price = 0.0


def download_covers(books):
    for b in books:
        img_url = b.cover_url[0]
        r = requests.get(img_url)
        path = 'covers/' + b.bookname.split('/')
        with open(path, 'wb') as f:
            f.write(r.content)


def book_from_table(table):
    book = Book()
    # .代表当前目录，表示从当前的div下面开始找
    # book.cover_url = table.xpath('.//td/a[@class="nbg"]/img/@src')
    names = table.xpath('.//td/div[@class="pl2"]/a/@title')[0]
    book.bookname = names.strip()
    book_info = table.xpath('.//p[@class="pl"]')[0].text
    book.author = book_info.split('/')[0]
    book.publish_info = book_info.split('/')[-3]
    book.price = book_info.split('/')[-1]
    book.rating = table.xpath('.//span[@class="rating_nums"]')[0].text
    comments_info = table.xpath('.//span[@class="pl"]')[0].text
    comments_info_string = comments_info.split('(')[1].strip().split('人评价')[0]
    # print('comments_info_string', comments_info_string)
    book.number_of_comments = comments_info_string
    return book

'''
<table width="100%">
        <tr class="item">
          <td width="100" valign="top">
            <a class="nbg" href="https://book.douban.com/subject/1770782/"
              onclick="moreurl(this,{i:'0'})">
              <img src="https://img3.doubanio.com/spic/s1727290.jpg" width="64" />
            </a>
          </td>
          <td valign="top">
            <div class="pl2">
              <a href="https://book.douban.com/subject/1770782/" onclick=&#34;moreurl(this,{i:&#39;0&#39;})&#34; title="追风筝的人">
                追风筝的人
              </a>
                &nbsp; <img src="https://img3.doubanio.com/pics/read.gif" alt="可试读" title="可试读"/>
                <br/>
                <span style="font-size:12px;">The Kite Runner</span>
            </div>
              <p class="pl">[美] 卡勒德·胡赛尼 / 李继宏 / 上海人民出版社 / 2006-5 / 29.00元</p>
              <div class="star clearfix">
                  <span class="allstar45"></span>
                  <span class="rating_nums">8.8</span>
                <span class="pl">(235609人评价)</span>
              </div>
          </td>
        </tr>
      </table>
'''

def books_from_url(url):
    page = requests.get(url)
    # print('debug page:', page)
    # 将html转化成一个树形结构
    root = html.fromstring(page.content)
    # print('debug root', root)
    # 双斜杠代表从html的根元素开始找找到一个table/trclass为item
    book_tables = root.xpath('//table/tr[@class="item"]')
    books = [book_from_table(table) for table in book_tables]
    return books


'''
下一页：
https://book.douban.com/top250?start=25
https://book.douban.com/top250?start=50
...
'''


def main():
    for i in range(10):
        if i == 0:
            url = 'https://book.douban.com/top250'
        else:
            print('debug i ', i)
            url = 'https://book.douban.com/top250?start=' + str(25*i)
        log('dubug url:', url)
        books = books_from_url(url)
        books.sort(key=lambda m: m.rating)
        for b in books:
            log(b)


if __name__ == '__main__':
    main()
