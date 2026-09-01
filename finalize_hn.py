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

# ---- zh translations (top 40 by hot, 2026-09-01) ----
zh = {
"49514878":"谷歌已从 Chrome 应用商店下架全部 MV2 扩展，uBlock Origin 在列——Manifest V2 时代正式终结，拦截类扩展生态被强制迁移（591\u25b2/452\U0001f4ac 登顶兼评论之王）",
"49510514":"Playa Phone：一部为「离网/沙漠场景」设计的手机——反智能机潮流的硬件实验（517\u25b2/188\U0001f4ac）",
"49507822":"OpenShot 4.0 发布——开源视频剪辑器大版本更新（538\u25b2/126\U0001f4ac）",
"49508982":"苹果被 AI 需求打了个措手不及：Mac Mini 与 Mac Studio 供不应求——本地跑大模型正在改写桌面机销量（312\u25b2/365\U0001f4ac）",
"49511856":"我把家里的安防摄像头改成了自动鸟类识别系统——边缘视觉模型的家用改造（375\u25b2/98\U0001f4ac）",
"49506819":"拆解 Claude Code Opus 5 的 Auto 模式——逆向 AI 编程工具的自动路由/降档策略（349\u25b2/113\U0001f4ac）",
"49506182":"12TB 的 Steam「teraleak」泄露：十余年 PC 游戏历史资料流出（365\u25b2/79\U0001f4ac）",
"49508506":"我怀疑军队超市的冷柜被黑了——一次从异常温度日志切入的实地排查（263\u25b2/156\U0001f4ac）",
"49504905":"互联网集中化与 NAT 的「原罪」——地址稀缺如何塑造了今天的中心化格局（191\u25b2/149\U0001f4ac）",
"49505217":"用一根网线直连传文件——最朴素的点对点传输实践（157\u25b2/168\U0001f4ac）",
"49505310":"OpenClaw 2.0，意外诞生——开源 Agent 项目的非计划性大版本（145\u25b2/171\U0001f4ac）",
"49506142":"uv：对 wheel 缓存里的所有文件做去重——Python 包管理器的磁盘占用优化（206\u25b2/100\U0001f4ac）",
"49505219":"2.4 亿域名的自动补全，P99 0 毫秒*——极致延迟工程实录（218\u25b2/83\U0001f4ac）",
"49511534":"RavynOS：基于 Darwin、FreeBSD 与苹果开源组件的预 alpha 系统（176\u25b2/106\U0001f4ac）",
"49512856":"最不怕 AI 的工作可能是写作——反直觉的职业替代论（114\u25b2/165\U0001f4ac）",
"49512975":"一个 HTML 文件里的可漫游 ASCII 赛博朋克城市（视频）（222\u25b2/30\U0001f4ac）",
"49508317":"把 Agent 记忆做成一种文件格式——记忆持久化的规范化尝试（165\u25b2/85\U0001f4ac）",
"49510000":"ChatGPT 工作工具与 Skill 参考手册——官方工具/技能体系的文档（189\u25b2/51\U0001f4ac）",
"49508290":"一次 CVE 争议——漏洞编号该不该发、由谁裁定（185\u25b2/44\U0001f4ac）",
"49511917":"康拉德·楚泽博物馆因资金短缺关闭——计算机先驱的纪念馆停摆（151\u25b2/75\U0001f4ac）",
"49506148":"自从被剥夺行星地位，冥王星的拥护者们一直在抗争（172\U0001f4ac/51\u25b2）",
"49510532":"乐天 Kobo 销量翻倍，重返美国线下零售（106\U0001f4ac/93\u25b2）",
"49509876":"Omarchy：1Password 与 37signals 成为杰出企业赞助方（99\U0001f4ac/55\u25b2）",
"49505351":"欧盟已开始执行《AI 法案》：首批问询函发往模型提供方（99\U0001f4ac/47\u25b2）",
"49511720":"这家 7-Eleven 可能就是你「持有」的（也是它为何看起来这么破）——特许加盟经济剖析（91\U0001f4ac/73\u25b2）",
"49508664":"AI 写的代码依然是你的代码——责任归属不因工具而转移（89\U0001f4ac/54\u25b2）",
"49505288":"加州大学伯克利分校无限期暂停国际学生工作许可（86\U0001f4ac/104\u25b2）",
"49505014":"为什么我失去热情、什么都不想做？——倦怠讨论（86\U0001f4ac/94\u25b2）",
"49512618":"如今的孩子们——代际观察随笔（83\U0001f4ac/62\u25b2）",
"49506805":"SK 海力士 CEO：内存芯片短缺将持续到 2030 年（79\U0001f4ac/63\u25b2）",
"49506978":"ReactOS 0.4.16 发布——开源 Windows 兼容系统更新",
"49515830":"在 Linux 上运行 macOS 软件——兼容层折腾",
"49512574":"你改我湖名，我搬走托管——一次以迁移表达抗议的实操",
"49512789":"实习教师因一条私人 Snapchat 消息被捕",
"49516199":"一项影响深远的「拖延症」研究被指存在数据造假",
"49507121":"研究：蓝光对眼睛分辨精细细节的能力损害最大",
"49505040":"Flock Safety 备受争议的 CEO 尝到了自己的药——监控公司创始人被反向监控",
"49508059":"可塑软件 = 稳固底座 + 自定义代码——软件形态的第三条路",
"49510511":"C++26：标准库加固（hardening）实验",
"49510302":"马克思、凯恩斯与 AI——用两套经典经济学框架看 AI 冲击",
}
def z(o): return zh.get(o,'')

top20 = [{'oid':h['oid'],'title':h['title'],'zh':z(h['oid']),'points':h['points'],'comments':h['num_comments'],'hot':h['hot']} for h in raw[:20]]
top20_ids={h['oid'] for h in raw[:20]}
highc = sorted([h for h in raw if h['oid'] not in top20_ids], key=lambda h:h['num_comments'], reverse=True)[:10]
highc_out=[{'oid':h['oid'],'title':h['title'],'zh':z(h['oid']),'points':h['points'],'comments':h['num_comments']} for h in highc]
all_lst = [{'oid':h['oid'],'title':h['title'],'zh':z(h['oid']),'points':h['points'],'comments':h['num_comments'],'hot':h['hot']} for h in raw]

# ---- left column summary (HTML) ----
summary = """<p>本窗口（<span class="hl">8/31 10:00 → 9/1 10:00 CST</span>）Hacker News 共 <span class="hl">1092 条</span>新帖，为近期最高。<span class="hl">「谷歌从 Chrome 应用商店下架全部 MV2 扩展、uBlock Origin 在列」</span>以 <span class="hl">591\u25b2/452\U0001f4ac</span> 同时拿下分数与评论双榜首——Manifest V2 时代正式终结，浏览器拦截生态被平台方一次性清场，这是今日无争议的头条。</p>
<p><b>「AI 吃掉硬件」是今天最硬的一条暗线。</b><span class="hl">「苹果被 AI 需求打了个措手不及：Mac Mini 与 Mac Studio 供不应求」</span>（312\u25b2/365\U0001f4ac，当日评论第二）撞上 <span class="hl">「SK 海力士 CEO：内存短缺持续到 2030 年」</span>（79\U0001f4ac）——本地跑模型的算力饥渴，已经从数据中心一路传导到桌面整机与内存现货。<span class="hl">「Xcena 式存算靠近」的对应物今日缺席，但 「uv 对 wheel 缓存去重」（206\u25b2）与「2.4 亿域名 P99 0ms 自动补全」（218\u25b2）</span>说明另一半工程注意力仍在抠资源与延迟。</p>
<p><b>「Agent 工程化」持续密集。</b><span class="hl">「拆解 Claude Code Opus 5 的 Auto 模式」</span>（349\u25b2/113\U0001f4ac）、<span class="hl">「把 Agent 记忆做成一种文件格式」</span>（165\u25b2/85\U0001f4ac）、<span class="hl">「ChatGPT 工作工具与 Skill 参考手册」</span>（189\u25b2）、<span class="hl">「OpenClaw 2.0 意外诞生」</span>（145\u25b2/171\U0001f4ac）四帖合流——社区正在把 Agent 从「能跑」推向「可解释、可持久化、可复用」。同日 <span class="hl">「AI 写的代码依然是你的代码」</span>（89\U0001f4ac）与 <span class="hl">「欧盟已开始执行 AI 法案，首批问询函发往模型提供方」</span>（99\U0001f4ac）把责任与合规摆回台面。排序方法：分数与评论 min-max 归一化加权（<span class="hl">0.6\u00d7分数 + 0.4\u00d7评论</span>），得热度 hot 降序取 Top20（中栏）；右栏为窗口全量 1092 条、按同热度排序、固定框内滚动——确保<span class="hl">零遗漏</span>。</p>"""

highc_html = "<p style='margin:0;'>" + " · ".join(
    f"<span class='hl'>{h['title'][:40]}</span>（{h['comments']}💬 / {h['points']}▲）" for h in highc_out[:3]
) + "</p><p style='margin:6px 0 0;color:#6b6357;font-size:12px;'>「高分低讨论」之外的有效信号，均可在右栏翻到。</p>"

out = {
    "window_label": "2026-08-31 10:00 → 2026-09-01 10:00 (CST)",
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
