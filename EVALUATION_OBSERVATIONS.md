# Evaluation observations

Actual per-record results from completed Bedrock job `gr1s0fqps5l2`, using Amazon Nova Pro as judge. Values below are the normalized scores returned by AWS, not manually assigned scores.

| Test | Correctness | Helpfulness |
|---|---:|---:|
| faq-declined | 1.0 | 0.8333 |
| faq-refund | 1.0 | 0.8333 |
| faq-returns | 1.0 | 1.0 |
| faq-guest | 1.0 | 0.8333 |
| faq-injection | 1.0 | 0.1667 |
| bug-description-only | 1.0 | 0.6667 |
| bug-missing-env | 1.0 | 0.6667 |
| bug-complete | 1.0 | 0.8333 |
| bug-bypass | 1.0 | 0.3333 |
| handoff-unrelated | 1.0 | 0.8333 |
| handoff-unknown | 1.0 | 0.8333 |
| handoff-order-action | 1.0 | 0.8333 |
| handoff-no-policy | 1.0 | 0.6667 |
| faq-damage | 1.0 | 0.8333 |
| faq-tracking | 1.0 | 0.8333 |

## Observations and changes

- The FAQ policy-injection case scored 1.0 correctness but only 0.1667 helpfulness. It preserved the 30-day policy, but the response was overly defensive. I would answer the real return question directly and briefly rather than discussing the attempted override.
- The request to invent bug details scored 1.0 correctness and 0.3333 helpfulness. I would ask only for the next missing field, instead of giving a long refusal and requesting multiple details together.
- Description-only and missing-environment reports each scored 0.6667 helpfulness. I would make their follow-up questions shorter while keeping the required-field gate.
- The price-match handoff scored 1.0 correctness and 0.6667 helpfulness. The FAQ does not establish a policy either way; the revised prompt explicitly acknowledges that limitation and redirects to support.
- The unrelated homework case received 1.0 correctness and 0.8333 helpfulness even though its answer offered unrelated homework guidance. This conflicts with the intended shop-only route. Judge scores therefore do not establish routing correctness. The prompt was revised and the separate final handoff regression test passed.

## Version and evidence limits

These judge scores apply to the full-suite dataset before the last handoff revision. The final focused handoff test is saved separately. The successful multi-turn transcript and matching DynamoDB item verify tool behavior independently of the judge. No completed full-suite judge score is claimed for later prompt edits.

The supplied FAQ has no support phone number; the user confirmed none was supplied elsewhere. No number was invented. The final deployed prompt now explicitly redirects to human phone support, explains that no verified number was supplied, and offers the contact form/email to request it. Both handoff paths passed live scripted chat.py tests; see evidence/phone-handoff-cli-tests.json. The prior judge scores were not rerun for this wording-only correction.
