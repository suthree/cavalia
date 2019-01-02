import requests
from lxml import etree

index_url = 'https://www.v2ex.com'


def parse_index_url(index_url):
    response = requests.get(index_url)
    res = etree.HTML(response.text)
    ele_list = res.xpath('//div[@class="cell item"]')
    article_list = list()
    for ele in ele_list:
        article_url = index_url + ele.xpath('./table/tr/td[@valign="middle"]/span[@class="item_title"]/a/@href')[0]
        article_title = ele.xpath('./table/tr/td[@valign="middle"]/span[@class="item_title"]/a/text()')[0]
        article_cat = ele.xpath('./table/tr/td[@valign="middle"]/span[@class="topic_info"]/a/text()')[0]
        article_cat_href = index_url + ele.xpath('./table/tr/td[@valign="middle"]/span[@class="topic_info"]/a/@href')[0]
        article_dict = dict(article_url=article_url, article_title=article_title, article_cat=article_cat,
                            article_cat_href=article_cat_href)
        article_list.append(article_dict)
    print(len(article_list))
    print(article_list)


if __name__ == '__main__':
    parse_index_url(index_url)
