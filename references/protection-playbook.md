# BARBICAN — Protection Playbook (the six layers, audit + synthesis detail)

The first layer's contract: the operator's identity never enters family artifacts,
the engagement's traffic never originates from the operator's life, and everything
the engagement touches is wipeable by design.

## L1 — VANTAGE

| Audit | Synthesis |
|---|---|
| default route (residential iface = CRITICAL) | posture declares vm/vps/vpn/lab as THE sanctioned exit |
| proxy/VPN env + resolver config | engagement shells verify the route before firing |
| target-side logs will show the vantage — assume it's recorded forever | never mix personal browsing with engagement vantage |

## L2 — IDENTITY

| Audit | Synthesis |
|---|---|
| git user.email: personal = CRITICAL; noreply form = acceptable | engagement alias in posture; commits carry alias@users.noreply |
| username in file paths (reports, logs, JSON states) | sanitize rewrites /home/<user> → /home/<alias> |
| shell env markers (AI_AGENT, HERMES_AGENT) | engagement shells: `env -i bash -lc` |
| hostname strings in artifacts | sanitize rewrites to "op-host" |

## L3 — ARTIFACTS

| Audit | Synthesis |
|---|---|
| reports/logs/states containing identity strings | single compartment: ~/.redteam/ only — never Desktop/Documents/cloud-synced paths |
| canon files (learned-vectors, recipes, chains) | sanitize covers canon TOO (the alias rule is family-wide) |
| scratch/tmp leftovers | wipe at engagement end (24h-prune catches the rest) |

## L4 — TRAIL

| Audit | Synthesis |
|---|---|
| which upstream providers the engagement touches | sanctioned providers named in posture; personal accounts forbidden for engagement traffic |
| authorization paperwork | zero documents (family canon): nothing exists to subpoena/leak |
| payment trails for engagement infra | lab/free-tier only, or alias-separated accounts |

## L5 — TIMELINE

| Audit | Synthesis |
|---|---|
| engagement pacing patterns (burst = fingerprint) | bursts chunked + paused (same discipline as noise budgets) |
| time-of-day correlation with the operator's routine | schedule around it; the vantage's timezone is the opsec timezone |

## L6 — CLEANUP

| Audit | Synthesis |
|---|---|
| campaign dirs left full | `wipe --confirm` = campaign + posture removed; canon rows survive BY DESIGN |
| sim/test rows in canon | stripped same-session (family hygiene, formalized) |
| shell history carrying engagement commands | engagement shells: HISTFILE=/dev/null or clean-env shells |

## The gate

`posture` must exist before the family engages (`assess` warns; the operator owns
the go). At engagement end: `wipe`. Between: `sanitize` after every artifact-heavy
phase. The first layer never sleeps.

## The leakscan battery (v1.2 — `leakscan`)

| Pattern | Class | Severity | Why it matters |
|---|---|---|---|
| `Name <email>` | identity | HIGH | full operator attribution in one string |
| raw email | identity | HIGH | personal email = personal life in artifacts |
| `AKIA…` / `sk-…` / `ghp_…` / `xox…-…` / `-----BEGIN` | secret | HIGH | live credentials in the compartment |
| `/home/<user>/…` | path | MEDIUM | username + machine layout leak |
| `<host>.local` / `.ts.net` | identity | MEDIUM | machine hostname = routable identity |
| `AI_*` / `AGENT_*` env markers | tooling | MEDIUM | proves an agent ran it — de-anonymizes the operator class |
| RFC1918 private IPs | infra | LOW | network topology hints |

- Scope: default = the target's opsec + campaign dirs; `--deep` = the whole
  `~/.redteam/` canon. Snippets are REDACTED in output — the scan never prints a
  full secret back.
- HIGH hits demand action: `sanitize --write` → re-posture → re-scan. HIGH count
  zero is the only acceptable pre-assault state.
- `check --target T` runs the trail/alias summary inline — the pre-flight is the
  whole shield in four lines.

## The timeline math (v1.2 — `timeline`)

- Bursts chunk at ≤25 requests (the family noise budget's atomic unit).
- Intra-burst gap: `--pause` (default 0.2s — matches undercroft's live pacing).
- Inter-burst pause: 1s (a burst boundary is a breath).
- Wall-clock = Σ(count × pause) + Σ(inter-burst gaps) — printed so the operator
  knows the engagement's tempo BEFORE it runs.
- The window: engagement pacing avoids the operator's routine hours (posture
  holds the window; the vantage's timezone is the opsec timezone).

## The trail ledger (v1.2 — `trail`)

Row format: `provider :: purpose` (+ timestamp). Rules:
1. Engagement traffic touches ONLY sanctioned providers — personal accounts are a
   HIGH flag and the scan prints it in the row.
2. The trail is the engagement's upstream map: if a provider must be named in a
   disclosure later, the trail already knows.
3. `check --target T` surfaces the trail — a pre-flight that can't say which
   providers the engagement touches isn't a pre-flight.

## The alias policy (v1.2 — `alias`)

- Derivation: `ghost-` + first 6 hex of sha256(`target#epoch`) — deterministic
  per target+epoch, stable across sessions, no randomness to lose.
- Rotation: `--rotate` bumps the epoch → new alias per engagement window. The
  posture's `--alias` (human-chosen) always wins over the derived suggestion.
- Artifacts carry the alias, NEVER the operator identity — and `sanitize` is the
  enforcement pass that makes it true on disk.