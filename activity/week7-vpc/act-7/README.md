# VPC

## Security Group
default: allow all outbound traffic, deny all inbound traffic
- can be changed e.g. SG2 allows inbound from SG1 (you don't need to add SG1 inbound from SG2)
- instance level
- looks at all the rules at once (allow only)

## Network ACL
- looks at the rules in priority order top->bottom (allow and deny)
- subnet level
- leave some space between rule numbers for future rules e.g. 100, 200 in case you need to add a rule in between 100 and 200

EC2 in public subnet can access the internet
```bash
# this needs SG with SSH inbound rule (All traffic inbound rule is not enough)
ssh -i "cloud-computing.pem" ec2-user@ec2-13-214-210-230.ap-southeast-1.compute.amazonaws.com

ping google.com

# cannot ping EC2 in private subnet
# after adding inbound from SG1 (public ec2) to SG2 (private ec2), you can ping
ping 10.0.21.125
```

## VPC Peering
- connect 2 VPCs
- VPC1: 10.0.0.0/16
- VPC2: 10.1.0.0/16
```bash
# in public ec2 on VPC1, ping private IP of ec2 on VPC2, not working
# 1. create peering connection between VPC1 and VPC2
# 2. accept the peering connection on VPC2
# 3. add to route table on VPC1: 10.1.0.0/16 -> peering connection
# 4. add to route table on VPC2: 10.0.0.0/16 -> peering connection
# 5. for ec2 in VPC2, add inbound rule from private IP of ec2 in VPC1 (10.0.1.103/32)
# now ec2 in VPC1 can ping ec2 in VPC2
ping 10.1.1.75
```

# Setup
## VPC
- name: wordpress
- IPv4 CIDR block: 10.0.0.0/16

## Internet Gateway
- name: wordpress-igw
- attach to wordpress VPC

## Public Subnet
- name: wordpress-public
- AZ: ap-southeast-1a
- IPv4 CIDR block: 10.0.1.0/24

### Public Route Table
- name: wordpress-public-rt
- 10.0.0.0/16 -> local
- 0.0.0.0/0 -> wordpress-igw
- don't forget to associate with wordpress-public subnet

## Private Subnet
- name: wordpress-private
- AZ: ap-southeast-1a
- IPv4 CIDR block: 10.0.2.0/24
- don't forget to associate with wordpress-private subnet

### NAT Gateway
- name: wordpress-ngw
- public, allocate EIP
- attach to wordpress-private subnet

### Private Route Table
- name: wordpress-private-rt
- 10.0.0.0/16 -> local
- 0.0.0.0/0 -> wordpress-ngw