import requests

from lxml import etree


index_url = 'https://www.dy2018.com'


def parse_index_page():
    response = requests.get(index_url)
    res = etree.HTML(response.text)
    ele_list = res.xpath('//div[@class="co_content222"]/ul/li')
    for ele in ele_list:
        film_url = ele.xpath('./a/@href')[0]
        film_title = ele.xpath('./a/text()')[0]


if __name__ == '__main__':
    parse_index_page()