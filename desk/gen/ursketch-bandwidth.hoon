/+  *ursketch-types, ursketch-wire
:-  %say
|=  *
=/  commands=(list line)
  %+  turn  (gulf 0 1.599)
  |=  i=@ud
  ^-  line
  ['#883e31' 3 (mod (mul i 17) 990) (mod (mul i 11) 690) (add 9 (mod (mul i 17) 990)) (add 9 (mod (mul i 11) 690)) %stroke 100 %.n 0 (cat 3 'load-' (scot %ud i))]
=/  totals=[snapshots=@ud deltas=@ud]
  %+  roll  (gulf 1 40)
  |=  [step=@ud acc=[snapshots=@ud deltas=@ud]]
  =/  count=@ud  (mul step 40)
  =/  history=(list line)  (scag count commands)
  =/  batch=(list line)  (slag (sub count 40) history)
  =/  before=json
    %-  obj:ursketch-wire
    :~  ['kind' s+'room']
        ['token' (numb:ursketch-wire 2)]
        ['title' s+'Bandwidth test']
        ['owner' s+'~zod']
        ['phase' s+'drawing']
        ['lines' a+(turn history |=(l=line (expand:ursketch-wire (pack:ursketch-wire l))))]
    ==
  =/  after=json
    %-  obj:ursketch-wire
    :~  ['kind' s+'draw']
        ['encoding' (numb:ursketch-wire 1)]
        ['token' (numb:ursketch-wire 2)]
        ['from' (numb:ursketch-wire (sub count 40))]
        ['count' (numb:ursketch-wire count)]
        ['seconds' (numb:ursketch-wire 80)]
        ['lines' a+(turn batch pack:ursketch-wire)]
    ==
  [(add snapshots.acc (met 3 (jam [%json before]))) (add deltas.acc (met 3 (jam [%json after])))]
[%noun totals]
