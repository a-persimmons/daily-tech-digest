#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request, re, json, sys, time, os

# 清掉 stale env proxy（HTTP_PROXY=127.0.0.1:9999 会让直连误走死代理），改走本机直连
for _k in ('HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'http_proxy', 'https_proxy', 'all_proxy'):
    os.environ.pop(_k, None)

URL = "https://www.producthunt.com/"
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

def fetch(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': UA,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
    })
    op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    return op.open(req, timeout=30).read().decode('utf-8', 'replace')

html = None
for attempt in range(4):
    try:
        html = fetch(URL)
        print("fetched attempt", attempt, "len", len(html))
        break
    except Exception as e:
        print("fail attempt", attempt, str(e)[:80])
    time.sleep(5)

if not html:
    sys.exit("could not fetch product hunt")

i = html.find('Top Products Launching Today')
if i < 0:
    print("segment not found; dumping tail markers")
    print(html[-500:])
    sys.exit(1)

# find the items array after the segment
rest = html[i:]
im = re.search(r'"items":\s*\[', rest)
if not im:
    print("items array not found")
    sys.exit(1)
start = im.end() - 1  # position of '['
depth = 0
j = start
while j < len(rest):
    c = rest[j]
    if c == '[':
        depth += 1
    elif c == ']':
        depth -= 1
        if depth == 0:
            break
    j += 1
arr_str = rest[start:j+1]
try:
    items = json.loads(arr_str)
except Exception as e:
    print("json parse err", e)
    sys.exit(1)
print("items count:", len(items))

import datetime
PT_DATE = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')  # PT date = CST date - 1
print("PT_DATE:", PT_DATE)
print("featuredAt seen:", sorted({(it.get('node', it) or {}).get('featuredAt') or '-' for it in items if isinstance(it, dict)}))
out = []
for it in items:
    # each item may wrap a node; handle both direct Post and {node:...}
    node = it.get('node', it) if isinstance(it, dict) else it
    if not isinstance(node, dict):
        continue
    name = node.get('name')
    tagline = node.get('tagline') or ''
    dailyRank = node.get('dailyRank')
    featuredAt = node.get('featuredAt') or node.get('featuredAt')

    def score_of(n):
        return n.get('launchDayScore') or n.get('latestScore') or 0
    upvotes = score_of(node)
    # topics: connection edges
    topics = []
    tc = node.get('topics')
    if isinstance(tc, dict):
        for e in tc.get('edges', []):
            nd = e.get('node', {})
            if nd.get('name'):
                topics.append(nd['name'])
    # slug: from url or name
    url = node.get('url') or node.get('website') or ''
    slug = node.get('slug') or ''
    if not url and slug:
        url = "https://www.producthunt.com/posts/" + slug
    # filter: must have dailyRank and featuredAt matching PT date
    if not dailyRank:
        continue
    if featuredAt and PT_DATE not in featuredAt:
        continue
    out.append({
        'name': name, 'tagline': tagline, 'upvotes': upvotes,
        'topics': topics, 'url': url, 'dailyRank': dailyRank
    })

out.sort(key=lambda x: int(x['dailyRank']) if str(x['dailyRank']).isdigit() else 999)
print("filtered (today) count:", len(out))
for r in out:
    print(f"  #{r['dailyRank']} {r['name']} | {r['upvotes']}▲ | {r['url']} | {','.join(r['topics'][:4])}")
    print("     tagline:", r['tagline'][:80])
json.dump(out[:8], open('/Users/peotry/WorkBuddy/2026-07-09-13-58-54/ph_data.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print("written ph_data.json")
