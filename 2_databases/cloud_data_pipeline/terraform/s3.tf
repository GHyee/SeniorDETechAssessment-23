resource "aws_s3_bucket" "membership_applications" {
  bucket = "membership-applications-processing-pipeline"
  acl    = "private"
}
