# Web interaction and durable events — v2

## Scope and precedence

When this project is being operated through `$start-workflow`, this adapter
replaces chat-only question/handoff delivery in the owning skill. Its product,
artifact ownership, verification, commit, review and scope rules still apply.
A web button invokes only its named offered stage. Without an active web
session, keep the skill's normal chat behavior; do not start a server for every
standalone utility or delegated test/review.

All 24 installed skills use the same protocol. Discovery/design/setup publish
question sets; prototype skills publish pages; specification/task/implementation
skills publish progress and explicit next actions; utilities/test/review skills
report evidence to their parent, which publishes the result. Delegated workers
must not run a competing event consumer. One parent agent owns the queue.

## CLI

Use the bundled `scripts/workflow.py` with an absolute `--project` on every
command. Here `BRIDGE` means that installed script path and `PROJECT` means
the consumer's root; resolve both before executing:

```bash
python3 BRIDGE --project PROJECT state
python3 BRIDGE --project PROJECT wait --timeout 25
python3 BRIDGE --project PROJECT publish --file /absolute/path/update.json --event 1
```

`wait` returns the oldest unacknowledged event or `{"status":"timeout"}`.
It does not acknowledge on delivery. After consuming the event and persisting
owned artifacts, publish a state update with its numeric `--event` to atomically
acknowledge it. Progress updates may omit `--event`; the final response to that
input acknowledges it. Process one event at a time. On resume, inspect existing
artifacts/evidence before reapplying any side effect: delivery is at least once,
not an exactly-once guarantee for filesystem edits or external effects.

SQLite state/event history lives in `.phat-workflow/events.sqlite3` under the
consumer project, separate from canonical docs. Keep it out of commits; do not
store secrets in browser answers. Uploaded reference files use collision-free
names under `docs/ref/`, preserving the original basename. Browser mutations
are loopback-only, same-origin and require a per-server token. Browser inputs
cannot publish agent state or execute commands; only the local agent CLI can.
Local project files are trusted with the same permissions as the current user.

## Browser events

Each event includes `id`, `kind`, parsed `payload`, creation time and ack state.

- `request.submitted`: `{text, files: [relative-path], skill: "grill-workflow"}`.
- `answers.submitted`: `{questionSet, answers: {question-id: value}, skill}`.
  Checkbox values are arrays; other inputs are strings. Only accept the current
  question set; the server rejects stale revisions and validates required fields.
- `action.requested`: `{action: offered-action-id, skill: offered-skill}`.
- `prototype.feedback`: `{text, page: stable-page-id, skill: "edit-prototype"}`.

Browser POSTs carry a unique `key` for idempotent retries and the current
`revision`. The server persists the event and state in one transaction. The
browser polls state every 1.2 seconds, refreshes its same-origin session token
after server restart, and follows the server-owned route. Completion exposes
a new-workflow button; it opens the request form without discarding prior
events. A new submitted request preserves recent activity; all prior browser and agent
events remain in SQLite.

## Publishing questions

Write actual JSON with a file tool, then call `publish`. Example update:

```json
{
  "stage": "grill-workflow",
  "status": "waiting",
  "message": "ขอข้อมูลเพิ่มเพื่อกำหนดขอบเขตงาน",
  "questions": [
    {"id":"audience","type":"input","label":"ใครเป็นผู้ใช้หลัก?","required":true},
    {"id":"platform","type":"select","label":"แพลตฟอร์ม","options":["Web","Mobile"],"required":true},
    {"id":"features","type":"checkbox","label":"ความสามารถที่ต้องใช้","options":["ค้นหา","ส่งออก"]},
    {"id":"constraints","type":"textarea","label":"ข้อจำกัดหรือเงื่อนไขเพิ่มเติม"}
  ],
  "actions": []
}
```

Ask only relevant dependency-ready questions; the four types are available,
not mandatory in every round. The bridge assigns a new `questionSet` ID.
Checkbox groups with `required: true` need at least one selected option.
Publish `questions: []` when the round is finished to clear it.

## Progress, handoffs and prototype

Allowed fields: `stage` (installed skill name), `status` (`idle`, `working`,
`waiting`, `blocked`, `complete`), plain-text `message`, `questions`, `pages`,
`actions`. Routes are derived: grill skills → `/grill`; prototype skills →
`/prototype`; all other stages → `/workflow`. Initial requests start at `/`.
No arbitrary HTML is interpreted in messages, questions, labels or answers.

```json
{
  "stage":"to-prototype",
  "status":"waiting",
  "message":"ตรวจหน้า prototype และส่งคำขอแก้ไข หรือยอมรับเพื่อจัดทำ spec",
  "questions":[],
  "pages":[{"id":"UI-001","title":"หน้าหลัก","path":"docs/assets/prototype/index.html"}],
  "actions":[{"id":"accept-prototype","label":"ยอมรับและจัดทำ spec","skill":"spec-with-prototype"}]
}
```

Page paths must exist under `docs/assets/prototype/`; relative CSS/JS/assets
are served under `/preview/`. The iframe is sandboxed, scripts may run but have
no same-origin privilege, parent access, top navigation or external network.
Preview is for local HTML prototypes; backend-dependent apps need a separately
agreed integration. Never copy a baseline into the editable directory simply
to bypass the prototype revision rules.

Do not manufacture a questionnaire on submit: the agent reads context and
publishes real questions. While no agent is consuming events the UI accurately
shows a queued/working request; server connectivity is not model connectivity.
When blocked, publish the concrete remedy and question(s), await the matching
answer, and do not mark unresolved work complete.
