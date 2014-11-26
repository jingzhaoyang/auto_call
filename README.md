### 安装所需库
ubuntu环境

```
wget http://download.ag-projects.com/agp-debian-gpg.key
sudo apt-key add agp-debian-gpg.key
#Add the repository to /etc/apt/sources.list (run commands as root):
echo "deb       http://ag-projects.com/ubuntu `lsb_release -c -s` main" >> /etc/apt/sources.list
echo "deb-src   http://ag-projects.com/ubuntu `lsb_release -c -s` main" >> /etc/apt/sources.list
#Update the list of available packages:
sudo apt-get update
#Install SIP SIMPLE client SDK:
sudo apt-get install python-sipsimple
#Install the Command Line Clients:
sudo apt-get install sipclients
```

### 代码说明
代码是从官方sipsimple的例子改的，时间仓促，没有详细看官方手册。例如自动挂断，呼叫超时后自动重呼叫这些都没有实现。只是简单的注册，呼叫，播放wav文件。
其中config文件树如下：
```
/auto_call/config
└── config
```
config配置里面都是用户和注册的一些设置信息。可以用`sip-settings`工具生成：
```
sip-settings --account add 1001@127.0.0.1 1234   #1001是用户，1234是密码，127.0.0.1是sip服务器地址
```
这样配置完成后，可以用`sip-register`命令来测试是否能注册成功。若成功，就可以将`~/.sipclient/config` 文件复制到脚本目录。
