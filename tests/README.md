# urSketch verification

The native generators exercise game rules, state migration, hint rewards,
codec bounds, snapshot caches, and vector bandwidth:

```hoon
+ursketch!ursketch-rules
+ursketch!ursketch-hints
+ursketch!ursketch-wire
+ursketch!ursketch-bandwidth
```

`browser.py`, `hints-and-settings.py`, `classic-layout.py`,
`tools-and-recovery.py`, and `vector-stream.py` use two isolated ships
(~zod and ~nec) on HTTP ports 18080/18081 and Ames ports 31337/31338.
Each prompts for a hidden JSON object with `host` and `guest` login codes.
`lobby-and-multiplayer.py` uses four ships and its own hidden code prompt.
Never save real ship login codes or cookies in artifacts.

`comet.py` authenticates to the local comet through Lens, checks the served
page and favicon, exercises room creation, invite search and refresh/rejoin,
and verifies the urSketch tile and Treaty image/version/route. It saves only
public metadata and screenshots in `artifacts/`.

JavaScript syntax: `node --check web/app.js` (also drawing.js/settings.js).
Build: `python3 scripts/build.py`. Python: `python3 -m compileall scripts tests`.

`NOTICE.md` records external artwork sources. Reference-sized Classic tests
retain the supplied drawer and guesser geometry while displaying urSketch.

## 0.6.0 results — October 31, 2026

Passed: all four native generators on the live comet; browser.py,
classic-layout.py, hints-and-settings.py, vector-stream.py on two clean
ships; comet.py before and after publication cutover; source/bundle/mounted
file naming audit; JavaScript/Python syntax and whitespace checks.

The 1,600-command vector test measured 4,463,815 bytes for repeated JSON
snapshots versus 85,583 bytes for deltas (98.08% reduction), with identical
canvas pixels. Full snapshots shrank from 217,765 to 82,698 bytes. These
measure payload bytes, not end-to-end network latency.

Fresh screenshots and public metadata are under artifacts/. No credentials
or real ship session cookies are saved.

## 0.7.0 intro verification

`intro.py` checks the actual ship routes and requires no saved credentials.
Default test URLs are HTTP 18080 and Lens 12322. Set URSKETCH_ORIGIN and
URSKETCH_LENS_URL to check another ship. It verifies authentication, every
asset's SHA-256 and byte length, MIME/cache headers, missing media 404,
actual video playback, frame-matched button targets including edge-on/fade
states, sound/mute/volume persistence, Instructions, reduced motion, mobile
fit, and navigation into the existing lobby.

Native binary import and intro checks passed on both isolated ships. Existing
browser.py multiplayer checks passed with both clients using the new direct
lobby route. The source/shipped video stream hash comparison confirms that
animation packets are identical. The selected wordmark and built-in imagegen
prompt are recorded in artifacts/intro-wordmark-prompt.md.

The final SVG wordmark was checked in the actual intro on the isolated ship.
The media suite verifies both its exact file hash and successful browser decode.

Passed on the live Zuse 408 comet: complete intro suite with final SVG logo,
exact media hashes, saved audio preferences on browser-history restoration,
and existing room/rejoin/tile/favicon/publication smoke checks for 0.7.0.

## 0.7.1 tile update

Visually checked the centred wordmark and exact #9fc1e0 blue in the 512×512
export. Live installed/published image equality and PNG decoding, Treaty
0.7.1, and the existing comet smoke checks passed October 31, 2026.

## 0.7.3 original PNG selection

Verified the canonical PNG SHA-256 equals the exact owner-selected file.
Visual checks confirmed the full original lettering in the intro and tile.
Live intro/media hashes and normal comet room/tile/publication checks passed.
The selection and rendering constraints are recorded in artifacts/logo-selection.json.

## 0.8.0 clean intro and theme settings

The intro suite runs an allowed-autoplay browser and a browser with an initial
audio denial. It holds the video request to prove music starts independently,
then checks first-gesture retry, disabled-song network suppression, quarter/off
settings shared with the game, history restoration, exact 80% scene dimensions,
decoded-video/background colour equality, no bottom controls, phone settings,
reduced motion, target tracking, and entry into the lobby. `URSKETCH_PREVIEW=1`
checks local generated HTML against the live backend before deployment.

Both the intro suite and normal comet smoke suite passed on the deployed
0.8.0 publisher desk after publication.
