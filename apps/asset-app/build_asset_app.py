#!/usr/bin/env python3
"""
Build AssetApp_import.zip from the export/ folder.
Same structure as AppointmentApp_import.zip:
  manifest.json + Microsoft.PowerApps/apps/{id}/ contents
"""
import os, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXPORT = os.path.join(ROOT, 'apps/asset-app/export')
BUILD = os.path.join(ROOT, 'apps/asset-app/build')
OUT = os.path.join(BUILD, 'AssetApp_import.zip')

APP_ID = os.listdir(os.path.join(EXPORT, 'apps'))[0]
APP_DIR = os.path.join(EXPORT, 'apps', APP_ID)
PKG_PREFIX = f'Microsoft.PowerApps/apps/{APP_ID}/'

os.makedirs(BUILD, exist_ok=True)

with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    zout.write(os.path.join(EXPORT, 'manifest.json'), 'manifest.json')
    for fname in os.listdir(APP_DIR):
        zout.write(os.path.join(APP_DIR, fname), PKG_PREFIX + fname)

print(f'Built {OUT} ({os.path.getsize(OUT):,} bytes)')
