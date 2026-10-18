"""Upload real harness outputs and start a Bedrock model-as-judge evaluation.

Reference: https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation-built-in-metrics.html
Run after generate-eval-dataset.py. Requires the testing CloudFormation stack.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

import boto3


def main():
    source = Path('output_eval_dataset.jsonl')
    records = [json.loads(line) for line in source.read_text(encoding='utf-8').splitlines()]
    if not records or any(not r['modelResponses'][0]['response'].strip() or
                          '[HARNESS_ERROR]' in r['modelResponses'][0]['response']
                          for r in records):
        raise ValueError('Resolve empty responses or harness errors before evaluation.')
    session = boto3.Session(region_name='us-east-1')
    stack = session.client('cloudformation').describe_stacks(
        StackName='bug-report-testing-stack')['Stacks'][0]
    outputs = {o['OutputKey']: o['OutputValue'] for o in stack['Outputs']}
    bucket = outputs['EvalDatasetBucketName']
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')
    key = f'input/{stamp}/output_eval_dataset.jsonl'
    session.client('s3').upload_file(str(source), bucket, key)
    request = {
        'jobName': f'support-chatbot-{stamp}',
        'jobDescription': 'Course chatbot: real harness outputs, Nova Pro judge.',
        'roleArn': outputs['BedrockEvalRoleArn'],
        'applicationType': 'ModelEvaluation',
        'evaluationConfig': {'automated': {
            'datasetMetricConfigs': [{
                'taskType': 'General',
                'dataset': {'name': 'support-chatbot-tests',
                            'datasetLocation': {'s3Uri': f's3://{bucket}/{key}'}},
                'metricNames': ['Builtin.Correctness', 'Builtin.Helpfulness'],
            }],
            'evaluatorModelConfig': {'bedrockEvaluatorModels': [{
                'modelIdentifier': 'arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-pro-v1:0',
            }]},
        }},
        'inferenceConfig': {'models': [{'precomputedInferenceSource': {
            'inferenceSourceIdentifier': records[0]['modelResponses'][0]['modelIdentifier'],
        }}]},
        'outputDataConfig': {'s3Uri': f's3://{bucket}/results/{stamp}/'},
    }
    evidence = Path('evidence')
    evidence.mkdir(exist_ok=True)
    (evidence / 'evaluation-request.json').write_text(
        json.dumps(request, indent=2) + '\n', encoding='utf-8')
    result = session.client('bedrock').create_evaluation_job(**request)
    (evidence / 'evaluation-job.json').write_text(
        json.dumps(result, indent=2, default=str) + '\n', encoding='utf-8')
    print('Evaluation job:', result['jobArn'])


if __name__ == '__main__':
    main()
