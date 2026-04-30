#!/usr/bin/env python3
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

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

RAW_YAML = f'https://raw.githubusercontent.com/{owner}/{repo}/main/Yaml/Overwrite-Clash-Bypass.yaml'
HEADER = (
    '# Auto-generated from upstream bypass config\n'
    '# Do not edit manually; regenerate via scripts/generate-ipv6-conf.py\n\n'
)

TARGETS = [
    ('Overwrite-smart-bypass-LGBM.conf', 'Overwrite-smart-bypass-LGBM-ipv6.conf'),
    ('Overwrite-smart-bypass.conf', 'Overwrite-smart-bypass-ipv6.conf'),
]

REPLACEMENTS = [
    (r'(?m)^IPV6_ENABLE\s*=\s*.*$', 'IPV6_ENABLE = 1'),
    (r'(?m)^IPV6_DNS\s*=\s*.*$', 'IPV6_DNS = 1'),
    (r'(?m)^#\s*IPV6_MODE\s*\(.*$', 'IPV6_MODE = 0'),
    (r'(?m)^#\s*ENABLE_V6_UDP_PROXY\s*\(.*$', 'ENABLE_V6_UDP_PROXY = 1'),
    (r'(?m)^#\s*CHINA_IP6_ROUTE\s*\(.*$', 'CHINA_IP6_ROUTE = 1'),
]

for src_name, dst_name in TARGETS:
    src = ROOT / 'Overwrite' / src_name
    dst = ROOT / 'Overwrite' / dst_name
    text = src.read_text(encoding='utf-8')

    for pattern, replacement in REPLACEMENTS:
        text, n = re.subn(pattern, replacement, text)
        if n == 0:
            print(f'Failed to apply replacement for {src_name}: {pattern}', file=sys.stderr)
            sys.exit(1)

    text, n = re.subn(
        r'(?m)^DOWNLOAD_FILE\s*=\s*url=.*$',
        f'DOWNLOAD_FILE = url={RAW_YAML}, path=/etc/openclash/config/Overwrite-Clash-Bypass.yaml, cron=0 6 * * *, force=true, RESTART=true',
        text,
    )
    if n == 0:
        print(f'Failed to update DOWNLOAD_FILE for {src_name}', file=sys.stderr)
        sys.exit(1)

    dst.write_text(HEADER + text, encoding='utf-8')
    print(f'Wrote {dst.relative_to(ROOT)}')
