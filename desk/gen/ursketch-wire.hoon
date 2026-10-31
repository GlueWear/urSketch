/+  *ursketch-types, ursketch-wire
:-  %say
|=  *
=/  l=line  ['#00000f' 3 0 1 999 700 %brush 25 %.n 0 'test-1']
?>  =(l (decode:ursketch-wire (pack:ursketch-wire l)))
?>  =('' id:(decode:ursketch-wire (pack:ursketch-wire l(id ''))))
?>  (levy kinds:ursketch-wire |=(kind=draw-kind =(l(kind kind) (decode:ursketch-wire (pack:ursketch-wire l(kind kind))))))
=/  extreme=line  l(color '#ffffff', width 40, x1 1.000, y1 700, filled %.y, seed 4.294.967.295)
?>  =(extreme (decode:ursketch-wire (pack:ursketch-wire extreme)))
?>  ?=(~ (mole |.((decode:ursketch-wire (pack:ursketch-wire l(width 0))))))
=/  initial=json
  %-  obj:ursketch-wire
  :~  ['kind' s+'room']
      ['token' (numb:ursketch-wire 2)]
      ['count' (numb:ursketch-wire 0)]
      ['lines' a+~]
      ['seconds' (numb:ursketch-wire 80)]
  ==
=/  patch=json
  %-  obj:ursketch-wire
  :~  ['kind' s+'draw']
      ['token' (numb:ursketch-wire 2)]
      ['from' (numb:ursketch-wire 0)]
      ['count' (numb:ursketch-wire 1)]
      ['lines' a+~[(pack:ursketch-wire l)]]
      ['seconds' (numb:ursketch-wire 79)]
  ==
=/  cached=json  (need (merge:ursketch-wire `initial patch))
?>  =(1 (lent (array:ursketch-wire cached 'lines')))
?>  =(`cached (merge:ursketch-wire `cached patch))
=/  metadata=json
  %-  obj:ursketch-wire
  :~  ['kind' s+'state']
      ['token' (numb:ursketch-wire 2)]
      ['count' (numb:ursketch-wire 1)]
      ['lines' a+~]
      ['seconds' (numb:ursketch-wire 70)]
  ==
=/  combined=json  (need (merge:ursketch-wire `cached metadata))
?>  =((array:ursketch-wire cached 'lines') (array:ursketch-wire combined 'lines'))
?>  =('room' (text:ursketch-wire combined 'kind'))
?>  =(70 (number:ursketch-wire combined 'seconds'))
?>  ?=(~ (merge:ursketch-wire ~ patch))
=/  bad=json  (obj:ursketch-wire ~[['kind' s+'draw'] ['token' (numb:ursketch-wire 3)]])
?>  ?=(~ (merge:ursketch-wire `cached bad))
[%noun 'PASS: compact vector round trips, proxy snapshots, duplicate patches, and gap rejection']
