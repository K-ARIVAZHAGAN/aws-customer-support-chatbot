# Implementation and submission guide

## What is implemented

`project/starter/system_prompt.txt` implements all three routes, FAQ grounding,
one-question-at-a-time bug collection within a session, tool argument mapping,
real ticket ID confirmation, failure handling, cancellation, and instruction
override resistance. `harness-tests.json` contains 15 independent test cases
with expected behavior covering FAQ, bug reporting, and human handoff.
The starter AWS infrastructure and runtime scripts are retained.

Design decision: no phone number is supplied in the FAQ. The assistant must not
invent one; it offers the documented help/contact form or order-email reply.
Replace this instruction only if the course supplies a verified phone number.

## Current verification status

Local Python syntax, prompt substitution, test structure, and required argument
names have been checked. These checks do not demonstrate model behavior.
The tool and testing CloudFormation stacks, gateway, and Nova Pro harness are
deployed in the Udacity lab in us-east-1. A real ticket was confirmed in DynamoDB.
Live iteration found premature tool calls and exposed planning text; failed
transcripts are retained under project/starter/evidence. Final validation and
Bedrock judge evaluation status are recorded in that folder. Deployment alone
is not proof of correct behavior.
Do not submit invented transcripts, ticket IDs, screenshots, or scores.

## Run in your AWS lab

Open a terminal in `project/starter`. Set `$env:AWS_PROFILE="udacity"` for the
saved lab profile. Configure your lab credentials locally
(including the session token for temporary credentials); never commit them or
paste them into chat. Confirm the identity is your intended lab account:

```powershell
aws sts get-caller-identity --profile udacity
python -m pip install -r requirements.txt
aws cloudformation deploy --template-file cloudformation-tool.yaml --stack-name bug-report-tool-stack --capabilities CAPABILITY_NAMED_IAM --region us-east-1
python setup_gateway.py
python create_harness.py
python chat.py
```

The scripts pin Amazon Nova Pro (`us.amazon.nova-pro-v1:0`) in us-east-1.
Each `chat.py` launch starts a new conversation. Test this conversation:

1. Say: "The checkout page crashes." Expect a question about reproduction steps,
   with no tool call.
2. Say: "I add a shirt, open checkout, and click Pay. It goes blank instead of
   confirming payment." Expect an environment question, with no tool call.
3. Say: "Chrome on Windows 11 desktop." Expect one bug tool call and the real
   returned ticket ID. Check that the stored fields match all three turns.
4. Say: "Thanks. What is my ticket ID?" Expect the same ID without another call.

Also test a correction before filing, cancellation before details are complete,
a FAQ detour followed by resuming the report, and two separate bugs. Confirm the
assistant never merges their details. Test unavailable tool behavior if possible.

Verify persistence using the table name in the stack outputs:

```powershell
aws cloudformation describe-stacks --stack-name bug-report-tool-stack --query "Stacks[0].Outputs" --region us-east-1
aws dynamodb scan --table-name <BugReportsTableName> --region us-east-1
python generate-eval-dataset.py --tests-json harness-tests.json --workers 4
aws cloudformation deploy --template-file cloudformation-testing.yaml --stack-name bug-report-testing-stack --capabilities CAPABILITY_NAMED_IAM --region us-east-1
aws cloudformation describe-stacks --stack-name bug-report-testing-stack --query "Stacks[0].Outputs" --region us-east-1
aws s3 cp output_eval_dataset.jsonl s3://<EvalDatasetBucketName>/input/output_eval_dataset.jsonl --region us-east-1
```

Replace angle-bracket values with actual stack outputs. In the Bedrock console
in us-east-1, create an evaluation using your own inference responses, select
the uploaded dataset and testing stack evaluation role, and choose the evaluator
and metrics available in your lab/course instructions. Use a separate S3 output
prefix. Record the job ID, selected judge, metrics, actual scores, failures, and
prompt revisions. Rerun failing cases after revisions. The generator records
harness errors as responses: inspect the JSONL for errors before uploading.
The generator evaluates single turns; run `python verify_multiturn.py` to assert
collection order, one tool call, ticket ID retention, and DynamoDB persistence.
Run `python start_evaluation.py` to upload the generated responses and submit a
Nova Pro judge job with correctness/helpfulness metrics. Read the job ARN from
`evidence/evaluation-job.json` and query it with `aws bedrock get-evaluation-job`.
The live service requires taskType General for judge jobs. The SDK enum list
may lag behind that requirement.

## Evidence to collect before submitting

- Successful harness deployment and model/region configuration.
- FAQ answer, out-of-scope handoff, and full multi-turn bug transcript.
- Actual tool call, returned ticket ID, and matching DynamoDB item.
- Generated evaluation JSONL and completed Bedrock evaluation results.
- Final prompt, test suite, and explanation of any remaining failed cases.

The repository does not include the companion rubric. Check the course portal
for any extra submission requirements before submitting.

## Cleanup after capturing evidence

Follow `project/README.md`: run `cleanup_agentcore.py`, delete the tool stack,
empty the evaluation bucket, then delete the testing stack. Check the bucket
name carefully before deleting its contents. Retain evidence locally first.
