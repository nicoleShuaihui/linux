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
def validation_yum():
    """
    检查是否存在可用的yum源，有则返回True，没有则返回False
    """
    f = os.popen('yum list| wc -l')
    yum_list_count = int(f.read().strip('\n'))
    if yum_list_count > 500:
        return True
    else:
        return False
def validation_dir(dir_path='/data/application'):
    '检测相关目录是否存在，不存在则创建'
    if not os.path.exists(dir_path):
        if not os.path.exists('/data'):
            os.mkdir('/data')
        os.mkdir('/data/application')
def install_jdk(jkd_name,jdk_rpm_path):
    """
    安装jdk
    """
    jdk_rpm_path = './rpm/' + jkd_name   
    shell_command = 'rpm -ivh %s' %(jdk_rpm_path) 
    os.system(shell_command)
    if os.path.exists('/usr/bin/java'):
        return 1
    else:
        return 0
