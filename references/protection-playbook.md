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