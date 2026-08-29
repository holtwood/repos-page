# 审计方法与字段定义

## 数据来源（2026-08-19 实时采样）

- 账号与组织仓库清单：`gh repo list holtwood --limit 100`、`gh api orgs/{org}/repos?per_page=100`
- Fork 上游：`gh api repos/holtwood/{repo}` 的 `parent.full_name`
- ahead/behind：`gh api repos/{upstream}/compare/{branch}...holtwood:{repo}:{branch}`
- 贡献者审计：`gh api repos/{repo}/contributors`
- 链接有效性：HTTP 状态码 + `Location` 头（`curl -sI`），区分 200/301/404
- Fork ahead 提交性质：抽样读取 compare API 返回的 commit message 与作者

## 每个仓库的记录字段

- 当前规范链接（canonical URL，即迁移后的最终归属地址）
- 所属账号或组织；公开/私有状态
- 属性：原创 / Fork / 迁移 / AI 翻译 / 组织项目
- Fork 上游地址与 ahead/behind 快照
- 主语言；AI Infra 相关性与学习优先级（P0–P3）
- 建议阅读范围（Fork 类）
- 简历可用性
- 最后审计日期

## 约束

- 私有仓库名称与描述不进入公开文档。
- Fork 与 AI 翻译内容不标为个人原创。
- 组织仓库只有通过 contributors 审计确认个人主导后，才在简历语境中表述为个人项目。
- ahead/behind 与链接状态均为审计日快照，随时间漂移；引用时注明日期。
