terraform {
  required_providers {
    aws = {
      version = "~> 5.37"
    }
  }
  backend "s3" {
    bucket         = "gchamon-tf-backend"
    key            = "city-search-backend/terraform.tfstate"
    region         = "us-east-2"
    dynamodb_table = "gchamon-tf-backend"
  }
}

provider "aws" {
  region = var.aws_region
}

data "aws_route53_delegation_set" "devops_xd1" {
  id = var.delegation_set_id
}

resource "aws_route53_zone" "devops_xd1" {
  name              = var.route53_zone
  delegation_set_id = data.aws_route53_delegation_set.devops_xd1.id
}

module "acm" {
  source  = "terraform-aws-modules/acm/aws"
  version = "5.0.0"

  domain_name = var.route53_zone
  zone_id     = aws_route53_zone.devops_xd1.id

  validation_method = "DNS"

  subject_alternative_names = [
    "*.${var.route53_zone}",
  ]

  wait_for_validation = true
}
#
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "my-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.aws_region}a", "${var.aws_region}b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true
  enable_vpn_gateway = true
}

module "s3_bucket_alb_logs" {
  source = "terraform-aws-modules/s3-bucket/aws"

  bucket = "gchamon-alb-logs"
  acl    = "log-delivery-write"

  # Allow deletion of non-empty bucket
  force_destroy = true

  control_object_ownership = true
  object_ownership         = "ObjectWriter"

  attach_elb_log_delivery_policy = true
}

module "alb" {
  source = "terraform-aws-modules/alb/aws"

  name    = "my-alb"
  vpc_id  = module.vpc.vpc_id
  subnets = module.vpc.private_subnets

  # Security Group
  security_group_ingress_rules = {
    all_http = {
      from_port   = 80
      to_port     = 80
      ip_protocol = "tcp"
      description = "HTTP web traffic"
      cidr_ipv4   = "0.0.0.0/0"
    }
    all_https = {
      from_port   = 443
      to_port     = 443
      ip_protocol = "tcp"
      description = "HTTPS web traffic"
      cidr_ipv4   = "0.0.0.0/0"
    }
  }
  security_group_egress_rules = {
    all = {
      ip_protocol = "-1"
      cidr_ipv4   = "10.0.0.0/16"
    }
  }

  access_logs = {
    bucket = module.s3_bucket_alb_logs.s3_bucket_id
  }

  listeners = {
    http-https-redirect = {
      port     = 80
      protocol = "HTTP"
      redirect = {
        port        = "443"
        protocol    = "HTTPS"
        status_code = "HTTP_301"
      }
    }
    https = {
      port            = 443
      protocol        = "HTTPS"
      certificate_arn = module.acm.acm_certificate_arn

      fixed_response = {
        status_code  = 404
        message_body = "not found"
        content_type = "text/plain"
      }
    }
  }

  #  target_groups = {
  #    ex-instance = {
  #      name_prefix = "h1"
  #      protocol    = "HTTP"
  #      port        = 80
  #      target_type = "instance"
  #    }
  #  }
}
