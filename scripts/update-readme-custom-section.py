#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / 'README.md'
START = '<!-- violin321-custom:start -->'
END = '<!-- violin321-custom:end -->'
BLOCK = f'''{START}
### 1️⃣ violin321 fork 额外提供

> 以下 3 个覆写文件由 **violin321/OpenClash_Overwrite** 额外提供，用于补充上游默认版本。

#### 🔹 主路由用户 - Url-test（Meta 内核，不使用 Smart）

```bash
https://raw.githubusercontent.com/violin321/OpenClash_Overwrite/main/Overwrite/Overwrite-meta.conf
```

#### 🔹 旁路由用户 - Smart-LGBM（IPv6 版）

```bash
https://raw.githubusercontent.com/violin321/OpenClash_Overwrite/main/Overwrite/Overwrite-smart-bypass-LGBM-ipv6.conf
```

#### 🔹 旁路由用户 - Smart（默认模型 + 数据收集，IPv6 版）

```bash
https://raw.githubusercontent.com/violin321/OpenClash_Overwrite/main/Overwrite/Overwrite-smart-bypass-ipv6.conf
```
{END}'''

text = README.read_text(encoding='utf-8')

# normalize any existing custom marker block to a single canonical block
marker_pattern = re.compile(rf'{re.escape(START)}.*?{re.escape(END)}', re.S)
text = marker_pattern.sub('', text)

# remove stray custom links/heading blocks to avoid duplication
for pattern in [
    r'\n### 1️⃣ Fork 额外提供：旁路由 IPv6 版\n.*?(?=\n### |\n## |\Z)',
    r'\n#### 🔹 主路由用户 - Url-test（Meta 内核，不使用 Smart）\n\n```bash\nhttps://raw\.githubusercontent\.com/violin321/OpenClash_Overwrite/main/Overwrite/Overwrite-meta\.conf\n```\n?',
    r'\n#### 🔹 旁路由用户 - Smart-LGBM（IPv6 版）\n\n```bash\nhttps://raw\.githubusercontent\.com/violin321/OpenClash_Overwrite/main/Overwrite/Overwrite-smart-bypass-LGBM-ipv6\.conf\n```\n?',
    r'\n#### 🔹 旁路由用户 - Smart（默认模型 \+ 数据收集，IPv6 版）\n\n```bash\nhttps://raw\.githubusercontent\.com/violin321/OpenClash_Overwrite/main/Overwrite/Overwrite-smart-bypass-ipv6\.conf\n```\n?',
]:
    text = re.sub(pattern, '\n', text, flags=re.S)

text = re.sub(r'\n{3,}', '\n\n', text).rstrip() + '\n'

insert_after_match = re.search(r'(### 1️⃣ 新增覆写模块.*?)(?=\n### 2️⃣ 配置环境变量|\Z)', text, flags=re.S)
if insert_after_match:
    insert_pos = insert_after_match.end(1)
    text = text[:insert_pos].rstrip() + '\n\n' + BLOCK + '\n\n' + text[insert_pos:].lstrip('\n')
else:
    text = text.rstrip() + '\n\n' + BLOCK + '\n'

text = re.sub(r'\n{3,}', '\n\n', text)
README.write_text(text, encoding='utf-8')
