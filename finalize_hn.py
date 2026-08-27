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
    h['hot']=round(0.6*norm(h['points'],smin,smax)+0.4*norm(h['num_comments'],cmin,cmax),4)
raw.sort(key=lambda h:h['hot'],reverse=True)

# ---- zh translations (top 40 by hot, 2026-08-27) ----
zh = {
"49449507":"GLM-5.3-Flash 发布（908▲/453💬 加权登顶兼评论之王，智谱新一代开放权重快速模型）",
"49448321":"AWS 收购 DuckLabs（987▲/293💬，当日最高分，DuckDB 背后公司被亚马逊纳入版图）",
"49448819":"Meta 就社交媒体对儿童的伤害达成 170 亿美元和解（484▲/462💬，史上最大规模平台和解之一）",
"49452709":"美国国务院暂停移民签证申请（315▲/432💬，政策突变引发广泛讨论）",
"49448210":"Qwen3.8-Flash-Next 发布（635▲/206💬，阿里开放权重模型继续高频迭代）",
"49451448":"蒂姆·柯瑞去世（601▲/197💬，《洛基恐怖秀》《小鬼当家》演员离世）",
"49447682":"Omarchy 的开发实践导致可预见的安全问题（282▲/415💬，热门 Linux 发行版被批安全流程失当）",
"49445727":"RAG 比你想的要简单（437▲/179💬，检索增强生成的去神秘化拆解）",
"49452990":"Tailcat——类似 netcat，但跑在 Tailscale 数据平面上（495▲/93💬，零配置内网连通新工具）",
"49446422":"Z.ai 确认 Ox Alpha 是 GLM 系列新模型并将开放权重（419▲/142💬，神秘打榜模型身份揭晓）",
"49448872":"法国 2026 年光纤覆盖率达 94.9%（298▲/225💬，欧洲宽带基建标杆）",
"49449576":"Twitter Viewer——无账号浏览 Twitter（334▲/166💬，X 封锁未登录访问后的民间绕道）",
"49450448":"Nebula Sans（356▲/132💬，新开源无衬线字体家族发布）",
"49452980":"一起持续中的 3D 打印机 AGPL 违规事件（327▲/148💬，开源许可证执行之困）",
"49448137":"比尔·盖茨：动荡的 AI 时代已经到来（182▲/243💬，行业元老对 AI 冲击的判断）",
"49454314":"Hugging Face 安全事件与后续之路（189▲/237💬，官方复盘入侵事件与整改计划）",
"49458161":"英伟达同意以 130 亿美元收购 Hugging Face（309▲/130💬，AI 开源枢纽被芯片巨头收入囊中）",
"49449749":"Taylor Farms：一家公司的供应链触角如何成为国家风险（246▲/164💬，食品供应集中度调查）",
"49450722":"GitHub 部分服务中断——已恢复（256▲/156💬，本周第二次大规模故障）",
"49453161":"关税成本：新一轮对加拿大关税给美国人带来的代价分析（175▲/204💬）",
"49444514":"美国过半成年人自认缺乏基本统计素养（135▲/201💬，数据素养调查）",
"49451313":"动荡的 AI 时代已经到来（181▲/167💬，盖茨同主题另一版本讨论）",
"49451343":"美国制裁意大利托管服务商 Autistici Inventati（154▲/176💬，激进主义托管商被列入名单）",
"49446748":"美国政府着手压制对数据中心的反对声音（173▲/148💬，算力扩张与社区抵制的博弈）",
"49454728":"GitHub 故障追踪器：GitHub 是不是废了？（193▲/117💬，社区自建可用性监测）",
"49450898":"要完成一个不属于你、只是 AI 建议的想法太难了（184▲/101💬，AI 辅助创作的动机困境）",
"49450188":"虚拟机挡不住具备网络攻击能力的 Agent（146▲/116💬，Agent 安全隔离边界之问）",
"49447600":"以色列出资设立的假美国智库试图操纵 AI 做宣传（239▲/42💬，信息战新形态）",
"49446210":"XCancel 与 Nitter 收到 X 公司的停止侵权函（281▲/3💬，第三方前端被法律清场）",
"49453510":"研究揭示联合健康的利润率是其对外宣称的四倍（168▲/77💬）",
"49452671":"CoMaps：在委内瑞拉无信号环境下指引救援队的离线地图应用（204▲/46💬）",
"49448665":"土耳其出土 1.1 万年前骑豹男子雕像（127▲/94💬，考古新发现）",
"49448560":"美加贸易战下美国卫生纸价格飙升（95▲/112💬，关税传导到日用品）",
"49457545":"亚马逊 Mechanical Turk 将于 9 月 30 日关停（169▲/58💬，众包标注时代落幕）",
"49445717":"编程的终结（80▲/117💬，AI 时代软件工程角色再讨论）",
"49454419":"Actinide 成为首家生产高含量低浓铀（HALEU）的初创公司（139▲/71💬，先进核燃料供应破局）",
"49449888":"PageRank 原理详解（120▲/81💬，经典算法可视化讲解）",
"49451675":"FDA 批准首个针对转移性胰腺癌的同类首创靶向疗法（169▲/43💬）",
"49445873":"Oldinsurancemaps.net 正式成为宪章项目（173▲/33💬，历史地图数字化）",
"49450353":"GLM-5.3-Flash 的智能、性能与价格分析（133▲/53💬，第三方独立评测）",
}
def z(o): return zh.get(o,'')

top20 = [{'oid':h['oid'],'title':h['title'],'zh':z(h['oid']),'points':h['points'],'comments':h['num_comments'],'hot':h['hot']} for h in raw[:20]]
top20_ids={h['oid'] for h in raw[:20]}
highc = sorted([h for h in raw if h['oid'] not in top20_ids], key=lambda h:h['num_comments'], reverse=True)[:10]
highc_out=[{'oid':h['oid'],'title':h['title'],'zh':z(h['oid']),'points':h['points'],'comments':h['num_comments']} for h in highc]
all_lst = [{'oid':h['oid'],'title':h['title'],'zh':z(h['oid']),'points':h['points'],'comments':h['num_comments'],'hot':h['hot']} for h in raw]

# ---- left column summary (HTML) ----
summary = """<p>本窗口（<span class="hl">8/26 10:00 → 8/27 10:00 CST</span>）Hacker News 共 <span class="hl">1000 条</span>新帖，工作日满载。<span class="hl">GLM-5.3-Flash</span> 以 <span class="hl">908▲/453💬</span> 加权登顶并同时拿下评论之王；当日最高原始分属 <span class="hl">「AWS 收购 DuckLabs」</span>（987▲/293💬）。一条是开放权重模型上新，一条是数据基础设施被巨头吞并——今日窗口的两个方向。</p>
<p><b>并购成为今日最硬的信号，且直插开源心脏</b>：<span class="hl">英伟达同意以 130 亿美元收购 Hugging Face</span>（309▲/130💬）与 <span class="hl">AWS 收购 DuckLabs</span>（987▲）同日落地；配套的 <span class="hl">「Hugging Face 安全事件与后续之路」</span>（189▲/237💬）官方复盘让这笔交易的时点更耐人寻味。AI 开源社区的两个中枢——模型集散地与嵌入式分析引擎——一天之内换了主人。</p>
<p><b>开放权重继续加速，中国模型占据前排</b>：<span class="hl">GLM-5.3-Flash</span>（908▲）登顶、<span class="hl">Qwen3.8-Flash-Next</span>（635▲）紧随、<span class="hl">Z.ai 确认 Ox Alpha 为 GLM 新成员并将开放权重</span>（419▲/142💬）揭开匿名打榜模型身份，再加第三方 <span class="hl">GLM-5.3-Flash 价格性能分析</span>（133▲）。同窗还有 <span class="hl">「RAG 比你想的要简单」</span>（437▲/179💬）与 <span class="hl">「虚拟机挡不住具备攻击能力的 Agent」</span>（146▲/116💬），把落地方法与安全边界一并摊开。</p>
<p><b>基础设施的脆弱与平台权力的账单同框</b>：<span class="hl">GitHub 服务中断（已恢复）</span>（256▲/156💬）叠加社区自建 <span class="hl">GitHub 故障追踪器</span>（193▲/117💬），中心化托管连续第二天被质疑；<span class="hl">Meta 就儿童伤害达成 170 亿美元和解</span>（484▲/462💬）、<span class="hl">XCancel/Nitter 收到 X 停止侵权函</span>（281▲）、<span class="hl">美政府压制数据中心反对声</span>（173▲/148💬）三帖则从司法、法务、政策三条线勾出平台权力的代价。排序方法：分数与评论 min-max 归一化加权（<span class="hl">0.6×分数 + 0.4×评论</span>），得热度 hot 降序取 Top20（中栏）；右栏为窗口全量 1000 条、按同热度排序、固定框内滚动——确保<span class="hl">零遗漏</span>。</p>"""

highc_html = "<p style='margin:0;'>" + " · ".join(
    f"<span class='hl'>{h['title'][:40]}</span>（{h['comments']}💬 / {h['points']}▲）" for h in highc_out[:3]
) + "</p><p style='margin:6px 0 0;color:#6b6357;font-size:12px;'>「高分低讨论」之外的有效信号，均可在右栏翻到。</p>"

out = {
    "window_label": "2026-08-26 10:00 → 2026-08-27 10:00 (CST)",
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
print("written /Users/peotry/WorkBuddy/2026-07-09-13-58-54/hn_window.json")
