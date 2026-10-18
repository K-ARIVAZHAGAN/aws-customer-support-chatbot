# Online Shop Customer Support Chatbot

A Udacity course project built with Amazon Bedrock AgentCore, Amazon Nova Pro,
an AgentCore Gateway, AWS Lambda, and DynamoDB.

The assistant answers shop questions using an embedded FAQ, collects website bug
reports over multiple turns before creating a ticket, and hands unsupported
requests to human support.

## Architecture

Customer -> AgentCore harness (Nova Pro + system prompt) -> AgentCore Gateway
-> create_bug_report Lambda -> DynamoDB.

The FAQ is embedded into the system prompt by `create_harness.py`. Routing and
information collection are defined in the prompt. The gateway exposes the tool
with required fields `description`, `stepsToReproduce`, and `environment`.

## Rubric evidence

See [rubric checklist](RUBRIC_CHECKLIST.md) and [per-record evaluation observations](EVALUATION_OBSERVATIONS.md). Required config and generated JSONL are included as submission evidence; neither contains AWS credentials.

## Deliverables

- [System prompt](project/starter/system_prompt.txt)
- [15-case test suite](project/starter/harness-tests.json)
- [Full evaluation dataset](project/starter/evidence/evaluation-revised.jsonl)
- [Successful multi-turn transcript](project/starter/evidence/multiturn.json)
- [Verified DynamoDB ticket](project/starter/evidence/verified-ticket.json)
- [Final handoff regression test](project/starter/evidence/handoff-regression.json)
- [Validation and limitations](VALIDATION.md)
- [Detailed run and submission guide](SUBMISSION_GUIDE.md)
- [Original course instructions](project/README.md)

Earlier failed test transcripts are retained in `project/starter/evidence` to
show the prompt iteration process.

## Results and limits

The live multi-turn test passed its assertions for information collection order,
one creation call, retained ticket ID, and database persistence. The full suite
made 15 successful harness calls; successful calls do not mean every behavior
passed. A final focused test confirmed the corrected unrelated-request handoff.

The supplied AWS console screenshot for the revised evaluation showed normalized
Correctness **1.00** and Helpfulness **0.73** across the 15-response dataset.
These scores apply to the evaluated prompt version before the final handoff
revision; they are not certification results or scores for the final revision.
The final handoff correction was checked separately. Judge results do not verify
tool calls; the multi-turn assertions and persisted ticket provide that evidence.

## Run locally against your AWS lab

Requires Python 3.9+, AWS CLI, and authorized lab access. Use **us-east-1** and
**us.amazon.nova-pro-v1:0**. Commands below are PowerShell examples.

```powershell
cd project/starter
$env:AWS_PROFILE = "udacity"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
aws sts get-caller-identity
aws cloudformation deploy --template-file cloudformation-tool.yaml --stack-name bug-report-tool-stack --capabilities CAPABILITY_NAMED_IAM --region us-east-1
python setup_gateway.py
python create_harness.py
python chat.py
```

Configure your credentials locally before running. Temporary lab credentials
need an access key, secret key, and session token. Credentials and environments are excluded from version control. The submitted resource config contains only lab resource identifiers. Setup scripts
regenerate `agentcore_config.json` for your own lab.

## Test and evaluate

```powershell
python verify_multiturn.py
python generate-eval-dataset.py --tests-json harness-tests.json --workers 4
aws cloudformation deploy --template-file cloudformation-testing.yaml --stack-name bug-report-testing-stack --capabilities CAPABILITY_NAMED_IAM --region us-east-1
python start_evaluation.py
```

The evaluation script uploads real responses, rejects harness errors/empty
responses, and starts a Nova Pro judge job with Correctness and Helpfulness
metrics. Its job ARN is saved to `evidence/evaluation-job.json`. Retrieve status
with `aws bedrock get-evaluation-job --job-identifier <job-arn> --region us-east-1`.

Tests create real tickets and AWS usage. After retaining evidence, follow the
cleanup instructions in [the course README](project/README.md). Empty the
project evaluation bucket before deleting the testing stack.

## Attribution and license

Adapted from the [Udacity starter repository](https://github.com/udacity/aws-c1-prompting-llm-reasoning-nd905-cd14762-project).
The original course instructions and [license](LICENSE.md) are retained. Project
work includes prompt engineering, test cases, runtime configuration improvements,
live verification, and evaluation helpers. AI assistance was used for development
and debugging; review the implementation and your course's disclosure rules before
submission.
