/* Game cues use decoded buffers: overlapping voices and an audio-clock ticker. */
function createGameAudio({urls,getPrefs,notify}) {
  let context=null,master=null,bridge=null,output=null,loading=null,disposed=false;
  let deadline=0,nextTick=null,ticker=null,outputRevision=0;
  const buffers=new Map(),voices=new Set();
  const audible=()=>!disposed&&!getPrefs().muted&&getPrefs().volume>0&&context?.state==='running';
  function stopVoice(voice){try{voice.stop();}catch{}voices.delete(voice);}
  function stopTicks(){for(const voice of voices)if(voice.urSketchCue==='TickingNoise')stopVoice(voice);nextTick=null;}
  function source(cue,when=context?.currentTime){
    if(!audible()||!buffers.has(cue))return;
    const voice=context.createBufferSource();voice.buffer=buffers.get(cue);voice.urSketchCue=cue;
    voice.connect(master);voices.add(voice);voice.onended=()=>{voices.delete(voice);voice.disconnect();};voice.start(when);
    window.dispatchEvent(new CustomEvent('ursketch:sound',{detail:{cue,when}}));
  }
  async function routeOutput(){
    if(!context)return;
    const revision=++outputRevision,id=getPrefs().output||'';
    try{
      if(context.setSinkId)await context.setSinkId(id);
      else if(output?.setSinkId){await output.setSinkId(id);if(revision===outputRevision)await output.play();}
    }catch{
      if(revision!==outputRevision)return;
      try{if(context.setSinkId)await context.setSinkId('');else if(output?.setSinkId){await output.setSinkId('');await output.play();}}catch{}
      notify?.('Saved audio output unavailable; using system default.');
    }
  }
  function settings(){
    if(!master)return;
    master.gain.setValueAtTime(getPrefs().muted?0:getPrefs().volume/100,context.currentTime);
    if(!audible())for(const voice of [...voices])stopVoice(voice);
    if(context.urSketchOutput!==getPrefs().output){context.urSketchOutput=getPrefs().output;void routeOutput();}
    schedule();
  }
  async function unlock(event){
    if(disposed||event&&!event.isTrusted)return;
    if(!context){
      const AudioContextClass=window.AudioContext||window.webkitAudioContext;if(!AudioContextClass)return;
      context=new AudioContextClass();master=context.createGain();
      // Firefox supports output selection on HTMLAudioElement, but not AudioContext.
      if(!context.setSinkId&&HTMLMediaElement.prototype.setSinkId){
        bridge=context.createMediaStreamDestination();output=new Audio();output.srcObject=bridge.stream;master.connect(bridge);void output.play().catch(()=>{});
      }else master.connect(context.destination);
      context.addEventListener('statechange',()=>{if(context.state!=='running')stopTicks();else schedule();});
      settings();
    }
    try{await context.resume();if(output)await output.play();}catch{return;}
    if(!loading)loading=Promise.all(Object.entries(urls).map(async([cue,url])=>{
      try{const response=await fetch(url);if(!response.ok)throw new Error('Audio unavailable');const bytes=await response.arrayBuffer();buffers.set(cue,await context.decodeAudioData(bytes));}
      catch{notify?.(`Could not load ${cue}. Reopen the app to retry.`);}
    })).then(()=>schedule());
    await loading;settings();
  }
  async function play(cue){
    const received=performance.now();if(!audible())return;
    await loading;if(disposed||performance.now()-received>1500)return;source(cue);
  }
  function schedule(){
    if(!audible()||!buffers.has('TickingNoise')||performance.now()>=deadline){stopTicks();return;}
    const now=context.currentTime,until=now+(deadline-performance.now())/1000;
    if(nextTick==null||nextTick<now-.025)nextTick=now+.015;
    // Schedule the whole remaining window so background-tab timer throttling
    // cannot change the tempo. Leaving/muting/reveal cancels these sources.
    while(nextTick<until){source('TickingNoise',nextTick);nextTick+=.25;}
  }
  function countdown(ms){
    if(ms==null||ms<=0){deadline=0;stopTicks();return;}
    const until=performance.now()+ms;
    // Authoritative updates refine the stop time without restarting the tick rhythm.
    deadline=until;schedule();
  }
  function stop(){deadline=0;for(const voice of [...voices])stopVoice(voice);nextTick=null;}
  document.addEventListener('pointerdown',unlock,{passive:true});document.addEventListener('keydown',unlock);
  window.addEventListener('pagehide',()=>{stop();disposed=true;clearInterval(ticker);void context?.close();output?.pause();});
  ticker=setInterval(schedule,25);
  return {play,countdown,settings,stop,get context(){return context;},get master(){return master;},get ready(){return loading;},get loaded(){return [...buffers.keys()];}};
}
