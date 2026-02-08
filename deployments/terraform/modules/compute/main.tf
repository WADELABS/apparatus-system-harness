# Production-grade Terraform module for Inquisitor deployment

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
  }
}

# VPC Configuration
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  
  name = "inquisitor-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  
  enable_nat_gateway     = true
  single_nat_gateway     = false
  one_nat_gateway_per_az = true
  
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Project     = "Inquisitor"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# EKS Cluster
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"
  
  cluster_name    = "inquisitor-cluster-${var.environment}"
  cluster_version = "1.28"
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
  
  # Node Groups
  eks_managed_node_groups = {
    general = {
      name           = "general"
      instance_types = ["m6i.xlarge", "m6i.2xlarge"]
      min_size       = 3
      max_size       = 10
      desired_size   = 3
      
      disk_size      = 100
      disk_type      = "gp3"
      
      # Node labels
      labels = {
        "node.kubernetes.io/role" = "general"
      }
      
      # Taints
      taints = []
      
      tags = {
        "k8s.io/cluster-autoscaler/enabled"               = "true"
        "k8s.io/cluster-autoscaler/inquisitor-cluster" = "owned"
      }
    }
    
    gpu = {
      name           = "gpu"
      instance_types = ["g5.xlarge", "g5.2xlarge"]
      min_size       = 1
      max_size       = 3
      desired_size   = 1
      
      disk_size      = 200
      disk_type      = "gp3"
      
      labels = {
        "node.kubernetes.io/role"       = "gpu"
        "nvidia.com/gpu"                = "true"
        "k8s.amazonaws.com/accelerator" = "nvidia-tesla-t4"
      }
      
      taints = [
        {
          key    = "nvidia.com/gpu"
          value  = "true"
          effect = "NO_SCHEDULE"
        }
      ]
      
      tags = {
        "k8s.io/cluster-autoscaler/enabled"               = "true"
        "k8s.io/cluster-autoscaler/inquisitor-cluster" = "owned"
      }
    }
  }
  
  cluster_addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent = true
    }
    aws-ebs-csi-driver = {
      most_recent = true
    }
  }
}

# RDS Database for Artifact Registry
module "database" {
  source  = "terraform-aws-modules/rds/aws"
  version = "~> 6.0"
  
  identifier = "inquisitor-artifact-registry"
  
  engine               = "postgres"
  engine_version       = "15.3"
  family               = "postgres15"
  major_engine_version = "15"
  instance_class       = "db.r6i.large"
  
  allocated_storage     = 100
  max_allocated_storage = 500
  storage_type         = "gp3"
  storage_encrypted    = true
  
  db_name  = "inquisitor"
  username = var.database_username
  password = var.database_password
  port     = 5432
  
  multi_az               = true
  db_subnet_group_name   = module.vpc.database_subnet_group
  vpc_security_group_ids = [module.database_sg.security_group_id]
  
  maintenance_window              = "Mon:00:00-Mon:03:00"
  backup_window                   = "03:00-06:00"
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
  
  backup_retention_period = 7
  skip_final_snapshot     = var.environment != "production"
  deletion_protection     = var.environment == "production"
  
  performance_insights_enabled          = true
  performance_insights_retention_period = 7
  
  parameters = [
    {
      name  = "autovacuum"
      value = 1
    },
    {
      name  = "client_encoding"
      value = "utf8"
    }
  ]
  
  tags = {
    Project     = "Inquisitor"
    Environment = var.environment
  }
}

module "database_sg" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 5.0"
  
  name        = "inquisitor-database-sg"
  description = "Security group for Inquisitor database"
  vpc_id      = module.vpc.vpc_id
  
  ingress_cidr_blocks = module.vpc.private_subnets_cidr_blocks
  ingress_rules       = ["postgresql-tcp"]
}

# S3 Bucket for Findings Storage
resource "aws_s3_bucket" "findings" {
  bucket = "inquisitor-findings-${var.environment}-${random_id.bucket_suffix.hex}"
  
  tags = {
    Project     = "Inquisitor"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_s3_bucket_versioning" "findings" {
  bucket = aws_s3_bucket.findings.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "findings" {
  bucket = aws_s3_bucket.findings.id
  
  rule {
    id     = "transition_to_glacier"
    status = "Enabled"
    
    transition {
      days          = 90
      storage_class = "GLACIER"
    }
    
    expiration {
      days = 365
    }
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "findings" {
  bucket = aws_s3_bucket.findings.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# ECR Repository for Container Images
resource "aws_ecr_repository" "inquisitor" {
  name                 = "inquisitor/${var.environment}"
  image_tag_mutability = "MUTABLE"
  
  image_scanning_configuration {
    scan_on_push = true
  }
  
  encryption_configuration {
    encryption_type = "AES256"
  }
  
  tags = {
    Project     = "Inquisitor"
    Environment = var.environment
  }
}

# Random suffix for bucket name
resource "random_id" "bucket_suffix" {
  byte_length = 8
}

# Variables
variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "production"
}

variable "database_username" {
  description = "Database username"
  type        = string
  sensitive   = true
}

variable "database_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

variable "alert_email" {
  description = "Email for alerts"
  type        = string
}

# Output definitions
output "cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = module.eks.cluster_endpoint
}
