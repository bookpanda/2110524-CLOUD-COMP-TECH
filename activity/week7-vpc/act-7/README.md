# VPC

EC2 in public subnet can access the internet
```bash
ssh -i "cloud-computing.pem" ec2-user@ec2-13-214-210-230.ap-southeast-1.compute.amazonaws.com

ping google.com

# cannot ping EC2 in private subnet
ping 10.0.21.125
```