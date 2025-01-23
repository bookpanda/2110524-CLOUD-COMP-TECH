# Commands
```bash
chmod 400 "cloud-computing.pem"
```

# Siege
- name: siege-web-client
- OS: Amazon Linux 2 AMI
- AZ: ap-southeast-1a
```bash
ssh -i "cloud-computing.pem" ec2-user@ec2-43-208-115-26.ap-southeast-7.compute.amazonaws.com

sudo yum install gcc aclocal autoheader automake libtool
wget https://github.com/JoeDog/siege/archive/refs/heads/master.zip
unzip master.zip

# in siege-master
utils/bootstrap
./configure
make
sudo make install
siege -c5 -d1 -r1 http://www.google.com

# after app is deployed & connected to db
# c = concurrent users, d = delay between requests (s), r = repetitions/user

# everything fine
siege -c10 -d1 -r1 http://ec2-43-208-115-242.ap-southeast-7.compute.amazonaws.com/index.php

# Transactions:                  78    hits
# Availability:                  51.32 %
# Elapsed time:                 231.24 secs
# Data transferred:               0.17 MB
# Response time:              76611.29 ms
# Transaction rate:               0.34 trans/sec
# Throughput:                     0.00 MB/sec
# Concurrency:                   25.84
# Succ
```

