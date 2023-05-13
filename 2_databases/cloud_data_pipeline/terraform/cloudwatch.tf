resource "aws_cloudwatch_event_rule" "hourly_execution" {
  name                = "process_membership_applications_hourly"
  description         = "Schedule to execute the process_membership_applications function hourly"
  schedule_expression = "cron(0 * * * ? *)"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = "${aws_cloudwatch_event_rule.hourly_execution.name}"
  arn       = "${aws_lambda_function.process_membership_applications.arn}"
}
