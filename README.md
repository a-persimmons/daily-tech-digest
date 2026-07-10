# 每日技术热点速递 Archive

Hacker News × GitHub Trending 每日技术热点速览的静态归档站，自动部署到 GitHub Pages。

## 结构

- `index.html` — 极简归档首页，列出各期速递
- `今日技术热点速览_YYYY-MM-DD.html` — 每日生成的结果网页
- `.github/workflows/deploy.yml` — 推送 `main` 分支时自动部署 GitHub Pages

## 本地仓库

本地克隆位于：`/Users/peotry/daily-tech-digest`

每日自动化任务生成新报告后，复制到该目录、更新 `index.html` 的列表、提交并推送，Pages 即自动更新。

## 访问

部署完成后，归档站地址为：`https://a-persimmons.github.io/daily-tech-digest/`
