# Commands
```bash
chmod 400 "act2-cloud.pem"
```

# Siege
- name: siege-web-client
- AZ: ap-southeast-7a
```bash
ssh -i "act2-cloud.pem" ec2-user@ec2-43-208-26-158.ap-southeast-7.compute.amazonaws.com

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

# Webserver
- name: webserver
- AZ: ap-southeast-7a
```bash
ssh -i "act2-cloud.pem" ec2-user@ec2-43-208-24-57.ap-southeast-7.compute.amazonaws.com

sudo yum install mariadb-server
sudo systemctl enable mariadb
sudo systemctl start mariadb

# verify
sudo systemctl is-enabled mariadb

mysqladmin -u root password 'new-password'
mysql -uroot -p

```

# Database
- name: database
- AZ: ap-southeast-7a