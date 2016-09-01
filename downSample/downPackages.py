'''
Created on Nov 2, 2015

@author: hwl122902
'''

import urllib2
import bz2
import gzip
from downSample import DownSample


class DownPackage:
    def __init__(self,hostName):
        self.hostname = hostName
        if(hostName.find("http://repo.so/") != -1):
            self.url = hostName + "Packages.gz"
        else:
            self.url = hostName + "Packages.bz2"
      
    def downSample(self,path):
        down = DownSample(self.hostname,path)
        down.getPage()
        
    def un_bz2(self,file_name):
        b_file = bz2.BZ2File(file_name).read()
        f_name = file_name.split(".")[0]
        newfile = open(f_name,'w+')
        newfile.write(b_file)
        newfile.close()
        #begin downloading sample from internet
        self.downSample(f_name)
        
    def un_gz(self,file_name):
        f_name = file_name.split(".")[0]
        g_file = gzip.GzipFile(file_name)
        open(f_name,"w+").write(g_file.read())
        g_file.close()
        #begin downloading sample from internet
        self.downSample(f_name)
        
    
    def downPackage(self):
        try:            
            user_agent = 'Mozilla/5.0 (iPad; CPU OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A452 Safari/601.1'  
            headers = { 'User-Agent' : user_agent } 
            filename = "packages." + self.url.split(".")[-1]
            print "filename=",filename
            request = urllib2.Request(self.url,headers=headers)  
            response = urllib2.urlopen(request) 
            with open(filename, 'wb') as f:
                f.write(response.read())
            #decompress the file
            print filename.split(".")[-1]
            if filename.split(".")[-1] == "bz2":
                print "un_bz2 is invoked"
                self.un_bz2(filename)  
            else:
                print "un_gz is invoked"
                self.un_gz(filename)
            
        except urllib2.URLError, e:            
            if hasattr(e,"reason"):               
                print "failed",e.reason
                return None 
    
  



