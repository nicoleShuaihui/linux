# linux
一些常用且提升效率的Linux命令

### 两个文件找出相同的值
1、前提：文件a 和b 文件本身都有重复的数据，文件本身去重，排序后保存在 1 和 2中
```
sort -u a > 1
sort -u b> 1

1和2的数据合一起找出重复的数据，三种方式：
1、使用sort
sort 1 2 | uniq -d
234
345
456

2、使用awk，不推荐，实质还是使用了sort性质
awk '{print $1}' 1 2  | sort | uniq -d 
234
345
456

3、grep -f 1 2
234
345
456
```

### 打隧道
在此需要使用 -N 选项。因为只允许用于建立隧道。

> sh -p 36000 -N -L 4430:10.18.131.52:443 calico_cat@114.117.211.190

显示过滤注释( # ; 开头) 和空行后的配置信息
> grep -Ev “^$|^[#;]” server.conf

20200520

1、获取数组的长度

array=(bill   chen  bai   hu);

num=${#array[@]}  //获取数组元素的个数

20200815

脚本写入定时任务：

```
1、touch /var/spool/cron/root && grep 'check_scheduler_alive' /var/spool/cron/root || echo '*/3 * * * * /bin/bash /server/scripts/check_scheduler_alive.sh' >> /var/spool/cron/root

LINUX 查看某个指定时间段的日志
2、sed -n '/Jun 17 13:39:54/ , /Jun 18 10:50:28/p' kern.log
3、grep '2019-03-02 11:4[1-2]' user-center.2019-03-02.log
4、修改hostname :hostname 名称 .su生效,su的作用是：变更其他使用者的身份，除root外，输入其他使用者的密码

```

5、怎么写提示性的用法

```
function Usage()
{
        echo "$0 install|update"
}

if [ $# == 0 ];then
        Usage;
        exit 1;
fi

cmd=$1
if [ "$cmd" != "install" -a "$cmd" != "update" ];then
        Usage;
        exit 1;
fi

```

关于用户ulimit的一些疑问

1、ulimit -HSn 600000

H：硬限制；S 软限制; 后置为限制的值


2、umask 0022

3、ulimit -c unlimited

4、ulimit -n 200000 2>/dev/null


```
shell注释说明：如果遇见大量的代码，可以使用定义函数，但是不调用，
 
if [ $# != 1 ] ; then
 echo "USAGE: $0 conf"
    exit 1;
fi

$#:表示传值的个数
$0:表示文件名
$?:表示上个命令退出的状态
$$:表示PID
```

最新：20200415

1、df -hT 查看磁盘类型与大小
i
2、sed -i '/UUID/d' /etc/fstab  查找某行字符包含的内容，并删除

3、分区挂载


```

parted -s /dev/sdb mk1abe1 g0pt
parted -s /dev/sdb mkpart primary 0% 100%
mkfs.xfs /dev/sdb
echo "dev/sdb1 /data1 xfs defaults 0 0" >>/etc/fstab

分区挂载：fdisk /dev/sdb 
d wq   可以取消挂载

```
4、grep /data$ $，表示以某个字符结尾

5、xfs_info 文件目录

6、cat filename |sort -f -k2 -t '-'|sort -f

7、vi文件中的替换：:%s/,/\r/g 

8、删除空行：:g/^$/d

9、查看grep的前后行5行 -C 5，后5行，-A 5，前5行 -B 5

```
-f:安装字母排序
-k：与-t连用，-t安装某个字符截断，第二部分的字母进行排序

pip install -U pandas -i "https://pypi.doubanio.com/simple/"

cp -f /etc/nginx/nginx.conf{,.backup}

1、Linux查看系统开机时间
last reboot:可以看到Linux系统历史启动的时间
who -b: 查看最后一次系统启动的时间

update 更新两个字段需要用逗号隔开
*** 通过表查看数据库
SELECT table_schema FROM information_schema.TABLES WHERE table_name = '表名';

*** 通过找字段再找表


use information_schema;
select * from columns where column_name='字段名' ;

```
##



1.grep -I etcd -R 递归查询某文件的内容

2.for i in {0..9};do 实施的命令；done 循环实施某个命令

3.ssh root@IP “需要执行的命令”
>    ssh root@IP “bash -s” < 脚本

例如：

> for i in `cat ip` ; do echo "*******$i**********";ssh root@$i  "bash -s" <  ./part.sh ;done

放于某台机子内的命令，这样的好处是，可不用批量发送到每台机子内

注意：后面跟的脚本不能加bash/sh

原因：bash -s:表示当前bash 执行，而加入bash 脚本执行相当于进入另一个bash里面了

> -bash: sh: No such file or directory


4.分盘的批量脚本 part.sh

```
#!/bin/bash
#可双tab查看所支持的文件类型有哪些，这边tbase支持的xfs
#关于数组的概念，1.输出所有的数组的符号有：*，@
```
```
 fsname=(sdb nvme1n1 nvme0n1)
 for i in ${fsname[@]};do
     mkfs.xfs /dev/$i
 done    
 mkdir -p {/data,/data1,/data2}
 if [ $? -eq 0 ];then
     echo "`blkid |grep  ${fsname[0]} | awk '{print $2}'` /data xfs defaults 1 1" >>/etc/fstab
     echo "`blkid |grep  ${fsname[1]} | awk '{print $2}'` /data1 xfs defaults 1 1" >>/etc/fstab
     echo "`blkid |grep  ${fsname[2]} | awk '{print $2}'` /data2 xfs defaults 1 1" >>/etc/fstab
 else
     echo "Failed to create file"
 fi
 mount -a
 lsblk
```
5、批量解压：for pkg in *.tar.gz; do tar xf $pkg; done

6、关闭swap:

```
swapoff –a
sed -i 's/.swap./#&/' /etc/fstabv
```

7、输出标题:
> ps -aux |head  -1;

8、使用xargs ，批量操作
> kubectl get cm -nouter-dns |grep -v 'NAME' |awk '{print $1}' |xargs kubectl delete cm -n outer-dns

9、查看文件存储
文件大小查看
```
du -sh  ：查看文件的目录总共占的容量
du -lh --max-depth=1:查看当前目录下一级文件和子目录占用的磁盘容量

```

10、ls 时间排序大小

```
（1）倒叙（最新-过去）：ls -lrt 
                 -r :-r表示reverse的意思，这里就是reverse order倒序
（2）查看大小： ls -shl
               -h 表示将文件大小转为我们习惯的M，K等为单位的大小
               -s表示排序，默认是降序排列。

```
11、rpm安装rpm包

> rpm -ivh XXXX.rpm

> rpm -ivh name --force --nodeps 

> 查询rpm 包： rpm -qf  `which vim`

-i ：安装的意思

-v ：可视化

-h ：显示安装进度

另外在安装一个rpm包时常用的附带参数有：

--force 强制安装，即使覆盖属于其他包的文件也要安装

--nodeps 当要安装的rpm包依赖其他包时，即使其他包没有安装，也要安装这个包
 
> yum install test.rpm -y --downloadonly --downloaddir=/usr/local/src 

12、查看系统信息

查看内核：

> 1、cat /proc/version

> 2、uname -a

查看Linux系统版本的命名

> 1、lsb_release -a，即可列出所有版本信息：

PS:适合所有的Linux发行版本

> 2、cat /etc/redhat-release，这种方法只适合Redhat系的Linux：

> 3、cat /etc/issue，此命令也适用于所有的Linux发行版。

13、查看某个包

> yum provides <程序名>

14、mysql查看id是否为自增的

> 查看是否有自增：SELECT auto_increment FROM information_schema.`TABLES` WHERE TABLE_SCHEMA='tdsql_oss' AND TABLE_NAME='tdsql_spec_config';

> 修改表结构：ALTER TABLE tdsql_spec_config CHANGE id id int(10) NOT NULL auto_increment ;

> 查看创建表结构:show create table tdsql_spec_config;

> 对比工具：vim -d file1 file2 / vimdiff file1 file2

15、查看tdsql的问题逻辑

```
在keeper节点
su - tdsql
cd /data/scheduler/bin && ./resource_tool status_res all    # 得到的是所有DB母机的信息，包括已经使用的端口、隔离的端口、有故障的端口等

```

16、ls查看信息

```

1) ls -lt  时间最近的在前面

2) ls -ltr 时间从前到后

3) 利用sort

    ls -l | sort +7 (日期为第8列)   时间从前到后

    ls -l | sort -r +7      时间最近的在前面

```

17、

> kubectl get cm -n tdsql |grep -v "NAME" |awk '{print $1}' |xargs kubectl delete cm -n tdsql
> kubectl get cm tdsql.cm.supervisord -n tdsql -o yaml

18、

ulimit -n ：可以查看当前的最大打开文件数

19、系统配置参数生效

sysctl -p


