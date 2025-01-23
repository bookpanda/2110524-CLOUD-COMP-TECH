# Instance Profile
```bash
aws iam create-instance-profile --instance-profile-name paas-autoscale

# role name from craeting beanstalk
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


# Policies in EB service role
- AWSElasticBeanstalkWebTier (for web tier permissions).
- AWSElasticBeanstalkWorkerTier (for worker tier permissions).
- AmazonS3FullAccess (for access to S3 buckets, very important for deployment).
- CloudWatchLogsFullAccess (for CloudWatch logs).
```bash
# ssh into EC2, not the Beanstalk
ssh -i "cloud-computing.pem" ec2-user@ec2-13-228-214-88.ap-southeast-1.compute.amazonaws.com

# check logs
sudo cat /var/log/eb-engine.log | less

# confirm symbolic link
ls -l /var/www/html

```
