import os
import boto3

class CloudWatchMetricsEmitter:
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch')
        self.stage = os.environ.get('STAGE', 'dev')  # Default to 'dev' if STAGE is not set

    def emit_metric(self, metric_name, value, unit='Count'):
        namespace = f'Dineseater-{self.stage}'
        metric_data = [
            {
                'MetricName': metric_name,
                'Value': value,
                'Unit': unit,
            },
        ]

        self.cloudwatch.put_metric_data(
            Namespace=namespace,
            MetricData=metric_data
        )