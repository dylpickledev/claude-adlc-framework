#!/bin/bash

# Create S3 bucket for ALB logs
BUCKET_NAME="graniterock-alb-logs-$(date +%s)"
aws s3api create-bucket \
  --bucket $BUCKET_NAME \
  --region us-west-2 \
  --create-bucket-configuration LocationConstraint=us-west-2

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket $BUCKET_NAME \
  --versioning-configuration Status=Enabled

# Add bucket policy for ALB logs
aws s3api put-bucket-policy \
  --bucket $BUCKET_NAME \
  --policy "{
    \"Version\": \"2012-10-17\",
    \"Statement\": [
      {
        \"Effect\": \"Allow\",
        \"Principal\": {
          \"AWS\": \"arn:aws:iam::797873946194:root\"
        },
        \"Action\": \"s3:PutObject\",
        \"Resource\": \"arn:aws:s3:::$BUCKET_NAME/*\"
      }
    ]
  }"

# Get ALB ARN
ALB_ARN=$(aws elbv2 describe-load-balancers \
  --names Skynet-ELB \
  --region us-west-2 \
  --query 'LoadBalancers[0].LoadBalancerArn' \
  --output text)

# Enable access logs
aws elbv2 modify-load-balancer-attributes \
  --load-balancer-arn $ALB_ARN \
  --attributes \
    Key=access_logs.s3.enabled,Value=true \
    Key=access_logs.s3.bucket,Value=$BUCKET_NAME \
  --region us-west-2

echo "ALB access logs enabled. Bucket: $BUCKET_NAME"
echo "Try authentication again, then check: aws s3 ls s3://$BUCKET_NAME/"
