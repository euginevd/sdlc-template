# tflint for every unit in infra/aws/: AWS mistakes terraform validate can't see, such as an invalid instance
# type or a retired Lambda runtime. Run by security.yml's terraform job and scripts/check.sh.
config {
  call_module_type = "local"
}

plugin "terraform" {
  enabled = true
  preset  = "recommended"
}

plugin "aws" {
  enabled = true
  version = "0.50.0"
  source  = "github.com/terraform-linters/tflint-ruleset-aws"
}
