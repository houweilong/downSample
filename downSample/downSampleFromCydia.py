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
import hashlib
import logging
import paramiko 

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
        return None 

def getUrlsOfSections(url):
    urls = set()
    soup = getPage(url)
    for h in soup.find_all("a", class_="updated"):
        u = url + h.get("href")
        if u not in urls:
            urls.add(u)
            logger.info("It will get the sample's url")
            getDownloadUrl(u)
            
def getDownloadUrl(url):
    soup = getPage(url)
    urls = set()
    for h in soup.find_all("a", class_="normal"):
        u = h.get("href")
        if u not in urls and u.endswith(".deb") and u.find("http")!=-1:
            urls.add(u)
            with open("section","a+") as f:
                f.write(u + "\n")
            logger.info("It will download the sample")
#             downSample(u)

def downSample(url):
    savePath = "sample/"
    try:
        logger.info("The sample's url is " + url)
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
            if content_type.find("application")!=-1:
                #deb file
                logger.info("it is preparing download sample from piqu.com")
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
                logger.info("it has finished downloading sample from piqu.com")
 
            elif content_type.find("text/plain")!=-1 or content_type == None:
                #zip file
                logger.info("it is preparing download sample from piqu.com")
                file_out = savePath+url.split("/")[-1].replace("deb","zip")
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
                logger.info("it has finished downloading sample from piqu.com")
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

        
if __name__ == "__main__":
    logger = setLogger()
    urlHost = "http://www.cydiacrawler.com/"
    urls = set()
    getUrlsOfSections(urlHost)
    
    
    
    
    
