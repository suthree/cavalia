import requests

from lxml import etree

from spiders.chromedriver import create_webdriver


def parse_index_page(index_url):
    """爬取首页信息,解析每个子网页的信息"""
    driver = create_webdriver()
    driver.get(index_url)
    pages = driver.find_elements_by_xpath('//td[@class="ListColumnClass15"]/a')
    for page in pages:
        page_url = page.get_attribute('href')
        parse_pub_page(page_url)


def parse_pub_page_by_webdriver(page_url):
    """通过webdriver 解析每个子页面"""
    driver = create_webdriver()
    driver.get(page_url)
    pub_title = driver.find_element_by_xpath('//td[@class="articletitle3"]/font/font').text.strip()
    pub_date = driver.find_element_by_xpath('//td[@class="articletddate3"]').text.split(' ')[0]
    urls = driver.find_elements_by_xpath('//a')
    page_info = list()
    for url in urls:
        file_title = url.text
        if file_title:
            file_url = url.get_attribute('href')
            file_type = file_url.split('.')[-1]


def parse_pub_page(page_url):
    """解析每个子页面"""
    driver = create_webdriver()
    driver.get(page_url)
    jar = requests.cookies.RequestsCookieJar()
    cookies = driver.get_cookies()
    for cookie in cookies:
        jar.set(name=cookie['name'], value=cookie['value'], domain=cookie['domain'], path=cookie['path'])
    res = requests.get(page_url, cookies=jar).text
    page = etree.HTML(res)
    pub_title = page.xpath('//tbody/tr[1]/td/font/font/text()')[0].strip()
    pub_date = page.xpath("//td[@class='articletddate3']/text()")[0].strip().split(' ')[0]
    urls = page.xpath('//a')
    page_info = list()
    for url in urls:
        if url.xpath('./text()'):
            file_url = 'http://samr.cfda.gov.cn' + url.xpath('./@href')[0]
            file_type = file_url.split('.')[-1]
            file_title = url.xpath('./text()')[0].strip()
            # if file_type in file_type_list:
            #     if len(each.xpath('./font')):
            #         file_title = each.xpath('./font/text()')[0].strip()
            #     elif len(each.xpath('./span')):
            #         file_title = each.xpath('./span/text()')[0].strip()
            #     elif len(each.xpath('./@title')):
            #         file_title = each.xpath('./@title')[0].strip()
            #     else:
            #         file_title = each.xpath('./text()')[0].strip()
            result = dict(pub_title=pub_title, pub_date=pub_date, file_url=file_url, file_title=file_title,
                          file_type=file_type)
            page_info.append(result)


def save_to_db():
    pass


def main():
    """爬虫入口"""
    # 总局地址
    center_url = 'http://samr.cfda.gov.cn/WS01/CL1687/'
    # 地方url
    country_url = 'http://samr.cfda.gov.cn/WS01/CL1688/'
    parse_index_page(center_url)
    pass
