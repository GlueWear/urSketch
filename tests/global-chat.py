"""Native shared-chat verification on isolated ~zod/~nec; never posts to humans."""
import json,re,sys,time,traceback,urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
sys.excepthook=lambda kind,error,tb:sys.stderr.write(''.join(line for line in traceback.format_exception(kind,error,tb) if 'cookie:' not in line.lower()))
ROOT=Path(__file__).resolve().parents[1]
def dojo(port,command):
 request=urllib.request.Request(f'http://127.0.0.1:{port}',data=json.dumps({'source':{'dojo':command},'sink':{'stdout':None}}).encode(),headers={'Content-Type':'application/json'})
 return json.load(urllib.request.urlopen(request,timeout=60))
LENSES={}
for port in (12322,12323):
 who=dojo(port,'our').strip()
 if who in ('~zod','~nec'):LENSES[who]=port
assert set(LENSES)=={'~zod','~nec'},'Use isolated fake ships only'
def login(context,port,origin):
 code=re.search(r'[a-z]{6}(?:-[a-z]{6}){3}',dojo(port,'+code')).group()
 assert context.request.post(origin+'/~/login',form={'password':code}).ok
with sync_playwright() as p:
 browser=p.chromium.launch();contexts=[browser.new_context(viewport={'width':1280,'height':720}) for _ in range(2)];pages=[];errors=[]
 for context,port,origin,name in zip(contexts,[LENSES['~zod'],LENSES['~nec']],['http://127.0.0.1:18080','http://127.0.0.1:18081'],['Alice','Bob']):
  login(context,port,origin);context.route('**/media/**/images/ursketch-logo.png',lambda route:route.fulfill(status=200,content_type='image/png',body=(ROOT/'desk/media/images/ursketch-logo.png').read_bytes()));page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(origin+'/apps/ursketch/connect');page.locator('#player-name').fill(name);page.locator('#connect-submit').click();page.wait_for_url('**/apps/ursketch/play')
  assert page.evaluate("GLOBAL_CHAT_HOST==='~zod'")
  expect(page.locator('#global-chat-input')).to_be_enabled(timeout=45000);pages.append(page)
 h,g=pages;tag=str(time.time_ns());first='Hello from Alice '+tag;second='Hello from Bob '+tag+' <b>literal text</b>'
 h.locator('#global-chat-input').fill(first);h.locator('#global-chat-send').click()
 for page in pages:expect(page.locator('#global-messages')).to_contain_text(first,timeout=30000)
 # Identity comes from the native sender, regardless of a supplied ship field.
 g.evaluate("text=>api.poke('global-chat',{text,ship:'~zod'},{host:GLOBAL_CHAT_HOST,room:''})",second)
 for page in pages:expect(page.locator('#global-messages')).to_contain_text(second,timeout=30000)
 assert h.evaluate('(text)=>globalMessages.find(m=>m.text===text).ship',second)=='~nec'
 assert h.locator('.global-message b').count()==0
 g.locator('#global-chat-input').fill('draft retained');g.evaluate('()=>{window.originalChatPoke=api.poke;api.poke=()=>Promise.reject(new Error("simulated send failure"));}')
 g.locator('#global-chat-send').click();expect(g.locator('#global-chat-status')).to_contain_text('Message not sent')
 expect(g.locator('#global-chat-input')).to_have_value('draft retained');g.evaluate('()=>{api.poke=originalChatPoke}')
 # Room searching never redirects or uses the shared chat input.
 subscription=g.evaluate('globalChatSub');g.locator('#host').fill('~nec');g.locator('#host-search').click();expect(g.locator('#host-search')).to_be_enabled(timeout=30000)
 assert g.evaluate('globalChatSub')==subscription;expect(g.locator('#host')).to_have_value('');expect(g.locator('#global-chat-input')).to_have_value('draft retained')
 h.wait_for_timeout(1100);third='Still one shared chat '+tag;h.locator('#global-chat-input').fill(third);h.locator('#global-chat-send').click()
 expect(h.locator('#global-chat-input')).to_have_value('')
 assert h.evaluate("api.poke('global-chat',{text:'too soon'},{host:GLOBAL_CHAT_HOST,room:''}).then(()=>false,()=>true)")
 expect(g.locator('#global-messages')).to_contain_text(third,timeout=30000)
 # Native bounds and identity cooldown reject malformed/rapid posts.
 assert h.evaluate("api.poke('global-chat',{text:'x'.repeat(241)},{host:GLOBAL_CHAT_HOST,room:''}).then(()=>false,()=>true)")
 assert h.evaluate("api.poke('global-chat',{text:'bad\\nmessage'},{host:GLOBAL_CHAT_HOST,room:''}).then(()=>false,()=>true)")
 g.reload();expect(g.locator('#global-chat-input')).to_be_enabled(timeout=30000);expect(g.locator('#global-messages')).to_contain_text(first);expect(g.locator('#global-messages')).to_contain_text(third)
 g.locator('#global-messages .global-chat-name').filter(has_text='Alice').first.click();expect(g.locator('#player-profile-ship')).to_have_text('~zod');g.locator('#player-profile-dialog form button').click()
 g.screenshot(path=str(ROOT/'artifacts/global-chat-fake-ships.png'))
 (ROOT/'artifacts/global-chat-verification.json').write_text(json.dumps({'isolatedShips':['~zod','~nec'],'sharedHost':'~zod','bothDirections':True,'senderIdentityVerified':True,'searchIndependent':True,'refreshHistory':True,'failedSendRetainsDraft':True,'boundsAndCooldown':True,'plainTextRendering':True},indent=2)+'\n')
 assert not errors,errors;browser.close()
 print('PASS: isolated native shared chat, both directions, trusted sender ID, independent search, retained failed draft, history after refresh, profile inspection, message bounds and cooldown')
