/+  *ursketch-types, ursketch-game
:-  %say
|=  *
=/  now=@da  ~2026.10.27
=/  r=room  (fresh:ursketch-game 'Hint rules' ~zod)
=.  r  r(players ~[[~zod 0 %.n] [~nec 0 %.n] [~bud 0 %.n]])
=.  r  (begin:ursketch-game r 'ice cream' now)
?>  =('' (hint-mask:ursketch-game r))
=/  one=room  (hint:ursketch-game r now)
?>  ?&  =(1 hints.one)
        =('___ _____' (hint-mask:ursketch-game one))
        =(0 ~(wyt in revealed.one))
    ==
=/  two=room  (hint:ursketch-game one now)
?>  ?&  =(2 hints.two)
        =(1 ~(wyt in revealed.two))
        =((met 3 answer.two) (met 3 (hint-mask:ursketch-game two)))
    ==
=/  three=room  (hint:ursketch-game two now)
?>  ?&  =(3 hints.three)
        =(2 ~(wyt in revealed.three))
        (levy ~(tap in revealed.two) |=(i=@ud (~(has in revealed.three) i)))
        =(' ' (snag 3 (trip (hint-mask:ursketch-game three))))
    ==
?>  ?=(~ (mole |.((hint:ursketch-game three now))))
=/  awarded=room  (award:ursketch-game one ~nec)
?>  =(5 score:(head players.awarded))
?>  ?=(~ (mole |.((hint:ursketch-game awarded now))))
=/  further=room  (award:ursketch-game awarded ~bud)
?>  =((turn players.further |=(p=player score.p)) ~[6 10 9])
?>  =(4 score:(head players:(award:ursketch-game two ~nec)))
?>  =(3 score:(head players:(award:ursketch-game three ~nec)))
?>  =(10 score:(head players:(award:ursketch-game r ~nec)))
?>  =(0 score:(head players.three))
=/  next=room  (choose:ursketch-game three now)
?>  ?&  =(0 hints.next)
        =(0 ~(wyt in revealed.next))
        =('' (hint-mask:ursketch-game next))
    ==
=/  saved=room-v3  ['Saved' ~zod ~[[~zod 12 %.n] [~nec 9 %.n]] %drawing 2 7 now 'cat' ~ ~[['#883e31' 4 1 2 3 4 %stroke 100 %.n 0 'saved-line']] ~]
=/  restored=room  (migrate-v3:ursketch-game saved)
?>  ?&  =(12 score:(head players.restored))
        =('saved-line' id:(head lines.restored))
        =(7 token.restored)
        =(0 hints.restored)
        =('' (hint-mask:ursketch-game restored))
    ==
[%noun 'PASS: hint masks, distinct persistent positions, three-use limit, 10/5/4/3 artist rewards, additional solves, lockout, reset, and state-3 migration']
