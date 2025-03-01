## Wordpress EC2
- AMI: Amazon Linux 2
- auto-assign public IP
- wordpress-public subnet
- wordpress SG
### Wordpress SG
- inbound: 22, 80
```bash
ssh -i "cloud-computing.pem" ec2-user@52.221.210.159

sudo yum update -y
sudo amazon-linux-extras enable php8.0
sudo yum install -y httpd php php-mysqlnd php-fpm php-json php-mbstring php-xml unzip
sudo yum install -y mariadb

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

# after creating database in mariadb (below)
# test connection
mysql -h 10.0.2.193 -u wpuser -p
```
- visit `http://52.221.210.159/wp-admin/setup-config.php` (public IP of wordpress ec2)
- DB_NAME: wordpress 
- DB_USER: wpuser
- DB_PASSWORD: notv3rysecurepassword
- DB_HOST: 10.0.2.193
- user: root
- password: ^0K%h4ENiqb#4^Svo9

## MariaDB EC2
- AMI: Amazon Linux 2
- wordpress-private subnet
- mariadb SG
### MariaDB SG
- inbound from wordpress SG: 22, 3306
```bash
# ssh from wordpress ec2
ssh -i "cloud-computing.pem" ec2-user@10.0.2.193

sudo yum update -y
sudo yum install -y mariadb-server
sudo systemctl enable --now mariadb

sudo nano /etc/my.cnf
sudo mysql -u root -p
```
```sql
CREATE DATABASE wordpress;
CREATE USER 'wpuser'@'%' IDENTIFIED BY 'notv3rysecurepassword';
GRANT ALL PRIVILEGES ON wordpress.* TO 'wpuser'@'%';
FLUSH PRIVILEGES;
EXIT;
```