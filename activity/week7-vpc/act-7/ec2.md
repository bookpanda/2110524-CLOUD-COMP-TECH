## Wordpress EC2
- auto-assign public IP
- wordpress-public subnet
- wordpress SG
### Wordpress SG
- inbound: 22, 80
```bash
sudo yum update -y
sudo amazon-linux-extras enable php8.0
sudo yum install -y httpd php php-mysqlnd php-fpm php-json php-mbstring php-xml unzip

sudo systemctl enable --now httpd

# download and setup wordpress
cd /var/www/html
sudo rm -rf *
sudo wget https://wordpress.org/latest.zip
sudo unzip latest.zip
sudo mv wordpress/* .
sudo rm -rf wordpress latest.zip

sudo chown -R apache:apache /var/www/html
sudo nano /etc/httpd/conf/httpd.conf
# <Directory "/var/www/html">
#     AllowOverride All <- change None to All
# </Directory>

sudo systemctl restart httpd

sudo nano /var/www/html/wp-config.php

```