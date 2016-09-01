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

def getUrls(url):
    soup = getPage(url)
    for h in soup.find_all("a", class_="navItem"):
        u = url + h.get("href")
        if u.endswith("html"):
            getUrlsInPage(u)
            getUrlsInOthersPage(u)
        else:
            getUrlsInPage(u)

def getUrlsInPage(url):
    with open("index.html","a+") as f:
        f.write(url+"\n")
    soup = getPage(url)
    for h in soup.find_all("a", target="_blank"):
        u = h.get("href")
        if u!="" and u!=None and u.endswith("html"):
            getDownloadUrl(u)
            
def getUrlsInOthersPage(url):
    soup = getPage(url)
    for h in soup.find_all("a", class_="num"):
        u = h.get("href")
        if u!="" and u!=None and u.endswith("html"):
            getUrlsInPage(urlHost+u)
            
def getDownloadUrl(url):
    soup = getPage(url)
    for h in soup.find_all("a", class_="Mbtn_s1"):
        u = h.get("href")
        if u!="" and u!=None:
            with open("index_down.html","a+") as f:
                f.write(u+"\n")
                print("the sample's url is " + url)
                downSample(u)  

def downSample(url):
    savePath = "samples/"
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'  
        headers = { 'User-Agent' : user_agent }
        print(url)
        request = urllib2.Request(url,headers=headers)  
        response = urllib2.urlopen(request)
        print("response code == " + str(response.code))
        if response.code == 200:
            fileHeader = response.headers
            content_type = fileHeader.get("Content-Type")
            if content_type == None:
                content_type = " "
            print(content_type)
            if content_type.find("application")!=-1:
                with open("index_down.html","a+") as f:
                    f.write(url+"\n")
                #ipa file
                print("it is preparing download sample from piqu.com")
                file_dis = fileHeader.get("Content-Disposition")
                 
                if file_dis == None:
                    file_out = savePath+url.split("/")[-1]
                else:
                    file_out = savePath + file_dis.split(";")[-1].split("=")[-1]
                if file_out==savePath:
                    file_out = savePath+url.split("/")[-1]
                print(file_out)
                with open(file_out,"wb") as f:
                    f.write(response.read())
 
                sendFiles(file_out,file_out.split("/")[-1]) 
                os.remove(file_out)
                print("it has finished downloading sample from piqu.com")
 
 
            elif content_type.find("text/plain")!=-1 or content_type == None:
                with open("index_down.html","a+") as f:
                    f.write(url+"\n")
                #zip file
                print("it is preparing download sample from piqu.com")
                file_out = savePath+url.split("/")[-1].replace("ipa","zip")
                with open(file_out,"wb") as f:
                    f.write(response.read())
                sendFiles(file_out,file_out.split("/")[-1]) 
                os.remove(file_out)
                print("it has finished downloading sample from piqu.com")
            else:
                pass
        else:
            print("this url can't be found")
    except urllib2.URLError, e:            
        if hasattr(e,"reason"):               
            print("this url needs a proxy and second scrapy")
            return None 
    except httplib.BadStatusLine,e:
        print("this url can't be acessed")
    except ssl.CertificateError,e:
        print("this url has a ssl.certificateError")
    except UnicodeEncodeError,e:
        pass
    except ValueError,e:
        pass

        
if __name__ == "__main__":
    urlHost = "http://www.piqu.com"
    getUrls(urlHost)
    
    
    
    
    
