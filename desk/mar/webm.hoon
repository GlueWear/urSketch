::  Exact-length binary media; preserve trailing zero bytes.
|_  data=octs
++  grow
  |%
  ++  mime  [/video/webm data]
  --
++  grab
  |%
  ++  mime  |=([type=mite bytes=octs] bytes)
  ++  noun  octs
  --
++  grad  %mime
--
