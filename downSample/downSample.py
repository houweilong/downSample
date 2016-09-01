
__author__ = 'CQC'
# -*- coding:utf-8 -*-
import urllib2
import json
from deb_pkg_tools.package import inspect_package_fields

class DownSample: 
    def __init__(self,hostname,readPath):
        self.hostname = hostname
        self.readPath = readPath                 
        #self.savePath = "sample/"
        self.savePath = "/mnt/hgfs/share/apt.feng.com/"
        self.d = {}
    def read(self):
        print self.readPath
        with open(self.readPath, 'r') as f:
            for line in f.readlines():
                if line.startswith("Package"):
                    filename = line.split(":")[1]
                elif line.startswith("Filename"):
                    tmpurl = line.split(":")[1].split("/")
                    fileurl = self.hostname + tmpurl[-2].strip() + "/" + tmpurl[-1].strip()
                    print "fileurl = ",fileurl
                    self.d[filename] = fileurl
                else:
                    pass
                
    #extract the content of the control file
    def extractControlFile(self,filename):
        dfile = {}
        try:
            dfile = repr(inspect_package_fields(filename))
        except:
            pass
        print dfile
        return json.dumps(dfile)

    def getPage(self): 
        self.read()      
        try:            
            user_agent = 'Mozilla/5.0 (iPad; CPU OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A452 Safari/601.1'  
            headers = { 'User-Agent' : user_agent } 
            for k in self.d.keys():
                k.replace("\n","")
                filename = self.savePath + k.strip() + ".deb"
                print "filename",filename
                url = self.d.get(k) 
                print "it is preparing download sample"
                request = urllib2.Request(url,headers=headers)  
                response = urllib2.urlopen(request)
                with open(filename, 'wb') as f:
                    f.write(response.read())
                #extract the content of the control file  
                self.extractControlFile(filename)
        except urllib2.URLError, e:            
            if hasattr(e,"reason"):               
                print "failed",e.reason
                return None 
            