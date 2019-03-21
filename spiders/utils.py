from selenium import webdriver
from fake_useragent import UserAgent, UserAgentError


def headers():
    try:
        ua = UserAgent()
    except UserAgentError:
        ua = None
    return ua


def get_proxy():
    proxies = {}
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
