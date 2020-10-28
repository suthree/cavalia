from selenium import webdriver
from fake_useragent import UserAgent, UserAgentError
from const import wuyou_proxy_url, xici_proxy_url
import requests
from lxml import etree
from bs4 import BeautifulSoup


def get_headers(browser='chrome'):
    """
    根据传入的浏览器类型，给出随机的请求头，默认返回chrome
    """
    try:
        ua = UserAgent()
        # ua.data_browsers.keys()
        # ['chrome', 'opera', 'firefox', 'internetexplorer', 'safari']
        user_agent = ua[browser]
    except UserAgentError:
        user_agent = None
    headers = {'User-Agent': user_agent}
    return headers


def get_proxy():
    """
    通过购买的 无忧代理 ，稳定获取代理
    """
    res = requests.get(wuyou_proxy_url)
    if res.status_code == 200:
        data = res.json()
        ip_port = data['data'][0]
        ip = ip_port['ip']
        port = ip_port['port']
        proxy = f'{ip}:{port}'
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }
        return proxies


def create_chromewebdriver():
    """webdriver """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.accept_untrusted_certs = True
    chrome_options.assume_untrusted_cert_issuer = True
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-impl-side-painting")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-seccomp-filter-sandbox")
    chrome_options.add_argument("--disable-breakpad")
    chrome_options.add_argument("--disable-client-side-phishing-detection")
    chrome_options.add_argument("--disable-cast")
    chrome_options.add_argument("--disable-cast-streaming-hw-encoding")
    chrome_options.add_argument("--disable-cloud-import")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-session-crashed-bubble")
    chrome_options.add_argument("--disable-ipv6")
    chrome_options.add_argument("--allow-http-screen-capture")
    chrome_options.add_argument('--headless')

    # 下载文件
    chrome_options.add_experimental_option(
        "prefs", {
            "download.default_directory":
            r"/Users/wcc/projects/cavalia/download",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
    driver = webdriver.Chrome(
        chrome_options=chrome_options,
        executable_path='/usr/local/bin/chromedriver')
    return driver

def get_xici_proxy():
    """
    西刺 高匿代理
    """
    # 会话对象让你能够跨请求保持某些参数。它也会在同一个 Session 实例发出的所有请求之间保持 cookie， 
    # 期间使用 urllib3 的 connection pooling 功能。

    # 使用上下文管理器或 基础用法 
    se =  requests.Session()
    res = se.get(xici_proxy_url, headers=get_headers())
    ip_list = BeautifulSoup(res.text, 'lxml')
    ip_list_2 =  BeautifulSoup(str(ip_list.find_all(id = 'ip_list')), 'lxml')
    ip_list_info  = ip_list_2.table.contents
    proxys_list = []
    for index, ip in enumerate(ip_list_info):
        if index % 2 == 1 and index != 1:
            dom = etree.HTML(str(ip))
            ip = dom.xpath('//td[2]')[0].text
            port = dom.xpath('//td[3]')[0].text
            protocol = dom.xpath('//td[6]')[0].text.lower()
            proxy = f"{protocol}://{ip}:{port}"
            proxys_list.append(proxy)

    # 对页面按照 页面的编码格式 进行解码， 再进行编码，默认utf-8
    # html_coding = res.encoding
    # html_data = res.text.decode(html_coding).encode()
    # page = etree.HTML(res.text)
    # ip_list = page.xpath('//table[@id="ip_list"]/tbody/tr/td')

if __name__ == "__main__":
    get_xici_proxy()