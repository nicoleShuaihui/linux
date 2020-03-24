# linux
一些常用且提升效率的Linux命令

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
