#!/usr/bin/env python
import urllib
import lxml.html
import urllib2
from urllib import urlretrieve
import time
import random
import urllib4
import os
import pycurl
from cStringIO import StringIO

header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_7) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.91 Safari/534.30'}

taobao_captcha_url = 'https://regcheckcode.taobao.com/auction/checkcode?sessionID=3920ea142a2600009b69df60e7c7a123'

def get_baidu_captcha(count=1000):
    """https://passport.baidu.com/?verifypic"""
    baidu_captcha_url = 'https://passport.baidu.com/?verifypic&t=%s'
    site = 'baidu'
    if not os.access(site, os.F_OK):
        os.mkdir(site)
        
    start_time = time.time()*100
    for i in range(count):
        url = baidu_captcha_url % str(start_time+i)
        r = urllib4.urlopen(url, headers=header)
        content = r.read()
        fname = os.path.join(site, "_".join([site, str(i)]) + ".jpg")
        with open(fname, 'wb') as f:
            f.write(content)
        print i

def get_icbc_captcha(count=1000):
    """https://passport.baidu.com/?verifypic"""
    url_base = 'https://vip.icbc.com.cn/servlet/com.icbc.inbs.person.servlet.Verifyimage2?disFlag=2&randomKey=132098559975661896'
    site = 'icbc'
    if not os.access(site, os.F_OK):
        os.mkdir(site)
        
    start_time = time.time()*100
    for i in range(count):
        url = url_base
        r = urllib4.urlopen(url, headers=header)
        content = r.read()
        fname = os.path.join(site, "_".join([site, str(i)]) + ".jpg")
        with open(fname, 'wb') as f:
            f.write(content)
        print i
   
    
def get_taobao_pay_captcha(count=1000):
    """
    nwe: http://checkcode.taobao.com/auction/checkcode?sessionID=4b9b83e4f8e6821c2e2929089f7b09bd&t=1323411260198&t=1323411260862&t=1323411261318&t=1323411261798&t=1323411262046&t=1323411262246&t=1323411262430&t=1323411262614&t=1323411262806&t=1323411262974&t=1323411263151&t=1323411263334&t=1323411263519&t=1323411263702&t=1323411263895&t=1323411264070&t=1323411264255&t=1323411264439&t=1323411264624&t=1323411264814&t=1323411265015&t=1323411265198&t=1323411265390&t=1323411265574&t=1323411265766&t=1323411265950&t=1323411266126&t=1323411266318&t=1323411266494&t=1323411266686&t=1323411266870&t=1323411267054&t=1323411267214&t=1323411267398&t=1323411277182
    """
    url_base = 'http://checkcode.taobao.com/auction/checkcode?sessionID=b5b6083c712d5a524d046e3324b3cec9&t=1321946037628'
    site = 'taobao'
    if not os.access(site, os.F_OK):
        os.mkdir(site)
        
    start_time = time.time()*100
    url = url_base
    for i in range(count):
        r = urllib4.urlopen(url, headers=header)
        content = r.read()
        fname = os.path.join(site, "_".join([site, str(i)]) + ".jpg")
        with open(fname, 'wb') as f:
            f.write(content)
        print i


def get_douban_captcha(count=1000):
    url = 'http://www.douban.com/accounts/login'    
    crl = pycurl.Curl()
    crl.setopt(pycurl.VERBOSE, 0)
    crl.setopt(pycurl.FOLLOWLOCATION, 1)
    crl.setopt(pycurl.MAXREDIRS, 5)
    
    crl.setopt(pycurl.COOKIEJAR, 'douban.cookie')
    crl.setopt(pycurl.COOKIEFILE, 'douban.cookie')
    
    crl.setopt(pycurl.CONNECTTIMEOUT, 60)
    crl.setopt(pycurl.TIMEOUT, 300)
    crl.setopt(pycurl.USERAGENT, r'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)')
    crl.setopt(pycurl.HTTPHEADER, ['Referer: http://www.douban.com/'])
    url = 'http://www.douban.com/login'
    crl.setopt(pycurl.URL, url)
    dictdata = {
        "source":"index_nav",
        "form_email":"zhxgigi@gmail.com",
        "form_password":"zhxathena"
    }
    #postdata_encoded = urllib.urlencode(dictdata)
    #crl.setopt(crl.POSTFIELDS, postdata_encoded)
    
    content = StringIO()
    
    xpath = "/html/body/div/div/div/form/div/div/p/img"
    outdir = "output"
    starttime = str(time.time())[:-3]
    for i in range(count):
        content = StringIO()
        crl.setopt(crl.WRITEFUNCTION, content.write)
        crl.perform()
        html = content.getvalue()
        with open('douban.html', 'w') as f:
            f.write(html)
            
        dom = lxml.html.fromstring(html)
        img = dom.xpath(xpath)
        img_link = img[0].get('src')
        img_content = urllib2.urlopen(img_link).read()
        print i, img_link
        time.sleep(random.randint(1, 3))
        with open(os.path.join(outdir, "douban_%s_%d.jpg"%(starttime, i)), 'wb') as f:
            f.write(img_content)
        
def get_sina_captcha(count=1000):    
    crl = pycurl.Curl()
    crl.setopt(pycurl.VERBOSE, 1)
    crl.setopt(pycurl.FOLLOWLOCATION, 1)
    crl.setopt(pycurl.MAXREDIRS, 5)
    
    crl.setopt(pycurl.COOKIEJAR, 'douban.cookie')
    crl.setopt(pycurl.COOKIEFILE, 'douban.cookie')
    
    crl.setopt(pycurl.CONNECTTIMEOUT, 60)
    crl.setopt(pycurl.TIMEOUT, 300)
    crl.setopt(pycurl.USERAGENT, r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2')
    crl.setopt(pycurl.HTTPHEADER, ['Referer: http://www.weibo.com/signup/signup.php?ps=u3&lang=zh'])
    url = 'http://www.weibo.com/signup/pincode/pin1.php?sinaId=7951da5169b57e3ddcedccd6421d5c64'
    crl.setopt(pycurl.URL, url)
    
    outdir = "output"
    for i in range(count):
        content = StringIO()
        crl.setopt(crl.WRITEFUNCTION, content.write)
        crl.perform()
        with open(os.path.join(outdir, "sina_%d.png"%i), 'wb') as f:
            f.write(content.getvalue())

def get_360_captcha(count=1000):
    url = r'http://captcha.360.cn/image.php?app=i360&r=0.874529683496803'
    site = '360cn'
    if not os.access(site, os.F_OK):
        os.mkdir(site)
    for i in range(count):
        r = urllib4.urlopen(url)
        content = r.read()
        fname = os.path.join(site, "_".join([site, str(i)]) + ".jpg")
        with open(fname, 'wb') as f:
            f.write(content)
        print i
    
if __name__ == '__main__':
    get_360_captcha()
    