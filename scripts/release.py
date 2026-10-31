"""The Docket version is authoritative for UI builds and Clay publication."""
import re
import base64
from pathlib import Path

_docket = Path(__file__).resolve().parents[1] / 'desk/desk.docket-0'
_match = re.search(r'^\s*version\+\[(\d+) (\d+) (\d+)\]', _docket.read_text(), re.MULTILINE)
if not _match:
    raise ValueError('desk/desk.docket-0 must contain a three-part release version')
VERSION_PARTS = tuple(int(part) for part in _match.groups())
VERSION = '.'.join(map(str, VERSION_PARTS))

LOGO_SVG = (_docket.parents[1] / 'web/logo.svg').read_text()
FAVICON_DATA_URL = 'data:image/svg+xml;base64,' + base64.b64encode(LOGO_SVG.encode()).decode()
# Centre an 80% copy within the tile's 64×64 viewBox.
TILE_LOGO_SVG = re.sub(r'(<svg\b[^>]*>)(.*)(</svg>)',
    r'\1<g transform="translate(6.4 6.4) scale(0.8)">\2</g>\3', LOGO_SVG, flags=re.DOTALL)
ICON_DATA_URL = 'data:image/svg+xml;base64,' + base64.b64encode(TILE_LOGO_SVG.encode()).decode()
