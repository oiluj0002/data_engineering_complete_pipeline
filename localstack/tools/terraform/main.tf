provider "aws" {
  region                      = "us-east-1"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true

  endpoints {
    s3 = "http://localstack:4566"
  }
}

resource "aws_s3_bucket" "s3_bucket_test" {
  bucket        = "s3-bucket-test"
  force_destroy = true
}