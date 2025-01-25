# Commands
```bash
# clean IP from known_hosts in case EC2 IP changes
ssh-keygen -R ec2-13-213-231-32.ap-southeast-1.compute.amazonaws.com
```

# Webserver
- name: webserver
- AMI: Amazon Linux 2 AMI
- AZ: ap-southeast-1a
- security group inbound: HTTP (80)
```bash
ssh -i "cloud-computing.pem" ec2-user@ec2-54-251-234-120.ap-southeast-1.compute.amazonaws.com

sudo yum install php-mysql php php-xml php-mcrypt php-mbstring php-cli mysql httpd tcpdump emacs

# give permission to ec2-user
sudo chown ec2-user:ec2-user /var/www/html

# transfer files
scp -i ./cloud-computing.pem -r ./webserver ec2-user@ec2-54-251-234-120.ap-southeast-1.compute.amazonaws.com:/var/www/html/

cd /var/www/html/webserver
mv * ..
cd ..
rm -r webserver

sudo systemctl enable httpd
sudo systemctl start httpd
# verify
sudo systemctl is-enabled httpd
sudo systemctl status httpd

# set $_SERVER envs
sudo nano /etc/httpd/conf/httpd.conf

SetEnv RDS_HOSTNAME "ec2-13-229-56-125.ap-southeast-1.compute.amazonaws.com"
SetEnv RDS_USERNAME "root"
SetEnv RDS_PASSWORD "new-password"

sudo systemctl restart httpd
```

# Database
- name: database
- AMI: Amazon Linux 2 AMI
- AZ: ap-southeast-1a
- security group inbound: MySQL/Aurora (3306)
```bash
ssh -i "cloud-computing.pem" ec2-user@ec2-13-229-56-125.ap-southeast-1.compute.amazonaws.com

sudo yum install mariadb-server
sudo systemctl enable mariadb
sudo systemctl start mariadb

# verify
sudo systemctl is-enabled mariadb
sudo systemctl status mariadb

mysqladmin -u root password 'new-password'
mysql -u root -p
```

```sql
-- in mariadb shell
CREATE DATABASE ebdb;
USE ebdb;

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(63) NOT NULL
);

-- check
DESCRIBE user;

-- Failed to connect to MySQL: Host 'ip-172-31-23-231.ap-southeast-7.compute.internal' is not allowed to connect to this MariaDB server
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'new-password' WITH GRANT OPTION;
FLUSH PRIVILEGES;
-- use root, new-password in app code
```

## Allow outside access to database
```bash
echo "[mysqld]" | sudo tee -a /etc/my.cnf
echo "bind-address = 0.0.0.0" | sudo tee -a /etc/my.cnf
sudo systemctl restart mariadb
```