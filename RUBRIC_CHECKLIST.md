# Rubric evidence checklist

| Requirement | File / status |
|---|---|
| System prompt and three routes | project/starter/system_prompt.txt |
| Harness and gateway ARNs | project/starter/agentcore_config.json (no credentials) |
| Bug questions, tool call, ticket | evidence/chat-cli-bug-report.png (interactive ticket 6317c165-579e-43ba-90b0-8ba50200c36b), plus evidence/bug-report-transcript.txt and evidence/verified-ticket.json (earlier verified test) |
| DynamoDB console screenshot | evidence/dynamodb-table.png and evidence/dynamodb-ticket-details.png (full fields for successful ticket 936d2171-a115-4dd4-a230-ebdcc901d478) |
| Covered FAQ / uncovered FAQ / other request | evidence/chat-cli-faq-and-handoff.png (actual interactive chat.py capture for all three cases), plus evidence/*-transcript.txt |
| Automated tests | project/starter/harness-tests.json |
| Generated dataset, no HARNESS_ERROR | project/starter/output_eval_dataset.jsonl; 15 records |
| S3 and Correctness judge job | evidence/evaluation-request.json, evidence/evaluation-job.json, evidence/judge-results/ |
| Completed results screenshot | evidence/evaluation-console-results.png |
| Actual per-record observations | EVALUATION_OBSERVATIONS.md |

Evidence paths above are relative to project/starter where not fully qualified.
The course supplied no phone number. The final prompt explicitly refers to the
human support phone line, states that no verified number is available, and uses
the documented contact form/email to request it. Both uncovered-FAQ and unrelated
request cases passed live scripted chat.py CLI tests; see
project/starter/evidence/phone-handoff-cli-tests.json.
DynamoDB screenshots and interactive chat.py screenshots for every required path
are included. Earlier screenshots show the previous handoff wording; the new CLI
evidence records the final deployed wording. Judge scores remain associated with
the earlier evaluated dataset, not this final wording change.
Optional standout features (a pre-model guardrail, Knowledge Base, classifier
node) are not required and have not been added.
