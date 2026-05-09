#!/usr/bin/env python3
"""
Build AssetApp_import.zip by patching the original .msapp with src/ files.
Patches only files that exist in src/, excludes checksum.json (always stale),
and validates all JSON before writing the output zip.
"""
import json, os, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, 'apps/asset-app/src')
EXPORT_APPS_DIR = os.path.join(ROOT, 'apps/asset-app/export/apps')
EXPORT = os.path.join(ROOT, 'apps/asset-app/export')
BUILD = os.path.join(ROOT, 'apps/asset-app/build')

APP_ID = os.listdir(EXPORT_APPS_DIR)[0]
EXPORT_APPS = os.path.join(EXPORT_APPS_DIR, APP_ID)
MSAPP_FILENAME = next(f for f in os.listdir(EXPORT_APPS) if f.endswith('-document.msapp'))
ORIG_MSAPP = os.path.join(EXPORT_APPS, MSAPP_FILENAME)

# Index src files
src_files = {}
for root, _, files in os.walk(SRC):
    for fname in files:
        full = os.path.join(root, fname)
        rel = os.path.relpath(full, SRC)
        src_files[rel] = full

# Patch original .msapp in memory
import io
buf = io.BytesIO()
with zipfile.ZipFile(ORIG_MSAPP, 'r') as orig, zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as out:
    orig_paths = set()
    for item in orig.infolist():
        norm = item.filename.replace('\\', '/')
        rel = norm.lstrip('/')
        orig_paths.add(rel)
        if rel == 'checksum.json':
            continue  # always omit — stale after any edit
        # Exclude old Shane Young screens replaced by new YAML-driven screens
        if rel in ('Controls/11.json', 'Controls/34.json'):
            continue
        if rel in src_files:
            with open(src_files[rel], 'rb') as f:
                out.writestr(norm, f.read())
        else:
            out.writestr(norm, orig.read(item.filename))
    # Write new src files not present in original .msapp (e.g. Src/*.pa.yaml)
    for rel, full in sorted(src_files.items()):
        if rel not in orig_paths and rel != 'checksum.json':
            with open(full, 'rb') as f:
                out.writestr(rel, f.read())

# Validate all JSON in the patched .msapp
buf.seek(0)
errors = []
with zipfile.ZipFile(buf) as chk:
    for name in chk.namelist():
        if name.endswith('.json'):
            try:
                json.loads(chk.read(name))
            except json.JSONDecodeError as e:
                errors.append(f'{name}: {e}')

if errors:
    print('JSON validation FAILED:', file=sys.stderr)
    for e in errors:
        print(f'  {e}', file=sys.stderr)
    sys.exit(1)

# Write output import zip
buf.seek(0)
msapp_data = buf.read()
pkg_prefix = f'Microsoft.PowerApps/apps/{APP_ID}/'
out_zip = os.path.join(BUILD, 'AssetApp_import.zip')

with zipfile.ZipFile(out_zip, 'w', zipfile.ZIP_DEFLATED) as zout:
    zout.write(os.path.join(EXPORT, 'manifest.json'), 'manifest.json')
    for f in os.listdir(EXPORT_APPS):
        if f.endswith('.msapp'):
            continue
        zout.write(os.path.join(EXPORT_APPS, f), pkg_prefix + f)
    zout.writestr(pkg_prefix + MSAPP_FILENAME, msapp_data)

print(f'Built {out_zip} ({os.path.getsize(out_zip):,} bytes)')
