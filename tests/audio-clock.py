"""Real browser audio decoding, background cues and cancellable scheduled ticks."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
urls={p.stem:'https://audio-test.invalid/'+p.name for p in (ROOT/'desk/media/audio/cues').glob('*.mp3')}
html='<button>Enable audio</button><script>'+ (ROOT/'web/audio.js').read_text()+'''
const prefs={volume:70,muted:false,output:''};window.scheduled=[];window.stopped=[];
const start=AudioBufferSourceNode.prototype.start,stop=AudioBufferSourceNode.prototype.stop;
AudioBufferSourceNode.prototype.start=function(when){scheduled.push({cue:this.urSketchCue,when});return start.call(this,when);};
AudioBufferSourceNode.prototype.stop=function(){stopped.push(this.urSketchCue);return stop.call(this);};
const engine=createGameAudio({urls:URLS,getPrefs:()=>prefs,notify:message=>{throw new Error(message);}});
</script>'''.replace('URLS',json.dumps(urls))
with sync_playwright() as p:
 browser=p.chromium.launch();page=browser.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 def route(request):
  name=request.request.url.rsplit('/',1)[-1]
  if name.endswith('.mp3'):request.fulfill(status=200,content_type='audio/mpeg',body=(ROOT/'desk/media/audio/cues'/name).read_bytes())
  else:request.fulfill(status=200,content_type='text/html',body=html)
 page.route('https://audio-test.invalid/**',route);page.goto('https://audio-test.invalid/');page.locator('button').click();page.wait_for_function('engine.loaded.length===9')
 # Verify a decoded file produces nonzero PCM at the actual gain output.
 page.evaluate("()=>{window.analyser=engine.context.createAnalyser();engine.master.connect(analyser);engine.play('JoinRoom');}")
 page.wait_for_function('()=>{const pcm=new Float32Array(analyser.fftSize);analyser.getFloatTimeDomainData(pcm);return pcm.some(x=>Math.abs(x)>.001);}')
 page.evaluate("()=>{engine.stop();scheduled.length=0;stopped.length=0;Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});engine.countdown(2000);}")
 ticks=page.evaluate("scheduled.filter(s=>s.cue==='TickingNoise').map(s=>s.when)")
 assert len(ticks)==8 and all(abs(b-a-.25)<1e-9 for a,b in zip(ticks,ticks[1:])),ticks
 assert ticks[-1]-ticks[0]==1.75
 page.evaluate("()=>{prefs.muted=true;engine.settings();}")
 assert page.evaluate("stopped.filter(c=>c==='TickingNoise').length")==8
 page.evaluate("()=>{prefs.muted=false;engine.settings();engine.play('YourTurnToDraw');}")
 page.wait_for_function("scheduled.some(s=>s.cue==='YourTurnToDraw')")
 page.evaluate('engine.stop()');n=page.evaluate('scheduled.length');page.wait_for_timeout(400);assert page.evaluate('scheduled.length')==n
 assert not errors,errors
 (ROOT/'artifacts/audio-clock-verification.json').write_text(json.dumps({'decodedCues':9,'nonzeroPCM':True,'backgroundCue':True,'wholeWindowScheduledAhead':True,'twoSecondTicks':8,'intervalSeconds':.25,'muteCancelsScheduledSources':True,'leavingStopsScheduler':True},indent=2)+'\n')
 browser.close();print('PASS: real decoded PCM, background turn alerts, ahead-scheduled 4 Hz ticks, mute cancellation and stopped scheduler')
