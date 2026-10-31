#!/usr/bin/env python3
"""Import urSketch-owned files into its existing %ursketch desk through Hood/Clay.

--batch commits related files together, so clients never see half an update.
"""
import json
import sys
import urllib.request
from pathlib import Path
from release import VERSION_PARTS, ICON_DATA_URL

ROOT = Path(__file__).resolve().parents[1] / 'desk'

def cord(text):
    return "'" + ''.join('\\%02x' % b if b in (10, 13, 39, 92) or b < 32 or b > 126 else chr(b) for b in text.encode()) + "'"

def change(name):
    remove = name.startswith('--remove=')
    if remove: name = name.split('=', 1)[1]
    path = ROOT / name
    mark = path.suffix[1:]
    parts = path.relative_to(ROOT).with_suffix('').parts
    destination = '/=ursketch=/' + '/'.join(parts) + '/' + mark
    if remove:
        return f'(fray:space:userlib {destination})'
    if mark == 'hoon':
        value = cord(path.read_text())
    elif mark == 'docket-0':
        # Native noun for the clauses in desk/desk.docket-0.
        version_noun = ' '.join(map(str, VERSION_PARTS))
        value = f"[%1 'urSketch' 'Draw, guess, and laugh together. Multiplayer drawing rooms hosted on Urbit ships.' 0x32.684e [%site /apps/ursketch] [~ {cord(ICON_DATA_URL)}] [{version_noun}] '' 'Unspecified']"
    else:
        value = path.read_text().strip()
    return f'(foal:space:userlib {destination} [%{mark} !>({value})])'

def send(names):
    changes = [change(name) for name in names]
    combined = changes[-1]
    for item in reversed(changes[:-1]):
        combined = f'(furl:space:userlib {item} {combined})'
    command = f'+hood/pass [%c %info {combined}]'
    payload = {'source': {'dojo': command}, 'sink': {'app': 'hood'}}
    request = urllib.request.Request('http://127.0.0.1:12321',
        data=json.dumps(payload).encode(), headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(request, timeout=90) as response:
        result = json.load(response)
    print(', '.join(names) + ': ' + str(result).strip(), flush=True)
    if str(result).strip() != '>=':
        raise SystemExit('Clay did not acknowledge the import.')

if __name__ == '__main__':
    arguments = sys.argv[1:]
    batch = '--batch' in arguments
    names = [name for name in arguments if name != '--batch']
    if not names:
        raise SystemExit('Specify urSketch desk source files to import.')
    if batch:
        send(names)
    else:
        for name in names:
            send([name])
