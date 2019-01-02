import requests
from lxml import etree
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'cache-control': "no-cache",
}
cookie = {
    "Cookie": "Hm_lvt_3d68bfed7a1e8a4300986c254ac663fd=1532418680; guest_id=1523678666; PHPSESSID=v1d8pq07296iftp2o9856s8rb4; Hm_lvt_c3f6328a1a952e922e996c667234cdae=1543887979; regsms=1543887979000; stat_sessid=f7l2ut2o4tle8eth9m4pm82tc3; gdxidpyhxdE=qnn5sKN26zeVQmj6jx8BHAs5GXV39fZdJ6IcfftaiLuPOZCUoQKhU7t9y42z3KTKTObjoL2e1MnvM64NdJKsmCIpe6YjABfNSQj%5CnZrmvtivuHrfv7S0f%2FjkVTY6Mw4e%2Bjeg%2BXfzCGb5pxSj3djv7MIOTMUWnkz7u8%2F%2BIrmq5PDY4XXX%3A1543888882423; _9755xjdesxxd_=32; PHPSESSID=o61esse4drgsp64f97ujtisb86; http_tK_cache=2ab3bdafa405d335d66c4fd941e6d5c36757fc16; cur_ck_time=1543888073; ck_request_key=124NypdAvdH6Hg5%2BIJ6NeOSGbWFl9EaNDBNhJ0Cpys0%3D; passport=562852%09u2953258676127%09BQUFBQwAAQldUwQBWlBWDFJcAQEGCgkJAFZeXgYHAVY%3D9710d4c4e7; rz_u_p=0; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22562852%22%2C%22%24device_id%22%3A%22164cb45626c9c-02e341a4219276-163b6952-1764000-164cb45626dbc%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22562852%22%7D; smppw_tz_auth=1; sensro_profile_has_set=1; quiz_back_url=https%3A%2F%2Fdc.simuwang.com%2F; evaluation_result=3; Hm_lpvt_c3f6328a1a952e922e996c667234cdae=1543901271; rz_token_6658=f90fa5c886f2a5543c03a06c8a5307d9.1543901271; gsScrollPos-2111079331=; fyr_ssid_n5776=fyr_n5776_jp9ayd3u"
}
import ipdb
ipdb.set_trace()
# 登录,获取cookies
login_url = "https://passport.simuwang.com/index.php"
querystring = {"m": "passport", "c": "auth", "a": "login"}
# payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n" \
#           "Content-Disposition: form-data; name=\"username\"\r\n\r\n 18621543714\r\n" \
#           "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n" \
#           "Content-Disposition: form-data; name=\"password\"\r\n\r\n smalex2015\r\n" \
#           "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n" \
#           "Content-Disposition: form-data; name=\"do_qualified\"\r\n\r\n 1\r\n" \
#           "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n" \
#           "Content-Disposition: form-data; name=\"reme\"\r\n\r\n 1\r\n" \
#           "------WebKitFormBoundary7MA4YWxkTrZu0gW--"
payload = dict(username="18621543714", password="smalex2015", do_qualified=1, reme=1)
response = requests.request("POST", login_url, data=payload, headers=headers, params=querystring)

index_url = 'https://dc.simuwang.com'

res = requests.get(index_url, headers=headers, cookies=response.cookies)
soup = BeautifulSoup(res.text, 'lxml')

pages = etree.HTML(res.text)
even_products = pages.xpath('//tr[@class="even"]/td[2]/a/@href')
odd_products = pages.xpath('//tr[@class="odd"]/td[2]/a/@href')
