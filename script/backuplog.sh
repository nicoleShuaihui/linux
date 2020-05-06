#!/bin/bash

#exit 0 表示先不执行
exit 0

logs_path=/var/log/nginx/

#date -d 中的参数表示date 日期，可以写now ,yesterday...

back_path=${ogs_path}$(date -d "yesterday" + "%Y")$(date -d "yesterday" + "%m")/

error_back_file=${back_path}error_$(date -d "yesterday" + "%Y%m%d").log
access_back_file=${back_path}access_$(date -d "yesterday" + "%Y%m%d").log

mkdir -p ${back_path}

mv ${logs_path}error.log ${error_back_file}
mv ${logs_path}access.log ${access_back_file}

kill -USER1 `${logs_path}/nginx.pid`

gzip ${error_back_file}
gzip ${access_back_file}
