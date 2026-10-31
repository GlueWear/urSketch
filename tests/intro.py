"""Native media hashes, intro playback/controls, exact hit tracking, and Play now routing."""
import hashlib,json,os,re,urllib.request,sys,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
sys.excepthook=lambda kind,error,tb:sys.stderr.write(''.join(line for line in traceback.format_exception(kind,error,tb) if 'cookie:' not in line.lower()))
ROOT=Path(__file__).resolve().parents[1]
ORIGIN=os.environ.get('URSKETCH_ORIGIN','http://127.0.0.1:18080')
LENS=os.environ.get('URSKETCH_LENS_URL','http://127.0.0.1:12322')
req=urllib.request.Request(LENS,data=json.dumps({'source':{'dojo':'+code'},'sink':{'stdout':None}}).encode(),headers={'Content-Type':'application/json'})
code=re.search(r'[a-z]{6}(?:-[a-z]{6}){3}',json.load(urllib.request.urlopen(req,timeout=30))).group()
manifest=json.loads((ROOT/'artifacts/media-manifest.json').read_text());track=json.loads((ROOT/'web/intro-motion.json').read_text())
with sync_playwright() as p:
 b=p.chromium.launch(args=['--autoplay-policy=user-gesture-required']);c=b.new_context(viewport={'width':1280,'height':900})
 denied=c.request.get(ORIGIN+'/apps/ursketch',max_redirects=0);assert denied.status==303
 denied=c.request.get(ORIGIN+manifest['audio/music/theme_song.mp3']['url'],max_redirects=0);assert denied.status==303 and len(denied.body())<1000
 assert c.request.post(ORIGIN+'/~/login',form={'password':code}).ok;code=None
 for name,asset in manifest.items():
  response=c.request.get(ORIGIN+asset['url'])
  assert response.status==200,(name,response.status,response.text()[:100])
  assert response.headers['content-type']==asset['mime']
  assert len(response.body())==asset['bytes'],name
  assert hashlib.sha256(response.body()).hexdigest()==asset['sha256'],name
  assert 'immutable' in response.headers['cache-control']
 assert c.request.get(ORIGIN+'/apps/ursketch/media/missing.mp3').status==404
 page=c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.add_init_script("window.OriginalAudio=Audio;window.Audio=class extends OriginalAudio{constructor(...args){super(...args);window.introTestAudio=this;}}")
 page.goto(ORIGIN+'/apps/ursketch');expect(page).to_have_title('urSketch · Play now')
 expect(page.locator('#intro-stage')).to_be_visible();assert not page.locator('#lobby').count()
 page.wait_for_function("document.body.classList.contains('art-ready') && document.querySelector('video').readyState>=2",timeout=30000)
 page.wait_for_function("document.querySelector('video').currentTime>.1")
 page.locator('#intro-motion').click();assert page.locator('video').evaluate('v=>v.paused')
 assert page.evaluate('introTestAudio.paused')
 # The real click area follows the baked-in button, including its edge-on phase.
 sizes=[]
 for frame in [0,24,60,96,180,300,420]:
  t=frame/24+.002
  page.locator('video').evaluate('(v,t)=>new Promise(resolve=>{v.addEventListener("seeked",resolve,{once:true});v.currentTime=t})',t);page.wait_for_function('(t)=>Math.abs(document.querySelector("video").currentTime-t)<.02',arg=t)
  page.wait_for_timeout(80)
  stage=page.locator('#intro-stage').bounding_box();box=page.locator('#intro-play').bounding_box();x,y,w,h=track['frames'][frame]
  assert abs((box['x']+box['width']/2-stage['x'])/stage['width']*1620-x)<3,(frame,box)
  assert abs((box['y']+box['height']/2-stage['y'])/stage['height']*1080-y)<3,(frame,box)
  assert abs(box['height']/stage['height']*1080-h)<3,(frame,box)
  sizes.append(box['width'])
 assert max(sizes)>min(sizes)*2,sizes
 page.locator('video').evaluate('v=>v.currentTime=4');page.wait_for_timeout(120)
 page.screenshot(path=str(ROOT/'artifacts/intro-desktop.png'))
 # Instructions are real accessible controls, and their close restores focus.
 page.locator('#intro-instructions').click();expect(page.locator('#intro-help')).to_be_visible();page.locator('#intro-help button').click();expect(page.locator('#intro-help')).not_to_be_visible()
 page.locator('#intro-motion').click();page.wait_for_function('!document.querySelector("video").paused')
 page.locator('#intro-sound').click()
 if page.evaluate('introTestAudio.muted'):page.locator('#intro-sound').click()
 page.wait_for_function('!introTestAudio.paused && introTestAudio.currentTime>0',timeout=15000)
 page.locator('#intro-volume').evaluate("el=>{el.value=35;el.dispatchEvent(new Event('input'));}");assert abs(page.evaluate('introTestAudio.volume')-.35)<.01
 page.locator('#intro-sound').click();assert page.evaluate('introTestAudio.muted && introTestAudio.paused')
 assert page.evaluate("JSON.parse(localStorage.getItem('ursketch.settings.v1')).muted")
 # Back/forward cache must honour volume and mute changes made in the game.
 page.evaluate("()=>{const s=JSON.parse(localStorage.getItem('ursketch.settings.v1'));s.volume=20;s.muted=true;localStorage.setItem('ursketch.settings.v1',JSON.stringify(s));window.dispatchEvent(new PageTransitionEvent('pageshow',{persisted:true}));}")
 assert page.evaluate('introTestAudio.muted && introTestAudio.paused && Math.abs(introTestAudio.volume-.2)<.01')
 for width,height in [(1024,600),(390,844),(320,568)]:
  page.set_viewport_size({'width':width,'height':height});page.wait_for_timeout(100)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth && document.documentElement.scrollHeight<=innerHeight')
  assert page.locator('#intro-play').is_visible()
 page.screenshot(path=str(ROOT/'artifacts/intro-mobile.png'))
 page.locator('#intro-play').click();page.wait_for_url('**/apps/ursketch/play');expect(page.locator('#lobby')).to_be_visible();expect(page.locator('#host-search')).to_be_enabled(timeout=30000)
 # App branding returns to the new intro; direct room/lobby URLs bypass it.
 assert page.locator('.brand').get_attribute('href')=='/apps/ursketch'
 reduced=b.new_context(viewport={'width':1024,'height':600},reduced_motion='reduce')
 assert reduced.request.post(ORIGIN+'/~/login',form={'password':re.search(r'[a-z]{6}(?:-[a-z]{6}){3}',json.load(urllib.request.urlopen(req,timeout=30))).group()}).ok
 rp=reduced.new_page();rp.goto(ORIGIN+'/apps/ursketch');rp.wait_for_function("document.body.classList.contains('art-ready')");assert rp.locator('video').evaluate('v=>v.paused&&!v.getAttribute("src")')
 expect(rp.locator('#intro-motion')).to_have_text('Play animation');rp.locator('#intro-play').click();expect(rp.locator('#lobby')).to_be_visible()
 assert not errors,errors
 print('PASS: authenticated exact-byte media, immutable URLs, original video playback, frame-matched Play now target, sound/mute/volume, Instructions, mobile fit, reduced motion, and lobby routing.')
 b.close()
