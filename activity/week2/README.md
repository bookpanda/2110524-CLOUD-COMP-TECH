# Commands
```bash
chmod 400 "act2-cloud.pem"
ssh -i "act2-cloud.pem" ec2-user@ec2-43-208-26-158.ap-southeast-7.compute.amazonaws.com
```

# Siege
- name: siege-web-client
- AZ: ap-southeast-1a
```bash
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
- AZ: ap-southeast-1a

# Database
- name: database
- AZ: ap-southeast-1a