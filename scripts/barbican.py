#!/usr/bin/env python3
"""
BARBICAN — the first layer: operator-protection synthesizer. stdlib-only.

Commands:
  assess   --target <t>                 live exposure audit → ranked risks
  posture  --target <t> --vantage vm|vps|vpn|lab --alias <alias>
                                        synthesize + store the engagement posture
  sanitize --target <t> [--write]       strip operator-identifying strings from
                                        family artifacts (dry-run default)
  check                                  fast pre-flight (vantage/identity/compartment)
  wipe     --target <t> --confirm       engagement-end cleanup (canon survives)
  verify                                self-check

State: ~/.redteam/opsec/<target>/posture.json
Exit codes: 0 ok · 2 usage/state error.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

VANTAGES = ("vm", "vps", "vpn", "lab")
OPSEC_DIR = Path.home() / ".redteam" / "opsec"
CAMP_DIR = Path.home() / ".redteam" / "campaigns"
CANON_FILES = [Path.home() / ".redteam" / "learned-vectors.jsonl",
               Path.home() / ".redteam" / "synthesized-recipes.md",
               Path.home() / ".redteam" / "synthesized-chains.jsonl"]


def posture_path(t):
    return OPSEC_DIR / t / "posture.json"


def load_posture(t):
    p = posture_path(t)
    if p.exists():
        try:
            return json.loads(p.read_text())
        except Exception:
            return None
    return None


def save_posture(t, st):
    p = posture_path(t)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(st, indent=2) + "\n")


def _git_identity():
    try:
        name = subprocess.run(["git", "config", "--global", "user.name"],
                              capture_output=True, text=True).stdout.strip()
        email = subprocess.run(["git", "config", "--global", "user.email"],
                               capture_output=True, text=True).stdout.strip()
        return name, email
    except Exception:
        return "", ""


def _default_route():
    try:
        r = subprocess.run(["ip", "route", "show", "default"],
                           capture_output=True, text=True).stdout.strip()
        return r[:120]
    except Exception:
        return "?"


def _identity_strings():
    """The operator's identifying strings, harvested locally (never sent anywhere)."""
    name, email = _git_identity()
    strs = set()
    if name:
        strs.add(name)
    if email:
        strs.add(email.split("@")[0])  # local part leaks via paths/commits
        if "noreply" not in email:
            strs.add(email)  # full personal email = worst leak
    strs.add(Path.home().name)  # username in paths
    return {s for s in strs if len(s) >= 3}


def _family_artifacts():
    files = list(CANON_FILES)
    if CAMP_DIR.exists():
        files += [p for p in CAMP_DIR.rglob("*") if p.is_file()]
    return files


def cmd_assess(args):
    risks = []
    name, email = _git_identity()
    if email and "noreply" not in email:
        risks.append(("CRITICAL", f"git identity is a personal email: {email} — every commit leaks it",
                      "posture --alias <new> + git config user.email <alias>@users.noreply.github.com"))
    elif email:
        risks.append(("LOW", f"git identity uses noreply form ({email}) — acceptable",
                      "keep it"))
    user = Path.home().name
    hits = 0
    checked = 0
    for f in _family_artifacts():
        try:
            if f.stat().st_size > 2_000_000:
                continue
            text = f.read_text(errors="replace")
            checked += 1
            if user in text:
                hits += 1
        except Exception:
            continue
    if hits:
        risks.append(("HIGH", f"{hits}/{checked} family artifact(s) contain the username string '{user}'",
                      "sanitize --target <t> --write (rewrites to the engagement alias)"))
    route = _default_route()
    risks.append(("INFO", f"default vantage route: {route}", "posture --vantage declares the sanctioned exit"))
    env_marks = [k for k in ("AI_AGENT", "HERMES_AGENT") if k in __import__("os").environ]
    if env_marks:
        risks.append(("MEDIUM", f"agent env markers active in shells: {env_marks} — engagement shells should strip them",
                      "run engagements from a clean env: env -i bash -lc"))
    camp = CAMP_DIR / args.target
    if camp.exists():
        n = len([p for p in camp.rglob("*") if p.is_file()])
        risks.append(("MEDIUM", f"campaign dir holds {n} artifact file(s) — wipe at engagement end",
                      "wipe --target <t> --confirm"))
    print(f"═══ BARBICAN ASSESS — {args.target} ═══")
    order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}
    for sev, msg, fix in sorted(risks, key=lambda r: order[r[0]]):
        print(f"  [{sev:8s}] {msg}")
        print(f"      fix: {fix}")
    save_posture(args.target, load_posture(args.target) or {
        "target": args.target, "created": datetime.now(timezone.utc).isoformat(),
        "last_assess": datetime.now(timezone.utc).isoformat(), "risks": len(risks)})
    return 0


def cmd_posture(args):
    if args.vantage not in VANTAGES:
        print(f"✗ vantage {VANTAGES}", file=sys.stderr)
        return 2
    st = {"target": args.target, "vantage": args.vantage, "alias": args.alias,
          "rules": [
              "all engagement traffic originates from the sanctioned vantage (never residential)",
              f"all family artifacts carry the alias '{args.alias}' — never the operator identity",
              "zero documents: no authorization paperwork requested, stored, or transmitted",
              "pacing inherits the family noise budget (bursts chunked, pauses honored)",
              "engagement shells run clean (no agent env markers)",
              "wipe at engagement end; canon rows survive, sims never do"],
          "created": datetime.now(timezone.utc).isoformat()}
    save_posture(args.target, st)
    print(f"▸ POSTURE SYNTHESIZED — {args.target}")
    print(f"  vantage: {args.vantage} · alias: {args.alias}")
    for r in st["rules"]:
        print(f"  rule: {r}")
    print("  ⚡ posture stored — the family may engage under this shield")
    return 0


def cmd_sanitize(args):
    st = load_posture(args.target)
    alias = (st or {}).get("alias") or "operator"
    user = Path.home().name
    _, email = _git_identity()
    patterns = {user: alias}
    if email:
        patterns[email] = f"{alias}@users.noreply.github.com"
        patterns[email.split("@")[0]] = alias
    hits = []
    for f in _family_artifacts():
        try:
            if f.stat().st_size > 2_000_000:
                continue
            text = f.read_text(errors="replace")
        except Exception:
            continue
        n = sum(text.count(k) for k in patterns)
        if n:
            hits.append((f, n, text))
    print(f"▸ sanitize scan: {len(hits)} file(s) with operator-identifying strings")
    for f, n, _ in hits[:15]:
        print(f"  {n:4d}× {f}")
    if args.write:
        for f, n, text in hits:
            new = text
            for k, v in patterns.items():
                new = new.replace(k, v)
            f.write_text(new)
        print(f"▸ wrote sanitized versions ({alias} substituted) — {len(hits)} file(s)")
    else:
        print("  (dry run — --write applies; alias from posture or 'operator')")
    return 0


def cmd_check(args):
    name, email = _git_identity()
    route = _default_route()
    compartment = CAMP_DIR.exists()
    print(f"▸ vantage:    {route}")
    print(f"▸ identity:   git={name} <{email or 'unset'}>")
    print(f"▸ compartment: ~/.redteam exists={compartment}")
    if email and "noreply" not in email:
        print("  ! personal email in git identity — see assess")
    return 0


def cmd_wipe(args):
    if not args.confirm:
        print("✗ wipe needs --confirm (canon survives, campaigns go)", file=sys.stderr)
        return 2
    camp = CAMP_DIR / args.target
    if camp.exists():
        n = len([p for p in camp.rglob("*") if p.is_file()])
        shutil.rmtree(camp)
        print(f"▸ wiped campaign: {camp} ({n} artifact files)")
    else:
        print("· no campaign dir")
    pp = posture_path(args.target)
    if pp.exists():
        pp.unlink()
        print(f"▸ posture removed: {pp}")
    print("▸ engagement closed — canon rows untouched by design")
    return 0


def cmd_verify(args):
    bad = []
    self = Path(__file__).resolve()
    if subprocess.run([sys.executable, "-m", "py_compile", str(self)],
                      capture_output=True).returncode != 0:
        bad.append("compile")
    help_out = subprocess.run([sys.executable, str(self), "--help"],
                              capture_output=True, text=True).stdout
    for want in ("assess", "posture", "sanitize", "check", "wipe", "verify", "vantage"):
        if want not in help_out:
            bad.append(f"subcommand {want}")
    if bad:
        print(f"✗ BARBICAN verify FAILED: {bad}")
        return 1
    print("✓ BARBICAN verify: compile · subcommands — ALL PASS")
    return 0


# ── v1.1.0 the vantage engine: exit verification · VMs · VPNs · hard gates ───

def _exit_ip():
    """What the target-side world sees as this machine's origin. Only called on demand."""
    import urllib.request
    for svc in ("https://api.ipify.org", "https://ifconfig.me/ip"):
        try:
            with urllib.request.urlopen(svc, timeout=6) as r:
                return r.read().decode().strip()
        except Exception:
            continue
    return None


def _vms():
    """Inventory VMs (libvirt + gnome-boxes images)."""
    out = {"running": [], "stopped": [], "tool": None}
    try:
        r = subprocess.run(["virsh", "list", "--all"], capture_output=True, text=True, timeout=10)
        if r.returncode == 0:
            out["tool"] = "libvirt"
            for line in r.stdout.splitlines()[2:]:
                parts = line.split()
                if len(parts) >= 3:
                    (out["running"] if parts[2] == "running" else out["stopped"]).append(parts[1])
    except Exception:
        pass
    return out


def _vpns():
    """Inventory VPN interfaces (wireguard + nmcli + tailscale)."""
    out = {"wg": [], "nmcli": [], "tailscale": None}
    try:
        r = subprocess.run(["wg", "show"], capture_output=True, text=True, timeout=5)
        if r.returncode == 0 and r.stdout.strip():
            out["wg"] = [l.split(":")[0].strip() for l in r.stdout.splitlines() if "interface" in l]
    except Exception:
        pass
    try:
        r = subprocess.run(["nmcli", "-t", "-f", "NAME,TYPE,DEVICE", "con", "show"],
                           capture_output=True, text=True, timeout=10)
        for line in r.stdout.splitlines():
            parts = line.split(":")
            if len(parts) >= 3 and parts[1] in ("vpn", "wireguard") and parts[2]:
                out["nmcli"].append(f"{parts[0]} ({parts[1]})")
    except Exception:
        pass
    try:
        r = subprocess.run(["tailscale", "status", "--json"], capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            out["tailscale"] = json.loads(r.stdout).get("Self", {}).get("Online")
    except Exception:
        pass
    return out


def cmd_vantage(args):
    """Verify/deploy the exit: exit-IP echo, VM inventory, VPN inventory, gate check."""
    if args.action == "check":
        ip = _exit_ip()
        print(f"▸ exit IP (what targets see): {ip or 'UNREACHABLE — no external egress?'}")
        r = _default_route()
        print(f"  default route: {r}")
        dns = Path("/etc/resolv.conf")
        if dns.exists():
            ns = [l.split()[1] for l in dns.read_text().splitlines()
                  if l.startswith("nameserver")]
            print(f"  DNS resolvers: {ns[:3]}" +
                  ("  ! system resolver — engagement DNS should route via the vantage" if ns else ""))
        vms = _vms()
        print(f"  VMs ({vms['tool'] or 'no libvirt'}): running={vms['running'] or '—'} stopped={vms['stopped'] or '—'}")
        vpns = _vpns()
        print(f"  VPNs: wg={vpns['wg'] or '—'} nmcli={vpns['nmcli'] or '—'} tailscale={'online' if vpns['tailscale'] else '—'}")
        st = load_posture(args.target) if args.target else None
        if st:
            v = st.get("vantage")
            ok = True
            if v == "vm":
                vm = st.get("vm")
                ok = vm in vms["running"]
                print(f"  GATE: posture demands VM '{vm}' → {'✓ RUNNING' if ok else '✗ NOT RUNNING — engagement BLOCKED'}")
            elif v == "vpn":
                ok = bool(vpns["wg"] or vpns["nmcli"] or vpns["tailscale"])
                print(f"  GATE: posture demands VPN → {'✓ UP' if ok else '✗ NO VPN UP — engagement BLOCKED'}")
            elif v in ("vps", "lab"):
                print(f"  GATE: posture demands {v} — operator confirms the engagement runs there (assess checks route)")
            if not ok:
                print("  ═══ ENGAGEMENT GATE CLOSED — fix the vantage or re-posture ═══")
                return 1
        return 0
    if args.action == "vm":
        vms = _vms()
        if args.name:
            if not vms["tool"]:
                print("✗ no libvirt tooling — install virt-manager/virsh or use --vantage vpn", file=sys.stderr)
                return 2
            r = subprocess.run(["virsh", "start", args.name], capture_output=True, text=True)
            print("▸ VM start:", (r.stdout or r.stderr).strip()[:100])
            return 0
        print(f"▸ VMs: running={vms['running'] or '—'} stopped={vms['stopped'] or '—'} (tool: {vms['tool'] or 'none'})")
        return 0
    if args.action == "vpn":
        vpns = _vpns()
        print(f"▸ VPNs: wg={vpns['wg'] or '—'} nmcli={vpns['nmcli'] or '—'} tailscale={'online' if vpns['tailscale'] else '—'}")
        if args.name:
            try:
                r = subprocess.run(["nmcli", "con", "up", args.name], capture_output=True, text=True, timeout=30)
                print("▸ VPN up:", (r.stdout or r.stderr).strip()[:100])
            except Exception as e:
                print(f"✗ vpn up failed: {e}", file=sys.stderr)
                return 2
        return 0
    return 2


def main():
    ap = argparse.ArgumentParser(description="BARBICAN — operator-protection synthesizer (first layer)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("assess", help="live exposure audit → ranked risks")
    a.add_argument("--target", required=True)
    p = sub.add_parser("posture", help="synthesize + store the engagement posture")
    p.add_argument("--target", required=True)
    p.add_argument("--vantage", required=True, choices=VANTAGES)
    p.add_argument("--alias", required=True)
    s = sub.add_parser("sanitize", help="strip operator strings from family artifacts")
    s.add_argument("--target", required=True)
    s.add_argument("--write", action="store_true")
    c = sub.add_parser("check", help="fast pre-flight")
    w = sub.add_parser("wipe", help="engagement-end cleanup")
    w.add_argument("--target", required=True)
    w.add_argument("--confirm", action="store_true")
    vf = sub.add_parser("verify", help="self-check")
    vt = sub.add_parser("vantage", help="exit verification: IP echo · VMs · VPNs · gate check")
    vt.add_argument("action", choices=["check", "vm", "vpn"])
    vt.add_argument("--target", help="enforce this posture's gate")
    vt.add_argument("--name", help="VM/VPN name to start")
    a2 = ap.parse_args()
    if a2.cmd == "assess":
        return cmd_assess(a2)
    if a2.cmd == "posture":
        return cmd_posture(a2)
    if a2.cmd == "sanitize":
        return cmd_sanitize(a2)
    if a2.cmd == "check":
        return cmd_check(a2)
    if a2.cmd == "wipe":
        return cmd_wipe(a2)
    if a2.cmd == "verify":
        return cmd_verify(a2)
    if a2.cmd == "vantage":
        return cmd_vantage(a2)
    return 2


if __name__ == "__main__":
    sys.exit(main())