#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
import re, sys, urllib.parse
ROOT=Path(__file__).resolve().parent
errors=[]
checked=[]

def local_target(base:Path, raw:str):
    raw=raw.strip()
    if not raw or raw.startswith(('#','data:','blob:','javascript:','mailto:','tel:')):
        return None
    u=urllib.parse.urlsplit(raw)
    if u.scheme or u.netloc:
        return None
    rel=urllib.parse.unquote(u.path)
    if not rel:
        return None
    if rel.startswith('/'):
        # Root-relative web URL maps to package root for verification.
        return ROOT / rel.lstrip('/')
    return (base.parent / rel).resolve()

class Parser(HTMLParser):
    def __init__(self, source):
        super().__init__(); self.source=source
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        for key in ('src','href'):
            if key in d:
                target=local_target(self.source,d[key])
                if target is not None:
                    checked.append((self.source.relative_to(ROOT),d[key],target))
                    if not target.exists(): errors.append((self.source.relative_to(ROOT),d[key],target))

for rel in ('index.html','canvas.html'):
    p=ROOT/rel
    Parser(p).feed(p.read_text(encoding='utf-8'))

css_url=re.compile(r"url\(\s*(['\"]?)([^)'\"]+)\1\s*\)",re.I)
for rel in ('css/huff.css','css/huff.min.css','css/canvas.css','css/canvas.min.css'):
    p=ROOT/rel
    text=p.read_text(encoding='utf-8')
    for _,raw in css_url.findall(text):
        target=local_target(p,raw)
        if target is not None:
            checked.append((p.relative_to(ROOT),raw,target))
            if not target.exists(): errors.append((p.relative_to(ROOT),raw,target))

# Runtime literals that are intentionally loaded from the package.
for rel in ('mirror-encoder-worker.js','canvas.html','css/huff.min.css','css/canvas.min.css','icon-name.jpg'):
    target=ROOT/rel
    checked.append(('runtime',rel,target))
    if not target.exists(): errors.append(('runtime',rel,target))

print(f'Checked {len(checked)} local asset linkages.')
if errors:
    print('FAILED: missing local assets:')
    for src,raw,target in errors:
        print(f'  {src}: {raw} -> {target}')
    sys.exit(1)
print('PASS: all checked local asset linkages resolve inside the package.')
