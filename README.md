# 幻兽帕鲁服务器GUI面板控制器
一个实现远程控制服务端行为的项目  
该项目是基于rcon协议远程操控palworld游戏服务器的插件，服务端通过HTTP api接收客户端GUI面板发送的指令
从而完成重启服务器，查看服务器信息，查看服务器内存占用等功能...

# 快速部署
服务端：bulid代码，填写配置文件，在服务器任意路径打开bulid后的可执行程序  
客户端：bulid代码，填写配置文件，在任意终端打开bulid后的操控面板  
全部部署完毕即可实现远程操控服务器

# 服务端配置文件 rconControllerConfig.ini
```ini
[Sever Http Controller Config]
palSeverPath=
rconPort=
adminPassword=
severProcessName=
listenPort=
```
palSeverPath是游戏服务器的路径，就是你双击打开游戏服务器的那个程序的路径，用于插件寻找服务器程序自动化打开  
rconPort是游戏服务器Rcon协议的监听端口，需要手动配置  
adminPassword是游戏服务器的管理员密码  
severProcessName游戏服务器的进程名字 不出意外应该是 PalServer-Win64-Test-Cmd.exe 我怕官方后续更新会修改进程名字，就没写成hardcode  
listenPort是插件运行的端口号  

# 客户端配置文件 palSeverController.ini
```ini
[Sever Http Controller Config]
severIp=
```
severIp是服务器公网ip+插件运行端口号，比如你的服务器公网ip是11.4.5.14，服务端配的listenPort是1919，那么这里serverIp就配11.4.5.14:1919 （悲）
