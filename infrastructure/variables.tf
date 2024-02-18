variable "aws_region" {
  description = "AWS Region"
  default     = "us-east-2"
}

variable "delegation_set_id" {
  description = "Reusable delegation set id for Route53 zone creation"
}

variable "route53_zone" {
  description = "Route53 zone name"
}