import json

raw = json.load(open('/Users/peotry/WorkBuddy/2026-07-09-13-58-54/hn_window_raw.json', encoding='utf-8'))
for h in raw:
    h['points'] = h.get('points') or 0
    h['num_comments'] = h.get('num_comments') or 0
    h['oid'] = h.get('objectID')
    h['title'] = h.get('title') or '(无标题)'
    h['created'] = h.get('created_at_i') or 0

sp = [h['points'] for h in raw]; cm = [h['num_comments'] for h in raw]
smin, smax = min(sp), max(sp); cmin, cmax = min(cm), max(cm)
def norm(v, a, b): return 0.0 if b == a else (v - a) / (b - a)
for h in raw:
    h['hot'] = round(0.6 * norm(h['points'], smin, smax) + 0.4 * norm(h['num_comments'], cmin, cmax), 4)
raw.sort(key=lambda h: h['hot'], reverse=True)

# ---- zh translations (2026-11-23) ----
zh = {
"50597612": "到 2028 年 Anthropic 的电力 87% 来自天然气、11% 来自煤电",
"50602947": "硅谷到底发生了什么",
"50601525": "Perplexity 与「智能」这件事",
"50602843": "GTA 6 的鸟类：罪恶都市与里奥尼达野生动物野外指南",
"50603845": "本地 AI 入门指南：Inkling、Qwen 与 Unsloth",
"50606192": "用互联网档案馆里被遗忘的影像搭一个免费另类电视网",
"50600511": "开放社交网络联盟",
"50599762": "Show HN：我做了个游戏，你就是 LLM 的 subagent",
"50605045": "Masullo 手稿 Lean 形式化进度地图",
"50603589": "带实时公交、飞机和船只的微缩旧金山",
"50607261": "XNU Linux：在 Linux 上跑完整的 OS X 图形用户空间",
"50598441": "Masullo 谈黎曼假设",
"50605479": "Nespresso 减少每颗胶囊咖啡克重的计划",
"50600677": "欧洲放松化学品监管，而科学正把这些化学品与「生活方式病」关联",
"50604988": "GL.iNet 安全公告 2026-11-20",
"50603143": "假设别人对你的博客文章不感兴趣",
"50604314": "用 agent 集群去解 P vs. NP",
"50600435": "Backblaze 用户担心政策更新后个人数据被出售或共享",
"50602847": "加拿大重申对新闻业的联邦资助",
"50599583": "联合国气候谈判因化石燃料激烈冲突而破裂",
"50600789": "挪威拟将 16 岁以下社媒禁令扩大到游戏与消息应用",
"50599313": "监狱获准干扰违禁手机信号",
"50597743": "对男性更严厉？评估 LLM 在冲突情境下的性别不对称道德判断",
"50603906": "GLP-1 类药物可能带来出乎意料的环境红利",
"50601823": "软件对人来说是不是一直过于复杂",
"50605483": "FBI 正大规模招聘 IT 专业人员",
"50600771": "Ask HN：转行做蓝领手艺是稳妥选择吗",
"50600838": "C++26 定稿（又一次）：2026 年 11 月 ISO C++ 会议纪要",
"50600521": "法西斯主义与垄断（2020）",
"50604959": "不要接受",
"50600622": "我加入了 NTP Pool，但用的不是 Stratum 1 的树莓派",
"50605699": "「这就是贪婪」：Mamdani 抨击亚马逊在纽约加收 5 美元费用",
}

def z(o): return zh.get(o, '')

top20 = [{'oid': h['oid'], 'title': h['title'], 'zh': z(h['oid']), 'points': h['points'],
          'comments': h['num_comments'], 'hot': h['hot']} for h in raw[:20]]
top20_ids = {h['oid'] for h in raw[:20]}
highc = sorted([h for h in raw if h['oid'] not in top20_ids], key=lambda h: h['num_comments'], reverse=True)[:10]
highc_out = [{'oid': h['oid'], 'title': h['title'], 'zh': z(h['oid']), 'points': h['points'],
              'comments': h['num_comments']} for h in highc]
all_lst = [{'oid': h['oid'], 'title': h['title'], 'zh': z(h['oid']), 'points': h['points'],
            'comments': h['num_comments'], 'hot': h['hot']} for h in raw]

# ---- left column summary (HTML) ----
summary = """<p>窗口（<span class="hl">11/22 16:30 → 11/23 16:30 CST</span>）共 <span class="hl">839 条</span>。<span class="hl">Anthropic 到 2028 年的电力 87% 来自天然气、11% 来自煤电（959▲/943💬）</span>以碾压姿态拿下全窗第一，943 条评论全在算同一笔账：AI 的电从哪来、谁买单。</p>
<p>第二梯队是「叙事反思」：硅谷发生了什么（628▲/332💬）、Perplexity 与智能（570▲/389💬）；实操侧本地 AI 入门（462▲/192💬）与 GTA6 鸟类指南（474▲）同热。风险线照旧密集：GL.iNet 安全公告（184▲）、Backblaze 条款改动引发数据被卖担忧（165▲/62💬）。</p>
<p><b>可切入口：</b>「AI 用量换算电与碳」和「订阅条款变更监控」都是无需许可、单人几天能出成品的方向（见机会卡 1、3）。</p>"""

highc_html = "<p style='margin:0;'><span class='hl'>挪威 16 岁社媒禁令扩到游戏与消息</span>（93💬 / 58▲） · <span class='hl'>监狱获准干扰违禁手机</span>（87💬 / 41▲） · <span class='hl'>LLM 道德判断的性别不对称</span>（78💬 / 93▲） · <span class='hl'>软件是不是一直过于复杂</span>（75💬 / 54▲） · <span class='hl'>FBI 大规模招 IT</span>（74💬 / 37▲） · <span class='hl'>Ask HN：转行做蓝领稳妥吗</span>（72💬 / 42▲）</p><p style='margin:6px 0 0;color:#6b6357;font-size:12px;'>「分数不高但讨论密集」的有效信号，均可在右栏翻到。</p>"

out = {
    "window_label": "2026-11-22 16:30 → 2026-11-23 16:30 (CST)",
    "count": len(raw),
    "summary": summary,
    "highc": highc_html,
    "top20": top20,
    "highc_list": highc_out,
    "all": all_lst,
}
json.dump(out, open('/Users/peotry/WorkBuddy/2026-07-09-13-58-54/hn_window.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print("top20[0]:", top20[0]['title'][:50], top20[0]['points'], top20[0]['comments'])
print("all count:", len(all_lst))
print("missing zh in top20:", [t['oid'] for t in top20 if not t['zh']])
print("missing zh in highc:", [t['oid'] for t in highc_out if not t['zh']])
print("written /Users/peotry/WorkBuddy/2026-07-09-13-58-54/hn_window.json")
