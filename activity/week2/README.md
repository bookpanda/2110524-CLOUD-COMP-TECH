# Commands
```bash
chmod 400 "act2-cloud.pem"
```

# Siege
- name: siege-web-client
- AZ: ap-southeast-7a
```bash
ssh -i "act2-cloud.pem" ec2-user@ec2-43-208-115-26.ap-southeast-7.compute.amazonaws.com

sudo yum install gcc aclocal autoheader automake libtool
wget https://github.com/JoeDog/siege/archive/refs/heads/master.zip
unzip master.zip

# in siege-master
utils/bootstrap
./configure
make
sudo make install
siege -c5 -d1 -r1 http://www.google.com
```

# Database
- name: database
- AZ: ap-southeast-7a
- security group inbound: MySQL/Aurora (3306)
```bash
ssh -i "act2-cloud.pem" ec2-user@ec2-43-208-204-45.ap-southeast-7.compute.amazonaws.com

sudo yum install mariadb-server
sudo systemctl enable mariadb
sudo systemctl start mariadb

# verify
sudo systemctl is-enabled mariadb

mysqladmin -u root password 'new-password'
mysql -uroot -p
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

-- Failed to connect to MySQL: Access denied for user 'root'@'ip-172-31-23-231.ap-southeast-7.compute.internal' (using password: YES)

```

# Allow outside access to database
```bash
echo "[mysqld]" | sudo tee -a /etc/my.cnf
echo "bind-address = 0.0.0.0" | sudo tee -a /etc/my.cnf
sudo systemctl restart mariadb
```

# Webserver
- name: webserver
- AZ: ap-southeast-7a
- security group inbound: HTTP (80)
```bash
sudo yum install php-mysql php php-xml php-mcrypt php-mbstring php-cli mysql httpd tcpdump emacs

# give permission to ec2-user
sudo chown ec2-user:ec2-user /var/www/html

# transfer files
scp -i ./act2-cloud.pem -r ./webserver ec2-user@ec2-43-208-115-242.ap-southeast-7.compute.amazonaws.com:/var/www/html/

cd /var/www/html/webserver
mv * ..
rm -r webserver

sudo systemctl start httpd
sudo systemctl enable httpd
# verify
sudo systemctl is-enabled httpd
sudo systemctl status httpd
```