"""Verify the live local comet without saving or displaying its login code."""
import json
import base64
import os
import re
import runpy
import urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

RELEASE = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'scripts/release.py'))
VERSION = RELEASE['VERSION']

request = urllib.request.Request('http://127.0.0.1:12321',
    data=json.dumps({'source': {'dojo': '+code'}, 'sink': {'stdout': None}}).encode(),
    headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(request, timeout=30) as response:
    output = json.load(response)
code = re.search(r'[a-z]{6}(?:-[a-z]{6}){3}', output).group()
artifacts = Path(__file__).resolve().parents[1] / 'artifacts'
with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={'width': 1440, 'height': 1000})
    login = context.request.post('http://127.0.0.1/~/login', form={'password': code})
    assert login.ok
    code = None
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    preview = os.environ.get('URSKETCH_PREVIEW') == '1'
    if preview:
        current = context.request.get('http://127.0.0.1/apps/ursketch/play').text()
        ship_name = re.search(r"window.URSKETCH_SHIP='([^']+)'", current).group(1)
        root = Path(__file__).resolve().parents[1]
        html = (root/'web/index.html').read_text().replace('URSKETCH_APP_VERSION', VERSION).replace('<!-- URSKETCH_LOGO -->', (root/'web/logo.svg').read_text()).replace('URSKETCH_FAVICON_DATA_URL', RELEASE['FAVICON_DATA_URL'])
        for marker,name in [('URSKETCH_CSS','style.css'),('URSKETCH_DRAWING','drawing.js'),('URSKETCH_SETTINGS','settings.js'),('URSKETCH_JS','app.js')]:
            source=(root/'web'/name).read_text()
            if name=='style.css':
                classic=(root/'web/classic.css').read_text()
                for asset in ('tools','hint','done'):
                    classic=classic.replace('CLASSIC_'+asset.upper()+'_IMAGE','data:image/gif;base64,'+base64.b64encode((root/f'web/classic-assets/{asset}.gif').read_bytes()).decode())
                for asset in ('metal','metal-small'):
                    classic=classic.replace('CLASSIC_'+asset.upper().replace('-','_')+'_IMAGE','data:image/svg+xml;base64,'+base64.b64encode((root/f'web/classic-assets/{asset}.svg').read_bytes()).decode())
                source=source.replace('/* URSKETCH_CLASSIC */',classic)
                for asset in ('skip','done'):
                    source=source.replace('DEFAULT_HINT_'+asset.upper()+'_IMAGE','data:image/svg+xml;base64,'+base64.b64encode((root/f'web/hint-{asset}.svg').read_bytes()).decode())
            html = html.replace('/* '+marker+' */',source)
        html = html.replace('<script>','<script>window.URSKETCH_SHIP='+json.dumps(ship_name)+';',1)
        page.route('**/apps/ursketch/play',lambda route:route.fulfill(status=200,content_type='text/html',body=html))
    response = page.goto('http://127.0.0.1/apps/ursketch/play')
    assert response.status == 200
    favicon=page.locator('link[rel="icon"]').get_attribute('href')
    assert favicon == RELEASE['FAVICON_DATA_URL'], 'Browser tab logo is missing'
    expect(page.locator('#status')).to_contain_text('Connected as', timeout=30000)
    expect(page.locator('#host-search')).to_be_enabled(timeout=30000)
    expect(page.locator('#host-search')).to_have_text('Search →')
    assert 'Draw a little closer.' not in page.locator('body').inner_text()
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    assert page.locator('#tool-grid button').count() == 10
    assert page.locator('#pen').get_attribute('title') == 'Pen (P)'
    assert page.locator('#brush').get_attribute('title') == 'Brush (B)'
    assert page.locator('#host-form').count() == 1
    assert page.locator('#invite-form').count() == 0
    assert page.evaluate("getComputedStyle(document.querySelector('.intro')).display") == 'grid'
    host_draft = page.locator('#host').input_value()
    page.locator('#search-invite-mode').click()
    expect(page.locator('#host')).to_have_attribute('placeholder','Paste your room invite code or link')
    page.locator('#host').fill('invalid invite')
    page.locator('#host-search').click()
    expect(page.locator('#toast')).to_contain_text('Paste a room invite link')
    page.locator('#search-host-mode').click()
    expect(page.locator('#host')).to_have_value(host_draft)
    page.locator('#host-search').click()
    expect(page.locator('#host-search')).to_be_enabled(timeout=30000)
    page.evaluate("$('toast').hidden=true")
    page.screenshot(path=str(artifacts / 'comet-lobby.png'), full_page=True)
    for width,height in [(1280,720),(1024,600),(390,844)]:
        page.set_viewport_size({'width':width,'height':height})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        page.locator('#host-form').scroll_into_view_if_needed()
        assert page.locator('#host-search').bounding_box()['width'] > 0
    page.set_viewport_size({'width':1440,'height':1000})
    page.locator('#create-open').click()
    page.locator('#title').fill('Installation check')
    page.locator('#create-form button.primary').click()
    expect(page.locator('#game')).to_be_visible(timeout=30000)
    page.wait_for_function("state && state.phase === 'waiting'")
    assert page.evaluate('roomStream'), 'The installed app did not use vector streaming'
    page.set_viewport_size({'width':1280,'height':720})
    page.wait_for_timeout(150)
    assert page.evaluate('document.documentElement.scrollHeight <= innerHeight')
    assert page.locator('#timer-dial').is_visible()
    assert page.locator('#chat-form').bounding_box()['y'] < 720
    expect(page.locator('#player-count')).to_have_text('1/12')
    page.screenshot(path=str(artifacts / 'comet-room.png'), full_page=True)
    room = page.evaluate('roomId')
    page.goto('http://127.0.0.1/apps/ursketch/play')
    expect(page.locator('#room-recovery')).to_be_visible(timeout=30000)
    expect(page.locator('#rejoin-room')).to_be_enabled(timeout=30000)
    page.locator('#rejoin-room').click()
    expect(page.locator('#game')).to_be_visible(timeout=30000)
    assert page.evaluate('roomId') == room
    # Both compact invite codes and existing copied invite URLs use Search.
    ship = page.evaluate('SELF')
    for invite in [f'{ship}/{room}',f'http://127.0.0.1/apps/ursketch/play?host={ship}&room={room}']:
        page.goto('http://127.0.0.1/apps/ursketch/play')
        expect(page.locator('#host-search')).to_be_enabled(timeout=30000)
        page.locator('#search-invite-mode').click()
        page.locator('#host').fill(invite)
        page.locator('#host-search').click()
        expect(page.locator('#game')).to_be_visible(timeout=30000)
        assert page.evaluate('roomId') == room
    page.locator('#leave').click()
    expect(page.locator('#lobby')).to_be_visible()
    tile = context.request.get('http://127.0.0.1/~/scry/docket/charges.json')
    assert tile.ok, f'Docket HTTP {tile.status}'
    charges = tile.json()
    assert 'urSketch' in json.dumps(charges), 'urSketch app tile is missing'
    assert '/apps/ursketch' in json.dumps(charges), 'urSketch tile route is missing'
    icon=runpy.run_path(str(Path(__file__).resolve().parents[1] / 'scripts/release.py'))['ICON_DATA_URL']
    assert icon in json.dumps(charges), 'urSketch logo is missing from the installed tile'
    ship = page.evaluate('SELF')
    treaty = page.evaluate("""() => new Promise(async (resolve, reject) => {
      const id=api.next;
      const timer=setTimeout(()=>reject(new Error('Publication subscription timed out')),20000);
      api.handlers.set(id,data=>{clearTimeout(timer);resolve(data);});
      await api.send({action:'subscribe',ship:SELF.slice(1),app:'treaty',path:`/treaty/${SELF}/ursketch`});
    })""")
    assert treaty['title'] == 'urSketch', 'urSketch publication is missing'
    assert treaty['image'] == icon, 'Published tile logo does not match the tile artwork'
    for label,src in [('Tile',icon),('Browser tab',favicon)]:
        assert page.evaluate("src=>new Promise(resolve=>{const image=new Image();image.onload=()=>resolve(image.naturalWidth>0);image.onerror=()=>resolve(false);image.src=src;})",src), label+' image did not decode'
    if not preview: assert treaty['version'] == VERSION
    assert treaty['href']['site'] == '/apps/ursketch'
    (artifacts / 'comet-publication.json').write_text(json.dumps(treaty, indent=2) + '\n')
    assert not errors, errors
    print(f'PASS on {ship}: login, search, tools, refresh recovery/rejoin, room create/leave, Landscape tile, and Treaty publication')
    browser.close()
