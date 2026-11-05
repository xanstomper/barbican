<div align="center">

```

```

# 🛡️ BARBICAN

### *Nothing runs unverified. The shield goes up first — always.*

**The First Layer of the HolyShit family.** Everything below it attacks; BARBICAN
protects the one holding the gun. It synthesizes the opsec posture for each
engagement the way KAIRO synthesizes attacks: audit the exposure, classify the
risks, compile the protection plan, enforce it at engagement start **and end**.

[![Version](https://img.shields.io/badge/version-1.2.0-blueviolet?style=for-the-badge)](#the-cli)
[![Python](https://img.shields.io/badge/python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](#quickstart)
[![Platform](https://img.shields.io/badge/platform-Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)](#quickstart)
[![Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen?style=for-the-badge)](#why-its-powerful)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)
[![CI](https://github.com/xanstomper/barbican/actions/workflows/verify.yml/badge.svg)](https://github.com/xanstomper/barbican/actions/workflows/verify.yml)
[![Use](https://img.shields.io/badge/use-AUTHORIZED%20TARGETS%20ONLY-crimson?style=for-the-badge)](#the-walls-non-negotiable)

**THE FAMILY** — six siblings and the dispatcher, one click each:

[![01 3AM · the performer](https://img.shields.io/badge/01-3AM%20·%20the%20performer-8B0000?style=for-the-badge)](https://github.com/xanstomper/3am-shinjitsu)
[![02 KAIRO · the synthesizer](https://img.shields.io/badge/02-KAIRO%20·%20the%20synthesizer-6B8E23?style=for-the-badge)](https://github.com/xanstomper/kairo)
[![03 UNDERCROFT · the descent](https://img.shields.io/badge/03-UNDERCROFT%20·%20the%20descent-4B0082?style=for-the-badge)](https://github.com/xanstomper/undercroft)
[![04 HOLYSHIT · the finder](https://img.shields.io/badge/04-HOLYSHIT%20·%20the%20finder-B8860B?style=for-the-badge)](https://github.com/xanstomper/HolyShit)
[![05 SHIKI · the command](https://img.shields.io/badge/05-SHIKI%20·%20the%20command-111111?style=for-the-badge)](https://github.com/xanstomper/shiki)
[![06 SHUKAKU · the harvester](https://img.shields.io/badge/06-SHUKAKU%20·%20the%20harvester-8B4513?style=for-the-badge)](https://github.com/xanstomper/shukaku)
[![SPYDERMONKEY · the dispatcher](https://img.shields.io/badge/🕷️-SPYDERMONKEY%20·%20the%20dispatcher-blueviolet?style=for-the-badge)](https://github.com/xanstomper/spydermonkey)

[How it works](#how-it-works) · [Why it's powerful](#why-its-powerful) ·
[Quickstart](#quickstart) · [The CLI](#the-cli) · [The Walls](#the-walls-non-negotiable)

</div>

---

## What is this?

BARBICAN is the shield — mandate #0, the first layer. The family's zero-document
gate is BARBICAN doctrine made rule: **the operator's identity never enters family
artifacts** — no names, no hosts, no residential vantage, no personal trails.

```
✓ BARBICAN verify: compile · subcommands — ALL PASS
```

## How it works

### The vantage engine — the exit, verified live

```bash
$ barbican check
▸ vantage:    default via 10.0.0.1 dev wlp1s0 proto dhcp src 10.0.0.97 metric 600
▸ identity:   git=jewboy420 <jewboy420@users.noreply.github.com>
▸ compartment: ~/.redteam exists=True
```

- **exit-IP echo** (api.ipify/ifconfig): what targets actually see as your origin —
  your residential IP showing here IS the finding
- **VM inventory** (`vantage vm`): libvirt/virsh listing and launch
- **VPN inventory** (`vantage vpn`): wireguard/nmcli/tailscale
- **DNS resolver flag**: system resolver in use = engagement DNS leaks
- **HARD GATE**: a posture demanding `vm`/`vpn` fails LOUD (rc=1,
  `ENGAGEMENT GATE CLOSED`) when the required vantage isn't live.

### The six protection layers (the synthesis contract)

| # | Layer | What it owns |
|---|---|---|
| 1 | **VANTAGE** | where attacks originate — never the residential IP; VM/VPS/VPN/lab box, verified live |
| 2 | **IDENTITY** | git commit identity, hostname in paths, AI-agent env markers, username strings in artifacts → `sanitize` rewrites them to the engagement alias |
| 3 | **ARTIFACTS** | naming carries no operator strings; storage in one compartment (`~/.redteam/`); nothing in cloud-synced paths |
| 4 | **TRAIL** | sanctioned providers only; no personal accounts for engagement traffic; zero documents = nothing to leak |
| 5 | **TIMELINE** | pacing avoids routine patterns; bursts chunked per the family noise budget |
| 6 | **CLEANUP** | `wipe` removes campaign scratch and sim rows at engagement end — canon survives, sims never do |

### The lifecycle

```bash
barbican posture --target t --vantage vm --alias ghost   # synthesize + gate (required first)
barbican assess --target t                               # live exposure audit → ranked risks
barbican sanitize --target t [--write]                   # strip operator strings (dry-run default)
barbican vantage check --target t                        # the hard gate — no verified exit, rc=1
barbican wipe --target t --confirm                       # engagement-end cleanup, canon survives
```

## Why it's powerful

- **The gate is enforced, not suggested.** `shiki assault` runs `barbican vantage
  check` as step 0 — no verified exit, no engagement, rc=1 before a single packet.
  The CI proves the gate: a posture demanding a dead vantage must close rc=1.
- **It audits from the attacker's view.** `assess` checks the live default route,
  git identity, hostname leaks inside family artifacts, agent env markers, and the
  storage compartment — then ranks the risks.
- **Zero documents, by design.** No paperwork exists to leak: the recorded
  declaration is the entire gate, and BARBICAN never even asks for your real name —
  identifying the operator is its job, not its input.
- **Sanitize is a compiler pass, not a tip.** Operator strings (username, hostname,
  git identity) are rewritten to the engagement alias across every family artifact
  — dry-run by default, `--write` applies. `leakscan` is the OTHER direction: an
  11-pattern battery (git-author pairs, emails, AKIA/sk-/ghp_/xox keys, PEM blocks,
  home paths, hostnames, agent-env markers) over the artifacts, severity-ranked
  with redacted snippets — HIGH hits must be zero before an assault fires.
- **The tempo is computed, not guessed.** `timeline` chunks any request count into
  bursts of ≤25 with the pause schedule and wall-clock printed before anything fires.
- **The trail is an upstream map.** `trail` records every provider the engagement
  touches; personal-account use flags HIGH in the row — and `check --target` shows
  the whole shield (vantage · identity · compartment · trail · alias) in five lines.
- **Aliases are derived, not invented.** `alias` computes a deterministic
  `ghost-xxxxxx` per target+epoch, rotates per engagement window, and the posture's
  human alias always wins.
- **One compartment.** All family state lives under `~/.redteam/` — nothing
  family-related in cloud-synced or shared paths.
- **Zero dependencies.** Pure Python stdlib. Clone and run.

## Quickstart

```bash
git clone https://github.com/xanstomper/barbican.git
python3 barbican/scripts/barbican.py verify    # → ALL PASS
python3 barbican/scripts/barbican.py check     # your exposure, one line per layer
```

## The CLI

| Command | What it does |
|---|---|
| `assess --target T` | live exposure audit: vantage, identity, artifact leaks, env markers, compartment → ranked risks |
| `posture --target T --vantage vm\|vps\|vpn\|lab --alias A` | synthesize + store the engagement posture (required before the family runs) |
| `sanitize --target T [--write]` | strip operator-identifying strings from all family artifacts (dry-run default) |
| `leakscan --target T [--deep]` | the operator-string battery: identity/secrets/paths/hostnames, severity-ranked, redacted snippets |
| `timeline --target T --burst N [--pause S]` | the noise-budget pacing planner — burst schedule + wall-clock before anything fires |
| `trail --target T [--add "provider :: purpose"]` | the provider trail ledger — personal-account use flags HIGH |
| `alias --target T [--rotate]` | engagement alias derivation (deterministic) + per-engagement rotation |
| `check [--target T]` | fast pre-flight: vantage + identity + compartment (+ trail/alias) |
| `vantage check\|vm\|vpn [--target T] [--name X]` | exit verification + VM/VPN inventory + **the hard gate** |
| `wipe --target T --confirm` | engagement-end cleanup: campaign dir + sim rows (canon survives) |
| `verify` | self-check |

## The Walls (non-negotiable)

The zero-document gate · declared estates only · the operator's identity never
enters family artifacts · destructive end-states refused — BARBICAN attacks
nothing, and that is exactly why everything else can.

## Files

```
barbican/
├── SKILL.md                        # the doctrine
├── scripts/
│   ├── barbican.py                 # assess/posture/sanitize/check/wipe/vantage/verify
│   └── safehouse.py                # the compartment keeper
├── references/
│   └── protection-playbook.md      # the six layers' audit + synthesis details
└── templates/
    └── posture.json                # posture state starter
```

## Relations

`spydermonkey` dispatches it (always first) · `shiki` gates on it (assault step 0) ·
`holyshit-mode` inherits its vantage policy · `3am-shinjitsu` inherits its timeline
layer · `undercroft` passes its artifacts through sanitize · `kairo` ships compiled
attacks only after posture · `shukaku`'s register stays inside its compartment.

## License

[MIT](LICENSE) — shield with it, build for it, route through it.

<div align="center">

*No verified exit, no engagement. The shield goes up first.*

</div>
