# urSketch deployment

- Publisher: `~livbec-pitsyd-botryp-hoshec--faltec-lavtel-firrup-marzod`
- Desk and Gall agent: `%ursketch`
- Version: 0.6.0
- Runtime: Vere 4.6 / Zuse 408
- Browser route: `/apps/ursketch`
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

urSketch 0.6.0 is installed and publicly published on the comet. Docket and
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
