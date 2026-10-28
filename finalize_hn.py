import json

raw = json.load(open('/Users/peotry/WorkBuddy/2026-07-09-13-58-54/hn_window_raw.json', encoding='utf-8'))
for h in raw:
    h['points']=h.get('points') or 0
    h['num_comments']=h.get('num_comments') or 0
    h['oid']=h.get('objectID')
    h['title']=h.get('title') or '(无标题)'
    h['created']=h.get('created_at_i') or 0

sp=[h['points'] for h in raw]; cm=[h['num_comments'] for h in raw]
smin,smax=min(sp),max(sp); cmin,cmax=min(cm),max(cm)
def norm(v,a,b): return 0.0 if b==a else (v-a)/(b-a)
for h in raw:
    h['hot']=round(0.6*norm(h['points'],smin,smax)+0.4*norm(h['num_comments'],cmin,cmax), 4)
raw.sort(key=lambda h:h['hot'],reverse=True)

# ---- zh translations (2026-10-28) ----
zh = {
"50257325":"AI 承诺少干活。可我从来没有这么忙过（622▲/618💬，热度第二、评论第一）",
"50261319":"Genie 4（765▲/463💬，热度第一、评论第二，DeepMind 新一代世界模拟）",
"50259604":"美国政府藏着一份关于它如何监视美国人的秘密法院裁决（814▲/297💬，分数第二）",
"50261998":"Ghostty 1.4（815▲/245💬，分数第一）",
"50260814":"Anthropic 用非法获取的斯坦福教授著作训练了 Claude（483▲/266💬）",
"50255298":"AI 时代的《人月神话》（440▲/309💬）",
"50256985":"Roblox 未经询问就从我们站点下载了 145GB 模型（含成人内容）（460▲/268💬）",
"50257419":"Python 的实验性 JIT 将被移除（456▲/246💬）",
"50258538":"搭载 M6 的新 iMac（317▲/383💬，评论第三）",
"50257326":"维基百科对 AI 生成内容的清理（460▲/211💬）",
"50261352":"搭载 M6 的新 14 英寸 MacBook Pro（295▲/379💬，评论第四）",
"50261819":"警方正用 AI 以「行为可疑」为由拦停司机（347▲/277💬）",
"50257548":"软件也许正在变糟，但它曾经糟得可怕（302▲/317💬）",
"50261589":"在持续失败之后，亚马逊正在掏空自己的 AI 部门（283▲/199💬）",
"50263854":"Discord 很快将允许任何人通过谷歌搜到公开服务器的消息（273▲/143💬）",
"50256738":"我不再向 NEW 上传了（232▲/140💬，Debian 开发者公开信）",
"50261784":"一个 28 岁的 DOGE 操盘手掏空了 USAID。人事处查无此人（217▲/135💬）",
"50258521":"搭载 M6 的新 14 英寸 MacBook Pro（160▲/196💬）",
"50264857":"Tailscale SSH：调查与修复进展更新（212▲/114💬）",
"50264853":"Survival LLM：跑在你自己电脑上的 AI 助手与应急资料库（211▲/108💬）",
"50259406":"我的数据被用于模型训练了吗？（215▲/99💬）",
"50265609":"用 Claude 加速药物研发的早期进展（149▲/130💬，漏网评论第一）",
"50258868":"此处有怪兽：当 agent 接手工作，你还需要知道什么？（161▲/87💬）",
"50259343":"PHP2Shell：利用尝试与修复趋势（185▲/59💬）",
"50261647":"有限单群分类在 Lean 中被形式化（178▲/45💬）",
"50253939":"我还在教 OpenGL ES 3.0（138▲/86💬）",
"50260526":"3000 亿美元的「债务墙」正逼近私募股权支持的公司（159▲/59💬）",
"50254836":"已经有 5 家推理服务商提供被「去审查」的 DeepSeek（93▲/118💬，漏网评论第二）",
"50256952":"Gforth 1.0（159▲/17💬）",
"50264228":"美国总统称他将封杀「人工智能」这个词（80▲/105💬，漏网评论第三）",
"50262229":"推出 LFM3：面向专用智能的全模态（125▲/51💬）",
"50259050":"一家据称的以色列间谍公司把 Starlink 用户当作目标（131▲/30💬）",
"50265594":"设备树里出现了 Raspberry Pi Zero 3W 与 Pi 4 Model A（111▲/43💬）",
"50256230":"AI 正在毁掉鬼屋（45▲/108💬，漏网评论第四）",
"50266780":"评测者很少谈可靠性。拥有者提起它的频率是两倍（70▲/69💬）",
"50265128":"四个月的 Zig（81▲/49💬）",
"50254935":"英国将对每名国际学生向大学收费 1200 美元（54▲/72💬）",
"50262942":"消息人士称巴西的弗拉维奥·博索纳罗已前往美国（57▲/51💬）",
"50262668":"摩萨德在「你能想到的每个国家」都放了类似爆炸寻呼机的装置（2025）（56▲/46💬）",
"50260242":"病毒式传播的民调不是代表性民调（37▲/60💬）",
"50255177":"写写 pratt 解析，好让自己记住（82▲/7💬）",
"50265413":"Hex 融资 1 亿美元（57▲/35💬）",
"50260714":"JetBrains 的 IDE 现在由 libghostty 驱动（65▲/10💬）",
"50263701":"GoAhead 里的三个 TLS bug（61▲/14💬）",
"50255346":"「AI 技能」到 2026 年一文不值（50▲/25💬）",
"50261583":"PHP2Shell、LiteLLM、GitLab：找到你需要打的补丁（56▲/13💬）",
"50262950":"缅因州禁止校园手机，帮青少年专注与连接。它奏效了（57▲/7💬）",
"50260960":"一家数据恢复公司 CEO 因涉嫌诈骗勒索受害者被起诉（54▲/9💬）",
"50262982":"带无线电标签的帝王蝶（36▲/10💬）",
"50260571":"Show HN：规范优先的 agentic 开发插件，并做证明（28▲/18💬）",
"50258574":"格雷格·阿博特从数据中心捐赠者那里拿了 900 万美元。现在他去监管他们（41▲/3💬）",
"50263699":"特朗普称他将禁止所有人使用「人工智能」这个说法（33▲/12💬）",
"50261533":"「我当时是盲目恐慌。」他们打开新的 2000 美元 iPhone Duo——它坏了（21▲/24💬）",
"50255318":"为什么远程岗位在 2026 年正在灭绝？（7▲/39💬）",
"50265393":"UEFI 固件里的代码执行漏洞威胁着地球上大多数服务器（36▲/5💬）",
"50266701":"扩大与 GSA 的合作，把 Claude 带进各级政府部门（27▲/15💬）",
"50263325":"警方拦人，只因为 AI 判定他们的驾驶「可疑」（33▲/8💬）",
"50268380":"Git for US Legislation——给美国立法做版本管理（27▲/12💬）",
"50254383":"美光台湾把工厂工人的薪资提高 2.7 倍（26▲/12💬）",
"50255406":"ETH 为假的简化证明 [pdf]（28▲/9💬）",
"50261579":"古董字体合集——修复的 19 世纪字体（25▲/11💬）",
"50260619":"我的视频有单元测试（25▲/11💬）",
"50259643":"在浏览器里玩《赛博朋克 2077》（24▲/11💬）",
"50261623":"恶性循环：关于一种新闻哲学的论纲（2020）（25▲/8💬）",
"50265960":"Dioxus fullstack 上线生产一年：好的、痛的（22▲/11💬）",
"50255159":"Anthropic 对 ETH 的反证（25▲/6💬）",
"50259271":"癌症疫苗终于来了。我们怎么把它们送到病人手里？（29▲/1💬）",
"50266373":"比亚迪 1 万美元的电动车在近 90 英里时速下爆胎——看看发生了什么（16▲/14💬）",
"50258614":"产业界几十年前就知道微塑料会侵入人体（26▲/2💬）",
"50261584":"我们让云端 agent 查生产库（用 OIDC，不用密钥）（17▲/12💬）",
}

def z(o): return zh.get(o,'')

top20 = [{'oid':h['oid'],'title':h['title'],'zh':z(h['oid']),'points':h['points'],'comments':h['num_comments'],'hot':h['hot']} for h in raw[:20]]
top20_ids={h['oid'] for h in raw[:20]}
highc = sorted([h for h in raw if h['oid'] not in top20_ids], key=lambda h:h['num_comments'], reverse=True)[:10]
highc_out=[{'oid':h['oid'],'title':h['title'],'zh':z(h['oid']),'points':h['points'],'comments':h['num_comments']} for h in highc]
all_lst = [{'oid':h['oid'],'title':h['title'],'zh':z(h['oid']),'points':h['points'],'comments':h['num_comments'],'hot':h['hot']} for h in raw]

# ---- left column summary (HTML) ----
summary = """<p>本窗口（<span class="hl">10/27 10:00 → 10/28 10:00 CST</span>）Hacker News 共 <span class="hl">1112 条</span>新帖。今天没有单一主角，而是一次<b>兑现落空</b>的集体记账：热度第一是 <span class="hl">Genie 4</span>（<span class="hl">765▲</span>/<span class="hl">463💬</span>，DeepMind 的新一代世界模拟），评论第一却是 <span class="hl">AI 承诺少干活。可我从来没有这么忙过</span>（<span class="hl">622▲</span>/<span class="hl">618💬</span>，热度第二）——能力冲到新高、体感反而变差，这两条并排就是今天的标题。</p>
<p><b>第一条主线：AI 的账从「钱」算到了「人」。</b><span class="hl">AI 时代的《人月神话》</span>（440▲/309💬）把布鲁克斯的老命题接到了 agent 身上：人多不等于快，工具多也不等于快；<span class="hl">软件也许正在变糟，但它曾经糟得可怕</span>（302▲/317💬）给了一个不肯怀旧的对照组。组织层面的代价同步落地：<span class="hl">在持续失败之后，亚马逊正在掏空自己的 AI 部门</span>（283▲/199💬）是第一个公开承认投入没换来产出的大厂动作，<span class="hl">「AI 技能」到 2026 年一文不值</span>（50▲/25💬）是这条线的个人版本。能力端仍在推：<span class="hl">用 Claude 加速药物研发的早期进展</span>（149▲/130💬，漏网评论第一）、<span class="hl">推出 LFM3：面向专用智能的全模态</span>（125▲/51💬）、<span class="hl">此处有怪兽：当 agent 接手工作，你还需要知道什么？</span>（161▲/87💬）。</p>
<p><b>第二条主线：抓取的一方被追着要收据。</b><span class="hl">Anthropic 用非法获取的斯坦福教授著作训练了 Claude</span>（483▲/266💬）把训练数据的来源问题钉在了一个具体机构上，同栏 <span class="hl">我的数据被用于模型训练了吗？</span>（215▲/99💬）是用户自己来找答案。另一侧是抓取行为的本体：<span class="hl">Roblox 未经询问就从我们站点下载了 145GB 模型（含成人内容）</span>（460▲/268💬）——不告而取已从模型公司扩散到平台公司。公开内容同样在被重新界定：<span class="hl">维基百科对 AI 生成内容的清理</span>（460▲/211💬）是百科全书第一次系统性回滚机器文本，<span class="hl">Discord 很快将允许任何人通过谷歌搜到公开服务器的消息</span>（273▲/143💬）则把「公开」两个字推到了用户没预期的方向。落地在治理与执法：<span class="hl">警方正用 AI 以「行为可疑」为由拦停司机</span>（347▲/277💬）与同题的 <span class="hl">警方拦人，只因为 AI 判定他们的驾驶「可疑」</span>（33▲/8💬）。</p>
<p><b>第三条主线：秘密与手艺各走一条路。</b>秘密这一头密度极高：<span class="hl">美国政府藏着一份关于它如何监视美国人的秘密法院裁决</span>（<span class="hl">814▲</span>/297💬，分数第二）、<span class="hl">一个 28 岁的 DOGE 操盘手掏空了 USAID。人事处查无此人</span>（217▲/135💬）、<span class="hl">一家据称的以色列间谍公司把 Starlink 用户当作目标</span>（131▲/30💬）、<span class="hl">摩萨德在「你能想到的每个国家」都放了类似爆炸寻呼机的装置</span>（56▲/46💬）；还有两条荒诞注脚——<span class="hl">美国总统称他将封杀「人工智能」这个词</span>（80▲/105💬，漏网评论第三）与同题的 <span class="hl">特朗普称他将禁止所有人使用「人工智能」这个说法</span>（33▲/12💬）。手艺这一头照常营业且今天格外厚实：<span class="hl">Ghostty 1.4</span>（<span class="hl">815▲</span>/245💬，分数第一）+ <span class="hl">JetBrains 的 IDE 现在由 libghostty 驱动</span>（65▲/10💬）、<span class="hl">Python 的实验性 JIT 将被移除</span>（456▲/246💬）、<span class="hl">有限单群分类在 Lean 中被形式化</span>（178▲/45💬）、<span class="hl">Gforth 1.0</span>（159▲/17💬）、<span class="hl">四个月的 Zig</span>（81▲/49💬）、<span class="hl">我还在教 OpenGL ES 3.0</span>（138▲/86💬）、<span class="hl">设备树里出现了 Raspberry Pi Zero 3W 与 Pi 4 Model A</span>（111▲/43💬）。硬件的大日子属于苹果：<span class="hl">搭载 M6 的新 iMac</span>（317▲/383💬，评论第三）与两条 <span class="hl">搭载 M6 的新 14 英寸 MacBook Pro</span>（295▲/379💬、160▲/196💬）。安全线还在昨天的延长线上：<span class="hl">PHP2Shell：利用尝试与修复趋势</span>（185▲/59💬）、<span class="hl">Tailscale SSH：调查与修复进展更新</span>（212▲/114💬）、<span class="hl">GoAhead 里的三个 TLS bug</span>（61▲/14💬）、<span class="hl">UEFI 固件里的代码执行漏洞威胁着地球上大多数服务器</span>（36▲/5💬）。排序：分数与评论 min-max 归一化加权（<span class="hl">0.6×分数 + 0.4×评论</span>）得 hot 降序取 Top20（中栏）；右栏为窗口全量 <span class="hl">1112 条</span>、按同一热度排序、固定框内滚动——确保<span class="hl">零遗漏</span>。</p>"""

highc_html = "<p style='margin:0;'>" + " · ".join(
    f"<span class='hl'>{h['title'][:40]}</span>（{h['comments']}💬 / {h['points']}▲）" for h in highc_out[:3]
) + "</p><p style='margin:6px 0 0;color:#6b6357;font-size:12px;'>「高分低讨论」之外的有效信号，均可在右栏翻到。</p>"

out = {
    "window_label": "2026-10-27 10:00 → 2026-10-28 10:00 (CST)",
    "count": len(raw),
    "summary": summary,
    "highc": highc_html,
    "top20": top20,
    "highc_list": highc_out,
    "all": all_lst,
}
json.dump(out, open('/Users/peotry/WorkBuddy/2026-07-09-13-58-54/hn_window.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print("top20[0]:", top20[0]['title'][:50], top20[0]['points'], top20[0]['comments'])
print("all count:", len(all_lst))
print("missing zh in top20:", [t['oid'] for t in top20 if not t['zh']])
print("missing zh in highc:", [t['oid'] for t in highc_out if not t['zh']])
print("written /Users/peotry/WorkBuddy/2026-07-09-13-58-54/hn_window.json")
