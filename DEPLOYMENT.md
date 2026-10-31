# urSketch deployment

- Publisher: `~livbec-pitsyd-botryp-hoshec--faltec-lavtel-firrup-marzod`
- Desk and Gall agent: `%ursketch`
- Version: 0.8.0
- Runtime: Vere 4.6 / Zuse 408
- Intro route: `/apps/ursketch`
- Lobby / direct room route: `/apps/ursketch/play`
- Source: `https://github.com/infosovereignstack/urSketch`

Install on another ship:

```hoon
|install ~livbec-pitsyd-botryp-hoshec--faltec-lavtel-firrup-marzod %ursketch
```

This is an independent desk and publication. Rooms, agent state, subscriptions,
and browser preferences are not imported from other desks. All participating
ships must install urSketch and use new room invitations. The original desk
is kept separately for rollback and is not a dependency of this app.

The source checkout is `urSketch/`. Historical Git revisions and external
source credits are retained; the active source, UI, protocol, installation
instructions, metadata, and browser storage use urSketch.

The comet uses native Hood/Clay imports because filesystem commits are not
reliable on its runtime. `scripts/import-clay.py --batch FILE...` atomically
imports related files; `--remove=FILE` removes a renamed file in that commit.
Standard runtime/mark files are inherited from the desk copy. The installed
bill starts only `%ursketch`.

Third-party Classic artwork provenance is in `NOTICE.md`.

## Release verification — October 31, 2026

urSketch 0.6.0 was installed and publicly published on the comet. Docket and
Treaty show the urSketch name, icon, route, and version. The previous app's
listing and HTTP bindings were removed; its desk/state remain private for
rollback. Only the urSketch game tile remains.

Passed on the live Zuse 408 comet: native game, hint/migration, vector codec,
and bandwidth generators; authenticated room creation, invite search,
refresh/rejoin, departure, favicon decoding, tile and Treaty checks. Native
bandwidth measured 2,210,462 snapshot bytes versus 92,202 delta bytes.

Passed on two clean Zuse 409 ships: source install/compilation, multiplayer
names and private answers, drawing replay/scoring/timers, Default/Classic
layout and palette persistence, hints and settings, and vector-stream pixel
parity, remote writes, reload/proxy/gap recovery, and full-view fallback.
JavaScript syntax, Python compilation, and whitespace checks passed.

Audited the active source, generated bundle, served page, and mounted desk:
no former app names remain. Third-party provenance is isolated in NOTICE.md.
The new repository starts with the renamed source; the original repository
retains the previous project's history and rollback material separately.

## 0.7.0 intro update — October 31, 2026

Landscape's existing route now opens the animated intro; Play now opens the
lobby at `/apps/ursketch/play`. Existing root invite URLs with queries continue
to open the app, and new invite links use the direct lobby route. Game state,
protocol, scoring, and subscriptions are unchanged.

Media files live under `desk/media/`, served after authentication. Custom
binary marks preserve byte lengths. The generated library holds only paths,
MIME types and hashes; it does not compile video data into Hoon source or HTML.
The importer packs binary files in bounded chunks for native Clay imports.
Assets have content-addressed URLs and private immutable cache headers. Eyre
controls transfer framing; the media response deliberately omits Content-Length.

The original video stream's SHA-256 is unchanged. The logo is a transparent
urSketch edit over the original wordmark, with its replacement background
masked to the old letters and its brightness following the source fade.
The control hit targets use all 442 source frames. The audio is stored as
`media/audio/music/theme_song.mp3`; `media/audio/cues/` is reserved for future
sounds. Browser audio policy may require Enable sound. Reduced motion starts
paused, and leaving/hiding the intro stops playback.

Passed on two isolated Zuse 409 ships: native source and binary import,
authenticated media hashes, original video decoding, dynamic hit tracking,
audio/mute/volume, Instructions, reduced motion, phone/laptop fit, and normal
cross-ship gameplay on the new lobby route. JavaScript/Python syntax and
whitespace checks passed. See `tests/intro.py`, fresh intro screenshots, and
`artifacts/intro-source-verification.json`.

The final wordmark uses the selected built-in imagegen lettering with a small
vector correction to the opening u, stored in `media/images/intro-wordmark.svg`.
This keeps its spelling unambiguous while retaining the reference lettering.
Native SVG media delivery and the complete intro suite also passed.

Deployed and published 0.7.0 on the live Zuse 408 comet. The full intro suite
passed against the final wordmark and media files, including restoring mute
and volume after browser-history navigation. Existing live room/rejoin,
Landscape tile, favicon, and Treaty 0.7.0 checks passed as well.

## 0.7.1 app tile — October 31, 2026

The Landscape tile uses the intro's urSketch wordmark centred on its exact
light blue background (#9fc1e0). The visible lettering occupies 80% of the
tile width. A 512×512 PNG export keeps the installed/published image compact;
Docket's color metadata matches the same blue. The header/favicon stay unchanged.
`python3 scripts/export_tile.py` regenerates the tile from the existing SVG
wordmark with Playwright, without re-generating the logo. Normal builds use
`web/tile.png`. Both the Docket file and native importer use the same image
and the Docket color as the source of truth.

Deployed and published October 31, 2026. Live checks passed for installed and
published PNG image equality/decoding, Treaty 0.7.1, favicon, and room/rejoin
flows. The 512×512 tile export was visually checked before deployment.

## 0.7.2 intro logo removal — October 31, 2026

Temporarily removes the intro wordmark image. The original baked-in lettering
stays covered; the cleanup samples the rendered video/poster background colours
so it stays clean through playback and fade-out. The coverage is restricted
to the old lettering, preserving animated artwork elsewhere in that corner.
The tile, favicon, audio, and Play now motion are unchanged. Existing wordmark
assets remain available for the tile and the forthcoming replacement SVG.

Deployed and published 0.7.2 on October 31, 2026. Visual checks confirmed the
logo is absent and background cleanup stays restricted to its old lettering.
The live intro suite passed playback, media integrity, moving controls, audio,
responsive layout, reduced motion, and navigation. Syntax/whitespace checks pass.

## 0.7.3 selected original logo — October 31, 2026

Uses the owner's selected original PNG directly in both the intro and tile.
`media/images/ursketch-logo.png` is copied byte-for-byte from the supplied file;
its SHA-256 match is recorded in artifacts/logo-selection.json. There are no
glyph replacements, vector corrections, or letter clipping in either path.
The intro renders the complete image with object-fit: contain and follows the
source fade. The tile exporter draws the complete PNG at one uniform scale,
centred by its visible bounds on the existing #9fc1e0 background. The original
lettering cleanup stays underneath the separate intro image. Older edited
variants are retained as historical assets but are not used by the intro/tile.

Deployed and published 0.7.3 on October 31, 2026. Visual previews confirmed the
selected image in both placements. Live media-integrity/intro checks and the
installed/published tile, favicon, room/rejoin, and Treaty 0.7.3 checks passed.

## 0.8.0 intro presentation and music — October 31, 2026

Removes the bottom controls and adds an intro Settings gear using the exact
same dialog/source and preference reader as the game. `themeQuiet` applies a
0.25 music gain after master volume; `themeDisabled` stops theme music without
affecting game/test sounds. Old saved settings default both options to false.
Changes apply immediately and survive navigation/history restoration. The
settings dialog also fits narrow phone screens in the normal lobby/game.

Music attempts playback immediately, independently of the video download.
Browser-denied autoplay retries synchronously on a real pointer/key gesture.
No artificial interaction or browser-policy bypass is used. Saved master mute
and audio output are respected; disabled music is not fetched automatically.
Reduced motion pauses visuals independently, and returning from instructions
aligns video to the continuing music instead of restarting the song.

The scene is uniformly scaled by 0.8. Its page background follows sampled
video/poster colours, including fades. Original-letter cleanup coverage is
expanded and a render-only alpha filter suppresses faint halo pixels while
leaving the canonical PNG unchanged and preserving opaque letter artwork.

Preview checks passed for exact media, music starting before held video
requests, quarter/off preferences across intro and game, disabled-music network
suppression, autoplay fallback, colour matching, 80% geometry, responsive
layout, moving controls, reduced motion, navigation, and normal room/rejoin.
JavaScript/Python syntax and whitespace checks passed.

Live verification on the publisher comet passed after the native Clay import
and Treaty publication: exact media, independent immediate audio with first-gesture
fallback, quarter/off settings, matched background, 80% sizing, responsive intro,
and the existing room/rejoin/tile smoke checks. Published version is 0.8.0.
