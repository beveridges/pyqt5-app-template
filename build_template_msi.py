#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Application Template — MSI + Portable ZIP Builder
--------------------------------------------------------------------------------
✓ Builds MSI installer via WiX Toolset (per-user)
✓ Archives .msi and .zip to Documents/.builds/<app>/msi/builds/
✓ Uses same versioning as build_template.py
✓ Auto-generates UpgradeCode (GUID) on first run
================================================================================
"""

import os, sys, shutil, subprocess, re, uuid
from pathlib import Path
from datetime import datetime
from utilities.path_utils import base_path

# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------
APP_NAME = "MyAppTemplate"
ICON_PATH = Path(base_path("resources/icons", "app.ico")).resolve()
PYI_BUILD_DIR = Path.home() / "Documents" / ".builds" / APP_NAME.lower() / "pyinstaller"
DIST_DIR = PYI_BUILD_DIR / "dist" / APP_NAME
MSI_ROOT = Path.home() / "Documents" / ".builds" / APP_NAME.lower() / "msi"
MSI_BUILDS = MSI_ROOT / "builds"
MSI_ROOT.mkdir(parents=True, exist_ok=True)
MSI_BUILDS.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------------------
# Versioning — read from utilities/version_info.py
# ------------------------------------------------------------------------------
VERSION_INFO = Path(base_path("utilities", "version_info.py"))
if not VERSION_INFO.exists():
    print("[ERROR] version_info.py not found. Run build_template.py first.")
    sys.exit(1)

BUILDNUMBER = "unknown"
for line in VERSION_INFO.read_text(encoding="utf-8").splitlines():
    if line.startswith("BUILDNUMBER"):
        BUILDNUMBER = line.split("=")[1].strip().strip('"')
        break

# --- Convert to WiX-safe version (integers only) ---
def to_wix_version(v: str) -> str:
    nums = re.findall(r"\d+", v)
    nums = (nums + ["0", "0", "0", "0"])[:4]
    return ".".join(nums)

WIX_VERSION = to_wix_version(BUILDNUMBER)
print(f"[OK] Using build number: {BUILDNUMBER}")
print(f"[OK] Converted WiX-safe version: {WIX_VERSION}")

# ------------------------------------------------------------------------------
# Locate the EXE
# ------------------------------------------------------------------------------
EXE_PATH = DIST_DIR / f"{APP_NAME}.exe"
if not EXE_PATH.exists():
    print(f"[ERROR] Missing EXE at: {EXE_PATH}")
    sys.exit(1)

# ------------------------------------------------------------------------------
# Generate or reuse UpgradeCode GUID
# ------------------------------------------------------------------------------
GUID_FILE = MSI_ROOT / "upgradecode.txt"
if GUID_FILE.exists():
    UPGRADE_CODE = GUID_FILE.read_text(encoding="utf-8").strip()
else:
    UPGRADE_CODE = str(uuid.uuid4())
    GUID_FILE.write_text(UPGRADE_CODE, encoding="utf-8")
print(f"[OK] Using UpgradeCode: {UPGRADE_CODE}")

# ------------------------------------------------------------------------------
# Generate .wxs file for WiX
# ------------------------------------------------------------------------------
WXS_PATH = MSI_ROOT / f"{APP_NAME}.wxs"
wxs_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Product Id="*" Name="{APP_NAME}" Language="1033" Version="{WIX_VERSION}"
           Manufacturer="Moviolabs" UpgradeCode="{UPGRADE_CODE}">
    <Package InstallerVersion="500" Compressed="yes" InstallScope="perUser" />

    <MediaTemplate />
    <Icon Id="AppIcon.ico" SourceFile="{ICON_PATH}" />
    <Property Id="ARPPRODUCTICON" Value="AppIcon.ico" />

    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="ProgramFilesFolder">
        <Directory Id="INSTALLFOLDER" Name="{APP_NAME}" />
      </Directory>
      <Directory Id="ProgramMenuFolder" />
      <Directory Id="DesktopFolder" />
    </Directory>

    <DirectoryRef Id="INSTALLFOLDER">

      <!-- 1️⃣ Main executable -->
      <Component Id="MainExecutable" Guid="*">
        <File Id="AppEXE" Source="{EXE_PATH}" KeyPath="yes" />
      </Component>

      <!-- 2️⃣ Registry marker for uninstall tracking -->
      <Component Id="RegistryMarker" Guid="*">
        <RegistryKey Root="HKCU" Key="Software\\{APP_NAME}"
                     ForceCreateOnInstall="yes" ForceDeleteOnUninstall="yes">
          <RegistryValue Name="Installed" Type="integer" Value="1" KeyPath="yes" />
        </RegistryKey>
      </Component>

      <!-- 3️⃣ Shortcuts, using registry as KeyPath -->
      <Component Id="UserShortcuts" Guid="*">
        <RegistryKey Root="HKCU" Key="Software\\{APP_NAME}\\Shortcuts"
                     ForceCreateOnInstall="yes" ForceDeleteOnUninstall="yes">
          <RegistryValue Name="Created" Type="integer" Value="1" KeyPath="yes" />
        </RegistryKey>

        <Shortcut Id="DesktopShortcut" Directory="DesktopFolder"
                  Name="{APP_NAME}" Target="[INSTALLFOLDER]{APP_NAME}.exe"
                  Icon="AppIcon.ico" IconIndex="0" Advertise="no" />
        <Shortcut Id="StartMenuShortcut" Directory="ProgramMenuFolder"
                  Name="{APP_NAME}" Target="[INSTALLFOLDER]{APP_NAME}.exe"
                  Icon="AppIcon.ico" IconIndex="0" Advertise="no" />

        <RemoveFile Id="RemoveShortcutDesktop" Name="{APP_NAME}.lnk"
                    On="uninstall" Directory="DesktopFolder" />
        <RemoveFile Id="RemoveShortcutMenu" Name="{APP_NAME}.lnk"
                    On="uninstall" Directory="ProgramMenuFolder" />
        <RemoveFolder Id="RemoveStartMenuFolder" Directory="ProgramMenuFolder" On="uninstall" />
      </Component>

    </DirectoryRef>

    <Feature Id="DefaultFeature" Level="1">
      <ComponentRef Id="MainExecutable" />
      <ComponentRef Id="RegistryMarker" />
      <ComponentRef Id="UserShortcuts" />
    </Feature>

    <UIRef Id="WixUI_InstallDir" />
    <Property Id="WIXUI_INSTALLDIR" Value="INSTALLFOLDER" />
  </Product>
</Wix>
"""

WXS_PATH.write_text(wxs_content, encoding="utf-8")
print(f"[OK] WXS file created at: {WXS_PATH}")

# ------------------------------------------------------------------------------
# Run WiX (candle + light)
# ------------------------------------------------------------------------------
os.chdir(MSI_ROOT)
try:
    subprocess.run(["candle", f"{APP_NAME}.wxs"], check=True)
    msi_path = MSI_BUILDS / f"{APP_NAME}-{BUILDNUMBER}.msi"
    subprocess.run([
        "light", "-ext", "WixUIExtension",
        f"{APP_NAME}.wixobj", "-o", str(msi_path)
    ], check=True)
    print(f"\n✅ MSI created: {msi_path}")
except subprocess.CalledProcessError as e:
    print(f"[ERROR] WiX build failed: {e}")
    sys.exit(1)

# ------------------------------------------------------------------------------
# Create portable ZIP (from dist folder)
# ------------------------------------------------------------------------------
ZIP_PATH = MSI_BUILDS / f"{APP_NAME}-{BUILDNUMBER}-portable.zip"
if DIST_DIR.exists():
    print(f"[OK] Creating portable ZIP: {ZIP_PATH.name}")
    shutil.make_archive(str(ZIP_PATH).replace(".zip", ""), "zip", root_dir=DIST_DIR)
    print(f"✅ Portable ZIP created at: {ZIP_PATH}")
else:
    print("[WARN] No dist folder found to zip.")

# ------------------------------------------------------------------------------
# Purge old builds (keep 3 latest)
# ------------------------------------------------------------------------------
def purge_old_builds(build_dir: Path, keep: int = 3):
    builds = sorted(build_dir.glob(f"{APP_NAME}-*"), key=lambda p: p.stat().st_mtime, reverse=True)
    for old in builds[keep:]:
        if old.is_file():
            old.unlink()
            print(f"[purged] {old}")

purge_old_builds(MSI_BUILDS, keep=3)
print("\n🎉 All done — MSI + ZIP ready!")
