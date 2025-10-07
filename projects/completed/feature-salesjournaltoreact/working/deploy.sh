#!/bin/bash

# App Launcher Portal - Complete Deployment Script
# This script builds Docker images, pushes to ECR, and deploys to ECS

set -e  # Exit on any error

# Docker path (Docker Desktop)
DOCKER="/Applications/Docker.app/Contents/Resources/bin/docker"
export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}App Launcher Portal Deployment${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""

# Configuration
AWS_REGION="us-west-2"
AWS_ACCOUNT_ID="129515616776"
ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
CLUSTER_NAME="skynet-apps-cluster"
VPC_ID="vpc-1900307e"

# Paths
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DA_AGENT_HUB_ROOT="/Users/TehFiestyGoat/da-agent-hub"
APP_LAUNCHER_DIR="${SCRIPT_DIR}/app-launcher"
SALES_JOURNAL_DIR="${DA_AGENT_HUB_ROOT}/react-sales-journal"

echo -e "${YELLOW}Configuration:${NC}"
echo "  AWS Region: ${AWS_REGION}"
echo "  AWS Account: ${AWS_ACCOUNT_ID}"
echo "  ECS Cluster: ${CLUSTER_NAME}"
echo "  VPC: ${VPC_ID}"
echo ""

# Step 1: Authenticate with ECR
echo -e "${YELLOW}Step 1: Authenticating with ECR...${NC}"
aws ecr get-login-password --region ${AWS_REGION} | $DOCKER login --username AWS --password-stdin ${ECR_REGISTRY}
echo -e "${GREEN}✅ ECR authentication successful${NC}"
echo ""

# Step 2: Build and push App Launcher
echo -e "${YELLOW}Step 2: Building App Launcher Docker image...${NC}"
cd "${APP_LAUNCHER_DIR}"
$DOCKER build -t app-launcher:latest .
echo -e "${GREEN}✅ App Launcher image built${NC}"

echo -e "${YELLOW}Tagging App Launcher image...${NC}"
$DOCKER tag app-launcher:latest ${ECR_REGISTRY}/app-launcher:latest
echo -e "${GREEN}✅ App Launcher image tagged${NC}"

echo -e "${YELLOW}Pushing App Launcher to ECR...${NC}"
$DOCKER push ${ECR_REGISTRY}/app-launcher:latest
echo -e "${GREEN}✅ App Launcher pushed to ECR${NC}"
echo ""

# Step 3: Build and push Sales Journal
echo -e "${YELLOW}Step 3: Building Sales Journal Docker image...${NC}"
cd "${SALES_JOURNAL_DIR}"

echo -e "${YELLOW}Building Sales Journal Docker image (includes React build)...${NC}"
$DOCKER build -t sales-journal:latest .
echo -e "${GREEN}✅ Sales Journal image built${NC}"

echo -e "${YELLOW}Tagging Sales Journal image...${NC}"
$DOCKER tag sales-journal:latest ${ECR_REGISTRY}/sales-journal:latest
echo -e "${GREEN}✅ Sales Journal image tagged${NC}"

echo -e "${YELLOW}Pushing Sales Journal to ECR...${NC}"
$DOCKER push ${ECR_REGISTRY}/sales-journal:latest
echo -e "${GREEN}✅ Sales Journal pushed to ECR${NC}"
echo ""

# Step 4: Create security group for ECS tasks (if not exists)
echo -e "${YELLOW}Step 4: Creating ECS task security group...${NC}"

# Check if security group already exists
SG_ID=$(aws ec2 describe-security-groups \
  --filters "Name=group-name,Values=ecs-apps-sg" "Name=vpc-id,Values=${VPC_ID}" \
  --query 'SecurityGroups[0].GroupId' \
  --output text \
  --region ${AWS_REGION} 2>/dev/null || echo "None")

if [ "$SG_ID" == "None" ]; then
  echo -e "${YELLOW}Creating new security group...${NC}"
  SG_ID=$(aws ec2 create-security-group \
    --group-name ecs-apps-sg \
    --description "Security group for ECS Fargate tasks (app-launcher and sales-journal)" \
    --vpc-id ${VPC_ID} \
    --region ${AWS_REGION} \
    --query 'GroupId' \
    --output text)

  echo -e "${GREEN}✅ Security group created: ${SG_ID}${NC}"

  # Get ALB security group
  ALB_SG=$(aws elbv2 describe-load-balancers \
    --names Skynet-ELB \
    --region ${AWS_REGION} \
    --query 'LoadBalancers[0].SecurityGroups[0]' \
    --output text)

  echo -e "${YELLOW}Allowing HTTP traffic from ALB security group: ${ALB_SG}${NC}"
  aws ec2 authorize-security-group-ingress \
    --group-id ${SG_ID} \
    --protocol tcp \
    --port 80 \
    --source-group ${ALB_SG} \
    --region ${AWS_REGION}

  echo -e "${GREEN}✅ Security group rule added${NC}"
else
  echo -e "${GREEN}✅ Security group already exists: ${SG_ID}${NC}"
fi
echo ""

# Step 5: Create ECS services
echo -e "${YELLOW}Step 5: Creating ECS services...${NC}"

# Get private subnet IDs
SUBNETS=$(aws ec2 describe-subnets \
  --filters "Name=vpc-id,Values=${VPC_ID}" "Name=tag:Name,Values=Skynet-Private-Subnet*" \
  --query 'Subnets[0:2].SubnetId' \
  --output text \
  --region ${AWS_REGION} | tr '\t' ',')

echo "  Private subnets: ${SUBNETS}"
echo ""

# Create App Launcher service
echo -e "${YELLOW}Creating App Launcher ECS service...${NC}"
aws ecs create-service \
  --cluster ${CLUSTER_NAME} \
  --service-name app-launcher \
  --task-definition app-launcher:1 \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[${SUBNETS}],securityGroups=[${SG_ID}],assignPublicIp=DISABLED}" \
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:${AWS_REGION}:${AWS_ACCOUNT_ID}:targetgroup/app-launcher-tg/b6ce8e538c04aefb,containerName=app-launcher,containerPort=80" \
  --health-check-grace-period-seconds 60 \
  --region ${AWS_REGION} \
  --no-cli-pager > /dev/null

echo -e "${GREEN}✅ App Launcher service created${NC}"

# Create Sales Journal service
echo -e "${YELLOW}Creating Sales Journal ECS service...${NC}"
aws ecs create-service \
  --cluster ${CLUSTER_NAME} \
  --service-name sales-journal \
  --task-definition sales-journal:1 \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[${SUBNETS}],securityGroups=[${SG_ID}],assignPublicIp=DISABLED}" \
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:${AWS_REGION}:${AWS_ACCOUNT_ID}:targetgroup/sales-journal-tg/fe4f6879199e4000,containerName=sales-journal,containerPort=80" \
  --health-check-grace-period-seconds 60 \
  --region ${AWS_REGION} \
  --no-cli-pager > /dev/null

echo -e "${GREEN}✅ Sales Journal service created${NC}"
echo ""

# Step 6: Monitor deployment
echo -e "${YELLOW}Step 6: Monitoring deployment status...${NC}"
echo ""
echo -e "${YELLOW}Waiting for services to stabilize (this may take 2-3 minutes)...${NC}"

# Wait for app-launcher service
aws ecs wait services-stable \
  --cluster ${CLUSTER_NAME} \
  --services app-launcher \
  --region ${AWS_REGION}
echo -e "${GREEN}✅ App Launcher service is stable${NC}"

# Wait for sales-journal service
aws ecs wait services-stable \
  --cluster ${CLUSTER_NAME} \
  --services sales-journal \
  --region ${AWS_REGION}
echo -e "${GREEN}✅ Sales Journal service is stable${NC}"
echo ""

# Step 7: Verify target health
echo -e "${YELLOW}Step 7: Checking target group health...${NC}"

APP_LAUNCHER_HEALTH=$(aws elbv2 describe-target-health \
  --target-group-arn arn:aws:elasticloadbalancing:${AWS_REGION}:${AWS_ACCOUNT_ID}:targetgroup/app-launcher-tg/b6ce8e538c04aefb \
  --region ${AWS_REGION} \
  --query 'TargetHealthDescriptions[0].TargetHealth.State' \
  --output text)

SALES_JOURNAL_HEALTH=$(aws elbv2 describe-target-health \
  --target-group-arn arn:aws:elasticloadbalancing:${AWS_REGION}:${AWS_ACCOUNT_ID}:targetgroup/sales-journal-tg/fe4f6879199e4000 \
  --region ${AWS_REGION} \
  --query 'TargetHealthDescriptions[0].TargetHealth.State' \
  --output text)

echo "  App Launcher target health: ${APP_LAUNCHER_HEALTH}"
echo "  Sales Journal target health: ${SALES_JOURNAL_HEALTH}"
echo ""

# Final summary
echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""
echo -e "${YELLOW}Access your application:${NC}"
echo "  🌐 App Launcher: https://apps.grc-ops.com"
echo "  📊 Sales Journal: https://apps.grc-ops.com/sales-journal"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Test authentication flow via Azure AD"
echo "  2. Verify all Sales Journal routes work"
echo "  3. Check CloudWatch logs for any errors:"
echo "     - aws logs tail /ecs/app-launcher --follow"
echo "     - aws logs tail /ecs/sales-journal --follow"
echo "  4. Monitor target group health in ALB console"
echo ""
echo -e "${YELLOW}Rollback (if needed):${NC}"
echo "  aws ecs update-service --cluster ${CLUSTER_NAME} --service app-launcher --desired-count 0"
echo "  aws ecs update-service --cluster ${CLUSTER_NAME} --service sales-journal --desired-count 0"
echo ""
