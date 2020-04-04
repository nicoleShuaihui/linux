### 准备机器

| 机器 | 配置  | 账户密码        | 公网IP          | 内网IP        |
| ---- | ----- | --------------- | --------------- | ------------- |
| init | 4C8G  | root/Tke@123456 | 106.52.130.104  | 192.168.0.7   |
| a1   | 8C16G | root/Tke@123456 | 129.204.224.52  | 192.168.0.110 |
| a2   | 8C16G | root/Tke@123456 | 106.52.232.62   | 192.168.0.109 |
| a3   | 8C16G | root/Tke@123456 | 111.230.210.135 | 192.168.0.58  |
| b1   | 8C16G | root/Tke@123456 | 106.52.130.11   | 192.168.0.88  |
| b2   | 8C16G | root/Tke@123456 | 129.204.236.25  | 192.168.0.120 |
| b3   | 8C16G | root/Tke@123456 | 193.112.179.193 | 192.168.0.28  |

### 物料下载

```bash
cd /opt && wget https://yz-trainning-1253183248.cos.ap-guangzhou.myqcloud.com/cpaas-20200306.tgz
cd /opt && wget  https://yz-trainning-1253183248.cos.ap-guangzhou.myqcloud.com/TKE-20200323-Tranning/cicd.tar.gz
```

### 解压物料

```bash
tar zxvf cpaas-20200306.tgz -C ./
tar zxvf cicd.tar.gz -C ./
```

## 安装管理集群

### 免密设置（优先）

```bash
# init机器上执行生成秘钥对
ssh-keygen -t rsa
# 将公钥复制到管理节点
ssh-copy-id -p 22 -i ~/.ssh/id_rsa.pub root@192.168.0.110 && ssh-copy-id -p 22 -i ~/.ssh/id_rsa.pub root@192.168.0.109 && ssh-copy-id -p 22 -i ~/.ssh/id_rsa.pub root@192.168.0.58
# 将公钥复制到业务节点 88 120 28
ssh-copy-id -p 22 -i ~/.ssh/id_rsa.pub root@192.168.0.88 && ssh-copy-id -p 22 -i ~/.ssh/id_rsa.pub root@192.168.0.120 && ssh-copy-id -p 22 -i ~/.ssh/id_rsa.pub root@192.168.0.28
# 然后输入密码
root/Tke@123456
```

### 环境检查

#### 初始节点

```bash
# 快捷操作
cat /etc/redhat-release && cat /proc/version && free -m|grep Swap|awk '{print $3}'

systemctl stop firewalld.service && setenforce 0

date && timedatectl

vim /etc/sysctl.conf 
vm.max_map_count=262144
net.ipv4.ip_forward = 1
cat /etc/sysctl.conf 

hostname tke7

chmod 777 /tmp

echo "" > /etc/hosts && cat /etc/hosts

cat <<EOF >/etc/hosts
127.0.0.1 localhost
192.168.0.7 tke7
192.168.0.110 tke110
192.168.0.109 tke109
192.168.0.58 tke58
192.168.0.88 tke88
192.168.0.120 tke120
192.168.0.28 tke28
EOF

cat /etc/hosts

--- --- --- ---- --- ---

# 系统版本 CentOS 7.6
cat /etc/redhat-release

# kernel 版本 大于 3.10.0-957
cat /proc/version

# Swap 返回0未开启（绝大多数），有数已开启
free -m|grep Swap|awk '{print $3}'

# 防火墙
systemctl stop firewalld.service
systemctl disable firewalld.service

# selinux
setenforce 0

# 时间同步
date

# 所有服务器时区必须统一
timedatectl

# 系统参数
vim /etc/sysctl.conf
vm.max_map_count=262144   
net.ipv4.ip_forward = 1

# hostname 字母开头，只能是字母、数字和短横线-组成，不能用短横线结尾，长度在 4-23 之间
hostname tke7

# hosts 所有服务器可以通过hostname 解析成 ip，可以将localhost解析成127.0.0.1，hosts 文件内，不能有重复的

echo "" > /etc/hosts && cat /etc/hosts

cat <<EOF >/etc/hosts
127.0.0.1 localhost
192.168.0.7 tke7
192.168.0.110 tke110
192.168.0.109 tke109
192.168.0.58 tke58
192.168.0.88 tke88
192.168.0.120 tke120
192.168.0.28 tke28
EOF

cat /etc/hosts

# /tmp 目录的权限是 777
chmod 777 /tmp
```

#### 全部节点

```bash
# 系统版本 CentOS 7.6（可跳过）
for i in 110 109 58 88 120 28 ; do  ssh 192.168.0.$i "cat /etc/redhat-release" ;  done 

# kernel 版本 大于 3.10.0-957（可跳过）
for i in 110 109 58 88 120 28 ; do  ssh 192.168.0.$i "cat /proc/version" ;  done

# Swap 返回0未开启（绝大多数），有数已开启
for i in 110 109 58 88 120 28 ; do  ssh 192.168.0.$i "free -m|grep Swap|awk '{print $3}'" ;  done

# 防火墙
for i in 110 109 58 88 120 28 ; do  ssh 192.168.0.$i "systemctl stop firewalld.service" ;  done
for i in 110 109 58 88 120 28 ; do  ssh 192.168.0.$i "systemctl disable firewalld.service" ;  done
for i in 110 109 58 88 120 28 ; do  ssh 192.168.0.$i "systemctl status firewalld.service" ;  done

# selinux
for i in 110 109 58 88 120 28 ; do  ssh 192.168.0.$i "setenforce 0" ;  done

# 时间同步（可跳过）
for i in 110 109 58 88 120 28 ; do  ssh 192.168.0.$i "date" ;  done

# 所有服务器时区必须统一（可跳过）
for i in 110 109 58 88 120 28 ; do  ssh 192.168.0.$i "timedatectl" ;  done

# 系统参数
for i in 110 109 58 88 120 28 ; do  ssh 192.168.0.$i "cat /etc/sysctl.conf | grep max_map_count" ;  done

for i in 110 109 58 88 120 28 ; do  ssh 192.168.0.$i "cat /etc/sysctl.conf | grep net.ipv4.ip_forward" ;  done

vim /etc/sysctl.conf
vm.max_map_count=262144   
net.ipv4.ip_forward = 1

# hostname 字母开头，只能是字母、数字和短横线-组成，不能用短横线结尾，长度在 4-23 之间
for i in 110 109 58 88 120 28 ; do  ssh 192.168.0.$i "hostname tke$i" ;  done

# hosts 所有服务器可以通过hostname 解析成 ip，可以将localhost解析成127.0.0.1，hosts 文件内，不能有重复的 hostname
for i in 110 109 58 88 120 28 ; do  ssh 192.168.0.$i "echo "" > /etc/hosts && cat /etc/hosts" ;  done 

cat <<EOF >/etc/hosts
127.0.0.1 localhost
192.168.0.7 tke7
192.168.0.110 tke110
192.168.0.109 tke109
192.168.0.58 tke58
192.168.0.88 tke88
192.168.0.120 tke120
192.168.0.28 tke28
EOF

for i in 110 109 58 88 120 28 ; do  ssh 192.168.0.$i "cat /etc/hosts" ;  done 

# /tmp 目录的权限是 777
for i in 110 109 58 88 120 28 ; do  ssh 192.168.0.$i "chmod 777 /tmp" ;  done
```

### 安装软件

```bash
# 初始节点
yum install -y curl tar ip ssh sshpass jq netstat timedatectl ntpdate nslookup base64 tr head openssl md5sum socat

# 全部节点
for i in 110 109 58 88 120 28 ; do  ssh 192.168.0.$i "yum install -y curl tar ip ssh sshpass jq netstat timedatectl ntpdate nslookup base64 tr head openssl md5sum socat telnet" ;  done
```

### 部署 haproxy

#### 安装

```bash
# 在init节点安装
yum -y install haproxy
```

#### 配置

```bash
global
    log     127.0.0.1 local0
    nbproc 1           # 1 is recommended
    maxconn  51200     # maximum per-process number of concurrent connections
    pidfile /etc/haproxy/haproxy.pid
    tune.ssl.default-dh-param 2048

defaults
        mode http      # { tcp|http|health }
        #retries 2
        #option httplog
        #option tcplog
        option redispatch
        option abortonclose
        timeout connect 5000ms
        timeout client 240m
        timeout server 240m
        log global
        balance roundrobin

listen stats
        bind 0.0.0.0:2936
        mode http
        stats enable
        stats refresh 10s
        stats hide-version
        stats uri  /admin
        stats realm LB2\ Statistics
        stats auth mathilde:Mathilde1861

listen web-service
    bind 127.0.0.1:9



frontend tke_frontend_80
  bind *:80
  mode tcp
  default_backend tke_80

frontend tke_frontend_443
  bind *:443
  mode tcp
  default_backend tke_443

frontend tke_frontend_6443
  bind *:6443
  mode tcp
  default_backend tke_6443



frontend tke_frontend_30900
  bind *:30900
  mode tcp
  default_backend tke_30900



frontend tke_frontend_30902
  bind *:30902
  mode tcp
  default_backend tke_30902



backend tke_80
  mode tcp
  balance roundrobin
server s0 192.168.0.110:80 check port 80 inter 1000 maxconn 51200
server s1 192.168.0.109:80 check port 80 inter 1000 maxconn 51200
server s2 192.168.0.58:80 check port 80 inter 1000 maxconn 51200


backend tke_443
  mode tcp
  balance roundrobin
server s0 192.168.0.110:443 check port 443 inter 1000 maxconn 51200
server s1 192.168.0.109:443 check port 443 inter 1000 maxconn 51200
server s2 192.168.0.58:443 check port 443 inter 1000 maxconn 51200


backend tke_6443
  mode tcp
  balance roundrobin
server s0 192.168.0.110:6443 check port 6443 inter 1000 maxconn 51200
server s1 192.168.0.109:6443 check port 6443 inter 1000 maxconn 51200
server s2 192.168.0.58:6443 check port 6443 inter 1000 maxconn 51200


backend tke_30900
  mode tcp
  balance roundrobin
server s0 192.168.0.110:30900 check port 30900 inter 1000 maxconn 51200
server s1 192.168.0.109:30900 check port 30900 inter 1000 maxconn 51200
server s2 192.168.0.58:30900 check port 30900 inter 1000 maxconn 51200

backend tke_30902
  mode tcp
  balance roundrobin
server s0 192.168.0.110:30902 check port 30902 inter 1000 maxconn 51200
server s1 192.168.0.109:30902 check port 30902 inter 1000 maxconn 51200
server s2 192.168.0.58:30902 check port 30902 inter 1000 maxconn 51200
```

#### 替换

```bash
# 查看
cat /etc/haproxy/haproxy.cfg
echo "" > /etc/haproxy/haproxy.cfg && cat /etc/haproxy/haproxy.cfg
vim /etc/haproxy/haproxy.cfg
# 启动
haproxy -c -f /etc/haproxy/haproxy.cfg
systemctl start haproxy && systemctl status haproxy
# 检查
netstat -tlunp | grep 80 && netstat -tlunp | grep 443 && netstat -tlunp | grep 6443 && netstat -tlunp | grep 30900 && netstat -tlunp | grep 30902
netstat -tlunp |grep -e "80|443|6443|30900|30902"
```

### 安装集群

#### 配置文件

```bash
[
  {
    "server_role": {
      "master":true,
      "global":true,
      "log":true
    },
    "ip_addr": "192.168.0.110",
    "ssh_port": "22",
    "ssh_user": "root",
    "ssh_passwd": "Tke@123456",
    "ssh_key_file": "/root/.ssh/id_rsa"
  },
  {
    "server_role": {
      "master":true,
      "global":true,
      "log":true
    },
    "ip_addr": "192.168.0.109",
    "ssh_port": "22",
    "ssh_user": "root",
    "ssh_passwd": "Tke@123456",
    "ssh_key_file": "/root/.ssh/id_rsa"
  },
  {
    "server_role": {
      "master":true,
      "global":true,
      "log":true
    },
    "ip_addr": "192.168.0.58",
    "ssh_port": "22",
    "ssh_user": "root",
    "ssh_passwd": "Tke@123456",
    "ssh_key_file": "/root/.ssh/id_rsa"
  }
]
```

#### 修改配置

```bash
# 配置文件
cd /opt/cpaas && cp server_list_3.json server_list.json
# 编辑文件
cd /opt/cpaas && echo "" > server_list.json && vim server_list.json
```

####  修改脚本

```bash
# 322行  改成 check_node_env=0
vim /opt/cpaas/up-cpaas.sh
```

#### 执行安装

```bash
# domain-name init节点外网地址
# kube_controlplane_endpoint init节点内网地址
cd /opt/cpaas
# 
./up-cpaas.sh \
--network-interface=eth0 \
--enabled-features=acp,devops,tke \
--global-network-mode=flannel \
--domain-name=106.52.130.104 \
--kube_controlplane_endpoint=192.168.0.7 \
--use-http
```

#### 访问界面

```bash
http://106.52.130.104  `admin@cpaas.io/password`
```

### 清理集群

```bash

```

## 安装业务集群

### 安装节点

```bash
# 看文档
```

### 安装helm①

```bash
# 在业务集群master上执行
1、registry=$(docker info |grep 60080  |tr -d ' ') && chart_repo_url=http://chartmuseum:chartmuseum@${registry/60080/8088}
2、docker run -ti --rm  -v /usr/local/bin/:/var/log/abc $registry/claas/helm:v2.14.3 sh -c "cp /systembin/helm /var/log/abc"
3、helm init  --stable-repo-url=$chart_repo_url --tiller-image=$registry/claas/tiller:v2.14.3
4、helm list
```

### 安装cert-manager②

```bash
# 在业务集群master上执行
registry=$(docker info |grep 60080  |tr -d ' ')
ACP_NAMESPACE=cpaas-system ## 改成部署时， --acp2-namespaces 参数指定的值，默认是cpaas-system
helm install \
     --name cert-manager \
     --namespace ${ACP_NAMESPACE} \
     --set global.registry.address=$registry \
     stable/cert-manager
     
#清理操作
helm delete --purge cert-manager
kubectl  delete crd certificates.certmanager.k8s.io
kubectl  delete crd challenges.certmanager.k8s.io
kubectl  delete crd clusterissuers.certmanager.k8s.io
kubectl  delete crd issuers.certmanager.k8s.io
kubectl  delete crd orders.certmanager.k8s.io
kubectl delete ns cert-manager
```

### 安装alauda-cluster-base③

```bash
# 在 global 的第一台 master 节点上执行以下命令

# 1
### 快捷操作
ROOT_USERNAME=admin@cpaas.io && REGISTRY_ENDPOINT=$(docker info |grep 60080  |tr -d ' ') && REGION_NAME=cls-2n5t95qk && ACP_NAMESPACE=cpaas-system
### 详细解释
ROOT_USERNAME=admin@cpaas.io  ## 默认为admin@cpaas.io，需要与登录global界面时使用的邮箱一致。
REGISTRY_ENDPOINT=$(docker info |grep 60080  |tr -d ' ')
REGION_NAME=cls-2n5t95qk ## 想要部署 alauda-cluster-base 的集群的名字，需要自行修改,tke集群名获取可从页面获取
ACP_NAMESPACE=cpaas-system ## 改成部署时， --acp2-namespaces 参数指定的值，默认是cpaas-system

# 2
mkdir /tmp/region_helmrequest

# 3
cat << EOF >/tmp/region_helmrequest/${REGION_NAME}-alauda-cluster-base.yaml
apiVersion: app.alauda.io/v1alpha1
kind: HelmRequest
metadata:
  finalizers:
  - captain.alauda.io
  generation: 1
  name: ${REGION_NAME}-alauda-cluster-base
  namespace: ${ACP_NAMESPACE}
spec:
  chart: stable/alauda-cluster-base
  namespace: ${ACP_NAMESPACE}
  releaseName: ${REGION_NAME}-alauda-cluster-base
  clusterName: ${REGION_NAME}
  values:
    global:
      auth:
        default_admin: ${ROOT_USERNAME}
      labelBaseDomain: cpaas.io
      namespace: ${ACP_NAMESPACE}
      registry:
        address: ${REGISTRY_ENDPOINT}
  version: $(helm search | grep '^stable/alauda-cluster-base ' | awk '{print $2}')
EOF
# 4
kubectl create -f /tmp/region_helmrequest/${REGION_NAME}-alauda-cluster-base.yaml
# 5.检查
kubectl get hr -n cpaas-system | grep alauda-cluster-base

# 清理操作
REGION_NAME=cls-2n5t95qk
kubectl delete -f /tmp/region_helmrequest/${REGION_NAME}-alauda-cluster-base.yaml
```

### 安装prometheus ④

#### 1.准备工作

```bash
# 1.准备工作，监控 etcd 先判断 etcd-ca 是否存在，在要部署普罗米修斯的集群的 master 节点操作
kubectl get secrets -n cpaas-system | grep etcd-ca

# 2.若不存在则按以下命令添加，若存在，跳过这一步。
`注意：命令要修改 ns ，不能复制粘贴。`
kubectl get secrets -n cpaas-system etcd-ca -o yaml >/tmp/etcd-ca.yaml
sed -i  '/namespace:/{s/kube-system/<改成部署时 配置的 ns 的值>/g}' /tmp/etcd-ca.yaml
kubectl apply -f /tmp/etcd-ca.yaml

# 3.如果上一步报错，提示找不到 etcd-ca，执行下面的命令创建
kubectl create secret tls etcd-ca --cert=/etc/kubernetes/pki/etcd/ca.crt --key=/etc/kubernetes/pki/etcd/ca.key -n cpaas-system
kubectl create secret tls etcd-peer --cert=/etc/kubernetes/pki/etcd/peer.crt --key=/etc/kubernetes/pki/etcd/peer.key -n cpaas-system
```

#### 2.安装 prometheus-operator

```bash
# 1 在要部署的业务集群的第一台 master 节点上执行以下命令
### 快捷操作 
REGISTRY_ENDPOINT=$(docker info |grep 60080  |tr -d ' ') && REGION_NAME=cls-2n5t95qk && ACP_NAMESPACE=cpaas-system
### 详细解释
REGISTRY_ENDPOINT=$(docker info |grep 60080  |tr -d ' ')
REGION_NAME=cls-2n5t95qk ## 想要部署 alauda-cluster-base 的集群的名字，需要自行修改
ACP_NAMESPACE=cpaas-system ## 改成部署时， --acp2-namespaces 参数指定的值，默认是cpaas-system

# 2
helm install --version $(helm search | grep '^stable/prometheus-operator ' | awk '{print $2}') \
             --namespace=${ACP_NAMESPACE} \
             --name=prometheus-operator \
             --set global.namespace=${ACP_NAMESPACE} \
             --set global.registry.address=${REGISTRY_ENDPOINT} \
             stable/prometheus-operator --wait --timeout 3000
```

#### 3.安装 kube-prometheus

```bash
# 1.给集群中的一个 node（不能是master节点） 添加 monitoring=enabled 的 label，用于 local volume 的调度。

# 需要将 ${test} 替换为这个 node 在 k8s 中的实际 hostname。
kubectl get nodes --all-namespaces
# 在要部署普罗米修斯的集群的 master 节点上操作，命令如下：
kubectl label --overwrite nodes ${test} monitoring=enabled
# kubectl label --overwrite nodes 192.168.0.28 monitoring=enabled

# 2.在该 node（和第一个点里面的节点对应） 上创建以下目录用作持久化目录，保证空间 granafa 5G / prometheus 30G / alertmanager 5G，ssh 到这台服务器上，执行如下命令：
mkdir -p /cpaas/monitoring/{grafana,prometheus,alertmanager} && chmod -R 777 /cpaas/monitoring

# 3.下面的操作在要部署的业务集群的第一台 master 节点上操作，执行如下命令
### 快捷操作
REGISTRY_ENDPOINT=$(docker info |grep 60080  |tr -d ' ') && DOMAIN_NAME=106.52.130.104 && REGION_NAME=cls-2n5t95qk && ACP_NAMESPACE=cpaas-system
### 详细解释
REGISTRY_ENDPOINT=$(docker info |grep 60080  |tr -d ' ')
DOMAIN_NAME=106.52.130.104 ## 需要修改为 global 界面的访问地址，也就是部署 global 的时候，--domain-name 参数的值
REGION_NAME=cls-2n5t95qk ## 想要部署 alauda-cluster-base 的集群的名字
ACP_NAMESPACE=cpaas-system ## 改成部署 global 时， --acp2-namespaces 参数指定的值，默认是cpaas-system


# 4.下面的操作在要部署的业务集群的第一台 master 节点上操作，执行如下命令
helm install --version $(helm search | grep '^stable/kube-prometheus ' | awk '{print $2}') \
             --namespace=${ACP_NAMESPACE} \
             --name=kube-prometheus \
             --set global.namespace=${ACP_NAMESPACE} \
             --set global.platform=ACP \
             --set global.labelBaseDomain=cpaas.io \
             --set prometheus.service.type=NodePort \
             --set grafana.service.type=NodePort \
             --set global.registry.address=${REGISTRY_ENDPOINT} \
             --set grafana.storageSpec.persistentVolumeSpec.local.path=/cpaas/monitoring/grafana \
             --set prometheus.storageSpec.persistentVolumeSpec.local.path=/cpaas/monitoring/prometheus \
             --set alertmanager.storageSpec.persistentVolumeSpec.local.path=/cpaas/monitoring/alertmanager \
             --set alertmanager.configForACP.receivers[0].name=default-receiver \
             --set alertmanager.configForACP.receivers[0].webhook_configs[0].url=https://${DOMAIN_NAME}/v1/alerts/${REGION_NAME}/router \
             stable/kube-prometheus
```

#### 4.安装失败清理

```bash
# 清理操作(如果需要重装监控组件,则执行此操作。包含：prometheus-operator、kube-prometheus)
kubectl delete -f /tmp/prometheus-feature.yaml
helm delete --purge kube-prometheus
# 如果使用本地路径方式部署，则还需要执行以下命令
kubectl delete pvc prometheus-kube-prometheus-db-prometheus-kube-prometheus-0 -n cpaas-system
kubectl delete pvc alertmanager-kube-prometheus-db-alertmanager-kube-prometheus-0 -n cpaas-system
helm delete --purge prometheus-operator

# helm（忽略）
helm ls --all kube-prometheus
helm delete kube-prometheus --purge
# pv（忽略）
kubectl get pv -n cpaas-system
kubectl patch pv alertmanager-pv -p '{"metadata":{"finalizers":null}}'
```

#### 5.检查安装情况

```bash
# 查看所有 pod 是否正常启动（pod 为 Running 或者 Completed 状态），在部署普罗米修斯的集群的 master 节点上执行以下命令
kubectl get pods -n cpaas-system | grep prometheus
```

#### 6.集群对接监控

```bash
# 1.在部署普罗米修斯的集群的 master 节点上操作

### 快捷操作
ip=106.52.130.11 && ACP_NAMESPACE=cpaas-system
###
ip=192.168.122.30 ## 需要修改为业务集群任意一个 master 节点的外网 ip，若没有外网地址，使用默认的实际ip
ACP_NAMESPACE=cpaas-system ## 改成部署时， --acp2-namespaces 参数指定的值，默认是cpaas-system

# 2
cat << eof > /tmp/prometheus-feature.yaml
apiVersion: infrastructure.alauda.io/v1alpha1
kind: Feature
metadata:
  labels:
    instanceType: prometheus
    type: monitoring
  name: prometheus
spec:
  accessInfo:
    grafanaAdminPassword: admin                # grafana 默认密码
    grafanaAdminUser: admin                    # grafana 默认用户
    grafanaUrl: http://$ip:30902               # grafana 地址
    name: kube-prometheus                      # 安装 kube-prometheus chart 时指定的名称
    namespace: ${ACP_NAMESPACE}                # kube-prometheus chart 所在的命名空间
    prometheusTimeout: 10                      # prometheus 请求超时时间
    prometheusUrl: http://$ip:30900            # prometheus 地址
  instanceType: prometheus
  type: monitoring
  version: "1.0"
eof

# 3
kubectl apply -f /tmp/prometheus-feature.yaml
```

#### 7.修改k8s配置

```bash
# 业务集群所有master节点,修改kubernetes 配置文件
kubectl get no -n cpaas-system

# 修改kubernetes 配置文件，监听网卡ip。
# 删除以下配置文件中以下行内容 - --bind-address=127.0.0.1
vim /etc/kubernetes/manifests/kube-scheduler.yaml
vim /etc/kubernetes/manifests/kube-controller-manager.yaml

# 执行以下命令，将其中 metricsBindAddress: 127.0.0.1:10249 改为 metricsBindAddress: 0.0.0.0:10249
kubectl edit cm -n kube-system kube-proxy
# 然后重建所有kube-system下kube-proxy的pod
kubectl get pod -n kube-system | grep kube-proxy

kubectl delete pod kube-proxy-d27gc kube-proxy-fmfs4 kube-proxy-q2q4n -n kube-system

# kubectl get pods kube-proxy-lsblp -n kube-system -o yaml
```

### 安装jenkins ⑤

```bash
# 1.在业务集群以本地路径的方式部署 jenkins，（对接了GitLab）。

### 如何获取token，到devops-apiserver所在集群（一般为global集群）执行
ACP_NAMESPACE=cpaas-system ; echo $(kubectl get secret -n ${ACP_NAMESPACE} $(kubectl get secret -n ${ACP_NAMESPACE} | grep devops-apiserver-token |awk '{print $1}') -o jsonpath={.data.token} |base64 --d) 

### 快捷操作
NODE_NAME="192.168.0.120" && global_vip="192.168.0.7" && path="/cpaas/data/jenkins" && password="Jenkins12345" && REGISTRY=$(docker info |grep 60080  |tr -d ' ') && ACP_NAMESPACE=cpaas-system && TOKEN=eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJjcGFhcy1zeXN0ZW0iLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlY3JldC5uYW1lIjoiZGV2b3BzLWFwaXNlcnZlci10b2tlbi16dng5ZCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJkZXZvcHMtYXBpc2VydmVyIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiNjAzNTdmYjAtNmU0YS0xMWVhLTg2ZDQtNTI1NDAwODZhMWVhIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmNwYWFzLXN5c3RlbTpkZXZvcHMtYXBpc2VydmVyIn0.AQgGCUnn9RdX6-I_Y72sQr5wdB4jJdo4hZNPMbr504-BPuJCwatp1E3lFIk_7uBOrHUVVWrhmom0R3ZUBi2ukKOQ3qQQe8w98LHSP4DJXc1gHc02gzSi0ODnSNGvT0rZp5NNBkqav9784UoT5IJ-dYb1_RdgGjEeeupOLwmQvLEumw-JCAnyh0Q0sLYVkKrSx_EDx3HjnAfiCb50syWdLUB7_IBRdRqYOvmvAkQ4jgVrIG4MFnJUIjoaRjtEuO4qEyrU__PKXwfOUXRjFjTXbOIz9uat5OyJs5MyDFZjPAWg6UpmhrQOBhqBX8KzN9J8OBL885oexvTK9K-0mE1Ghw
### 详细解释
NODE_NAME="192.168.0.120"  ##需要修改为集群中实际存放jenkins数据的某个节点的hostname
global_vip="192.168.0.7" ##需要修改为平台的访问地址，如果访问地址是域名，就必须配置成域名，因为 jenkins 需要访问 global 平台的 erebus，如果平台是域名访问的话，erebus 的 ingress 策略会配置成只能域名访问。
path="/cpaas/data/jenkins" ##默认数据目录为/root/alauda/jenkins，若有需要可更改。
password="Jenkins12345" ##默认密码为Jenkins12345，若有需要可更改
REGISTRY=$(docker info |grep 60080  |tr -d ' ')
TOKEN=[获取token]
ACP_NAMESPACE=cpaas-system ##改成部署时， --acp2-namespaces 参数指定的值，默认是cpaas-system

# 2
cat <<EOF > values.yaml
  
global:
  registry:
    address: ${REGISTRY}
Master:
  ServiceType: NodePort
  NodePort: 32001
  AdminPassword: "$password"
  gitlabConfigs:
    - name: gitlab
      manageHooks: true
      serverUrl: http://192.168.122.20:31101
      token: xxxx
  Location:
    url: http://192.168.122.20:32001
Persistence:
  Enabled: false
  Host:
    NodeName: ${NODE_NAME}
    Path: $path
AlaudaACP:
  Enabled: false
alaudapipelineplugin:
  consoleURL: ""
  apiEndpoint: ""
  apiToken: ""
  account: ""
  spaceName: ""
  clusterName: ""
  namespace: ""
AlaudaDevOpsCredentialsProvider:
  globalNamespaces: "${ACP_NAMESPACE}-global-credentials,${ACP_NAMESPACE},kube-system"
AlaudaDevOpsCluster:
  Cluster:
    masterUrl: "https://$global_vip:6443"
    token: ${TOKEN}
Erebus:
  Namespace: "${ACP_NAMESPACE}"
  URL: "https://$global_vip:443/kubernetes"
 
EOF

# 3
helm install stable/jenkins --name jenkins --namespace default -f values.yaml

# 清理操作
# helm delete --purge  jenkins 
# 清除本地数据

# 访问
http://129.204.236.25:32001
用户名：admin 密码：Jenkins12345。

# 配置
1.Alauda Jenkins Sync
2.Kubernetes Cluster Configuration
jenkins-token
3.Test Connection

# 集成
jenkins
http://192.168.0.120:32001

# 绑定项目
jenkins-demo
```

### 安装gitlab ⑥

```bash
# 1

# 快捷操作
REGISTRY=$(docker info |grep 60080  |tr -d ' ') && NODE_NAME=192.168.0.28 && NODE_IP="192.168.0.88" && potal_path="/cpaas/data/gitlab/portal" && database_path="/cpaas/data/gitlab/database" && redis_path="/cpaas/data/gitlab/redis"
# 详细解释
REGISTRY=$(docker info |grep 60080  |tr -d ' ')
NODE_NAME=192.168.0.28  ##需要修改为选择部署gialab的节点的hostname
NODE_IP="192.168.0.88" ##这个ip为gitlab的访问地址，需要修改为部署集群中任意master节点一个节点的实际ip
potal_path="/cpaas/data/gitlab/portal" ##potal的数据目录，一般不需要修改，若有规划，可修改为别的目录
database_path="/cpaas/data/gitlab/database" ##database的目录，一般不需要修改，若有规划，可修改为别的目录
redis_path="/cpaas/data/gitlab/redis" ##redis的目录，一般不需要修改，若有规划，可修改为别的目录


# 2
helm install stable/gitlab-ce --name gitlab-ce --namespace default \
    --set global.registry.address=${REGISTRY} \
    --set portal.debug=true \
    --set gitlabHost=${NODE_IP} \
    --set gitlabRootPassword=Gitlab12345 \
    --set service.type=NodePort \
    --set service.ports.http.nodePort=31101 \
    --set service.ports.ssh.nodePort=31102 \
    --set service.ports.https.nodePort=31103 \
    --set portal.persistence.enabled=false \
    --set portal.persistence.host.nodeName=${NODE_NAME} \
    --set portal.persistence.host.path="$potal_path" \
    --set portal.persistence.host.nodeName="${NODE_NAME}" \
    --set database.persistence.enabled=false \
    --set database.persistence.host.nodeName=${NODE_NAME} \
    --set database.persistence.host.path="$database_path" \
    --set database.persistence.host.nodeName="${NODE_NAME}" \
    --set redis.persistence.enabled=false \
    --set redis.persistence.host.nodeName=${NODE_NAME} \
    --set redis.persistence.host.path="$redis_path" \
    --set redis.persistence.host.nodeName="${NODE_NAME}"

# 清除操作
helm delete -purge gitlab-ce
# 清除本地数据

# 访问
Your gitlab URL is http://106.52.130.11:31101, login it with the account:

username: root
password: Gitlab12345

# 集成
http://192.168.0.88:31101

# 绑定项目
gitlab-demo
```

### 安装harbor ⑦

```bash
# 1

# 快捷操作
REGISTRY=$(docker info |grep 60080  |tr -d ' ') && NODE_IP="192.168.0.88" && NODE_NAME="192.168.0.28" &&HOST_PATH=/cpaas/data/harbor && harbor_password="Harbor12345" && db_password="Harbor4567"  && redis_password="Redis789"
# 详细解释
REGISTRY=$(docker info |grep 60080  |tr -d ' ')
NODE_IP="192.168.0.88"  ###此参数为部署时指定的访问地址，写当前集群中任意一个master节点的ip即可
NODE_NAME="192.168.0.28"  ###需要修改为选择部署harbor节点的hostname
HOST_PATH=/cpaas/data/harbor###这个目录为harbor的数据目录路径，一般不需要修改，若有别的规划，可修改。
harbor_password="Harbor12345" ####harbor的密码，默认不需要修改，若有规划，可改
db_password="Harbor4567"      ####harbor数据库的密码，默认不需要修改，若有规划，可改
redis_password="Redis789"     ###harbor的redis的密码，默认不需要修改，若有规划，可改

# 2
helm install --name harbor --namespace default stable/harbor \
    --set global.registry.address=${REGISTRY} \
    --set externalURL=http://${NODE_IP}:31104 \
    --set harborAdminPassword=$harbor_password \
    --set ingress.enabled=false \
    --set service.type=NodePort \
    --set service.ports.http.nodePort=31104 \
    --set service.ports.ssh.nodePort=31105 \
    --set service.ports.https.nodePort=31106 \
    --set database.password=$db_password \
    --set redis.usePassword=true \
    --set redis.password=$redis_password \
    --set database.persistence.enabled=false \
    --set database.persistence.host.nodeName=${NODE_NAME} \
    --set database.persistence.host.path=${HOST_PATH}/database \
    --set redis.persistence.enabled=false \
    --set redis.persistence.host.nodeName=${NODE_NAME} \
    --set redis.persistence.host.path=${HOST_PATH}/redis \
    --set chartmuseum.persistence.enabled=false \
    --set chartmuseum.persistence.host.nodeName=${NODE_NAME} \
    --set chartmuseum.persistence.host.path=${HOST_PATH}/chartmuseum \
    --set registry.persistence.enabled=false \
    --set registry.persistence.host.nodeName=${NODE_NAME} \
    --set registry.persistence.host.path=${HOST_PATH}/registry \
    --set jobservice.persistence.enabled=false \
    --set jobservice.persistence.host.nodeName=${NODE_NAME} \
    --set jobservice.persistence.host.path=${HOST_PATH}/jobservice \
    --set AlaudaACP.Enabled=false

#清除操作
#helm delete --purge harbor
#清除本地数据

# 访问
Then you should be able to visit the Harbor at http://106.52.130.11:31104. 

username: admin
password: Harbor12345

# 集成
http://192.168.0.88:31104

# 绑定项目
harbor-demo
```





## 全局检查

```bash
# 管理节点master
helm list --failed
kubectl get helmrequest --all-namespaces | awk '{if ($NF != "Synced")print}'
kubectl get rel --all-namespaces | awk '{if ($3 != "deployed")print}'
kubectl get pod --all-namespaces | awk '{if ($4 != "Running" && $4 != "Completed")print}' | awk -F'[/ ]+' '{if ($3 != $4)print}'

# 业务节点master
helm list --failed 
kubectl get helmrequest --all-namespaces | awk '{if ($NF != "Synced")print}'
kubectl get rel --all-namespaces | awk '{if ($3 != "deployed")print}'
kubectl get pod --all-namespaces | awk '{if ($4 != "Running" && $4 != "Completed")print}' | awk -F'[/ ]+' '{if ($3 != $4)print}'
```

## 访问平台

```bash
用户名：--root-username 参数指定的值，默认为 admin@cpaas.io。
密码：password
```







## 常见问题

### 集群管理页面404

#### 错误信息

```bash
tke stable/tke v2.6.9 cpaas-system 6h Failed
```

#### 修正操作

```bash
# 访问 `http://106.52.130.104/console-cluster` 404报错
1、kubectl get hr -n cpaas-system
2、`tke stable/tke v2.6.9 cpaas-system 6h Failed` #tke没成功
3、kubectl delete hr -n cpaas-system tke
4、cat /cpaas/install.log | grep stable/tke #在init节点 
5、kubectl captain create --version $(helm search | grep '^stable/tke ' | awk '{print $2}') --configmap=tke-config --namespace=cpaas-system tke --chart=stable/tke
```

### helm list报错

#### 错误信息

```bash
Error: configmaps is forbidden: User "system:serviceaccount:kube-system:default" cannot list resource "configmaps" in API group "" in the namespace "kube-system"
```

#### 修正操作

```bash
# 报以上错误请用以下命令加权限
1、kubectl create serviceaccount --namespace kube-system tiller
2、kubectl patch deploy --namespace kube-system tiller-deploy -p '{"spec":{"template":{"spec":{"serviceAccount":"tiller"}}}}'
3、kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
```



### K8S常见命令

```bash
# 获取所有命名空间
kubectl get ns 
#
kubectl get pods -n  kube-system　
#
kubectl get hr -n cpaas-system
```



































