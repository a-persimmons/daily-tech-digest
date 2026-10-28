# -*- coding: utf-8 -*-
import json

# ---- HF: 当日批次 top12（直连 api，date=2026-10-28） ----
hf_raw = json.load(open('/Users/peotry/WorkBuddy/2026-07-09-13-58-54/hf_1028.json', encoding='utf-8'))
rows = []
for p in hf_raw:
    paper = p.get('paper', {})
    rows.append({
        'id': paper.get('id'),
        'title': paper.get('title'),
        'upvotes': paper.get('upvotes') or 0,
        'publishedAt': (paper.get('publishedAt') or '')[:10],
    })
rows.sort(key=lambda x: -x['upvotes'])
hf = rows[:12]
json.dump(hf, open('/Users/peotry/WorkBuddy/2026-07-09-13-58-54/hf_data.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('hf total:', len(rows), '-> top12')

C = {}
C['date'] = '2026-10-28'

C['hero'] = [
    {
        "url": "https://news.ycombinator.com/item?id=50257325",
        "meta": "HN 622▲/618💬 · 今日评论第一、热度第二 · Hacker News 讨论页",
        "title": "AI promised less work. I've never worked more",
        "zh": "「AI 承诺更少的工作。可我从来没有这么忙过」——618 条评论让它成为今天 HN 讨论量第一。它不是反 AI 宣言，而是一线工程师的体感记账：产出门槛降低之后，需要审、需要改、需要背的东西成倍增加，人被挪到了流水线的末端而不是上游。同一语境里还有《AI 时代的人月神话》（440▲/309💬）与《软件也许正在变糟，但它曾经糟得可怕》（302▲/317💬）。"
    },
    {
        "url": "https://news.ycombinator.com/item?id=50261319",
        "meta": "HN 765▲/463💬 · 今日热度第一 · DeepMind 官方博客",
        "title": "Genie 4 — a new generation of world simulation",
        "zh": "DeepMind 的 Genie 4 以 765▲/463💬 拿下今天的热度第一、评论第二：世界模拟从「生成一段视频」推进到「可交互、可推演的环境」。能力侧的峰值与体感侧的抱怨同一天登顶，是本期最刺眼的一组对照。学术侧的同频证据在 Hugging Face：《Rollback：世界模型中的经验回溯用于策略改进》（28▲）与《ThinkWorld：世界想象强化动力学链推理》（18▲）。"
    },
    {
        "url": "https://news.ycombinator.com/item?id=50260814",
        "meta": "HN 483▲/266💬 · 今日分数前五 · 斯坦福日报",
        "title": "Anthropic trained Claude on illegally obtained Stanford professors' books",
        "zh": "《Anthropic 用非法获取的斯坦福教授著作训练了 Claude》：训练数据争议第一次落到一个有名有姓的机构与一批有名有姓的作者身上，而不是抽象的「互联网」。同栏《我的数据被用于模型训练了吗？》（215▲/99💬）是用户自己来找答案，《Roblox 未经询问下载了 145GB 模型》（460▲/268💬）说明不告而取已从模型公司扩散到平台公司。今天是「抓取者被追着要收据」的一天。"
    },
]

C['insights'] = [
    {
        "src": "兑现落差被同时量出来",
        "title": "能力的峰值和体感的谷底同一天登顶：Genie 4 拿下热度，「我更忙了」拿下评论",
        "text": "四个源给出的是同一条曲线的两端。HN 上 Genie 4（765▲/463💬）代表能力侧再破一层——世界模拟进入可交互阶段，Hugging Face 当日批次里《Rollback：世界模型中的经验回溯》（28▲）与《ThinkWorld》（18▲）在学术侧同频；另一端是《AI 承诺少干活。可我从来没有这么忙过》（622▲/618💬）以评论第一压过它，《AI 时代的人月神话》（440▲/309💬）给出理论解释。GitHub 侧的答案不再是更大的模型而是更规矩的接口：Nutlope/hallmark 以 +2,830★ 登顶，做的正是「反 AI 味」的设计语言约束。Product Hunt 当日榜首 TheySaid 4.0（329▲）卖的是「在你构建的地方就看见用户反应」——把验证前置，正是为体感落差买单。这条线的共同结论是：瓶颈已经不在生成，在确认。"
    },
    {
        "src": "默认许可正在失效",
        "title": "抓取者第一次被逐个点名：训练数据、模型下载、公开消息三个口径同时收紧",
        "text": "HN 今天把「不告而取」拆成了三个层次：训练数据层面《Anthropic 用非法获取的斯坦福教授著作训练了 Claude》（483▲/266💬）+《我的数据被用于模型训练了吗？》（215▲/99💬）；抓取行为层面《Roblox 未经询问下载了 145GB 模型（含成人内容）》（460▲/268💬）；公开性层面《维基百科对 AI 生成内容的清理》（460▲/211💬）与《Discord 将允许任何人通过谷歌搜到公开服务器的消息》（273▲/143💬）。治理侧的回应是《警方正用 AI 以「行为可疑」为由拦停司机》（347▲/277💬）。四源里唯一在补洞的是 Hugging Face 的《HABIT-Bench》（11▲）与《Memory Tax》（1▲）——开始量化 agent 记忆到底值多少。共同结论：默认许可正在失效，明示同意正在从道德要求变成工程要求。"
    },
    {
        "src": "可自己跑、自己验成为刚需",
        "title": "手艺层与秘密层同时加厚：Ghostty 拿了分数第一，政府秘密裁决拿了分数第二",
        "text": "今天的数字很整齐：Ghostty 1.4（815▲）是分数第一，《美国政府藏着一份关于它如何监视美国人的秘密法院裁决》（814▲）是分数第二，两者只差 1 分。手艺这条线今天格外厚实——Python 实验性 JIT 被移除（456▲/246💬）、有限单群分类在 Lean 中被形式化（178▲/45💬）、Gforth 1.0（159▲/17💬）、四个月的 Zig（81▲/49💬）、我还在教 OpenGL ES 3.0（138▲/86💬）、JetBrains IDE 转由 libghostty 驱动（65▲/10💬）；GitHub 侧 obra/superpowers（+617★）与 affaan-m/ECC（+1,165★）继续给 agent 加装方法论骨架。秘密这条线同样密集：DOGE 操盘手掏空 USAID（217▲/135💬）、据称的以色列间谍公司盯上 Starlink 用户（131▲/30💬）。Product Hunt 里 Off Grid AI（101▲，手机与电脑上的私有 AI）与 Survival LLM（211▲/108💬）是同一姿态的产品化版本。共同结论：当平台与机构都不再可信，可自己跑、自己验的东西就成了刚需。"
    },
]

C['gh_tr'] = {
    "Nutlope/hallmark": "反 AI 味设计技能包，给 Claude Code、Cursor 与 Codex 用——用一套可被机器执行的审美约束，压掉 agent 生成界面里那种千篇一律的滑腻感。",
    "HKUDS/DeepTutor": "DeepTutor：终身个性化辅导。把长期记忆与学习画像接进 AI 家教，让辅导跨会话累积而不是每次从零开始。",
    "makecindy/cindy": "「想到，就能做到。」开箱即用的开源 AI Agent，主打不折腾配置就能跑起来。",
    "pbakaus/impeccable": "给你的编码 agent 用的设计词汇表：用 polish 与 bolder 去引导，用 critique 与 audit 去评审，顺手把 AI 味拦下来。",
    "elayadesign/ai-design-skills": "给 AI 编码助手用的设计技能集合，把设计规范打包成 agent 可直接调用的技能。",
    "JetBrains/thinkrail": "在一款轻量、真实、会围绕你的工作方式自我定制的 IDE 里做 vibe coding。",
    "affaan-m/ECC": "agent harness 性能优化体系：技能、直觉、记忆、安全与研究优先的开发流程，全部围绕把 harness 跑快。",
    "gitroomhq/postiz-app": "终极 agentic 社媒排期工具，把发布流程交给 agent 自动排程。",
    "togg53192-cmd/jailbreaks": "我收集的全部越狱提示词，一次列完。",
    "nightly-labs/openbot": "本地优先的桌面工作区，用于常驻 AI 队友：让 Codex、Claude、Grok 各有独立工作区、任务与上下文。",
    "obra/superpowers": "一套 agentic 技能框架与软件开发方法论，确实能跑通的那一种。",
}

C['ph_tr'] = {
    "TheySaid 4.0": "就在你构建的地方，看见用户会怎么反应。",
    "Overmind": "面向持续学习的开源平台。",
    "Orbit": "别再无休止刷屏了。每一次解锁应用都要先挣得。",
    "Spacesheep": "未来的文档：由 AI 生成，给你的团队阅读。",
    "SavorApp_AI": "记下真正重要的事，把你的意图往前推。",
    "Notra": "Notra 是一款 GEO 工具，帮你在 AI 搜索里排上去。",
    "Nuvio 5.0": "把你的财务杂务交给你的 AI agent。",
    "iPad mini 8": "OLED、A20 Pro 与 IP67——苹果最小的那台 iPad。",
    "PulseDev": "在 localhost 上点任意一个界面 bug，你的 AI agent 就去修好它。",
    "Arcade Controller Pro": "一款没有摇杆、自带屏幕的格斗手柄。",
    "NuPlay": "AI 转型，跑在同一个会自我改进的平台之上。",
    "Off Grid AI": "跑在你手机与电脑上的私有 AI。",
}

C['hf_tr'] = {
    "2610.34283": "ChronoReplay：流式空间智能只有一个问答接口是不够的（34▲，当日最高）",
    "2610.36729": "Hy-Nomas：走向自由形式的交互式世界生成（29▲）",
    "2610.36068": "Rollback：世界模型中的经验回溯用于策略改进（28▲）",
    "2610.36456": "LociArt：自由风格局部视频风格化的统一范式（22▲）",
    "2610.37666": "ThinkWorld：世界想象强化动力学链推理（18▲）",
    "2610.24520": "HABIT-Bench：从纵向弱证据评估 agent 记忆中的习惯养成（11▲）",
    "2610.33624": "RSI Arena：带人类反馈的递归自我改进（7▲）",
    "2610.36269": "跨模态 steering vector 在图像与文本生成中同时存在（6▲）",
    "2610.35724": "MatAnyone-E：用稀疏记忆传播做高效高分辨率视频抠像（5▲）",
    "2610.35439": "Omni-InteractScope：连续全模态流中的主动式 agentic 交互基准（4▲）",
    "2610.34491": "我该选哪一档努力程度？论 LLM agent 中推理努力的经济学（2▲）",
    "2610.37341": "CodeCap-Bench：代码能当好视频字幕吗？（1▲）",
}

C['gh_summary'] = """<p>今日 GitHub Trending 共 <span class="hl">11 条</span>（按页面 <span class="hl">&lt;article&gt;</span> 计数核对，周三短榜，如实呈现不补数）。榜首是 <span class="hl">Nutlope/hallmark +2,830★</span>——一个<b>反 AI 味</b>的设计技能包，给 Claude Code、Cursor、Codex 用，把审美约束写成 agent 能执行的规则。这句话本身就是今天的总结：当生成变得无限便宜，稀缺的是「不像机器做的」。</p>
<p>其余条目基本在做同一件事——<b>给 agent 装上规矩、记忆与工位</b>。<span class="hl">affaan-m/ECC +1,165★</span>（harness 性能优化体系）、<span class="hl">obra/superpowers +617★</span>（agentic 技能框架与方法论）、<span class="hl">makecindy/cindy +1,465★</span>（开箱即用的开源 agent）、<span class="hl">JetBrains/thinkrail +1,204★</span>（会自我定制的轻量 IDE）属于规矩层；<span class="hl">nightly-labs/openbot +777★</span>（本地优先的常驻 AI 队友工作区）与 <span class="hl">HKUDS/DeepTutor +1,598★</span>（终身个性化辅导）属于记忆层；<span class="hl">gitroomhq/postiz-app +951★</span> 是把发布流程整条交给 agent。设计侧形成一个小集群：hallmark、<span class="hl">pbakaus/impeccable +1,449★</span>（给编码 agent 的设计词汇表）、<span class="hl">elayadesign/ai-design-skills +1,395★</span> 三条同日进榜。</p>
<p>对照 HN 今天的《AI 承诺少干活。可我从来没有这么忙过》（622▲/618💬）：GitHub 上没有一个项目在宣称「更少的工作」，全在解决「更多产出之后怎么收口」——扫描、评审、约束、记忆、工位。<span class="hl">togg53192-cmd/jailbreaks +902★</span> 把越狱提示词整包公开，是这条线另一端的注脚：能力开放之后，边界也得公开。</p>"""

C['ph_summary'] = """<p>Product Hunt 当日（PT <span class="hl">2026-10-27</span>）共 <span class="hl">12+ 款</span>精选，此处列前 <span class="hl">8</span>（按当日票数降序）。榜首是 <span class="hl">TheySaid 4.0（329▲）</span>——「就在你构建的地方，看见用户会怎么反应」：把用户反馈的采集挪到开发流程内部，是今天最直白的一次<b>验证前置</b>。</p>
<p>第二条线是<b>注意力与意图的自我管理</b>。<span class="hl">Orbit（208▲）</span>要你「每一次解锁应用都先挣得」，<span class="hl">SavorApp_AI（144▲）</span>做「记下真正重要的事」——两者都在对抗同一个东西：无限生成带来的无限分心。第三类是<b>文档与知识的机器化</b>：<span class="hl">Spacesheep（196▲）</span>做「由 AI 生成、给团队阅读的未来文档」，<span class="hl">Notra（140▲）</span>做 GEO——帮你在 AI 搜索结果里被排到前面。这一条与 HN 今天的《维基百科对 AI 生成内容的清理》（460▲/211💬）恰好构成一对：一边在往里灌，一边在往外清。</p>
<p>第四类是<b>把具体岗位外包给 agent</b>：<span class="hl">Nuvio 5.0（113▲）</span>把财务杂务交给 AI agent，<span class="hl">PulseDev（112▲）</span>点一下 localhost 上的界面 bug 就让 agent 去修——后者是「agent 修 UI」这条线最落地的一次产品化。硬件侧今天有 <span class="hl">iPad mini 8（112▲）</span>，与 HN 的 M6 iMac、M6 MacBook Pro 撞在同一天。开源侧 <span class="hl">Off Grid AI（101▲）</span>做手机与电脑上的私有 AI，与 HN 的 Survival LLM（211▲/108💬）是同一个姿态。</p>"""

C['papers_summary'] = """<p>Hugging Face Daily Papers <span class="hl">2026-10-28 当日批次</span>共 <span class="hl">20 篇</span>，此处按 upvotes 降序列前 <span class="hl">12</span>。今天的主语只有一个：<b>世界模型</b>。榜首 <span class="hl">ChronoReplay（34▲）</span>提出流式空间智能不该只有一个问答接口；<span class="hl">Hy-Nomas（29▲）</span>做自由形式的交互式世界生成；<span class="hl">Rollback（28▲）</span>把「经验回溯」引入世界模型以改进策略；<span class="hl">ThinkWorld（18▲）</span>用世界想象强化动力学链推理。四篇连起来是一条完整链路：生成世界 → 在世界里回溯 → 用想象驱动推理。</p>
<p>第二条线是<b>给 agent 的记忆与努力算账</b>，也是今天最值得注意的方法论转向。<span class="hl">HABIT-Bench（11▲）</span>用纵向弱证据评估 agent 记忆能否养成习惯；同批的 <span class="hl">Memory Tax（1▲）</span>直接解剖 agent 记忆的净价值；<span class="hl">《我该选哪一档努力程度？》（2▲）</span>把推理努力当成一项经济决策来建模。这三条与 HN 今天的《AI 承诺少干活。可我从来没有这么忙过》（622▲/618💬）、《AI 时代的人月神话》（440▲/309💬）指向同一个问题：投入的算力与产出之间到底有没有正比。</p>
<p>其余落在多模态与具身评测：<span class="hl">LociArt（22▲）</span>做局部视频风格化，<span class="hl">RSI Arena（7▲）</span>带人类反馈做递归自我改进，<span class="hl">跨模态 steering vector（6▲）</span>证明图像与文本生成中共用同一类控制向量，<span class="hl">MatAnyone-E（5▲）</span>做高效高分辨率抠像，<span class="hl">Omni-InteractScope（4▲）</span>评测连续全模态流里的主动交互，<span class="hl">CodeCap-Bench（1▲）</span>问代码能不能当好视频字幕。整体士气：世界模型进入可交互阶段，但评测侧已经在追问它值不值。</p>"""

C['note_hf'] = "数据源：huggingface.co/api/daily_papers?date=2026-10-28（当日批次）。本机直连官方 API（清除所有 *PROXY* 环境变量 + 浏览器 UA）HTTP 200，返回 20 篇，按 paper.upvotes 降序取前 12 列示，未沿用任何历史批次。"

json.dump(C, open('/Users/peotry/WorkBuddy/2026-07-09-13-58-54/content.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written content.json + hf_data.json')
