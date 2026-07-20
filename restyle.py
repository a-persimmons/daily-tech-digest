# -*- coding: utf-8 -*-
"""
报刊风格改造脚本 — 统一处理：
1. 归档页 index.html → 报纸版面风格
2. 所有详情页 今日技术热点速览_*.html → 报纸正文风格 + "← 返回归档"入口
3. 详情页 CSS 整体替换为报刊配色（米白纸感、衬线标题、双线分隔）
"""
import re, os, glob, html as html_mod

REPO = "/Users/peotry/daily-tech-digest"

# ================================================================
# 报刊风格 CSS — 归档页
# ================================================================
ARCHIVE_CSS = r"""
:root{
  --paper:#f4ede0; --paper2:#efe7d8; --ink:#1a1a1a; --ink2:#333;
  --muted:#6b6357; --rule:#2b2b2b; --rule-light:#c9bfa9;
  --accent:#9b1b1b; --accent2:#1a3a5c; --highlight:#e8e0d0;
}
*{box-sizing:border-box;margin:0;padding:0;}
body{
  font-family:'Source Serif 4','Noto Serif SC',Georgia,'Times New Roman',serif;
  background:var(--paper);color:var(--ink);min-height:100vh;
  background-image:radial-gradient(ellipse at top,rgba(0,0,0,.02),transparent 60%);
}
.wrap{max-width:820px;margin:0 auto;padding:0 24px 60px;}

/* Masthead */
.masthead{text-align:center;padding:40px 0 0;}
.masthead .top-rule{height:3px;background:var(--rule);margin-bottom:1px;}
.masthead .thin-rule{height:1px;background:var(--rule);margin-bottom:18px;}
.masthead .kicker{
  font-size:11px;letter-spacing:.3em;text-transform:uppercase;
  color:var(--muted);font-weight:400;margin-bottom:6px;
}
.masthead .nameplate{
  font-size:48px;font-weight:900;letter-spacing:-.01em;
  line-height:1.05;color:var(--ink);
  font-family:'Playfair Display','Noto Serif SC',Georgia,serif;
}
.masthead .nameplate .small{font-size:.55em;font-weight:400;letter-spacing:.05em;}
.masthead .tagline{
  font-size:13px;color:var(--muted);font-style:italic;
  margin-top:8px;margin-bottom:16px;
}
.masthead .bottom-rules{height:1px;background:var(--rule);margin-bottom:2px;}
.masthead .bottom-rules::after{content:"";display:block;height:3px;background:var(--rule);margin-top:2px;}
.dateline-bar{
  display:flex;justify-content:space-between;align-items:center;
  font-size:12px;color:var(--muted);letter-spacing:.05em;
  padding:8px 0;border-bottom:1px solid var(--rule-light);
  margin-bottom:32px;
}
.dateline-bar .vol{font-variant:numeric:tabular-nums;}

/* Edition list */
.list{display:flex;flex-direction:column;}
a.item{
  display:flex;align-items:baseline;gap:18px;
  padding:18px 4px;border-bottom:1px solid var(--rule-light);
  text-decoration:none;color:var(--ink);
  transition:background .15s ease;
}
a.item:hover{background:var(--highlight);}
a.item:hover .title{color:var(--accent);}
a.item:hover .date-num{text-decoration:underline;}
.item .left{display:flex;align-items:baseline;gap:14px;flex:1;}
.item .dot{
  font-size:20px;font-weight:900;color:var(--accent);
  font-variant-numeric:tabular-nums;min-width:32px;
  font-family:'Playfair Display',Georgia,serif;
}
.item .title{
  font-size:17px;font-weight:700;flex:1;
  transition:color .15s ease;
}
.item .date{color:var(--muted);font-size:13px;white-space:nowrap;font-style:italic;}
.item .arrow{color:var(--muted);font-size:16px;transition:all .15s ease;}
a.item:hover .arrow{color:var(--accent);transform:translateX(4px);}

footer.colophon{
  margin-top:50px;padding-top:20px;
  border-top:3px double var(--rule);
  text-align:center;color:var(--muted);font-size:12px;line-height:1.8;font-style:italic;
}
.empty{color:var(--muted);text-align:center;padding:40px;border:1px dashed var(--rule-light);font-style:italic;}
"""

# ================================================================
# 报刊风格 CSS — 详情页
# ================================================================
DETAIL_CSS = r"""
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

# Google Fonts for newspaper style
ARCHIVE_FONTS = '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Serif+4:ital,wght@0,400;0,600;0,700;1,400&family=Noto+Serif+SC:wght@400;700;900&display=swap" rel="stylesheet">'
DETAIL_FONTS = ARCHIVE_FONTS

# ================================================================
# Build new archive page (index.html)
# ================================================================
def build_archive():
    """Read existing index.html, extract all <a class="item"> entries,
    rebuild with newspaper style."""
    html_path = os.path.join(REPO, "index.html")
    with open(html_path, encoding="utf-8") as f:
        content = f.read()

    # Extract all item entries: href + date label
    items = re.findall(
        r'<a class="item" href="([^"]+)">.*?<div class="title">(.*?)</div>\s*<div class="date">(.*?)</div>',
        content, re.S
    )
    # items = [(href, title, date), ...]
    print(f"  found {len(items)} archive entries")

    items_html = "            <!-- NEW-ENTRY-HERE -->\n"
    for href, title, date_label in items:
        # Skip already-placed NEW-ENTRY-HERE placeholder text
        items_html += f"""            <a class="item" href="{href}">
                <div class="left">
                    <div class="dot">§</div>
                    <div>
                        <div class="title">{html_mod.escape(title.strip())}</div>
                        <div class="date">{html_mod.escape(date_label.strip())}</div>
                    </div>
                </div>
                <div class="arrow">→</div>
            </a>
"""

    import datetime
    now = datetime.date.today()
    wd = ['MON','TUE','WED','THU','FRI','SAT','SUN'][now.weekday()]

    new_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日技术热点 · 归档</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Serif+4:ital,wght@0,400;0,600;0,700;1,400&family=Noto+Serif+SC:wght@400;700;900&display=swap" rel="stylesheet">
    <style>{ARCHIVE_CSS}</style>
</head>
<body>
    <div class="wrap">
        <div class="masthead">
            <div class="top-rule"></div>
            <div class="thin-rule"></div>
            <div class="kicker">Daily Tech Briefing · Established 2026</div>
            <div class="nameplate">每日技术热点 <span class="small">· The Tech Dispatch</span></div>
            <div class="tagline">"All the tech that's fit to print" — Hacker News · GitHub · Product Hunt · Hugging Face</div>
            <div class="bottom-rules"></div>
        </div>

        <div class="dateline-bar">
            <span class="vol">VOL. I</span>
            <span>{now.strftime('%Y年%m月%d日')} · {wd}</span>
            <span class="vol">{len(items)} EDITIONS</span>
        </div>

        <div class="list">
{items_html}        </div>

        <footer class="colophon">
            由每日自动化任务自动生成 · 经 GitHub Pages 部署<br>
            数据来源：Hacker News · GitHub Trending · Product Hunt · Hugging Face Papers
        </footer>
    </div>
</body>
</html>
"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"  index.html rewritten ({len(new_html)} bytes)")


# ================================================================
# Transform a detail page to newspaper style
# ================================================================
def transform_detail(filepath):
    """Replace CSS + add back-to-archive links in a detail page."""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    fname = os.path.basename(filepath)

    # 1. Replace the entire <style>...</style> block
    content = re.sub(
        r'<style>.*?</style>',
        f'<style>{DETAIL_CSS}</style>',
        content,
        count=1,
        flags=re.S
    )

    # 2. Replace font links (Inter → serif newspaper fonts)
    content = re.sub(
        r'<link href="https://fonts\.googleapis\.com/css2\?family=Inter[^"]*"[^>]*>',
        DETAIL_FONTS,
        content
    )
    # Also handle the preconnect line if it references Inter
    # (leave preconnect as-is, it's harmless)

    # 3. Add "← 返回归档" link at the start of header (if not present)
    if 'class="back-link"' not in content:
        # Match various header patterns
        for hdr_pat in [
            '<header class="site-header">',
            '<header class="site-header" >',
        ]:
            if hdr_pat in content:
                content = content.replace(
                    hdr_pat,
                    f'{hdr_pat}\n  <a class="back-link" href="index.html">← 返回归档</a>',
                    1
                )
                break
        else:
            # Fallback: insert after <body> tag
            content = re.sub(
                r'(<body[^>]*>)',
                r'\1\n<a class="back-link" href="index.html" style="display:block;text-align:center;padding:10px;font-size:12px;color:#6b6357;text-decoration:none;">← 返回归档</a>',
                content,
                count=1
            )

    # 4. Add "← 返回归档" in footer (before "回到顶部" or at end)
    #    Check only footer section, not the header back-link we just added
    footer_section = ""
    if '</footer>' in content:
        parts = content.split('</footer>')
        if '<footer' in parts[0]:
            footer_section = parts[0].split('<footer')[-1]
    if 'href="index.html"' not in footer_section:
        # Pattern A: footer with 回到顶部
        if re.search(r'本报告由自动化任务每日生成.*?回到顶部', content, re.S):
            content = re.sub(
                r'(本报告由自动化任务每日生成[^<]*·\s*)(<a href="#top-story">回到顶部)',
                r'<a href="index.html">← 返回归档</a> · \1\2',
                content
            )
        # Pattern B: footer without 回到顶部 — insert before </footer>
        elif '</footer>' in content:
            content = re.sub(
                r'(</footer>)',
                r'  <a href="index.html">← 返回归档</a>\n\1',
                content,
                count=1
            )
        # Pattern C: no footer at all — append one before </body>
        else:
            content = re.sub(
                r'(</body>)',
                r'<footer style="text-align:center;padding:20px;border-top:1px solid #c9bfa9;margin-top:40px;font-size:12px;color:#6b6357;"><a href="index.html" style="color:#1a3a5c;text-decoration:none;">← 返回归档</a></footer>\n\1',
                content,
                count=1
            )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  {fname} → newspaper style ({len(content)} bytes)")


# ================================================================
# Main
# ================================================================
if __name__ == "__main__":
    print("=== Rebuilding index.html (newspaper archive) ===")
    build_archive()

    print("\n=== Transforming detail pages ===")
    reports = sorted(glob.glob(os.path.join(REPO, "今日技术热点速览_*.html")))
    for r in reports:
        transform_detail(r)

    print(f"\nDone. {len(reports)} detail pages + index.html transformed.")
