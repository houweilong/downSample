'''
Created on Dec 23, 2015

@author: hwl122902
'''
import hashlib

def getFileSha1(filename):
    sha1 = hashlib.sha1(open(filename,"rb").read())
    return sha1.hexdigest()

if __name__ == "__main__":
    print(getFileSha1("IPadQQ"))
    
