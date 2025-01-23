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
```bash
# ssh into EC2, not the Beanstalk
ssh -i "cloud-computing.pem" ec2-user@ec2-13-228-32-11.ap-southeast-1.compute.amazonaws.com

```
