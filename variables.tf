variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-east-1"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "crypto-glance"
}

variable "docker_image" {
  description = "Docker image to run"
  type        = string
}

variable "flask_secret_key" {
  description = "Flask secret key"
  type        = string
}

variable "app_count" {
  description = "Number of instances to run"
  type        = number
  default     = 2
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default = {
    Environment = "production"
    Project     = "crypto-glance"
  }
}