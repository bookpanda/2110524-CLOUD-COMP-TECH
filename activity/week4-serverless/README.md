# Commands
```bash
chmod 400 "cloud-computing.pem"
```

# Siege
- name: siege-web-client
- OS: Amazon Linux 2 AMI
- AZ: ap-southeast-1a
```bash
ssh -i "cloud-computing.pem" ec2-user@ec2-52-221-248-144.ap-southeast-1.compute.amazonaws.com

sudo yum install gcc aclocal autoheader automake libtool
sudo yum install gcc openssl openssl-devel
wget https://github.com/JoeDog/siege/archive/refs/heads/master.zip
unzip master.zip

# in siege-master
utils/bootstrap
./configure --with-ssl=/usr/lib64
make
sudo make install

sudo make uninstall

siege -c5 -d1 -r1 --content-type "application/json" 'https://szzhh8og17.execute-api.ap-southeast-1.amazonaws.com/default/act4 POST {"a": "1", "b": 1, "op": "+"}' -l


sudo chmod 777 siege.log
cat /usr/local/var/log/siege.log

# clear log (BE CAREFUL)
truncate -s 0 siege.log

# custom script
sudo nano siege_runner.sh
sudo chmod +x siege_runner.sh
./siege_runner.sh

# download log
scp -i ./cloud-computing.pem -r ec2-user@ec2-52-221-248-144.ap-southeast-1.compute.amazonaws.com:/usr/local/var/log/siege.log ./siege.log
```

# Lambda
- name: act4
- Trigger: API Gateway
- Region: ap-southeast-1 (Lambda is a region-level service)

