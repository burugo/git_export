#!/usr/bin/env python 
#-*- coding: utf-8 -*- 
import sys
import os,shutil
from ftplib import FTP,error_perm
from datetime import time,datetime
import tarfile
_files=[]
#ftp config //cmp
_address=""
_port = 21
_user_name = ""
_password=""
_root="/"



def copy_dir(source_dir,target_dir):
    #print(source_dir) 
    for f in os.listdir(source_dir):
        source_f = os.path.join(source_dir,f)
        target_f = os.path.join(target_dir,f)

        if os.path.isfile(source_f):
            _files.append(target_f)
            if not os.path.exists(target_dir):  
                os.makedirs(target_dir)  

        if os.path.isdir(source_f):
            copy_dir(source_f,target_f) 


def get_ftp_filename(filename):
    parts = filename.split(os.path.sep)
    parts.pop(0)
    return os.path.sep.join(parts)

def ftp_down(dirname):
    if not dirname or not os.path.isdir(dirname):
        print ("请带上文件夹路径")
        return False

    #orig_path = os.path.realpath(dirname)
    t = datetime.now()
    target_path = dirname+"_server"+t.strftime("_%m%d_%H%M%S")
    copy_dir(dirname,target_path)
    if not  _files:
        print("no files") 
        return 
    #print(_files)
    ftp=FTP() 
    ftp.set_debuglevel(0)
    errors = [] 
    try:
        ftp.connect(_address,_port) 
    except Exception as e:
        print("ERROR:Can't connect to %s" % _address)
        shutil.rmtree(target_path)
        return
    try:
        ftp.login(_user_name,_password) 
    except Exception as e:
        print("ERROR: cannot login,please check username&password!")
        shutil.rmtree(target_path)
        ftp.quit()
        return
    print (ftp.getwelcome())#显示ftp服务器欢迎信息 

    ftp.cwd(_root) #选择操作目录 
    bufsize = 1024
    for filename in _files:
        _f = get_ftp_filename(filename)
        _ = os.path.split(_f)
        try:
            ftp.cwd("/"+_[0].replace("\\","/")) #选择操作目录
        except error_perm as e:
            print(e.args[0]+":"+_[0])
            continue
        bufsize = 1024
        file_handler = open(filename,'wb') #以写模式在本地打开文件 
        try:
            print("download:"+ _f)
            ftp.retrbinary('RETR %s' % _[1],file_handler.write,bufsize)#接收服务器上文件并写入本地文件 
            file_handler.close() 
        except error_perm as e:
            print(e.args)
            errors.append(_f)
            file_handler.close()
            os.remove(filename)
    ftp.quit() 
    print ("ftp down OK") 
    if errors:
        print("Not exist:")
        print(errors)

def extract_tar(commit_id):
   if os.path.isdir(commit_id):
       return True
   _f = commit_id+".tar"
   if not os.path.isfile(_f):
       return False
   tar = tarfile.open(_f,"r")
  # _f = os.path.basename(filename).split(".")[0]
   tar.extractall("./"+commit_id)
   tar.close()
   return True

if __name__ == '__main__':
    """放到当前目录下运行
    """
    commit_id = sys.argv[1]
    need_down = sys.argv[2]
    rt=extract_tar(commit_id)
    if rt and need_down!='n':
        ftp_down(commit_id)

