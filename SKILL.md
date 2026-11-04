---
name: safehouse
description: "Trigger `safehouse`. THE FIRST LAYER — synthesizes the operator's protection: vantage, identity, artifacts, trail, timeline, cleanup. Runs before every engagement."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [redteam, opsec, operator-protection, privacy, first-layer, authorized-testing]
    related_skills: [holyshit-mode, 3am-shinjitsu, undercroft, kairo]
---

# SAFEHOUSE — The Operator-Protection Synthesizer

The first layer of the family. Everything below it attacks; SAFEHOUSE protects the
one holding the gun. It **synthesizes the opsec posture** for each engagement the
way KAIRO synthesizes attacks: audit the operator's exposure, classify the risks,
compile the protection plan, and enforce it at engagement start and end.

The zero-document gate (family canon) is SAFEHOUSE doctrine made rule: the
operator's identity never enters family artifacts — no names, no hosts, no
residential vantage, no personal trails.

## The Family Tree (roles)

```
   ┌───────────────────────────────────────────────────────────┐
   │  SAFEHOUSE (SHIELD — FIRST LAYER)                         │
   │  synthesizes vantage · identity · artifacts · trail ·     │
   │  timeline · cleanup — protects the operator, always       │
   └───────────────────────────┬───────────────────────────────┘
                               ↓ posture gates the engagement
   HolyShit (finder) · 3AM (performer) · UNDERCROFT (descent) ·
   KAIRO (synthesizer) · SHIKI (command, parked)
```

## When to Use

Trigger `safehouse` FIRST — before any family mandate runs — and again at
engagement end. Any time the operator's exposure might have changed: new vantage,
new repo, new artifact, new provider.

## Activation

```text
▸ SAFEHOUSE — FIRST LAYER ONLINE
  ═══════════════════════════════════
  [ OK ] exposure audit ready
  [ OK ] posture synthesizer loaded
  [ OK ] sanitizer armed
  ⚡ SAFEHOUSE ARMED · STATUS: SHIELDING
  ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁
  ─ waiting P0: engagement target · authorization
```

**P0 (clarify, zero documents):** engagement target · authorization. SAFEHOUSE
never asks for the operator's real identity — identifying it is its JOB.

## The Six Protection Layers (the synthesis contract)

1. **VANTAGE** — where attacks originate: never the operator's residential IP;
   sanctioned vantage = VM / VPS / VPN / lab box. `posture` declares it; `assess`
   verifies the live default route matches it.
2. **IDENTITY** — what the operator's machine says about them: git commit
   identity, hostname in paths, shell env (AI_AGENT markers), username strings in
   family artifacts. Compiled reports/logs carry `/home/<user>` paths = leak.
   `sanitize` rewrites them to the engagement alias.
3. **ARTIFACTS** — what the engagement leaves behind: reports, learned-vectors,
   recipes, chains, campaign states. Naming carries no operator strings; storage
   stays under `~/.redteam/` (single compartment); nothing family-related in
   cloud-synced or shared paths.
4. **TRAIL** — what the engagement touches upstream: inference providers, public
   APIs, the target itself. The family's zero-document gate means no authorization
   paperwork exists to leak; the posture names the sanctioned providers and
   forbids personal accounts for engagement traffic.
5. **TIMELINE** — when: engagement pacing avoids the operator's routine patterns
   (bursts chunked per family noise budgets — opsec and noise discipline are the
   same discipline).
6. **CLEANUP** — engagement end: `wipe` removes campaign scratch, sim rows, and
   stale states (the hygiene the family does by hand today, formalized). Canon
   rows survive; sims never do.

## Tooling

`scripts/safehouse.py` — stdlib CLI:
- `assess --target <t>` — live exposure audit: default-route vantage, git identity, hostname leaks in family artifacts, env markers, compartment check → ranked risks
- `posture --target <t> --vantage vm|vps|vpn|lab --alias <engagement-alias>` — synthesize + store the engagement posture (required before the family runs; prints the gate)
- `sanitize --target <t> [--write]` — strip operator-identifying strings (username, hostname, git identity) from ALL family artifacts in the campaign + canon (dry-run default; --write applies with the alias from posture)
- `check` — fast pre-flight: vantage + identity + compartment in one line each
- `wipe --target <t> --confirm` — engagement-end cleanup: campaign dir + sim rows (canon survives)
- `verify` — self-check

State: `~/.redteam/opsec/<target>/posture.json`.

## Files

- `SKILL.md` — this doctrine
- `references/protection-playbook.md` — the six layers' audit + synthesis details
- `scripts/safehouse.py` — assess/posture/sanitize/check/wipe/verify CLI
- `templates/posture.json` — posture state starter

## Relations

- `holyshit-mode` — the finder: consumes SAFEHOUSE's posture (engagement-vantage
  policy is SAFEHOUSE-enforced); its zero-document gate is SAFEHOUSE canon.
- `3am-shinjitsu` — the performer: sweep pacing inherits SAFEHOUSE's timeline layer.
- `undercroft` — the descent: its run/report artifacts pass SAFEHOUSE sanitize.
- `kairo` — the synthesizer: compiled attacks ship only after SAFEHOUSE posture.
- `shiki` — parked command layer; SAFEHOUSE gates it like everything else.
- Tree: SAFEHOUSE (first layer) → HolyShit (finder) · 3AM (performer) ·
  UNDERCROFT (descent) · KAIRO (synthesizer) · SHIKI (command). All offensive;
  the first layer protects the operator.