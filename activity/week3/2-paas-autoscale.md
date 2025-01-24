# Commands
```bash
# clean IP from known_hosts in case EC2 IP changes
ssh-keygen -R ec2-13-213-231-32.ap-southeast-1.compute.amazonaws.com
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
- Service role: aws-elasticbeanstalk-service-role
- EC2 instance profile: aws-elasticbeanstalk-ec2-role
- tick "Public IP Address" + AZ subnets

## aws-elasticbeanstalk-service-role 
### Policies
- AWSElasticBeanstalkWebTier (for web tier permissions).
- AWSElasticBeanstalkWorkerTier (for worker tier permissions).

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
you can create this role to use instead of instance profile
### Policies
- AWSElasticBeanstalkWebTier (has access to S3, CloudWatch, etc.)

### Deployment not updating
- My EC2 instance did not contain the app in `/var/www/html`/`var/app/current`.
- That was because my EC2 did not have the correct instance profile/role.

## Debugging in EC2
```bash
# ssh into EC2, not the Beanstalk
ssh -i "cloud-computing.pem" ec2-user@ec2-13-213-231-32.ap-southeast-1.compute.amazonaws.com

# check logs
sudo cat /var/log/eb-engine.log | less

# confirm symbolic link
ls -l /var/www/html



/etc/nginx/nginx.conf
/etc/nginx/conf.d/elasticbeanstalk

sudo tail -f /var/log/nginx/error.log
```

## 504 timeout for index.php (/)
check if web is running, go to
> `http://act3-paas-autoscale-5-env.eba-4ifhnppy.ap-southeast-1.elasticbeanstalk.com/logo_aws_reduced.gif`

you should point health check to `/logo_aws_reduced.gif` as there's no matrix mul

### This does not work
- setting Max execution time: 300s in EB console
- set `$size` in `index.php` to smaller values e.g. 128 -> 32
- `$size` = 128 took 90s to load
- `$size` = 8 took 90s to load

> Note that Sol 1, 2 do not persist when uploading a new version of the app or when scaling
### Sol 1: use Nginx
```bash
sudo nano /etc/nginx/nginx.conf
# FastCGI timeouts
fastcgi_read_timeout 300;
fastcgi_send_timeout 300;
fastcgi_connect_timeout 300;

sudo systemctl restart nginx
sudo systemctl status nginx
```
### Sol 2: use Apache (httpd)
```bash
sudo nano /etc/httpd/conf/httpd.conf

Timeout 300
KeepAliveTimeout 300

sudo systemctl restart httpd
sudo systemctl status httpd
```

### REAL Solution
- Since `$size` 8, 128 took same time to load, it's not causing the PHP timeout.
- The real culprit is the MySql connection, which hadn't been set up yet.

## Deploying RDS
- do it in EB env console

You don't have to modify the `indedx.php` file for connection; set the environment variables in the EB console instead:
- RDS_HOSTNAME: your_rds_endpoint (look in RDS service in AWS console)
- RDS_USERNAME: your_rds_username
- RDS_PASSWORD: your_rds_password

it will match with
```php
$conn = new mysqli(
        $_SERVER['RDS_HOSTNAME'],
        $_SERVER['RDS_USERNAME'],
        $_SERVER['RDS_PASSWORD'],
        'ebdb'
    );
```
