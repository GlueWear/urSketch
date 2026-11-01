# urSketch for Urbit

A multiplayer drawing game hosted on Urbit ships. One Gall agent owns rooms,
checks guesses, awards points, and synchronizes vector drawings over Ames.
The browser uses Eyre channels directly, with no npm dependencies or external
services. All browser assets are embedded and served by the ship.

## Install from the publisher

urSketch 0.8.2 is published from
`~livbec-pitsyd-botryp-hoshec--faltec-lavtel-firrup-marzod`.
On another ship, run:

```hoon
|install ~livbec-pitsyd-botryp-hoshec--faltec-lavtel-firrup-marzod %ursketch
```

You can also browse that ship in Landscape’s app discovery and select urSketch.
After installation, open its tile or `/apps/ursketch` for the animated intro.
Choose **Play now** to enter the lobby at `/apps/ursketch/play`. The
publisher must be online for a new ship to download the desk and updates.
The published desk currently targets Zuse 408.

## Install from source

Use a **new dedicated desk** on each participating ship. In the Dojo:

```hoon
|new-desk %ursketch, =gall &
|mount %ursketch
```

In your computer’s terminal, from this directory:

```sh
python3 scripts/build.py
python3 scripts/install.py /absolute/path/to/your/pier/ursketch
```

Back in the Dojo:

```hoon
|commit %ursketch
|install our %ursketch
```

Log into the ship’s web interface, then open `/apps/ursketch` on that same origin.
The installer preserves the runtime version and standard mark files created by
`|new-desk`, so it does not copy a stale kernel version from another project.

To update source later, rerun the two Python commands and `|commit %ursketch`.

The desk and agent are both `%ursketch`. `/apps/ursketch` is the animated intro;
`/apps/ursketch/play` opens the lobby directly.
Install this desk on every participating ship. Existing rooms and browser
preferences from another app are separate; create new rooms and invitations.

## Play

- The room search box switches between **Browse a host ship** and
  **Room invite code**, using one input and **Search →** button. Each mode
  remembers its input when you switch.
- Save or select a display name in **Who’s playing?** on the landing page.
  Profiles stay in your browser, while names in a room are synchronized by its
  host. Urbit ship identity still authenticates actions.
- The game fits laptop viewports; the players and game log are on the left,
  conversation is below, and the canvas is on the right. The timer uses a grey dial that turns red for the final 20 seconds.
- Create a room on your own ship. It supports 2–12 players.
- Friends install urSketch on their ships, open their own `/apps/ursketch/play`, and
  enter your ship in **Browse a host ship**. Search and join each show progress until the host responds.
- Invite URLs carry `host` and `room`. Friends paste the copied URL into
  **Room invite code** on their own ship. No one needs to log into another
  player’s ship. Compact codes like `~sampel-palnet/room-abcd1234` also work.
- The owner starts the game. Each artist chooses among three words in 15 seconds,
  then has 80 seconds to draw. Guessers use the input under the Game log.
- Correct guesses earn 10, 9, 8, 7, 6, then 5 points each. The drawer earns
  10 points for the first solve and 1 for each additional solve. Hints reduce
  that initial artist reward to 5, then 4, then 3 points. No solves means
  no drawer points. A turn ends when everyone guesses,
  time expires, or the artist passes. The answer stays visible for seven seconds.
- Before anyone guesses correctly, the drawer can press **Give hint** at most
  three times. The first shows the word's letter count and blanks. The next
  two reveal one random, previously hidden letter position each. Spaces stay
  visible, and revealed letters last through the turn and refresh/rejoin.
  Give hint closes after the first correct guess; Skip becomes Done.
- Open the game screen's **⚙ Settings** for volume, mute, audio output,
  a test sound, theme, reduced motion, and larger chat text. Preferences are
  saved in this browser. Default and Classic are available; Classic uses the supplied drawer/
  guesser layouts, floating palettes, compact panes, and original control sprites. Grubbery
  Theme is a coming-soon placeholder. Game sound effects will be added later.
  Output selection depends on [browser support](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/setSinkId);
  unsupported browsers use system default. Microphone permission is not requested.
- Players rotate through three rounds. The owner can start another game afterward.
- The drawer has Pen (**P**), Brush (**B**), Spray (**Y**), Eraser (**E**),
  Rectangle (**S**), Circle (**C**), Line (**L**), Fill, Zoom (**Z**), and Clear,
  following the reference drawing controls.
  Brush is translucent; selecting a shape again toggles filled/outline.
  Shift constrains shapes; Shift+Clear clears with the selected color.
- Use **1–8**, **9**, **0** for widths 1–8, 16, 32; left/right arrows adjust
  width and up/down arrows adjust brightness. **D** toggles black/white,
  **Alt+click** samples a color, **Space+drag** pans, and **+ / −** zoom.
  Space+Alt+click zooms in; Space+Command+click or Shift+Zoom zooms out.
  Double-click Zoom to reset zoom and pan. **Tab** switches between Game and Chat inputs.
- There are 24 reference colors including browns, an advanced color picker,
  width preview, and palettes whose grip allows rearrangement or double-click
  rotation. Their placement is saved in your browser.
- After a refresh or interrupted connection, the lobby offers **Rejoin** and
  **Leave room**. Your identity and score are held for up to two minutes while
  disconnected. Connected players renew their place automatically. Temporary heartbeat failures
  retry within that window instead of immediately returning you to the lobby.
  Recovery state is synchronized between tabs. An expired lobby recovery card
  never sends a leave request for a game active in another tab. Departure
  messages distinguish leaving from a two-minute disconnect timeout.

One identity per ship prevents a browser from claiming another ship’s score or
artist permissions. Correct guesses are replaced with a success message.
The game log and conversation are separate. Chat messages containing the
answer are rejected during a drawing turn. Guessers receive no word length or letters until the drawer gives a hint.
The full answer remains private until the turn is revealed.
Returning to a room restores the authoritative drawing and scores.

## Source and checks

```text
desk/app/ursketch.hoon       Gall, HTTP, private per-ship views, JSON actions
desk/lib/ursketch-game.hoon      Pure turn and timer rules; 100 drawing prompts
desk/lib/ursketch-types.hoon     Versioned state’s shared data types
desk/lib/ursketch-wire.hoon      Compact vector codec and stream proxy cache
desk/lib/ursketch-assets.hoon    Generated browser bundle
desk/gen/ursketch-rules.hoon Rules regression checks
desk/gen/ursketch-wire.hoon  Codec, bounds, and snapshot cache checks
desk/gen/ursketch-bandwidth.hoon Encoded-payload benchmark
web/drawing.js             Drawing tools and deterministic command replay
web/settings.js            Local audio, theme, and accessibility preferences
web/logo.svg               Header logo and browser favicon
web/tile.png               Centred intro wordmark on the light blue app tile
web/                       HTML, CSS, and JavaScript source
scripts/                   Asset builder and dedicated-desk installer
tests/                     Browser integration checks
```

Run the Hoon rules checks from a Dojo with the urSketch desk selected:

```hoon
=dir /=ursketch=
+ursketch-rules
```

`python3 scripts/build.py` regenerates the embedded browser bundle. JavaScript
can be checked with `node --check web/app.js` and `node --check web/drawing.js` and `node --check web/settings.js`. See `tests/README.md` for the
browser integration checks and verification record.

## Current scope

Rooms live on the host ship; browse a known host to find its rooms. There is no
global directory, password room, spectator role, moderation panel, or imported
external word list. urSketch code and branding are original. Third-party Classic
control graphics are credited in [NOTICE.md](NOTICE.md).

Drawings travel as lossless vector commands, with up to 12,000 commands per
turn and 80 commands per batch. Updated clients use compact numeric tuples
and indexed drawing deltas. Ordinary drawing updates send only new commands;
chat, guesses, scores, and other room metadata do not resend drawing history.
Joining, reload, and recovery use complete snapshots. Missing deltas trigger
an automatic snapshot request; duplicates are ignored. Proxy ships maintain
a complete cached view for additional local tabs.

## Animated introduction and audio

Landscape opens the supplied animation with the selected original PNG wordmark.
The original video stream is preserved rather than recreated. The real Play
now target follows its button frame by frame; Instructions opens the rules.
Play now opens the existing lobby, while direct invitations open the game.

The music is `desk/media/audio/music/theme_song.mp3`. Future cue files belong
in `desk/media/audio/cues/`; game cue events are not wired yet. The theme starts
immediately without waiting for video loading, subject to browser autoplay
permissions and saved mute preferences. If autoplay is blocked, the first real
click or key retries it; there is no bottom control bar.

The intro's top-right gear opens the same Settings menu as the game. **Theme
song at 25% volume** applies one quarter of its normal level after master volume;
**Disable theme song** stops only the music. Both are saved in this browser.
Master mute, volume, and selected audio output still apply. Each animation loop
resets the song to the video’s local playhead so music, logo brightness and moving
buttons repeat together. Reduced motion
pauses visuals independently of music. Leaving or hiding the intro pauses audio.

The animation displays at 90% of the 0.8.0 size (72% of its original size).
Decoded footage is rendered on one sRGB canvas, with compression noise in the
two flat blues normalized to the sampled colours. Screenshot pixels at the
scene boundary match the page, including fades. The entire original-logo
rectangle is rebuilt from the blue background and circle, removing all baked
lettering beneath the new logo.
The selected PNG stays unchanged; rendering removes faint low-alpha halo pixels
while preserving the opaque lettering. See `desk/media/README.md` for media
storage/build details and `NOTICE.md` for source credits.
