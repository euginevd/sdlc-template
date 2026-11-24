# Set by the pipeline: TF_VAR_project, TF_VAR_environment, TF_VAR_region and TF_VAR_monitoring.
variable "project" {
  description = "Project name, the prefix for every resource name"
  type        = string
}

variable "environment" {
  description = "Deployment target, such as dev or prod"
  type        = string
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "ap-southeast-2"
}

# Set by the pipeline from the MONITORING repo variable: on adds the alarms in alarms.tf.
variable "monitoring" {
  description = "Whether to create alarms that email the bootstrap's alerts topic"
  type        = bool
  default     = false
}
