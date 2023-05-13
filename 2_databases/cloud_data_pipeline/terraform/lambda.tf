data "archive_file" "process_membership_applications" {
  type        = "zip"
  source_dir  = "src"
  output_path = "process_membership_applications.zip"
}

resource "aws_lambda_function" "process_membership_applications" {
  filename      = "process_membership_applications.zip"
  function_name = "process_membership_applications"
  role          = "${aws_iam_role.lambda_exec.arn}"
  handler       = "main.lambda_handler"
  runtime       = "python3.9"
  timeout       = 900  # 15 minutes in seconds

  environment {
    variables = {
      BUCKET_NAME = "${aws_s3_bucket.membership_applications.id}"
    }
  }

  source_code_hash = data.archive_file.process_membership_applications.output_base64sha256
}

resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_exec_s3_access" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
  role       = "${aws_iam_role.lambda_exec.name}"
}

resource "aws_cloudwatch_log_group" "lambda_logs" {
  name = "process_membership_applications_logs"
}

resource "aws_iam_role_policy" "lambda_exec_cloudwatch_access" {
  name   = "lambda_exec_cloudwatch_access"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "clouwatch:*"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
  
  role = "${aws_iam_role.lambda_exec.id}"
}
