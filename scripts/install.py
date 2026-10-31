#!/usr/bin/env python3
"""Copy only urSketch-owned files to an already mounted, dedicated desk."""
import argparse
import shutil
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('desk', type=Path, help='Mounted ursketch desk, e.g. /path/to/pier/ursketch')
args = parser.parse_args()
target = args.desk.resolve()
if target.name != 'ursketch' or not (target / 'sys.kelvin').is_file():
    parser.error('Use a dedicated mounted ursketch desk created with |new-desk %ursketch, =gall &')
source = Path(__file__).resolve().parents[1] / 'desk'
for folder in ('app', 'lib', 'gen', 'mar', 'sur'):
    for file in (source / folder).glob('*.hoon'):
        destination = target / folder / file.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file, destination)
if (source/'media').exists():
    shutil.copytree(source/'media',target/'media',dirs_exist_ok=True)
shutil.copy2(source / 'desk.bill', target / 'desk.bill')
for name in ('desk.docket-0', 'desk.ship'):
    if (source / name).exists():
        shutil.copy2(source / name, target / name)
print('Copied urSketch source. Preserved the desk’s runtime version and standard Urbit files.')
print('In the Dojo: |commit %ursketch, then |install our %ursketch')
