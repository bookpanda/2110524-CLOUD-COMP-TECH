# Commands
```bash
# clean IP from known_hosts in case EC2 IP changes
ssh-keygen -R ec2-13-228-214-88.ap-southeast-1.compute.amazonaws.com  
```

# Instance Profile (you can use EC2 instance role instead)
```bash
aws iam create-instance-profile --instance-profile-name paas-autoscale

# role name from creating beanstalk
aws iam add-role-to-instance-profile --instance-profile-name paas-autoscale --role-name aws-elasticbeanstalk-service-role

aws iam list-instance-profiles
```

# Beanstalk
- name: act3-paas-autoscale
- Platform: PHP 8.3
- EC2 instance profile: paas-autoscale
- Root volume type: gp3 (General Purpose 3 SSD)
- No need to tick "Public IP Address", that's for public EC2 (we are using Beanstalk's load balancer dns)

### Deployment not updating
My EC2 instance did not contain the app in `/var/www/html`/`var/app/current`, so I had to redeploy
- try changing Deployment policy to `Immutable`, then deploy again


## aws-elasticbeanstalk-service-role 
### Policies
- AWSElasticBeanstalkWebTier (for web tier permissions).
- AWSElasticBeanstalkWorkerTier (for worker tier permissions).
- CloudWatchLogsFullAccess (for CloudWatch logs).

### Trust policy
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "elasticbeanstalk.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

## aws-elasticbeanstalk-ec2-role (EC2 instance role)
you create this role to use instead of instance profile
### Policies
- AmazonEC2ReadOnlyAccess
- AmazonS3ReadOnlyAccess
- CloudWatchLogsFullAccess

```bash
# ssh into EC2, not the Beanstalk
ssh -i "cloud-computing.pem" ec2-user@ec2-13-228-214-88.ap-southeast-1.compute.amazonaws.com

# check logs
sudo cat /var/log/eb-engine.log | less

# confirm symbolic link
ls -l /var/www/html

sudo systemctl status nginx
sudo systemctl restart nginx

/etc/nginx/nginx.conf
/etc/nginx/conf.d/elasticbeanstalk

sudo tail -f /var/log/nginx/error.log
```

## 504 timeout
### Sol 1
```bash
sudo nano /etc/nginx/nginx.conf
# FastCGI timeouts
fastcgi_read_timeout 300;
fastcgi_send_timeout 300;
fastcgi_connect_timeout 300;
```
### Sol 2
Max execution time: 300s
