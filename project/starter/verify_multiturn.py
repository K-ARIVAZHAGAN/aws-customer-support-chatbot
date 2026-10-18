"""Run a real multi-turn smoke test and save its transcript (requires AWS)."""
import contextlib
import io
import json
import re
import uuid
from pathlib import Path

import boto3
from botocore.config import Config
from chat import invoke


def main():
    config = json.loads(Path('agentcore_config.json').read_text(encoding='utf-8'))
    rt = boto3.client('bedrock-agentcore', region_name=config['region'],
                      config=Config(read_timeout=300, retries={'max_attempts': 1}))
    session = str(uuid.uuid4()) + '-multiturn-test'
    prompts = [
        'The checkout page crashes.',
        'I add a shirt, open checkout, and click Pay. It goes blank instead of confirming payment.',
        'Chrome on Windows 11 desktop.',
        'Thanks. What is my ticket ID?',
    ]
    evidence = []
    destination = Path('evidence')
    destination.mkdir(exist_ok=True)
    for prompt in prompts:
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            reply = invoke(rt, config, session, prompt)
        evidence.append({'user': prompt, 'assistant': reply,
                         'stream_output': captured.getvalue()})
        (destination / 'multiturn.json').write_text(
            json.dumps(evidence, indent=2) + '\n', encoding='utf-8')
        print('USER:', prompt, '\nASSISTANT:', captured.getvalue(), flush=True)

    assert all('[tool call]' not in e['stream_output'] for e in evidence[:2]), \
        'Premature tool call before all required details were supplied'
    assert evidence[2]['stream_output'].count('[tool call]') == 1, \
        'Expected exactly one tool call after environment collection'
    assert '[tool call]' not in evidence[3]['stream_output'], 'Duplicate ticket call'
    ids = re.findall(r'\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b',
                     evidence[2]['assistant'])
    assert len(ids) == 1 and ids[0] in evidence[3]['assistant'], 'Ticket ID not retained'
    item = boto3.resource('dynamodb', region_name=config['region']).Table(
        config['table_name']).get_item(Key={'ticketId': ids[0]}).get('Item')
    assert item, 'Returned ticket is absent from DynamoDB'
    assert all(item.get(k) for k in ('description', 'stepsToReproduce', 'environment'))
    (destination / 'verified-ticket.json').write_text(
        json.dumps(item, indent=2) + '\n', encoding='utf-8')
    print('PASS: collection order, one tool call, remembered ID, DynamoDB persistence.')


if __name__ == '__main__':
    main()
