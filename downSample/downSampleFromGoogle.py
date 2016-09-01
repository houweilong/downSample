'''
Created on Nov 19, 2015

@author: hwl122902
'''
__author__ = 'CQC'
# -*- coding:utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import httplib
import re
import ssl
import ftplib 
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
        print soup.prettify()
        with open("index.html","a+") as f:
            for h in soup.find_all("h3"):
                for c in h.children:
                    f.write(c.get("href")+"\n")
                    print(c.get("href"))
		    downSample(c.get("href"))
        urls = soup.find_all("a",class_="pn")
	if urls != None:
            if urls[0] != urls[-1]:
                url = "https://www.google.com" + urls[-1].get("href")
                print("the next page's url is : " + url)
                getPage(url)
            else:
                pass
    except urllib2.URLError, e:            
        if hasattr(e,"reason"):               
            print("this url is can't be accessed,the reason is : ",e.reason)
            return None 
    except ValueError,e:
	    pass 


def getSeccondPage(url):
    with open("index_new.html","a+") as f:
	f.write(url + "\n")
    try:  
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'  
        headers = { 'User-Agent' : user_agent }
        req = urllib2.Request(url,None,headers)
        html = urllib2.urlopen(req).read()
        soup = BeautifulSoup(html)
        secondUrls = soup.find_all("a",href=re.compile("ipa"))
        for h in secondUrls:
            secondUrl = h.get("href")
            if secondUrl.find("http") == -1:
                urls = url.split("/")
                secondUrl = urls[0] + "//" + urls[2] + secondUrl
            print("the url in the second page is : " + secondUrl)
            #down the sample in the second page
            downSecondSample(secondUrl)
    except urllib2.URLError, e:            
        if hasattr(e,"reason"):               
            print("this url is can't be accessed,the reason is : ",e.reason)
            return None 
    except ValueError,e:
	    pass
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
            if content_type.find("text/html")!=-1:
                #this url express a html,not an ipa,save the url for second scrapy
                print("this url needs a second scrapy")
                with open("index_second.html","a+") as f:
                    f.write(url+"\n")
                    #get the url in the second page
                    getSeccondPage(url)
            elif content_type.find("application")!=-1:
                #ipa file
                print("it is preparing download sample from google")
                file_dis = fileHeader.get("Content-Disposition")
                
                if file_dis == None:
                    file_out = savePath+url.split("/")[-1]
                else:
                    file_out = savePath + file_dis.split(";")[-1].split("=")[-1]
                if file_out==savePath:
                    file_out = savePath+url.split("/")[-1]

                with open(file_out,"wb") as f:
		    f.write(response.read())

		sendFiles(file_out,file_out.split("/")[-1]) 

                with open("index_down.html","a+") as f:
                    f.write(url+"\n")
            elif content_type.find("text/plain")!=-1 or content_type == None:
                with open("index_down.html","a+") as f:
                    f.write(url+"\n")

                #zip file
                print("it is preparing download sample from google")
                file_out = savePath+url.split("/")[-1].replace("ipa","zip")
                #multiDownload.mutiDown(url, file_out)
                with open(file_out,"wb") as f:
		    f.write(response.read())
		sendFiles(file_out,file_out.split("/")[-1]) 
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

def downSecondSample(url):
    savePath = "samples/"
    with open("index_new.html","a+") as f:
	f.write(url + "\n")
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'  
        headers = { 'User-Agent' : user_agent }
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
                #ipa file
                print("it is preparing download sample from google")
                file_dis = fileHeader.get("Content-Disposition")
                
                if file_dis == None:
                    file_out = savePath+url.split("/")[-1]
                else:
                    file_out = savePath + file_dis.split(";")[-1].split("=")[-1]
                if file_out==savePath:
                    file_out = savePath+url.split("/")[-1]

                with open(file_out,"wb") as f:
		    f.write(response.read())

		sendFiles(file_out,file_out.split("/")[-1]) 
                with open("index_down.html","a+") as f:
                    f.write(url+"\n")
            elif content_type.find("text/plain")!=-1 or content_type == None:
                with open("index_down.html","a+") as f:
                    f.write(url+"\n")

                #zip file
                print("it is preparing download sample from google")
                file_out = savePath+url.split("/")[-1].replace("ipa","zip")
                #multiDownload.mutiDown(url, file_out)
                with open(file_out,"wb") as f:
		    f.write(response.read())
		sendFiles(file_out,file_out.split("/")[-1]) 
            else:
                pass
    except urllib2.URLError, e:            
        if hasattr(e,"reason"):               
            print("this url needs a proxy and second scrapy")
    except httplib.BadStatusLine,e:
        print("this url can't be acessed")
    except ssl.CertificateError,e:
        print("this url has a ssl.certificateError")
    except UnicodeEncodeError,e:
        pass
    except ValueError,e:
	pass

def readUrl(filename):
    with open(filename,"r") as f:
        for line in f.readlines():
            line = line.strip()
            print("the url in the index.html is : " + line)
            downSample(line)
def readSecondUrl(filename):
    with open(filename,"r") as f:
        for line in f.readlines():
            line = line.strip()
            print("the url in the index_second.html is : " + line)
            downSecondSample(line)
   
        
if __name__ == "__main__":
    #url="https://www.google.com.tw/search?q=ext:ipa&biw=1280&bih=923&tbs=qdr:w&ei=-SZuVpaBNsi60gSQ1qToDg&start=0&sa=N"
    #getPage(url)
    readUrl("index.html")
    
    
    
    
    
    
