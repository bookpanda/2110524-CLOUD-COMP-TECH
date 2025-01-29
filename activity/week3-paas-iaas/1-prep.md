# Commands
```bash
chmod 400 "cloud-computing.pem"
```

# Siege
- name: siege-web-client
- OS: Amazon Linux 2 AMI
- AZ: ap-southeast-1a
```bash
ssh -i "cloud-computing.pem" ec2-user@ec2-13-212-58-124.ap-southeast-1.compute.amazonaws.com

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

