# Week 5: S3
## How do we set this up?
- Create a S3 bucket
- Create a custom IAM policy for THAT bucket
- Create IAM role with THAT policy
- Create Lambda Function with THAT role

## Upload a file to S3
- get a presigned upload url from the lambda function
- upload the file as BINARY to the url
- make sure that the presigned url and the uploaded file have the same `Content-Type`

# Week 6: DynamoDB

## Table 1: `myDropboxUsers`
- `username` (Primary Key)
- `password`

## Table 2: `myDropboxShares`
- `username` (Primary Key)
- `objectKey` (Sort Key)