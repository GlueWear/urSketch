#!/usr/bin/env python3
"""Export the app tile from the existing wordmark. Requires Playwright/Chromium.

Only needed when changing tile artwork; normal builds use web/tile.png.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
source=(root/'desk/media/images/intro-wordmark.svg').read_text()
art=source.partition('>')[2].rsplit('</svg>',1)[0]
# Centre the visible lettering, accounting for the transparent canvas around it.
svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 256 256"><rect width="256" height="256" fill="#9fc1e0"/><svg x="25.6" y="92.577" width="204.8" height="70.846" viewBox="51 91 1853 641">'+art+'</svg></svg>'
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':512,'height':512},device_scale_factor=1)
 page.set_content('<style>html,body{margin:0;width:512px;height:512px;overflow:hidden}</style>'+svg)
 page.wait_for_function("Promise.all([...document.querySelectorAll('image')].map(el=>new Promise((resolve,reject)=>{const image=new Image();image.onload=resolve;image.onerror=reject;image.src=el.getAttribute('href');})))")
 page.locator('body').screenshot(path=str(root/'web/tile.png'),omit_background=False)
 b.close()
print('Exported web/tile.png at 512×512.')
