terraform {
  required_providers {
    aws = {
      version = "~> 5.37"
    }
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
