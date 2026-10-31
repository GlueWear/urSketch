/* The original footage is the animation; controls follow its source-frame geometry. */
'use strict';
(() => {
  const $=id=>document.getElementById(id),video=$('intro-video'),play=$('intro-play'),sound=$('intro-sound'),motion=$('intro-motion'),wordmark=$('intro-wordmark');
  const track=URSKETCH_INTRO_MOTION,settingsKey='ursketch.settings.v1';
  let prefs={volume:70,muted:false,output:'',reduceMotion:false};
  try{prefs={...prefs,...JSON.parse(localStorage.getItem(settingsKey)||'{}')};}catch{}
  prefs.volume=Number.isFinite(prefs.volume)?Math.max(0,Math.min(100,prefs.volume)):70;
  const audio=new Audio('URSKETCH_INTRO_AUDIO_URL');audio.preload='none';audio.loop=true;audio.volume=prefs.volume/100;audio.muted=!!prefs.muted;
  let unlocked=false,loading=null,videoUrl=null,paused=!!prefs.reduceMotion||matchMedia('(prefers-reduced-motion: reduce)').matches,framePending=false,wasHidden=false,resumeHelp=false;
  const status=text=>$('intro-status').textContent=text;
  function save(){try{const old=JSON.parse(localStorage.getItem(settingsKey)||'{}');localStorage.setItem(settingsKey,JSON.stringify({...old,volume:prefs.volume,muted:prefs.muted}));}catch{}}
  function controls(){motion.textContent=paused?'Play animation':'Pause animation';motion.setAttribute('aria-label',motion.textContent);sound.textContent=unlocked&&!prefs.muted?'Mute':'Enable sound';sound.setAttribute('aria-pressed',String(unlocked&&!prefs.muted));}
  function align(time){
    const n=Math.max(0,Math.min(track.frames.length-1,Math.floor(time*track.fps+0.001))),[x,y,w,h]=track.frames[n];
    play.style.left=`${x/track.width*100}%`;play.style.top=`${y/track.height*100}%`;play.style.width=`${w/track.width*100}%`;play.style.height=`${h/track.height*100}%`;
    wordmark.style.filter=`brightness(${track.brightness[n]??1})`;
    if(unlocked&&!audio.paused&&Math.abs(audio.currentTime-time)>.18){try{audio.currentTime=time;}catch{}}
  }
  function frames(){if(framePending||video.paused||document.hidden)return;framePending=true;
    if(video.requestVideoFrameCallback)video.requestVideoFrameCallback((_,data)=>{framePending=false;align(data.mediaTime);frames();});
    else requestAnimationFrame(()=>{framePending=false;align(video.currentTime);frames();});
  }
  async function output(){if(audio.setSinkId&&prefs.output){try{await audio.setSinkId(prefs.output);}catch{try{await audio.setSinkId('');}catch{}}}}
  async function startSound(gesture=false){
    if(prefs.muted||prefs.volume===0)return;
    try{audio.currentTime=video.currentTime;}catch{}
    try{const attempt=audio.play();void output();await attempt;unlocked=true;if(paused||document.hidden)audio.pause();status('');}
    catch{if(gesture)status('Sound could not start. Check your browser audio settings.');else status('Enable sound to hear the theme.');}
    controls();
  }
  async function load(){if(loading)return loading;
    loading=(async()=>{try{
      const response=await fetch('URSKETCH_INTRO_VIDEO_URL',{cache:'force-cache'});if(!response.ok)throw new Error('Video unavailable');
      videoUrl=URL.createObjectURL(await response.blob());video.src=videoUrl;video.load();status('');
      if(!paused&&!document.hidden){await video.play();void startSound();}
    }catch{loading=null;status('Animation unavailable. You can still choose Play now.');}})();return loading;
  }
  async function setPaused(value){paused=value;controls();if(paused){video.pause();audio.pause();return;}await load();try{await video.play();if(unlocked||!prefs.muted)void startSound();}catch{status('Choose Play animation to start.');}}
  sound.onclick=()=>{if(unlocked&&!prefs.muted){prefs.muted=true;audio.muted=true;audio.pause();save();controls();return;}prefs.muted=false;audio.muted=false;if(prefs.volume===0){prefs.volume=70;audio.volume=.7;$('intro-volume').value='70';}save();void startSound(true);};
  $('intro-volume').value=String(prefs.volume);$('intro-volume').oninput=e=>{prefs.volume=Number(e.target.value);audio.volume=prefs.volume/100;save();if(prefs.volume>0&&!prefs.muted&&(!unlocked||audio.paused&&!paused))void startSound(true);};
  motion.onclick=()=>void setPaused(!paused);
  video.addEventListener('playing',()=>{frames();if(!unlocked&&!prefs.muted)void startSound();});
  video.addEventListener('seeked',()=>align(video.currentTime));
  video.addEventListener('error',()=>status('Animation unavailable. You can still choose Play now.'));
  $('intro-instructions').onclick=()=>{resumeHelp=!paused;void setPaused(true);$('intro-help').showModal();};
  $('intro-help').addEventListener('close',()=>{if(resumeHelp)void setPaused(false);});
  play.addEventListener('click',()=>{video.pause();audio.pause();});
  function refreshSound(){
    try{const saved=JSON.parse(localStorage.getItem(settingsKey)||'{}');if(Number.isFinite(saved.volume))prefs.volume=Math.max(0,Math.min(100,saved.volume));if(typeof saved.muted==='boolean')prefs.muted=saved.muted;if(typeof saved.output==='string')prefs.output=saved.output;if(typeof saved.reduceMotion==='boolean')prefs.reduceMotion=saved.reduceMotion;}catch{}
    audio.volume=prefs.volume/100;audio.muted=!!prefs.muted;$('intro-volume').value=String(prefs.volume);if(prefs.muted)audio.pause();controls();
  }
  document.addEventListener('visibilitychange',()=>{if(document.hidden){wasHidden=!paused;video.pause();audio.pause();}else{refreshSound();if(wasHidden&&!paused){wasHidden=false;void setPaused(!!prefs.reduceMotion);}}});
  window.addEventListener('pagehide',event=>{video.pause();audio.pause();if(!event.persisted&&videoUrl)URL.revokeObjectURL(videoUrl);});
  window.addEventListener('pageshow',event=>{if(event.persisted){refreshSound();if(!paused)void setPaused(!!prefs.reduceMotion);}});
  const artwork=Promise.all(['URSKETCH_INTRO_MASK_URL','URSKETCH_INTRO_WORDMARK_URL','URSKETCH_INTRO_POSTER_URL'].map(src=>new Promise((resolve,reject)=>{const image=new Image();image.onload=resolve;image.onerror=reject;image.src=src;}))).then(()=>document.body.classList.add('art-ready')).catch(()=>status('Artwork unavailable. Use Play now to continue.'));
  align(0);controls();if(paused)status('Animation paused for reduced motion.');else void load();
})();
