/+  *ursketch-types, ursketch-game
:-  %say
|=  *
=/  now=@da  ~2026.10.25
=/  r=room  (fresh:ursketch-game 'Rules test' ~zod)
=.  r  r(players ~[[~zod 0 %.n] [~nec 0 %.n]])
?>  =((normalize:ursketch-game 'Ice Cream') (normalize:ursketch-game ' ICECREAM '))
=.  r  (choose:ursketch-game r now)
?>  ?&(?=(%choosing phase.r) =(3 (lent choices.r)) =(1 token.r))
?>  =(deadline.r (add now ~s15))
=/  r=room  r
=.  r  (advance:ursketch-game r deadline.r)
?>  ?&(?=(%drawing phase.r) !=('' answer.r) =(2 token.r))
=/  r=room  r
=.  r  (advance:ursketch-game r deadline.r)
?>  ?&(?=(%reveal phase.r) =(3 token.r))
=/  r=room  r
=.  r  (advance:ursketch-game r deadline.r)
?>  ?&(?=(%choosing phase.r) =(1 turn.r) =(~nec who:(head players.r)))
=/  r=room  r
=.  r
  |-  ^-  room
  ?:  ?=(%finished phase.r)  r
  $(r (advance:ursketch-game r deadline.r))
?>  =(5 turn.r)
?>  (levy players.r |=(p=player =(0 score.p)))
=/  scoring=room  (fresh:ursketch-game 'Scoring test' ~zod)
=.  scoring
  scoring(players ~[[~zod 0 %.n] [~nec 0 %.n] [~bud 0 %.n] [~wes 0 %.n] [~sev 0 %.n] [~per 0 %.n] [~sut 0 %.n] [~let 0 %.n] [~ful 0 %.n] [~pen 0 %.n] [~syt 0 %.n] [~dur 0 %.n]])
=/  solvers=(list player)  (slag 1 players.scoring)
=.  scoring
  |-  ^-  room
  ?~  solvers  scoring
  $(scoring (award:ursketch-game scoring who.i.solvers), solvers t.solvers)
?>  =((turn players.scoring |=(p=player score.p)) ~[20 10 9 8 7 6 5 5 5 5 5 5])
=/  legacy=old-room
  ['Saved room' ~zod ~[[~zod 12 %.n] [~nec 9 %.n]] %drawing 2 7 (add now ~s80) 'cat' ~ ~[['#883e31' 4 1 2 3 4]] ~]
=/  migrated=room  (migrate-room:ursketch-game legacy)
?>  ?&  =(12 score:(head players.migrated))
        =('cat' answer.migrated)
        =(7 token.migrated)
        =('#883e31' color:(head lines.migrated))
        =(%stroke kind:(head lines.migrated))
        =(100 opacity:(head lines.migrated))
    ==
=/  lone=room  (depart:ursketch-game migrated ~nec now)
?>  ?&(?=(%waiting phase.lone) =(1 (lent players.lone)) =(~zod owner.lone))
=/  empty=room  (depart:ursketch-game lone ~zod now)
?>  ?=(~ players.empty)
=/  reassigned=room  (depart:ursketch-game migrated ~zod now)
?>  ?&(?=(%waiting phase.reassigned) =(~nec owner.reassigned))
[%noun 'PASS: timers, rotation, scoring, saved drawing migration, and departure rules']
