#!/usr/bin/env python3
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / 'Overwrite' / 'Overwrite-smart-bypass-LGBM.conf'
DST = ROOT / 'Overwrite' / 'Overwrite-smart-bypass-LGBM-ipv6.conf'

text = SRC.read_text(encoding='utf-8')

owner = 'violin321'
repo = 'OpenClash_Overwrite'
try:
    origin = subprocess.check_output(
        ['git', 'config', '--get', 'remote.origin.url'],
        cwd=ROOT,
        text=True,
    ).strip()
    m = re.search(r'github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?$', origin)
    if m:
        owner = m.group('owner')
        repo = m.group('repo')
except Exception:
    pass

replacements = [
    (r'(?m)^IPV6_ENABLE\s*=\s*.*$', 'IPV6_ENABLE = 1'),
    (r'(?m)^IPV6_DNS\s*=\s*.*$', 'IPV6_DNS = 1'),
    (r'(?m)^#\s*IPV6_MODE\s*\(.*$', 'IPV6_MODE = 0'),
    (r'(?m)^#\s*ENABLE_V6_UDP_PROXY\s*\(.*$', 'ENABLE_V6_UDP_PROXY = 1'),
    (r'(?m)^#\s*CHINA_IP6_ROUTE\s*\(.*$', 'CHINA_IP6_ROUTE = 1'),
]

for pattern, replacement in replacements:
    new_text, n = re.subn(pattern, replacement, text)
    if n == 0:
        print(f'Failed to apply replacement: {pattern}', file=sys.stderr)
        sys.exit(1)
    text = new_text

raw_yaml = f'https://raw.githubusercontent.com/{owner}/{repo}/main/Yaml/Overwrite-Clash-Bypass.yaml'
text, n = re.subn(
    r'(?m)^DOWNLOAD_FILE\s*=\s*url=.*$',
    f'DOWNLOAD_FILE = url={raw_yaml}, path=/etc/openclash/config/Overwrite-Clash-Bypass.yaml, cron=0 6 * * *, force=true, RESTART=true',
    text,
)
if n == 0:
    print('Failed to update DOWNLOAD_FILE', file=sys.stderr)
    sys.exit(1)

header = (
    '# Auto-generated from Overwrite-smart-bypass-LGBM.conf\n'
    '# Do not edit manually; regenerate via scripts/generate-ipv6-conf.py\n\n'
)
DST.write_text(header + text, encoding='utf-8')
print(f'Wrote {DST.relative_to(ROOT)}')
