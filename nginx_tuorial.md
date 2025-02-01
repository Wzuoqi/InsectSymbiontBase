以下是使用`gunicorn`部署Django项目的详细流程，包括从环境准备到Nginx配置的所有步骤。

# **1. 环境准备**

安装必要的软件

确保您已经安装了以下软件（**一般在虚拟环境中**）：

- Python 3.x
- pip
- virtualenv
- Nginx
- Gunicorn

# **2. 创建并配置虚拟环境**

在您的项目目录中创建一个虚拟环境（**往往与Django环境一起**）并激活配置它：

```bash
cd ~/lab_web/lab_platform  # 替换为您的项目路径
python3 -m venv labplat_env
source labplat_env/bin/activate

pip install gunicorn
```

确保您的Django项目的`settings.py`文件中配置了`ALLOWED_HOSTS`，包括您的服务器IP地址或域名：

```python
ALLOWED_HOSTS = ['192.168.1.12','*']  # 替换为您的IP地址或域名
```

使用以下命令收集静态文件：

```python
python manage.py collectstatic
```

# 3.创建gunicorn systemd服务

为了让Gunicorn在后台运行并在系统重启时自动启动，您可以创建一个`systemd`服务文件。

```bash
sudo vim /etc/systemd/system/gunicorn.service
```

service服务文件如下：

```bash
[sudo] password for zju:
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=zju
Group=www-data # 注意用户组问题
WorkingDirectory=/home/zju/lab_web/lab_platform/labplatform
Environment="PATH=/home/zju/lab_web/lab_platform/labplat_env/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
# 如果不在这里添加gunicorn所在的环境变量，可能会报错
ExecStart=/home/zju/lab_web/lab_platform/labplat_env/bin/gunicorn --access-logfile - --workers 3 --bind 127.0.0.1:8030 labplatform.wsgi:application

[Install]
WantedBy=multi-user.target
```

启用并启动gunicorn服务：

```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn # 查看状态
```

# 4.创建并配置nginx服务

```bash
sudo vim /etc/nginx/sites-available/labplatform
```

在文件中添加以下内容：

```bash
server {
    listen 8023;
    server_name 192.168.1.12;  # 替换为您的IP地址

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /home/zju/lab_web/lab_platform/staticfiles;  # 确保此路径正确
        expires 1d;
        add_header Cache-Control "public";
    }

    location / {
        proxy_pass http://127.0.0.1:8030;  # 将请求转发到Gunicorn
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 端口映射过程

gunicorn 8030端口——nginx Django 8023端口——提供前端API

启用Nginx配置：

```bash
sudo ln -s /etc/nginx/sites-available/labplatform /etc/nginx/sites-enabled
```

测试Nginx配置

```bash
sudo nginx -t
```

重启Nginx, 如果测试通过，则重启Nginx以应用更改：

```bash
sudo systemctl restart nginx
```

检查防火墙设置

```bash
sudo ufw allow 'Nginx Full'
```

# 5.重启服务器后的重启服务命令

- 使用`sudo systemctl restart gunicorn`和`sudo systemctl restart nginx`来重启服务。
- 使用`sudo systemctl status gunicorn`和`sudo systemctl status nginx`来检查服务状态。
- 使用`sudo systemctl enable gunicorn`和`sudo systemctl enable nginx`来确保服务在系统启动时自动启动。

# 在生产服务器上部署Django项目（阿里云）

因为生产阿里云服务器上有所区别需要注意一下额外的区别

比如nginx的位置为

**/usr/local/nginx/conf**

```bash
sudo vim /etc/systemd/system/gunicorn.service
```

# 配置 Gunicorn

为 Gunicorn 创建一个 Systemd 服务文件：

```bash
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=zju
Group=zju
WorkingDirectory=/home/zju/lab_website_1
Environment="PATH=/home/zju/lab_website_1/labwebsite_venv/bin"
ExecStart=/home/zju/lab_website_1/labwebsite_venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8012 lab_website_1.wsgi:application

[Install]
WantedBy=multi-user.target
```

# nginx配置方案

```bash
sudo vim /usr/local/nginx/conf/conf.d/labwebsite.conf
```

```bash
server {
    listen 80;
    server_name lab.insect-genome.com;

    # 静态文件配置
    location /static/ {
        alias /home/zju/lab_website_1/staticfiles/;
        expires 1d;
        add_header Cache-Control "public";
    }

    location /media/ {
        alias /home/zju/lab_website_1/media;
    }

    # 反向代理到 Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8012;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
}
```

保存并重新加载nginx

```bash
sudo /usr/local/nginx/sbin/nginx -t
sudo /usr/local/nginx/sbin/nginx -s reload
```

### **4. 检查文件权限**

确保 Nginx 对静态文件目录有读取权限：

```bash
sudo chown -R nginx:nginx /home/zju/lab_website_1/staticfiles
sudo chown -R nginx:nginx /home/zju/lab_website_1/media
sudo chmod -R 755 /home/zju/lab_website_1/staticfiles
sudo chmod -R 755 /home/zju/lab_website_1/media
```