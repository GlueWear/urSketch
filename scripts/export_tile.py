#!/usr/bin/env python3
"""Centre the selected, unedited PNG on a blue tile. Requires Playwright/Chromium.

Only needed when changing tile artwork; normal builds use web/tile.png.
"""
import base64
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
source=root/'desk/media/images/ursketch-logo.png'
data='data:image/png;base64,'+base64.b64encode(source.read_bytes()).decode()
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page()
    result=page.evaluate('''async src=>{
      const image=new Image();image.src=src;await image.decode();
      const scratch=document.createElement('canvas');scratch.width=image.naturalWidth;scratch.height=image.naturalHeight;
      const ctx=scratch.getContext('2d');ctx.drawImage(image,0,0);
      const pixels=ctx.getImageData(0,0,scratch.width,scratch.height).data;
      let x0=scratch.width,y0=scratch.height,x1=-1,y1=-1;
      for(let y=0;y<scratch.height;y++)for(let x=0;x<scratch.width;x++)if(pixels[(y*scratch.width+x)*4+3]>16){x0=Math.min(x0,x);x1=Math.max(x1,x);y0=Math.min(y0,y);y1=Math.max(y1,y);}
      if(x1<x0)throw new Error('The logo has no visible pixels');
      const tile=document.createElement('canvas');tile.width=tile.height=512;
      const out=tile.getContext('2d');out.fillStyle='#9fc1e0';out.fillRect(0,0,512,512);
      const scale=512*.8/(x1-x0+1);
      // Draw the complete image with one uniform scale; transparent padding is retained.
      const left=256-(x0+x1+1)/2*scale,top=256-(y0+y1+1)/2*scale;
      out.drawImage(image,left,top,image.naturalWidth*scale,image.naturalHeight*scale);
      return tile.toDataURL('image/png').split(',')[1];
    }''',data)
    (root/'web/tile.png').write_bytes(base64.b64decode(result))
    browser.close()
print('Exported web/tile.png at 512×512 from the unedited selected PNG.')
