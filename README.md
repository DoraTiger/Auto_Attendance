# 声明

本项目仅仅作为学习交流用途使用。

打卡任务部分，参考开源项目 [NEU_health_daka](https://github.com/Bmaili/NEU_health_daka)，可以自行设计任何定时任务。

# 部署

## 配置文件

将`config_default.yaml`复制为`config.yaml`。

### 配置账号信息

1. 在student中添加学号、密码，多个账户用 `-` 隔开，如有报错，yaml语法请参考官方文档。

### 配置定时任务

1. 将 `config:trigger:enable:` 设置为 `True` 则开启定时任务，反之任务只执行一次。
   
2. 在 `config:trigger:cron:` 中配置任务定时计划，语法请参考cron相关文档。

### 配置日志

1. 在 `config:log:level:` 中配置日志级别。

2. 在 `config:log:file:` 中配置日志保存路径，默认路径 `logs/error.log` 是为了适配宝塔面板的python项目管理器。

### 配置推送

1. 在 `config:push:global:` 中配置推送需求，默认只在任务执行失败后推送。

2. 在 `config:push:channel:` 中配置推送渠道，设置 `enable` 为 `True` 后开启相关推送通道。

    2.1. 邮件推送

    自行配置SMTP服务器，不推荐使用免费的**阿里云邮箱**，经测试会被当做垃圾邮件拒收。

    2.2. ServerChan推送

    自行在 [ServerChan官网](https://sct.ftqq.com/) 注册并获取sckey。

    2.3 其他推送

    TODO：待研究 `Telegram BOT` , `Discord BOT` , `feishu WebHooks`，…… 。

3. 在 `student` 中可为每个账户单独配置推送通道，自动覆盖对应通道的全局设置。***需要完整配置，只配置部分文件会报错***

## 执行

### 配置环境
项目基于 `python 3.8.5` 开发，相关依赖已经保存在 `requirements.txt` 文件中，可以通过下列命令进行安装。***建议使用conda虚拟环境进行环境隔离。***
```python
pip install -r requirements.txt
```

#### 命令行启动

直接在命令行启动
```python
python ./main.py
```

### 通过宝塔面板启动

参考个人博客（未发布）。

### 通过github action启动

TODO：待开发。

### 通过腾讯云函数自动部署启动

TODO：待开发，目前可参考 [NEU_health_daka](https://github.com/Bmaili/NEU_health_daka)手动部署。

# 其他

* 本项目通过MIT协议开源

