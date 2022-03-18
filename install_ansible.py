#! /usr/bin/env python
# coding: utf-8

from py_modules import functions
import os
import shutil
import sys

os_version = functions.get_os_version()
work_dir = os.path.dirname(sys.argv[0])
os.chdir(work_dir)

msg_info = functions.colored('Ansible is install successful!', 'green')

if os_version == 1:
    os.system('rpm -ivh --force ansible/centos6/*')
    print msg_info
elif os_version == 2:
    os.system('yum install -y openssl openssl-devel')
    os.system('rpm -ivh --force ansible/centos7/*')
    print msg_info
else:
    print 'The OS type neither centos-6 nor centos-7, the program will be exit!'

shutil.copy('ansible.cfg', '/etc/ansible/ansible.cfg')
