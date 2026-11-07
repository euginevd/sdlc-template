variable "project" {
  description = "Project name, the prefix for every resource name"
  type        = string
  default     = "<project>"
}

variable "environment" {
  description = "Deployment target, such as dev or prod"
  type        = string
  default     = "dev"
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "ap-southeast-2"
}
