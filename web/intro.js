/* Source footage supplies the animation; the theme song starts independently. */
'use strict';
(() => {
  const $=id=>document.getElementById(id),video=$('intro-video'),play=$('intro-play');
  const track=URSKETCH_INTRO_MOTION,settingsKey='ursketch.settings.v1',themeUrl='URSKETCH_INTRO_AUDIO_URL';
  const music=new Audio();music.preload='auto';music.loop=true;
  let prefs={},unlocked=false,pendingMusic=null,loading=null,videoUrl=null,poster=null,visualPaused=false,framePending=false,leaving=false;
  const systemMotion=matchMedia('(prefers-reduced-motion: reduce)');
  const samples=document.createElement('canvas');samples.width=2;samples.height=1;
  const sampleContext=samples.getContext('2d',{willReadFrequently:true});
  const status=text=>$('intro-status').textContent=text;
  const themeEnabled=()=>!prefs.themeDisabled&&!prefs.muted&&prefs.volume>0;
  function paintCover(source){
    if(!source)return;
    try{
      sampleContext.drawImage(source,1590,10,1,1,0,0,1,1);sampleContext.drawImage(source,738,70,1,1,1,0,1,1);
      const c=sampleContext.getImageData(0,0,2,1).data,sky=`rgb(${c[0]},${c[1]},${c[2]})`;
      $('intro-cover-sky').setAttribute('fill',sky);$('intro-cover-circle').setAttribute('fill',`rgb(${c[4]},${c[5]},${c[6]})`);
      document.documentElement.style.setProperty('--intro-sky',sky);
    }catch{}
  }
  function align(time){
    const n=Math.max(0,Math.min(track.frames.length-1,Math.floor(time*track.fps+.001))),[x,y,w,h]=track.frames[n];
    play.style.left=`${x/track.width*100}%`;play.style.top=`${y/track.height*100}%`;play.style.width=`${w/track.width*100}%`;play.style.height=`${h/track.height*100}%`;
    paintCover(video.readyState>=2?video:poster);$('intro-wordmark').style.filter=`url(#logo-alpha-cleanup) brightness(${track.brightness[n]??1})`;
    if(!video.paused&&!visualPaused&&unlocked&&!music.paused&&Math.abs(music.currentTime-time)>.18){try{music.currentTime=time;}catch{}}
  }
  function frames(){
    if(framePending||video.paused||document.hidden)return;framePending=true;
    if(video.requestVideoFrameCallback)video.requestVideoFrameCallback((_,data)=>{framePending=false;align(data.mediaTime);frames();});
    else requestAnimationFrame(()=>{framePending=false;align(video.currentTime);frames();});
  }
  async function output(){
    if(music.setSinkId&&music.sinkId!==prefs.output){try{await music.setSinkId(prefs.output||'');}catch{try{await music.setSinkId('');}catch{}}}
  }
  function startMusic(){
    if(!themeEnabled()||document.hidden||leaving)return Promise.resolve();
    if(pendingMusic)return pendingMusic;
    if(!music.src)music.src=themeUrl;
    if(!music.paused){void output();return Promise.resolve();}
    if(!video.paused&&video.readyState>=2){try{music.currentTime=video.currentTime;}catch{}}
    // Call play synchronously so a real pointer/key event can unlock browser audio.
    pendingMusic=music.play().then(()=>{unlocked=true;if(!themeEnabled()||document.hidden||leaving)music.pause();else status('');})
      .catch(()=>{status('Theme music will start after your first interaction if your browser blocks autoplay.');})
      .finally(()=>{pendingMusic=null;});
    void output();return pendingMusic;
  }
  async function load(){
    if(loading)return loading;
    loading=(async()=>{try{
      const response=await fetch('URSKETCH_INTRO_VIDEO_URL',{cache:'force-cache'});if(!response.ok)throw new Error('Video unavailable');
      videoUrl=URL.createObjectURL(await response.blob());
      const metadata=new Promise((resolve,reject)=>{video.addEventListener('loadedmetadata',resolve,{once:true});video.addEventListener('error',reject,{once:true});});
      video.src=videoUrl;video.load();await metadata;
      if(!visualPaused&&!document.hidden&&!leaving){if(!music.paused&&Number.isFinite(video.duration))video.currentTime=music.currentTime%video.duration;await video.play();}
    }catch{loading=null;status('Animation unavailable. Use Play now to continue.');$('intro-fallback').hidden=false;}})();
    return loading;
  }
  async function setVisualPaused(value){
    visualPaused=value;if(value){video.pause();if((prefs.reduceMotion||systemMotion.matches)&&video.readyState>=1)video.currentTime=1/12;paintCover(video.readyState>=2?video:poster);return;}
    await load();if(!visualPaused&&!document.hidden&&!leaving)try{if(!music.paused&&Number.isFinite(video.duration))video.currentTime=music.currentTime%video.duration;await video.play();}catch{status('Use Settings to change Reduce motion, or choose Play now.');}
  }
  function applyPrefs(next){
    prefs=next;music.volume=(prefs.volume/100)*(prefs.themeQuiet ? .25 : 1);music.muted=!!prefs.muted;
    if(!themeEnabled())music.pause();else void startMusic();
    const reduced=!!prefs.reduceMotion||systemMotion.matches;
    if(reduced!==visualPaused)void setVisualPaused(reduced);
  }
  const preferences=createSettings({notify:status,onChange:applyPrefs});
  function refreshPrefs(){preferences.refresh();}
  function interaction(event){if(event.isTrusted&&(!unlocked||music.paused))void startMusic();}
  document.addEventListener('pointerdown',interaction,{capture:true});document.addEventListener('keydown',interaction,{capture:true});
  video.addEventListener('playing',frames);video.addEventListener('seeked',()=>align(video.currentTime));
  video.addEventListener('error',()=>{status('Animation unavailable. Use Play now to continue.');$('intro-fallback').hidden=false;});
  let resumeHelp=false;
  $('intro-instructions').onclick=()=>{resumeHelp=!visualPaused;void setVisualPaused(true);$('intro-help').showModal();};
  $('intro-help').addEventListener('close',()=>{if(resumeHelp)void setVisualPaused(!!prefs.reduceMotion||systemMotion.matches);});
  function leave(){leaving=true;video.pause();music.pause();}
  play.addEventListener('click',leave);$('intro-fallback').addEventListener('click',leave);
  document.addEventListener('visibilitychange',async()=>{if(document.hidden){video.pause();music.pause();}else{if(pendingMusic)await pendingMusic;refreshPrefs();if(!visualPaused)void setVisualPaused(false);}});
  window.addEventListener('storage',event=>{if(event.key===settingsKey)refreshPrefs();});
  window.addEventListener('pagehide',event=>{leave();if(!event.persisted&&videoUrl)URL.revokeObjectURL(videoUrl);});
  window.addEventListener('pageshow',event=>{if(event.persisted){leaving=false;refreshPrefs();if(!visualPaused)void setVisualPaused(false);}});
  systemMotion.addEventListener?.('change',()=>void setVisualPaused(!!prefs.reduceMotion||systemMotion.matches));
  const image=src=>new Promise((resolve,reject)=>{const img=new Image();img.onload=()=>resolve(img);img.onerror=reject;img.src=src;});
  Promise.all([image('URSKETCH_INTRO_POSTER_URL').then(img=>{poster=img;paintCover(img);}),image('URSKETCH_INTRO_MASK_URL'),image('URSKETCH_INTRO_WORDMARK_URL')])
    .then(()=>document.body.classList.add('art-ready')).catch(()=>{status('Artwork unavailable. Use Play now to continue.');$('intro-fallback').hidden=false;});
  align(0);if(!visualPaused)void load();
})();
