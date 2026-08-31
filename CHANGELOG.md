# Changelog

本文件遵循 [Keep a Changelog](https://keepachangelog.com/) 格式。

## [Unreleased] — 2026-08-19

### Changed
- 数据快照更新（2026-08-31）：ahead/behind 与链接状态已刷新
- 账号迁移:LessUp → holtwood(repos-page);README 主页化 + GitHub Pages 部署
- 新增 README 主要项目精选区(render_featured)与 GitHub Pages 文档站部署(pages.yml)

- 恢复本仓库作为**独立仓库导航中心**的职责：README 从"已合并跳转页"重写为导航首页，
  含账号概览、目录结构与职责边界表。
- 新增 `catalog/` 八个分类文件（lessup-owned / forks-and-translations / organizations /
  original-projects / ai-infra / hpc-and-transferable / tools-and-unrelated /
  retired-and-migrated），基于 2026-08-19 GitHub API 实时数据。
- Fork 目录记录 22 个 Fork 的上游、ahead/behind 快照与中文注释性质说明。
- 组织仓库全部通过 contributors 审计，确认个人主导的项目清单。
- 新增 `methodology.md` 记录审计方法与字段定义。

### Removed

- 删除被 `catalog/` 取代的旧扁平分类文件：ai-infra-core.md、ai-infra-auxiliary.md、
  hpc-and-systems.md、personal-projects.md、tools-and-others.md、repo-index.md、
  learning-path.md（与 ai-infra-interview-prep 中同名文件逐字节相同，经 diff 验证；
  learning-path 属于学习计划，保留在 ai-infra-interview-prep）。

### Unchanged

- `deep-dives/`（21 个仓库深读笔记）保留在本仓库，作为唯一事实来源；
  ai-infra-interview-prep 中的相同副本已在该仓库删除（见其 CHANGELOG）。
