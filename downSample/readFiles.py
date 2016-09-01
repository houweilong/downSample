'''
Created on Nov 26, 2015

@author: hwl122902
'''
import os

def read():
    f_index = open("index.html").readlines()
    f_index_down = open("index_down.html").read()
    f_index_failed = open("index_failed.html").read()
    f_index_proxy = open("index_proxy.html").read()
    f_index_second = open("index_second.html").read()
    f_list = f_index_down+f_index_failed+f_index_proxy+f_index_second

    for line in f_index:
        line = line.strip()
        if f_list.find(line)!=-1:
            print line
        else:
            with open("index1.html","a+") as f:
                f.write(line+"\n")
    
    os.rename("index1.html", "index.html")
    
if __name__=='__main__':
    read()
