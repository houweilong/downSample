'''
Created on Nov 19, 2015

@author: hwl122902
'''
__author__ = 'CQC'
# -*- coding:utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import httplib
import ssl
import os
import paramiko 
import logging
import hashlib

def setLogger():
    logger_root = logging.getLogger()
    console = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s][%(levelname)s][%(process)d][%(filename)s]%(funcName)s: %(message)s")
    console.setFormatter(formatter)
    logger_root.addHandler(console)
    logger_root.setLevel(logging.INFO)
    return logger_root

def sendFiles(localpath,remotepath):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("150.70.175.181",username="trt_shared", password="ftp%shared##!")
    sftp = ssh.open_sftp()
    localpath = '/home/weilongh/work/downSample/' + localpath
    remotepath = '/ipattern/iVES-Write/samples/GOOGLE_CRAWL/' + remotepath
    sftp.put(localpath, remotepath)
    sftp.close()
    ssh.close()


def getPage(url):
    try: 
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'  
        headers = { 'User-Agent' : user_agent }
        req = urllib2.Request(url,None,headers)
        html = urllib2.urlopen(req).read()
        soup = BeautifulSoup(html)
        return soup
    except urllib2.URLError, e:            
        if hasattr(e,"reason"):               
            print("this url is can't be accessed,the reason is : ",e.reason)
            return None 
    except ValueError,e:
        pass 
    except httplib.IncompleteRead, e:
        return BeautifulSoup(e.partial)

def getUrls(url):
    soup = getPage(url)
    if soup==None:
        soup=""
    try:
        for h in soup.find_all("a", hidefocus="true"):
            u = h.get("href")
            if u.find("http")!=-1:
                logger.info(u)
    except AttributeError:
        pass
            
def getUrlsInBbs(url):
    soup = getPage(url)
    if soup==None:
        soup=""
    try:
        for h in soup.find_all("a"):
            u = h.get("href")
            if u.find("http")==-1 and u.find("forum")!=-1 and u.endswith("html"):
                if u not in urls:
                    urls.add(u)
                    with open("index1.html","a+") as f:
                        f.write(urlHost+u + "\n")
                    logger.info("It will get the url in further")
#                     getFinalUrlsInBbs(urlHost+u)
    except AttributeError:
        pass
                    
def getFinalUrlsInBbs(url):
    soup = getPage(url)
    if soup==None:
        soup=""
    logger.info("it is getting the final url")
    try:
        for h in soup.find_all("a"):
            u = h.get("href")
            if u.find("http")==-1 and u.find("thread")!=-1 and u.endswith("html"):
                if u not in urls:
                    urls.add(u)
                    with open("index2.html","a+") as f:
                        f.write(urlHost+u + "\n")
                    logger.info("it will get the download url")
#                     getDownloadUrl(urlHost+u)
        nextPage = soup.find_all("a",class_="nxt")
        if len(nextPage)>0:
            if len(nextPage)>0:
                getFinalUrlsInBbs(urlHost+nextPage[0].get("href"))
    except AttributeError,e:
        logger.info(e)
            
def getDownloadUrl(url):
    soup = getPage(url)
    if soup==None:
        soup=""
    try:
        for h in soup.find_all("a"):
            u = h.get("href")
            if u!="" and u!=None:
                if u.find("ipa")!=-1 or u.find("deb")!=-1:
                    if u.find("http://")==-1:
                        u = urlHost+u
                    if u not in down_urls:
                        down_urls.add(u)
                        with open("download.html","a+") as f:
                            f.write(u+"\n")
                        logger.info("the sample's url is " + url)
#                     downSample(u) 
                        
        nextPage = soup.find_all("a",class_="nxt")
        if len(nextPage)>0:
            getDownloadUrl(urlHost+nextPage[0].get("href"))
                 
    except AttributeError:
        pass

def downSample(url):
    savePath = "sample/"
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'  
        headers = { 'User-Agent' : user_agent }
        request = urllib2.Request(url,headers=headers)  
        response = urllib2.urlopen(request)
        logger.info("response code == " + str(response.code))
        if response.code == 200:
            fileHeader = response.headers
            content_type = fileHeader.get("Content-Type")
            if content_type == None:
                content_type = " "
            logger.info(content_type)
            s1 = ""
            if content_type.find("application")!=-1:
                #ipa file
                logger.info("it is preparing download sample from bbs.25pp.com")
                file_dis = fileHeader.get("Content-Disposition")
                 
                if file_dis == None:
                    file_out = savePath+url.split("/")[-1]
                else:
                    file_out = savePath + file_dis.split(";")[-1].split("=")[-1]
                if file_out==savePath:
                    file_out = savePath+url.split("/")[-1]
                logger.info(file_out)
                with open(file_out,"wb") as f:
                    content = response.read()
                    logger.info("It is calculating the sha1 of this sample")
                    s1 = hashlib.sha1(content).hexdigest()
                    logger.info("The sha1 is "+s1)
                    f.write(content)
                with open("index_down.html","a+") as f:
                    f.write(url + "\t"+ s1 + "\n")
 
#                 sendFiles(file_out,file_out.split("/")[-1]) 
#                 os.remove(file_out)
                logger.info("it has finished downloading sample from bbs.25pp.com")
 
 
            elif content_type.find("text/plain")!=-1 or content_type == None:
                #zip file
                logger.info("it is preparing download sample from bbs.25pp.com")
                file_out = savePath+url.split("/")[-1].replace("ipa","zip")
                with open(file_out,"wb") as f:
                    content = response.read()
                    logger.info("It is calculating the sha1 of this sample")
                    s1 = hashlib.sha1(content).hexdigest()
                    logger.info("The sha1 is "+s1)
                    f.write(content)
                with open("index_down.html","a+") as f:
                    f.write(url + "\t"+ s1 + "\n")
#                 sendFiles(file_out,file_out.split("/")[-1]) 
#                 os.remove(file_out)
                logger.info("it has finished downloading sample from bbs.25pp.com")
            else:
                pass
        else:
            logger.info("this url can't be found")
    except urllib2.URLError, e:            
        if hasattr(e,"reason"):               
            logger.info("this url needs a proxy and second scrapy")
            return None 
    except httplib.BadStatusLine,e:
        logger.info("this url can't be acessed")
    except ssl.CertificateError,e:
        logger.info("this url has a ssl.certificateError")
    except UnicodeEncodeError,e:
        pass
    except ValueError,e:
        pass

def readUrl(filename):
    with open(filename,"r") as f:
        for line in f.readlines():
            line = line.strip()
            print("the url in the index.html is : " + line)
            getFinalUrlsInBbs(line)
       
if __name__ == "__main__":
    urlHost = "http://bbs.25pp.com/"
    urls = set()
    down_urls = set()
    logger = setLogger()
#     readUrl("index1.html")
    downSample("http://d.appsre.com/xinshipin/pq_mgTV.ipa")
    
    
    
    
