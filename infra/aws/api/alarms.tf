# Alarms (guide 04, control 24), when the MONITORING repo variable is on and the bootstrap's Monitoring
# parameter has made the ${project}-alerts topic: errors in the function, and 5xx from the API, email the
# alerts topic's subscriber. The first 10 alarms in an account are free.
locals {
  alerts_topic = "arn:${data.aws_partition.current.partition}:sns:${var.region}:${data.aws_caller_identity.current.account_id}:${var.project}-alerts"
}

resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  count               = var.monitoring ? 1 : 0
  alarm_name          = "${var.project}-api-${var.environment}-errors"
  alarm_description   = "The api function raised errors"
  namespace           = "AWS/Lambda"
  metric_name         = "Errors"
  dimensions          = { FunctionName = aws_lambda_function.api.function_name }
  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  threshold           = 0
  comparison_operator = "GreaterThanThreshold"
  treat_missing_data  = "notBreaching"
  alarm_actions       = [local.alerts_topic]
  ok_actions          = [local.alerts_topic]
}

resource "aws_cloudwatch_metric_alarm" "api_5xx" {
  count               = var.monitoring ? 1 : 0
  alarm_name          = "${var.project}-api-${var.environment}-5xx"
  alarm_description   = "The HTTP API returned 5xx responses"
  namespace           = "AWS/ApiGateway"
  metric_name         = "5xx"
  dimensions          = { ApiId = aws_apigatewayv2_api.api.id, Stage = aws_apigatewayv2_stage.default.name }
  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  threshold           = 0
  comparison_operator = "GreaterThanThreshold"
  treat_missing_data  = "notBreaching"
  alarm_actions       = [local.alerts_topic]
  ok_actions          = [local.alerts_topic]
}
