/+  *ursketch-types
|%
::  Lossless compact vector commands. Kinds are stable wire-protocol indices.
++  kinds
  ^-  (list draw-kind)
  ~[%stroke %brush %eraser %spray %rectangle %ellipse %fill %clear]
++  pack
  |=  l=line
  ^-  json
  =/  code=@ud
    ?-  kind.l
      %stroke     0
      %brush      1
      %eraser     2
      %spray      3
      %rectangle  4
      %ellipse    5
      %fill       6
      %clear      7
    ==
  =/  rgb=@ud
    %+  roll  (slag 1 (trip color.l))
    |=  [c=@tD acc=@ud]
    (add (mul acc 16) ?:((lte c '9') (sub c '0') (add 10 (sub c 'a'))))
  :-  %a
  :~  (numb code)
      (numb rgb)
      (numb width.l)
      (numb x1.l)
      (numb y1.l)
      (numb x2.l)
      (numb y2.l)
      (numb opacity.l)
      b+filled.l
      (numb seed.l)
      s+id.l
  ==
++  expand
  |=  j=json
  ^-  json
  ?>  ?=(%a -.j)
  ?>  =(11 (lent p.j))
  =/  code=@ud  (ni:dejs:format (snag 0 p.j))
  ?>  (lth code 8)
  =/  rgb=@ud  (ni:dejs:format (snag 1 p.j))
  ?>  (lte rgb 0xff.ffff)
  =/  color=@t
    %-  crip
    :-  '#'
    %+  turn  (gulf 0 5)
    |=  i=@ud
    (snag (end [2 1] (rsh [2 (sub 5 i)] rgb)) (trip '0123456789abcdef'))
  %-  obj
  :~  ['kind' s+(snag code kinds)]
      ['color' s+color]
      ['width' (snag 2 p.j)]
      ['x1' (snag 3 p.j)]
      ['y1' (snag 4 p.j)]
      ['x2' (snag 5 p.j)]
      ['y2' (snag 6 p.j)]
      ['opacity' (snag 7 p.j)]
      ['filled' (snag 8 p.j)]
      ['seed' (snag 9 p.j)]
      ['id' (snag 10 p.j)]
  ==
::  Proxies cache a complete snapshot while forwarding only incoming patches.
++  merge
  |=  [cached=(unit json) update=json]
  ^-  (unit json)
  =/  kind=@t  (text update 'kind')
  ?:  ?|(=(kind 'room') =(kind 'removed'))  `update
  ?~  cached  ~
  =/  old=json  u.cached
  ?.  =((text old 'kind') 'room')  ~
  =/  prior=(list json)  (array old 'lines')
  =/  same=?  =((number old 'token') (number update 'token'))
  ?:  =(kind 'draw')
    ?.  same  ~
    =/  start=@ud  (number update 'from')
    =/  finish=@ud  (number update 'count')
    ?:  (lte finish (lent prior))  cached
    ?.  =(start (lent prior))  ~
    =/  added=(list json)  (array update 'lines')
    ?.  =(finish (add start (lent added)))  ~
    ?>  ?=(%o -.old)
    =/  fields=(map @t json)  (~(put by p.old) 'lines' a+(welp prior added))
    =.  fields  (~(put by fields) 'count' (numb finish))
    =.  fields  (~(put by fields) 'seconds' (numb (number update 'seconds')))
    =.  fields  (~(put by fields) 'remainingMs' (numb (optional-number update 'remainingMs' (mul 1.000 (number update 'seconds')))))
    `[%o fields]
  ?.  =(kind 'state')  ~
  =/  count=@ud  (number update 'count')
  ?.  ?|(=(count 0) ?&(same =(count (lent prior))))  ~
  ?>  ?=(%o -.update)
  =/  fields=(map @t json)  (~(put by p.update) 'kind' s+'room')
  =.  fields  (~(put by fields) 'lines' a+?:(=(count 0) ~ prior))
  `[%o fields]
++  obj
  |=  pairs=(list [@t json])
  ^-  json
  [%o (~(gas by *(map @t json)) pairs)]
++  numb
  |=  n=@ud
  ^-  json
  (numb:enjs:format n)
++  text
  |=  [j=json key=@t]
  ^-  @t
  ?>  ?=(%o -.j)
  (so:dejs:format (need (~(get by p.j) key)))
++  number
  |=  [j=json key=@t]
  ^-  @ud
  ?>  ?=(%o -.j)
  (ni:dejs:format (need (~(get by p.j) key)))
++  array
  |=  [j=json key=@t]
  ^-  (list json)
  ?>  ?=(%o -.j)
  =/  value=json  (need (~(get by p.j) key))
  ?>  ?=(%a -.value)
  p.value
::  Validate bounded replay commands before accepting an artist update.
++  decode
  |=  j=json
  ^-  line
  ?:  ?=(%a -.j)  (decode (expand j))
  ?>  ?=(%o -.j)
  =/  color=@t  (text j 'color')
  ?>  =(7 (lent (trip color)))
  ?>  =('#' (snag 0 (trip color)))
  ?>  (levy (slag 1 (trip color)) |=(c=@tD ?|(?&((gte c '0') (lte c '9')) ?&((gte c 'a') (lte c 'f')))))
  =/  width=@ud  (number j 'width')
  ?>  ?&((gte width 1) (lte width 40))
  =/  x1=@ud  (number j 'x1')
  =/  y1=@ud  (number j 'y1')
  =/  x2=@ud  (number j 'x2')
  =/  y2=@ud  (number j 'y2')
  ?>  ?&((lte x1 1.000) (lte x2 1.000) (lte y1 700) (lte y2 700))
  =/  kind=@tas  (slav %tas (optional-text j 'kind' 'stroke'))
  ?>  ?=(?(%stroke %brush %eraser %spray %rectangle %ellipse %fill %clear) kind)
  =/  opacity=@ud  (optional-number j 'opacity' 100)
  ?>  ?&((gth opacity 0) (lte opacity 100))
  =/  filled=?  (bo:dejs:format (~(gut by p.j) 'filled' b+%.n))
  =/  seed=@ud  (optional-number j 'seed' 0)
  ?>  (lte seed 0xffff.ffff)
  =/  ident=@t  (optional-text j 'id' '')
  ?>  (lte (met 3 ident) 128)
  [color width x1 y1 x2 y2 kind opacity filled seed ident]
++  optional-text
  |=  [j=json key=@t fallback=@t]
  ^-  @t
  ?>  ?=(%o -.j)
  (so:dejs:format (~(gut by p.j) key s+fallback))
++  optional-number
  |=  [j=json key=@t fallback=@ud]
  ^-  @ud
  ?>  ?=(%o -.j)
  (ni:dejs:format (~(gut by p.j) key (numb fallback)))
--
