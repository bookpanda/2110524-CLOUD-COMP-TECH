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

# A. Assess your application's baseline IaaS performance
In siege-web-client EC2
```bash
ssh -i "cloud-computing.pem" ec2-user@ec2-52-77-227-237.ap-southeast-1.compute.amazonaws.com

# See permissions
ls -l siege.log 

chmod 777 siege.log
cat /usr/local/var/log/siege.log

# clear log (BE CAREFUL)
truncate -s 0 siege.log

# custom script
sudo nano siege_runner.sh
chmod +x siege_runner.sh
./siege_runner.sh

# download log
scp -i ./cloud-computing.pem -r ec2-user@ec2-52-77-227-237.ap-southeast-1.compute.amazonaws.com:/usr/local/var/log/siege.log ./siege.log
```

# B. Set up your IaaS auto-scaling environment
- create an AMI from the webserver instance: "phpiaasapp"
- try creating EC2 from that AMI to see if it works

> ASG uses launch template + ELB (aka target group), launch template uses AMI

## Launch Template
- name: phpiaasapplaunch
- AMI: phpiaasapp
- instance type: t2.micro
- subnet: ap-southeast-1a
- security group inbound: 22, 80
- security group outbound: all

## Auto Scaling Group
- name: phpiaasgroup
- launch template: phpiaasapplaunch
- subnets: ap-southeast-1a, ap-southeast-1b
- load balancing: attach to a new load balancer, ALB, internet-facing
- min: 1, max: 4
- metric: Average CPU Utilization, target value 60, warmup 60s
- Enable group metrics collection within CloudWatch

### Add security groups to ELB
- 80, 22

### ELB health check
- target group -> health check -> /logo_aws_reduced.gif

# C. Experiment with siege to trigger events to add instances and remove instances
- use ELB DNS, not EC2's

# D. Experiment with fault tolerance
- change min instances to 2 in ASG