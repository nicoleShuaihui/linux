# -*- coding:utf-8 -*-
import commands

#当前时间：date +%s;python版本：python --version 2>&1 |awk 'print $2';最大文件打开：ulimit -n
#使用该些函数的方法：在main中调用例如：
#kernel_version=该文件名.kernal_version()
#获取hostname:import socket   ;hostname=socket.gethostname()

logfile='log/envcheck.log'

def logger (key,val):
    f=open(logfile, 'a+')
    f.write('%s: %s \n'%(key,val))
    f.close()

def wlogger (key,val):
    f=open(logfile, 'w+')
    f.write('%s: %s \n'%(key,val))
    f.close()
    
def kernal_version():
    try:
        test_cmd= 'uname -r'
        status, output =commands.getstatusoutput(test_cm)
        if status == 0:
            return output
        else:
            return "error"
    except:
        return "error"

def java_version():
    try:
        test_cmd="java -version 2>&1 |grep 'java version' |awk -F '\' '{print $2}'"
        status, output =commands.getstatusoutput(test_cm)
        if status == 0:
            return output
        else:
            return "error"
    except:
        return "error"

def cpu_capcity():
    try:
        test_cmd= 'cat /proc/cpuinfo|grep "proccessor" |wc -l'
        status, output =commands.getstatusoutput(test_cm)
        if status == 0:
            return output
        else:
            return "error"
    except:
        return "error"

def mem_capcity():
        try:
        test_cmd= 'cat /proc/meminfo|grep "MemAvailable" |awk '{print $2}''
        status, output =commands.getstatusoutput(test_cm)
        if status == 0:
            return output
        else:
            return "error"
    except:
        return "error"

