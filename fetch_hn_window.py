import json, urllib.request, urllib.parse, sys, time

START=int(sys.argv[1]); END=int(sys.argv[2])
def get(url, proxy=False):
    req=urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 WorkBuddy/1.0'})
    if proxy:
        op=urllib.request.build_opener(urllib.request.ProxyHandler({'http':'http://127.0.0.1:7890','https':'http://127.0.0.1:7890'}))
    else:
        op=urllib.request.build_opener()
    try:
        return json.loads(op.open(req,timeout=30).read().decode())
    except Exception as e:
        return {'__err__':str(e)}

all_hits=[]

def fetch_range(a, b, depth=0):
    """Algolia caps retrievable results at 1000; split the time range when nbHits>1000."""
    u=f'https://hn.algolia.com/api/v1/search?tags=story&numericFilters=created_at_i>{a},created_at_i<{b}&hitsPerPage=1000&page=0'
    d=get(u)
    if isinstance(d,dict) and d.get('__err__'):
        d=get(u,proxy=True)
    if not isinstance(d,dict) or 'hits' not in d:
        print("ERR range",a,b,d); return
    nbh=d.get('nbHits',0)
    if nbh>1000 and depth<6 and b-a>60:
        mid=(a+b)//2
        fetch_range(a,mid,depth+1)
        fetch_range(mid,b,depth+1)
        return
    all_hits.extend(d['hits'])
    time.sleep(0.3)

fetch_range(START,END)

print("total hits in window:", len(all_hits))
# dedup by objectID
seen={}
for h in all_hits:
    oid=h.get('objectID')
    if oid and oid not in seen:
        seen[oid]=h
items=list(seen.values())
print("unique stories:", len(items))
# basic stats
scores=[h.get('points') or 0 for h in items]
comms=[h.get('num_comments') or 0 for h in items]
print("score max/min:", max(scores), min(scores))
print("comments max/min:", max(comms), min(comms))
# save raw
json.dump(items, open('/Users/peotry/WorkBuddy/2026-07-09-13-58-54/hn_window_raw.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
# show top by raw points
items_sorted=sorted(items, key=lambda h:(h.get('points') or 0), reverse=True)
print("=== top15 by raw points ===")
for h in items_sorted[:15]:
    print(f"{h.get('points')}▲ {h.get('num_comments')}💬 {h.get('objectID')} | {h.get('title','')[:70]}")
