#!/usr/bin/env python3
"""Local Urbit Lens helper for installing and checking urSketch."""
import json
import sys
import urllib.request

mode, value = sys.argv[1:3]
source = {'clay' if mode == 'read' else 'dojo': value}
request = urllib.request.Request('http://127.0.0.1:12321',
    data=json.dumps({'source': source, 'sink': {'app': mode} if mode in ('hood', 'treaty', 'docket') else {'stdout': None}}).encode(),
    headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(request, timeout=60) as response:
    result = json.load(response)
if mode == 'read':
    number = int(result.strip().replace('.', ''))
    print(number.to_bytes((number.bit_length()+7)//8, 'little').decode(), end='')
else:
    print(result)
