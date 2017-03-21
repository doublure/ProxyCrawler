# coding: utf-8

import requests
from bs4 import BeautifulSoup
import time
import os


class ProxyCrawler:

    def __init__(self, proxy_pool_dest, valid_proxy_dest):
        self.domain = 'http://www.xicidaili.com/nn/'
        self.temp_proxy_pool = proxy_pool_dest
        self.valid_proxy_pool = valid_proxy_dest

    def crawl_single_page(self, page):
        time.sleep(1)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        }
        r = requests.get(self.domain+str(page), headers = headers)
        r.encoding = 'UTF-8'

        soup = BeautifulSoup(r.text,'lxml')
        ip_items = soup.find('table',{'id':'ip_list'}).find_all('tr')

        ip_list = []
        for ip_item in ip_items[1:]:
            ip_info = ip_item.find_all('td')
            ip = ip_info[1].get_text()
            port = ip_info[2].get_text()
            proxy_port = ip +":" + port
            print ip +":" + port + ' retrived'
            ip_list.append(proxy_port)
        return ip_list

    def crawl_pages(self, page_num):
        if os.path.exists(self.temp_proxy_pool):
            os.remove(self.temp_proxy_pool)
        for page_index in range(1, page_num+1):
            proxy_list = self.crawl_single_page(page_index)
            self.write_to_txt(proxy_list, self.temp_proxy_pool, 'a')
            print 'page ' + str(page_index) + ' written to pool'

    def proxy_validation(self):
        time.sleep(1)
        valid_proxy = []
        with open(self.temp_proxy_pool,'r') as f:
            while True:
                p = f.readline()
                if p:
                    p_clean = p.strip()
                    print 'testing ' + p_clean
                    if self.proxy_is_valid(p_clean):
                        valid_proxy.append(p_clean)
                        print p_clean + ' is valid'
                    else:
                        print p_clean + ' is bad proxy'
                        continue
                else:
                    break
        print 'end of validation, about to write to file'
        self.write_to_txt(valid_proxy,self.valid_proxy_pool,'w')
        print 'valid proxies successfully retrieved to ' + self.valid_proxy_pool

    def proxy_is_valid(self, proxy_item):
        proxies = {
            'http': 'http://'+proxy_item
        }
        try:
            r = requests.get('http://baidu.com', proxies = proxies, timeout = 2)
            if r.status_code == 200:
                return True
            else:
                return False
        except:
            return False

    def write_to_txt(self, content_list, dest, mode):
        with open(dest,mode) as f:
            for content_item in content_list:
                f.write(content_item)
                f.write('\n')

pc = ProxyCrawler(r'proxy_pool.txt', r'valid_proxies.txt')
pc.crawl_pages(10)
pc.proxy_validation()