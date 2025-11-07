#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
MyApp Template — PyInstaller Build Script (Bernstein-style)
--------------------------------------------------------------------------------
Builds and archives PyInstaller output:
✓ Safe (no recursion)
✓ Versioned builds (YY.MM-channel.seq)
✓ Archives last N builds
✓ Git tag and commit tracking
================================================================================
"""

from __future__ import annotations
import argparse, os, re, shutil, subprocess, sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

# ------------------------------------------------------------------------------
# 1. Disable UPX by default
# ------------------------------------------------------------------------------
os.environ["PYINSTALLER_NOUPX"] = "1"
os.environ["UPX"] = "disabled"

try:
    from PyInstaller.__main__ import run as pyinstaller_run
except ImportError:
    print("PyInstaller not installed. Run: pip install pyinstaller")
    sys.exit(1)


# ------------------------------------------------------------------------------
# 2. Git helpers
# ------------------------------------------------------------------------------
def _run_git(args: list[str]) -> Optional[str]:
    try:
        return subprocess.run(["git"] + args, check=True, capture_output=True, text=True).stdout.strip()
    except Exception:
        return None

def in_git_repo() -> bool:
    return _run_git(["rev-parse", "--is-inside-work-tree"]) == "true"

def git_rev_head(short: int = 7) -> str:
    return _run_git(["rev-parse", f"--short={short}", "HEAD"]) or "unknown"

def git_latest_tag() -> str:
    return _run_git(["describe", "--tags", "--abbrev=0"]) or ""


# ------------------------------------------------------------------------------
# 3. Version helpers
# ------------------------------------------------------------------------------
def read_previous_from_file(repo_root: Path) -> Tuple[Optional[str], Optional[str]]:
    vi = repo_root / "utilities" / "version_info.py"
    if not vi.exists():
        return None, None
    text = vi.read_text(encoding="utf-8", errors="ignore")
    m_build = re.search(r'BUILDNUMBER\s*=\s*"([^"]+)"', text)
    m_ver   = re.search(r'VERSIONNUMBER\s*=\s*"([^"]+)"', text)
    return (
        m_build.group(1) if m_build else None,
        m_ver.group(1) if m_ver else None,
    )

def increment_last_segment(prev_build: str) -> str:
    parts = prev_build.split(".")
    if not parts: 
        return "00"
    last = parts[-1]
    return f"{int(last) + 1:0{len(last)}d}" if last.isdigit() else "00"


# ------------------------------------------------------------------------------
# 4. Archiving helpers
# ------------------------------------------------------------------------------
def archive_latest(distpath: Path, builds_dir: Path, tag: str, app_name: str | None = None) -> Optional[Path]:
    if not distpath.exists():
        print("[error] dist folder missing.")
        return None
    candidates = [p for p in distpath.iterdir()]
    if not candidates:
        print("[warn] nothing to archive.")
        return None
    latest = max(candidates, key=lambda p: p.stat().st_mtime)
    dest_root = builds_dir / tag
    shutil.rmtree(dest_root, ignore_errors=True)
    dest_root.mkdir(parents=True, exist_ok=True)

    if latest.is_dir():
        shutil.copytree(latest, dest_root, dirs_exist_ok=True)
    else:
        shutil.copy2(latest, dest_root / latest.name)
    return dest_root


def purge_old_archives(builds_dir: Path, keep: int = 3):
    if not builds_dir.exists():
        return
    dirs = sorted(builds_dir.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)
    for p in dirs[keep:]:
        shutil.rmtree(p, ignore_errors=True)
        print(f"[purged] {p}")


# ------------------------------------------------------------------------------
# 5. Main build
# ------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Build MyApp Template via PyInstaller")
    ap.add_argument("--onefile", action="store_true", help="Build single-file exe")
    ap.add_argument("--purge", action="store_true", help="Clear dist/work dirs first")
    ap.add_argument("--keep", type=int, default=3, help="Archived builds to keep")
    ap.add_argument("--channel", default="alpha.01", help="Version channel (alpha/beta/release)")
    ap.add_argument("--upx", action="store_true", help="Enable UPX explicitly")
    args = ap.parse_args()

    project_root = Path(__file__).resolve().parent
    entry_script = project_root / "main.py"
    app_name = "MyAppTemplate"

    if not entry_script.exists():
        print(f"[error] Missing entry script: {entry_script}")
        sys.exit(2)

    # --- versioning ---
    base = datetime.now().strftime("%y.%m")
    VERSIONNUMBER = f"{base}-{args.channel}"

    prev_build, prev_version = read_previous_from_file(project_root)
    SEQ = increment_last_segment(prev_build) if prev_build and prev_version == VERSIONNUMBER else "00"
    BUILDNUMBER = f"{VERSIONNUMBER}.{SEQ}"

    GITREVHEAD = git_rev_head() if in_git_repo() else "unknown"
    GITTAG = git_latest_tag() if in_git_repo() else ""

    FRIENDLYVERSIONNAME = "MyApp Template"
    CONDAENVIRONMENTNAME = os.environ.get("CONDA_DEFAULT_ENV", "unknown")
    PYTHONVERSION = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    CONDAENVIRONMENTFILENAME = "environment.yml"

    version_py = project_root / "utilities" / "version_info.py"
    version_py.parent.mkdir(parents=True, exist_ok=True)
    version_py.write_text(f'''# Auto-generated by build_template.py
BUILDNUMBER = "{BUILDNUMBER}"
VERSIONNUMBER = "{VERSIONNUMBER}"
VERSIONNAME = "Template Build"
FRIENDLYVERSIONNAME = "{FRIENDLYVERSIONNAME}"
GITREVHEAD = "{GITREVHEAD}"
GITTAG = "{GITTAG}"
CONDAENVIRONMENTNAME = "{CONDAENVIRONMENTNAME}"
PYTHONVERSION = "{PYTHONVERSION}"
CONDAENVIRONMENTFILENAME = "{CONDAENVIRONMENTFILENAME}"
''', encoding="utf-8")

    print(f"\nBuilding {FRIENDLYVERSIONNAME}")
    print(f"VERSIONNUMBER = {VERSIONNUMBER}")
    print(f"BUILDNUMBER   = {BUILDNUMBER}")
    print(f"GITREVHEAD    = {GITREVHEAD}")
    print(f"GITTAG        = {GITTAG}")

    # --- PyInstaller setup ---
    base_build = Path.home() / "Documents" / ".builds" / app_name.lower() / "pyinstaller"
    workpath = base_build / "work"
    distpath = base_build / "dist"
    specpath = base_build
    builds_dir = base_build / "builds"

    if args.purge:
        shutil.rmtree(workpath, ignore_errors=True)
        shutil.rmtree(distpath, ignore_errors=True)
        print("[purged] previous dist/work")

    for p in (workpath, distpath, builds_dir):
        p.mkdir(parents=True, exist_ok=True)

    datasep = ";" if os.name == "nt" else ":"
    args_pi = [
        "--noconfirm", "--clean", "--console",
        f"--name={app_name}",
        f"--workpath={workpath}",
        f"--distpath={distpath}",
        f"--specpath={specpath}",
        "--onefile" if args.onefile else "--onedir",
        str(entry_script)
    ]

    # --- include resources ---
    data_dirs = [
        ("config", "config"),
        ("uis", "uis"),
        ("docs_site", "docs_site"),
        ("resources", "resources"),
        ("utilities", "utilities"),
        ("processors", "processors"),
    ]
    for src, dest in data_dirs:
        src_path = project_root / src
        if src_path.exists():
            args_pi.append(f"--add-data={src_path}{datasep}{dest}")

    icon_path = project_root / "resources" / "icons" / "app.ico"
    if icon_path.exists():
        args_pi.append(f"--icon={icon_path}")

    # --- run PyInstaller ---
    print("\n[PyInstaller] Running command:\n", " ".join(args_pi))
    pyinstaller_run(args_pi)

    # --- archive result ---
    tag = f"{app_name}-{BUILDNUMBER}"
    archived_at = archive_latest(distpath, builds_dir, tag, app_name)
    if archived_at:
        purge_old_archives(builds_dir, keep=args.keep)
        print(f"\n✅ Done — Build archived at: {archived_at}")
    else:
        print("[warn] Nothing archived (no dist found)")


if __name__ == "__main__":
    if getattr(sys, "frozen", False):
        print("[SAFEGUARD] Refusing to rebuild from a frozen EXE.")
        sys.exit(0)
    main()



