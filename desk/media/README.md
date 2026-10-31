# urSketch media

Canonical media files shipped inside the desk:

- `audio/music/theme_song.mp3`: the supplied intro's audio, extracted to MP3.
- `audio/cues/`: future game sounds. Use descriptive filenames, e.g.
  correct_guess.mp3, turn_start.mp3, and round_end.mp3. Cue events are not
  wired yet; these are naming examples only.
- `video/intro.mp4`: the original video stream, copied without re-encoding.
- `images/ursketch-logo.png`: the owner-selected, unedited canonical logo.
  Both the intro and tile exporter use this exact PNG.
- Other `images/` files include the poster and original-lettering removal mask.
  Older wordmark variants are retained for historical compatibility and are not
  used by the intro or tile.

The video is the animation. Real Play now and Instructions controls sit over
its rendered buttons. `web/intro-motion.json` stores the source-frame target
geometry and fade brightness. The logo overlay follows that fade as well.

Run `python3 scripts/build.py` after adding or changing media. It generates a
small native lookup table and content-addressed URLs. The files stay separate
from the HTML bundle. Supported formats: MP3, MP4, PNG, JPEG, OGG, WAV, WebM, SVG.
Native binary marks preserve exact lengths, including trailing zero bytes.
Assets require ship authentication and use private immutable browser caching.
The `artifacts/media-manifest.json` records byte counts and SHA-256 hashes.

Source credit is recorded in the repository's NOTICE.md.
