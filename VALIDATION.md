# Live validation record - 18 October 2026

The Udacity `udacity` profile authenticated successfully. No credentials are
included in this repository.

## Deployed resources

- CloudFormation `bug-report-tool-stack`: CREATE_COMPLETE.
- CloudFormation `bug-report-testing-stack`: CREATE_COMPLETE.
- AgentCore gateway: READY.
- AgentCore harness `support_chatbot-pOkEEP3Das`: READY.
- Region: us-east-1; model: us.amazon.nova-pro-v1:0.

## Verified behavior

`evidence/multiturn.json` and `evidence/verified-ticket.json` record the successful
four-turn bug scenario. Assertions passed for no premature call, exactly one
creation call after all details, no duplicate call on asking for the ID, and
DynamoDB persistence. Actual ticket: 936d2171-a115-4dd4-a230-ebdcc901d478.

All 15 independent tests completed with actual model responses and zero harness
errors. This measures successful invocations, not a claim of 15 behavioral passes.
The latest full dataset is `output_eval_dataset.jsonl`. Manual review identified
and corrected an unsupported price-match claim and missing cancellation condition.
A scope-specific final prompt revision was applied after the full suite; its
focused check is saved as `evidence/handoff-regression.json`. Read that file to
assess the correction. Earlier failed transcripts are retained for transparency.

## Judge evaluation

Two actual Bedrock Nova Pro judge jobs were submitted with Correctness and
Helpfulness metrics:

- Baseline: hepdu6htc3zd (dataset and request saved with baseline filenames).
- Revised full suite: gr1s0fqps5l2 (`evidence/evaluation-job.json`).

The user supplied an AWS console report screenshot showing Correctness 1.00
and Helpfulness 0.73 for the revised evaluation. The raw completed judge output has now been downloaded under
project/starter/evidence/judge-results; see EVALUATION_OBSERVATIONS.md. The second
job evaluates the full dataset before the last scope-specific prompt revision.
Use get-evaluation-job and download results from the saved request's S3 output
prefix when complete. Preserve results before cleaning up the lab.

## Remaining submission work

- The focused final handoff test passed; review any per-case judge findings.
- Download raw judge outputs if the rubric requires them; rerun affected cases if necessary.
- Compare deliverables against the course-portal rubric, which is not in this repo.
- Capture any console screenshots explicitly required by the course.
- Clean up the deployed resources after collecting evidence and finishing demos.

Python syntax checks and git diff whitespace checks passed. Model behavior can
vary; the saved real transcripts and results are the evidence, not the prompt's
intended behavior alone.

## Final rubric wording correction

Both uncovered FAQ and unrelated request paths now explicitly refer to the human
support phone line without inventing a number. Actual successful chat.py CLI
outputs are saved in project/starter/evidence/phone-handoff-cli-tests.json. These
focused tests validate the final wording; the reported full-suite judge scores
remain those of the earlier evaluated version.
