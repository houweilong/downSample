'''
Created on Nov 26, 2015

@author: hwl122902
'''
import os  
from threading import Thread  
import urllib2
  
class AxelPython(Thread):  
    '''''Multi-thread downloading class. 
 
        run() is a vitural method of Thread. 
    '''  
    def __init__(self, threadname, url, filename, ranges=0):  
        Thread.__init__(self, name=threadname)  
        self.name = threadname  
        self.url = url  
        self.filename = filename  
        self.ranges = ranges  
        self.downloaded = 0  

    def run(self):  
        try:  
            self.downloaded = os.path.getsize(self.filename)  
        except OSError:  
            self.downloaded = 0  
  
        self.startpoint = self.ranges[0] + self.downloaded  
        
        if self.startpoint >= self.ranges[1]:  
#             print 'Part %s has been downloaded over.' % self.filename  
            return  
  
        self.oneTimeSize = 102400  # 100kByte/time  
#         print 'task %s will download from %d to %d' % (self.name, self.startpoint, self.ranges[1])  
        
        req = urllib2.Request(self.url)
        req.headers['Range'] = 'bytes=%s-%s' % (self.startpoint, self.ranges[1])
        urlhandle  = urllib2.urlopen(req)

        data = urlhandle.read(self.oneTimeSize)
        
        filehandle = open(self.filename, 'wb')
        while data and self.startpoint<self.ranges[1]:  
            filehandle.write(data) 
            self.startpoint += len(data) 
            self.downloaded += len(data)  
            data = urlhandle.read(self.oneTimeSize)  
        filehandle.close() 
        
def GetUrlFileSize(url):  
    urlHandler = urllib2.urlopen(url)  
    headers = urlHandler.info().headers  
    length = 0  
    for header in headers:  
        if header.find('Length') != -1:  
            length = header.split(':')[-1].strip()  
            length = int(length)  
    return length  
   
def SpliteBlocks(totalsize, blocknumber): 
    blocksize = totalsize / blocknumber  
    ranges = []  
    for i in range(0, blocknumber - 1):  
        ranges.append((i * blocksize, i * blocksize + blocksize - 1))  
    ranges.append((blocksize * (blocknumber - 1), totalsize - 1))  
    
    return ranges  
   
def islive(tasks):  
    for task in tasks:  
        if task.isAlive():  
            return True  
    return False  
   
def mutiDown(url, output, blocks=6):  
    size = GetUrlFileSize(url)  
    ranges = SpliteBlocks(size, blocks)
  
    threadname = ["thread_%d" % i for i in range(0, blocks)]  
    filename = ["tmpfile_%d" % i for i in range(0, blocks)]  
  
    tasks = []  
    for i in range(0, blocks):  
        task = AxelPython(threadname[i], url, filename[i], ranges[i])  
        task.setDaemon(True)  
        task.start()  
        tasks.append(task)  
  
    while islive(tasks):  
        pass
   
    filehandle = open(output, 'wb+')  
    for i in filename:  
        f = open(i, 'rb')  
        filehandle.write(f.read())  
        f.close()  
        try:  
            os.remove(i)  
        except:  
            pass  
   
    filehandle.close()  
