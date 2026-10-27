# Controlled runner evidence
1. `python3 checks/check_navigation.py` from fixture root covers four-page
navigation AC functional scope.
2. `python3 checks/check_baselines.py` from fixture root covers preservation of
accepted baseline dependencies used in visual AC verification.
These are distinct task-relevant checks; neither establishes rendered fidelity.

## Browser journey runner (b2 follow-up)

The available Codex app-browser via `mcp__cua_repl` is the host-provided journey
runner for this static fixture. No Playwright package/CLI install is required.
Use its documented browser API: discover/select the browser, read its viewport
capability documentation, set 1280×900 then 390×844, open a temporary localhost
app tab, and click the four navigation links using role/name locators. After
each click read current state and assert expected h1 and page URL. Baseline
captures are at `docs/assets/prototype-baselines/pages/b2/pageN.html` and consumer
pages at `app/pageN.html`. The test parent starts a fixture-only server at
127.0.0.1:8765; this role must not launch/install services itself. Reset viewport
and close only its created tabs after testing. The parent already recorded all
32 source/target/viewport transitions and 16 captures in `../b2-review/`.
The e2e role should independently replay the four-page navigation at both
specified viewports; saving source files or changing task status is forbidden.
Report the exact browser actions and observed assertions as the runner commands,
plus the browser availability and any limitations. A missing browser/server
blocks this runner; it must never become a pass from saved JSON alone.
