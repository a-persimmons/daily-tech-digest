#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日技术热点速览生成器（数据驱动）。
读取 4 个数据 JSON + content.json（内容层），输出报刊风格 HTML。

布局 / CSS / JS 经 2026-08-06 产出验证，须与归档页视觉完全一致：
  - HN 三栏（.hn-three）：左「当日综述」固定 --summary-w:290px，中 Top20，右全量；中/右高度由 JS 对齐左栏
  - GitHub / Product Hunt / Hugging Face Papers 两栏（.two-col）：左「当日综述」290px，右内容滚动
  - 四板块左栏共用同一 --summary-w，确保等宽
  - HN 每条链接必须指向 item?id=<id>，绝不可统一写成首页
禁止改写 HN3_CSS / 三栏 HTML 结构 / JS 撑高逻辑。
"""
import json
import html
import datetime
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = "/Users/peotry/daily-tech-digest"

def load(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return json.load(f)

hn = load("hn_window.json")        # top20 / all / summary / highc / window_label / count
gh = load("gh_data.json")          # [{name,desc,lang,today,total}]
ph = load("ph_data.json")          # [{name,tagline,upvotes,topics,url,dailyRank}]
hf = load("hf_data.json")          # [{id,title,upvotes,publishedAt}]
C = load("content.json")           # hero / insights / *_summary / note_hf / *_tr

DATE = C.get("date") or datetime.date.today().strftime("%Y-%m-%d")
dt = datetime.date.fromisoformat(DATE)
WEEKDAYS = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
WD = WEEKDAYS[dt.weekday()]

esc = html.escape

# ================================================================
# 报刊基础 CSS（与详情页 / 归档页完全一致，来自 restyle.py DETAIL_CSS）
# ================================================================
DETAIL_CSS = """
:root{
  --paper:#f4ede0; --paper2:#efe7d8; --ink:#1a1a1a; --ink2:#333;
  --muted:#6b6357; --rule:#2b2b2b; --rule-light:#c9bfa9;
  --accent:#9b1b1b; --accent2:#1a3a5c; --highlight:#e8e0d0;
  --green:#2d6a2d; --orange:#8a5a00;
}
*{box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{
  margin:0;background:var(--paper);color:var(--ink);
  font-family:'Source Serif 4','Noto Serif SC',Georgia,'Times New Roman',serif;
  line-height:1.65;font-size:15.5px;
  background-image:radial-gradient(ellipse at top,rgba(0,0,0,.02),transparent 60%);
}
a{color:var(--accent2);}
.wrap{max-width:980px;margin:0 auto;padding:0 24px 50px;}
.zh{color:var(--muted);font-size:12.5px;font-weight:400;line-height:1.45;margin-top:3px;font-style:italic;}
.gh-desc .zh{font-size:11.5px;margin-top:2px;}
.section,.hero{scroll-margin-top:64px;}

/* Masthead header */
header.site-header{
  padding:36px 24px 20px;text-align:center;
  border-bottom:3px double var(--rule);
  background:var(--paper);
}
.back-link{
  display:inline-block;font-size:12px;color:var(--muted);
  text-decoration:none;margin-bottom:10px;letter-spacing:.03em;
  transition:color .15s ease;
}
.back-link:hover{color:var(--accent);}
header.site-header .kicker{
  font-size:11px;letter-spacing:.3em;text-transform:uppercase;
  color:var(--muted);margin-bottom:4px;
}
header.site-header h1{
  margin:0 0 6px;font-size:32px;letter-spacing:-.01em;
  font-family:'Playfair Display','Noto Serif SC',Georgia,serif;
  font-weight:900;color:var(--ink);
}
header.site-header .date{color:var(--accent);font-weight:700;font-size:14px;letter-spacing:.05em;}
header.site-header .sub{color:var(--muted);font-size:12px;margin-top:6px;font-style:italic;}

/* Quick nav */
.quick-nav{
  position:sticky;top:0;z-index:100;display:flex;flex-wrap:wrap;
  gap:6px;justify-content:center;padding:10px 0;
  margin:0 0 28px;background:rgba(244,237,224,.92);
  -webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);
  border-bottom:1px solid var(--rule-light);
}
.quick-nav a{
  font-size:12px;font-weight:600;color:var(--ink2);
  text-decoration:none;padding:4px 11px;
  border:1px solid var(--rule-light);background:var(--paper2);
  white-space:nowrap;transition:all .15s ease;
  font-family:'Source Serif 4',Georgia,serif;letter-spacing:.02em;
}
.quick-nav a:hover{color:var(--accent);border-color:var(--accent);background:var(--highlight);}

/* Section title */
.sec-title{
  display:flex;align-items:center;gap:10px;margin:36px 0 16px;font-size:20px;
  border-bottom:2px solid var(--rule);padding-bottom:8px;
  font-family:'Playfair Display','Noto Serif SC',Georgia,serif;font-weight:800;
}
.sec-title .emo{font-size:18px;}
.sec-title .bar{display:none;}

/* Hero cards */
.hero-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;}
.hero-card{
  display:block;text-decoration:none;color:var(--ink);
  background:var(--paper2);border:1px solid var(--rule-light);
  border-radius:2px;padding:16px 16px 14px;transition:all .18s ease;
  position:relative;
}
.hero-card::before{
  content:"";position:absolute;top:0;left:0;right:0;height:3px;background:var(--accent);
}
.hero-card:hover{border-color:var(--ink);transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,.1);}
.hero-meta{color:var(--green);font-size:12px;font-weight:700;letter-spacing:.03em;}
.hero-title{font-size:16px;font-weight:800;margin:6px 0 4px;font-family:'Playfair Display','Noto Serif SC',Georgia,serif;}

/* Tables (HN / Papers) */
.hn-table{
  width:100%;border-collapse:collapse;
  background:var(--paper2);border:2px solid var(--rule);
}
.hn-table th{
  text-align:left;font-size:11px;color:var(--ink);font-weight:800;
  padding:10px 12px;background:var(--highlight);
  border-bottom:2px solid var(--rule);
  text-transform:uppercase;letter-spacing:.08em;
}
.hn-table td{padding:11px 12px;border-bottom:1px solid var(--rule-light);vertical-align:top;}
.hn-table tr:last-child td{border-bottom:none;}
.hn-table .rank{
  color:var(--accent);font-weight:900;width:34px;text-align:center;
  font-family:'Playfair Display',Georgia,serif;font-size:16px;
}
.hn-table .hn-title a{color:var(--ink);font-weight:700;text-decoration:none;font-size:14.5px;}
.hn-table .hn-title a:hover{color:var(--accent);text-decoration:underline;}
.hn-table .hn-score{color:var(--orange);font-weight:800;white-space:nowrap;width:74px;font-variant-numeric:tabular-nums;}
.hn-table .hn-comments{color:var(--muted);white-space:nowrap;width:64px;font-variant-numeric:tabular-nums;}
.tag{
  display:inline-block;font-size:10.5px;color:var(--accent2);
  background:transparent;border:1px solid var(--accent2);
  padding:1px 7px;border-radius:0;white-space:nowrap;
  text-transform:uppercase;letter-spacing:.05em;
}

/* GitHub / PH grid */
.gh-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:13px;}
.gh-card,.ph-card{
  background:var(--paper2);border:1px solid var(--rule-light);
  border-radius:2px;padding:14px 15px;transition:all .18s ease;
}
.gh-card:hover,.ph-card:hover{border-color:var(--ink);box-shadow:0 4px 14px rgba(0,0,0,.08);}
.gh-head,.ph-top{display:flex;align-items:center;gap:8px;margin-bottom:7px;}
.gh-name{
  font-weight:800;color:var(--ink);text-decoration:none;font-size:14.5px;
  font-family:Georgia,serif;
}
.gh-name:hover{color:var(--accent);}
.gh-lang{
  margin-left:auto;font-size:10.5px;color:var(--muted);
  background:transparent;border:1px solid var(--rule-light);
  padding:1px 7px;border-radius:0;text-transform:uppercase;letter-spacing:.05em;
}
.gh-desc,.ph-desc{font-size:13px;color:var(--ink2);line-height:1.55;}
.gh-meta{display:flex;gap:14px;margin-top:9px;font-size:12px;font-variant-numeric:tabular-nums;}
.gh-today{color:var(--green);font-weight:800;}
.gh-total{color:var(--orange);font-weight:700;}
.ph-rank{
  display:inline-flex;align-items:center;justify-content:center;
  width:26px;height:26px;border-radius:50%;background:var(--accent);
  color:var(--paper);font-size:12px;font-weight:900;
  font-family:'Playfair Display',Georgia,serif;
}
.ph-name{font-size:16px;font-weight:900;color:var(--ink);text-decoration:none;font-family:'Playfair Display','Noto Serif SC',Georgia,serif;}
.ph-name:hover{color:var(--accent);}
.ph-up{color:var(--green);font-weight:800;}
.ph-topics{color:var(--muted);font-size:11px;}

/* Insights */
.insight{
  background:var(--paper2);border:1px solid var(--rule-light);
  border-left:4px solid var(--accent);border-radius:0;
  padding:16px 18px;margin-bottom:14px;
}
.insight-head{display:flex;align-items:center;gap:9px;margin-bottom:6px;}
.insight-dot{width:9px;height:9px;border-radius:50%;background:var(--accent);}
.insight-head h3{margin:0;font-size:16px;font-family:'Playfair Display','Noto Serif SC',Georgia,serif;font-weight:800;}
.insight-src{
  margin-left:auto;font-size:10.5px;color:var(--muted);
  border:1px solid var(--rule-light);padding:2px 8px;border-radius:0;
  text-transform:uppercase;letter-spacing:.05em;
}
.insight p{margin:4px 0 0;color:var(--ink2);font-size:13.5px;}

/* Footer */
footer.site-footer{
  margin-top:40px;padding:22px 24px;text-align:center;
  border-top:3px double var(--rule);color:var(--muted);
  font-size:12px;line-height:1.7;font-style:italic;
}
footer.site-footer a{color:var(--accent2);text-decoration:none;}
.note{
  font-size:12px;color:var(--muted);background:var(--paper2);
  border:1px solid var(--rule-light);border-radius:0;
  padding:10px 13px;margin:0 0 14px;font-style:italic;
}
"""

# ================================================================
# HN3 布局 CSS（三栏 / 两栏 / 滚动对齐，2026-08-06 验证）
# ================================================================
HN3_CSS = """
.wrap{max-width:1180px;--summary-w:290px;}
.hn-window-note{font-size:12px;color:#6b6357;background:#efe7d8;border-left:3px solid #9b1b1b;padding:7px 11px;margin-bottom:16px;line-height:1.6;}
/* 公共：综述栏 */
.col-summary{border:1px solid #ddd2c0;padding:13px 15px;background:#efe7d8;}
.col-title{font-family:'Playfair Display',Georgia,serif;font-size:12.5px;letter-spacing:.07em;text-transform:uppercase;color:#9b1b1b;border-bottom:2px solid #9b1b1b;padding-bottom:6px;margin-bottom:12px;}
.col-summary p{margin:0 0 11px;font-family:'Source Serif 4',Georgia,serif;font-size:13px;line-height:1.72;color:#2a2a2a;}
.col-summary p:last-child{margin-bottom:0;}
.col-summary .hl{color:#9b1b1b;font-weight:600;}
/* 公共：滚动内容栏（高度由 JS 设为左侧综述高度；CSS 兜底防 JS 失效） */
.col-mid,.col-right{overflow-y:scroll;scrollbar-width:thin;border:1px solid #ddd2c0;background:#efe7d8;padding:10px 13px;max-height:80vh;overscroll-behavior:contain;}
.col-mid::-webkit-scrollbar,.col-right::-webkit-scrollbar{width:8px;}
.col-mid::-webkit-scrollbar-thumb,.col-right::-webkit-scrollbar-thumb{background:#c9bca6;border-radius:4px;}
.col-mid .zh,.col-right .zh{font-size:10.5px;color:#8a8175;}
/* HN 三栏：左综述(固定宽，与 GitHub 左栏一致) / 中 Top20 / 右全量 */
.hn-three{display:grid;grid-template-columns:var(--summary-w) 1.6fr 1.15fr;gap:18px;align-items:start;}
@media(max-width:1000px){.hn-three{grid-template-columns:1fr;}}
.hn-col-title{font-family:'Playfair Display',Georgia,serif;font-size:12.5px;letter-spacing:.07em;text-transform:uppercase;color:#9b1b1b;border-bottom:2px solid #9b1b1b;padding-bottom:6px;margin-bottom:12px;}
.hn-top-item{padding:8px 0;border-bottom:1px solid #ddd2c0;}
.hn-top-item a{font-family:'Source Serif 4',Georgia,serif;font-size:13px;color:#1a1a1a;text-decoration:none;font-weight:600;line-height:1.35;}
.hn-top-item a:hover{color:#9b1b1b;}
.hn-rank{color:#9b1b1b;font-weight:700;margin-right:6px;font-family:'Playfair Display',serif;}
.hn-top-meta{font-size:11px;color:#6b6357;margin-top:2px;}
.hn-all-row{padding:5px 0;border-bottom:1px dotted #ccc1ad;font-size:12px;line-height:1.45;}
.hn-all-row a{color:#1a3a5c;text-decoration:none;}
.hn-all-row a:hover{text-decoration:underline;}
.hn-all-meta{color:#9b1b1b;font-weight:600;font-size:10.5px;margin-right:4px;}
/* 两栏：左侧当日综述(固定宽) + 右侧原内容（GitHub / Product Hunt / Papers） */
.two-col{display:grid;grid-template-columns:var(--summary-w) 1fr;gap:26px;align-items:start;}
@media(max-width:900px){.two-col{grid-template-columns:1fr;}}
"""

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Serif+4:ital,wght@0,400;0,600;0,700;1,400&family=Noto+Serif+SC:wght@400;700;900&display=swap" rel="stylesheet">'

JS = """
function fitTwoCol(row){
  var s = row.querySelector('.col-summary');
  var r = row.querySelector('.col-right');
  if(s && r){ r.style.maxHeight = s.offsetHeight + 'px'; }
}
function fitThreeCol(row){
  var s = row.querySelector('.col-summary');
  if(!s) return;
  var m = row.querySelector('.col-mid');
  var r = row.querySelector('.col-right');
  var h = s.offsetHeight + 'px';
  if(m){ m.style.maxHeight = h; }
  if(r){ r.style.maxHeight = h; }
}
function fitCols(){
  document.querySelectorAll('.two-col').forEach(fitTwoCol);
  document.querySelectorAll('.hn-three').forEach(fitThreeCol);
}
function rafFit(){ requestAnimationFrame(function(){ requestAnimationFrame(fitCols); }); }
fitCols(); rafFit();
window.addEventListener('resize', fitCols);
window.addEventListener('load', function(){ fitCols(); setTimeout(fitCols, 200); setTimeout(fitCols, 600); setTimeout(fitCols, 1200); });
if(document.fonts && document.fonts.ready){ document.fonts.ready.then(function(){ fitCols(); rafFit(); }); }
"""

# ================================================================
# 各板块 HTML 构建
# ================================================================

def build_hero():
    cards = []
    for h in C["hero"]:
        cards.append(
            f'      <a class="hero-card" href="{esc(h["url"])}" target="_blank" rel="noopener">\n'
            f'        <div class="hero-meta">{esc(h["meta"])}</div>\n'
            f'        <div class="hero-title">{esc(h["title"])}</div>\n'
            f'        <div class="zh">{esc(h["zh"])}</div>\n'
            f'      </a>'
        )
    return (
        '  <section id="top-story" class="hero">\n'
        '    <div class="sec-title"><span class="emo">🔥</span><span>今日头条 · Top 3</span></div>\n'
        '    <div class="hero-grid">\n' + "\n".join(cards) + '\n    </div>\n  </section>\n'
    )


def build_hn():
    wl = hn.get("window_label", "")
    cnt = hn.get("count", len(hn.get("all", [])))
    note = (
        f'    <div class="hn-window-note">时间窗：{esc(wl)} · 窗口内共 <b>{cnt}</b> 条新帖 · '
        f'排序：分数与评论 min-max 归一化后加权（0.6×分数 + 0.4×评论），降序取 Top20（中栏）。'
        f'右栏为窗口内全量，滚动浏览。左栏「当日综述」完整展示、不滚动；中/右栏高度与左栏对齐。</div>\n'
    )
    # 左栏：综述 + 漏网高讨论（均来自 hn_window.json 预生成 HTML）
    left = (
        '      <div class="col-summary">\n'
        '        <div class="col-title">📝 当日综述</div>\n'
        f'        <div class="hn-summary">{hn.get("summary","")}</div>\n'
        '        <div class="col-title" style="margin-top:18px;">⚠️ 漏网高讨论</div>\n'
        f'        <div class="hn-summary">{hn.get("highc","")}</div>\n'
        '      </div>'
    )
    # 中栏：Top20
    mid_items = []
    for i, t in enumerate(hn.get("top20", [])):
        zh = f'<div class="zh">{esc(t.get("zh",""))}</div>' if t.get("zh") else ""
        mid_items.append(
            f'        <div class="hn-top-item">\n'
            f'          <span class="hn-rank">{i+1}</span>'
            f'<a href="https://news.ycombinator.com/item?id={esc(t["oid"])}" target="_blank" rel="noopener">{esc(t["title"])}</a>\n'
            f'          <div class="hn-top-meta">{t["points"]}▲ · {t["comments"]}💬 · hot {t.get("hot",0):.4f}</div>{zh}\n'
            f'        </div>'
        )
    mid = (
        '      <div class="col-mid">\n'
        '        <div class="hn-col-title">🔥 算法 Top 20</div>\n'
        + "\n".join(mid_items) + '\n      </div>'
    )
    # 右栏：全量
    right_items = []
    for i, t in enumerate(hn.get("all", [])):
        zh = f'<div class="zh">{esc(t.get("zh",""))}</div>' if t.get("zh") else ""
        right_items.append(
            f'<div class="hn-all-row"><span class="hn-all-meta">{i+1}. {t["points"]}▲/{t["comments"]}💬</span> '
            f'<a href="https://news.ycombinator.com/item?id={esc(t["oid"])}" target="_blank" rel="noopener">{esc(t["title"])}</a>{zh}</div>'
        )
    right = (
        '      <div class="col-right">\n'
        '        <div class="hn-col-title">🗂️ 全量（窗口内 · 滚动）</div>\n'
        + "\n".join(right_items) + '\n      </div>'
    )
    return (
        '  <section id="hn" class="section">\n'
        '    <div class="sec-title"><span class="emo">📰</span><span>Hacker News · 全窗口热门</span></div>\n'
        + note
        + '    <div class="hn-three">\n' + left + "\n" + mid + "\n" + right + '\n    </div>\n  </section>\n'
    )


def build_github():
    tr = C.get("gh_tr", {})
    cards = []
    for r in gh:
        name = r["name"]
        zh = tr.get(name, "")
        zh_html = f'<div class="zh">{esc(zh)}</div>' if zh else ""
        # desc 在 gh_data.json 中已做 HTML 转义（含 &amp; 等），原样输出，勿二次转义
        cards.append(
            f'        <div class="gh-card">\n'
            f'          <div class="gh-head">\n'
            f'            <a class="gh-name" href="https://github.com/{esc(name)}" target="_blank" rel="noopener">{esc(name)}</a>\n'
            f'            <span class="gh-lang">{esc(r.get("lang",""))}</span>\n'
            f'          </div>\n'
            f'          <div class="gh-desc">{r.get("desc","")}{zh_html}</div>\n'
            f'          <div class="gh-meta">\n'
            f'            <span class="gh-today">▲ {r["today"]:,} 今日</span>\n'
            f'            <span class="gh-total">★ {r["total"]:,}</span>\n'
            f'          </div>\n'
            f'        </div>'
        )
    return (
        '  <section id="github" class="section">\n'
        '    <div class="sec-title"><span class="emo">⭐</span><span>GitHub Trending · 当日热门（按 star 增量排序）</span></div>\n'
        '    <div class="two-col">\n'
        '      <div class="col-summary"><div class="col-title">📝 当日综述</div>' + C["gh_summary"] + '</div>\n'
        '      <div class="col-right"><div class="gh-grid">\n' + "\n".join(cards) + '\n      </div></div>\n'
        '    </div>\n  </section>\n'
    )


def build_producthunt():
    tr = C.get("ph_tr", {})
    cards = []
    for r in ph:
        name = r["name"]
        zh = tr.get(name, "")
        zh_html = f'<div class="zh">{esc(zh)}</div>' if zh else ""
        topics = " · ".join(r.get("topics", []))
        cards.append(
            f'        <div class="ph-card">\n'
            f'          <div class="ph-top">\n'
            f'            <span class="ph-rank">#{r.get("dailyRank","")}</span>\n'
            f'            <a class="ph-name" href="{esc(r["url"])}" target="_blank" rel="noopener">{esc(name)}</a>\n'
            f'          </div>\n'
            f'          <div class="ph-desc">{esc(r.get("tagline",""))}{zh_html}</div>\n'
            f'          <div class="ph-topics">▲ {r["upvotes"]} · {esc(topics)}</div>\n'
            f'        </div>'
        )
    return (
        '  <section id="producthunt" class="section">\n'
        '    <div class="sec-title"><span class="emo">🚀</span><span>Product Hunt · 今日精选发布</span></div>\n'
        '    <div class="two-col">\n'
        '      <div class="col-summary"><div class="col-title">📝 当日综述</div>' + C["ph_summary"] + '</div>\n'
        '      <div class="col-right"><div class="gh-grid">\n' + "\n".join(cards) + '\n      </div></div>\n'
        '    </div>\n  </section>\n'
    )


def build_papers():
    tr = C.get("hf_tr", {})
    cards = []
    for r in hf:
        rid = r["id"]
        zh = tr.get(rid, "")
        zh_html = f'<div class="zh">{esc(zh)}</div>' if zh else ""
        cards.append(
            f'        <div class="ph-card">\n'
            f'          <div class="ph-top">\n'
            f'            <span class="ph-rank">{r["upvotes"]}▲</span>\n'
            f'            <a class="ph-name" href="https://huggingface.co/papers/{esc(rid)}" target="_blank" rel="noopener">{esc(r["title"])}</a>\n'
            f'          </div>\n' + zh_html +
            f'        </div>'
        )
    if not cards:
        cards.append(
            '        <div class="ph-card" style="grid-column:1/-1;">\n'
            '          <div class="ph-desc">当日 Hugging Face Daily Papers 批次为空（周末休更），无条目可列。说明见下方「注」。</div>\n'
            '        </div>'
        )
    note = f'    <div class="note">{C["note_hf"]}</div>\n' if C.get("note_hf") else ""
    return (
        '  <section id="papers" class="section">\n'
        '    <div class="sec-title"><span class="emo">📄</span><span>Hugging Face Daily Papers</span></div>\n'
        + note
        + '    <div class="two-col">\n'
        '      <div class="col-summary"><div class="col-title">📝 当日综述</div>' + C["papers_summary"] + '</div>\n'
        '      <div class="col-right"><div class="gh-grid">\n' + "\n".join(cards) + '\n      </div></div>\n'
        '    </div>\n  </section>\n'
    )


def build_insights():
    items = []
    for it in C.get("insights", []):
        items.append(
            f'    <div class="insight">\n'
            f'      <div class="insight-head"><span class="insight-dot"></span>'
            f'<h3>{esc(it["title"])}</h3><span class="insight-src">{esc(it["src"])}</span></div>\n'
            f'      <p>{esc(it["text"])}</p>\n'
            f'    </div>'
        )
    return (
        '  <section id="insights" class="section">\n'
        '    <div class="sec-title"><span class="emo">💡</span><span>趋势洞察 · 跨四源</span></div>\n'
        + "\n".join(items) + '\n  </section>\n'
    )


def build_html():
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>今日技术热点速览 · {DATE} · {WD}</title>
{FONTS}
<style>{DETAIL_CSS}</style>
<style>{HN3_CSS}</style>
</head>
<body>
<header class="site-header">
  <a class="back-link" href="index.html">← 返回归档</a>
  <div class="kicker">The Tech Dispatch</div>
  <h1>🔥 今日技术热点速览</h1>
  <div class="date">{DATE} · {WD}</div>
  <div class="sub">数据来源：Hacker News · GitHub Trending · Product Hunt · Hugging Face Papers</div>
</header>

<nav class="quick-nav">
  <a href="#top-story">🔥 今日头条</a>
  <a href="#hn">📰 Hacker News</a>
  <a href="#github">⭐ GitHub</a>
  <a href="#producthunt">🚀 Product Hunt</a>
  <a href="#papers">📄 Papers</a>
  <a href="#insights">💡 趋势洞察</a>
</nav>

<div class="wrap">

{build_hero()}
{build_hn()}
{build_github()}
{build_producthunt()}
{build_papers()}
{build_insights()}
</div>

<footer class="site-footer">
  数据来源：Hacker News · GitHub Trending · Product Hunt · Hugging Face Papers<br>
  由每日自动化任务自动生成 · 经 GitHub Pages 部署<br>
  <a href="index.html">← 返回归档</a> · <a href="#top-story">回到顶部 ↑</a>
</footer>
<script>{JS}</script>
</body>
</html>"""


def main():
    out = build_html()
    fname = f"今日技术热点速览_{DATE}.html"
    with open(os.path.join(HERE, fname), "w", encoding="utf-8") as f:
        f.write(out)
    print(f"HTML report saved: {fname}")
    print(f"Size: {len(out):,} chars")


if __name__ == "__main__":
    main()
