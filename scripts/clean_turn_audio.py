#!/usr/bin/env python3
"""Remove a time-aligned reference cue without trimming any target samples.

Manual audio-asset preparation only; requires NumPy, SciPy and ffmpeg.
"""
import argparse,json,subprocess
from pathlib import Path
import numpy as np
from scipy import signal,optimize,ndimage
p=argparse.ArgumentParser();p.add_argument('--ffmpeg',required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--reference',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--report',type=Path,required=True);args=p.parse_args()
rate=44100
def decode(path):
 raw=subprocess.check_output([args.ffmpeg,'-v','error','-i',str(path),'-f','f32le','-acodec','pcm_f32le','-ar',str(rate),'-ac','2','-'])
 return np.frombuffer(raw,dtype='<f4').reshape(-1,2).astype(np.float64)
a=decode(args.source);b=decode(args.reference);x=a.mean(1);y=b.mean(1)
corr=signal.correlate(x,y,method='fft');lags=signal.correlation_lags(len(x),len(y));lag=int(lags[np.argmax(np.abs(corr))])
reference=np.zeros_like(a);start=max(lag,0);offset=max(-lag,0);count=min(len(a)-start,len(b)-offset);reference[start:start+count]=b[offset:offset+count]
def aligned(fraction):
 return np.column_stack([np.interp(np.arange(len(a))+fraction,np.arange(len(a)),reference[:,channel],left=0,right=0) for channel in range(2)])
def residual(fraction):
 r=aligned(fraction);g=np.sum(a*r)/max(np.sum(r*r),1e-20);return np.sum((a-g*r)**2)
fraction=float(optimize.minimize_scalar(residual,bounds=(-.6,.6),method='bounded').x);r=aligned(fraction)
# A smooth reference projection follows level differences between the two MP3
# encodes. Silence stays silent; no time slice of the desired clip is removed.
sigma=rate*.012;cross=ndimage.gaussian_filter1d(np.sum(a*r,axis=1),sigma);power=ndimage.gaussian_filter1d(np.sum(r*r,axis=1),sigma)
gain=np.clip(cross/np.maximum(power,power.max()*1e-5),0,1.6)
gate=np.clip((power/power.max()-1e-5)/1e-4,0,1);gain*=gate
activity=ndimage.gaussian_filter1d(np.sum(a*a,axis=1),rate*.001)
ref_activity=ndimage.gaussian_filter1d(np.sum(r*r,axis=1),rate*.001)
gain*=np.clip(activity/np.maximum(ref_activity*.03,activity.max()*1e-6),0,1)
clean=a-r*gain[:,None]
assert len(clean)==len(a) and np.isfinite(clean).all()
args.output.parent.mkdir(parents=True,exist_ok=True)
subprocess.run([args.ffmpeg,'-y','-v','error','-f','f32le','-ar',str(rate),'-ac','2','-i','-','-c:a','libmp3lame','-q:a','2',str(args.output)],input=clean.astype('<f4').tobytes(),check=True)
encoded=decode(args.output);assert len(encoded)==len(a),'The processed clip must retain its decoded sample count'
support=np.flatnonzero(np.max(np.abs(r),axis=1)>1e-12);tail=int(support[-1]+1) if len(support) else 0
report={'method':'fractional-delay reference cancellation with smooth local gain; no cropping','sampleRate':rate,'channels':2,'inputSamples':len(a),'outputSamples':len(encoded),'durationSeconds':len(a)/rate,'referenceOffsetSamples':lag,'fractionalOffsetSamples':fraction,'maximumGain':float(gain.max()),'removedSignalRms':float(np.sqrt(np.mean((a-clean)**2))),'unmodifiedTailStartsAtSeconds':tail/rate,'tailErrorBeforeEncoding':float(np.max(np.abs(clean[tail:]-a[tail:]))) if tail<len(a) else 0}
args.report.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
