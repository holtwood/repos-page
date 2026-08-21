# GitHub Repos Hub 数据驱动化升级 — 设计文档

日期：2026-08-21
状态：待审阅
范围：本仓库（LessUp/github-repos-hub）的结构升级，不含 deep-dives 内容重写。

## 1. 背景与目标

当前仓库是个人全部 GitHub 仓库的盘点、分类与导航中心，包含 `catalog/`（8 个分类文件）、
`deep-dives/`（21 篇 Fork 深读笔记）、`methodology.md`（审计方法）、`CHANGELOG.md`。

现状痛点：

- **数据快照会漂移**：fork ahead/behind、链接状态、仓库数量均为 2026-08-19 手工审计快照，
  随上游变动而过时，无机制自动刷新。
- **数据与展示耦合**：仓库元数据（上游、ahead/behind、语言、优先级）以 markdown 表格形式
  散落在多个分类文件中，无法程序化读取，也无法复用（README 概览表、docsify 侧边栏、
  徽章均需人工同步）。
- **无阅读型站点**：内容仅能以 GitHub 目录方式浏览，无搜索与侧边栏导航。

目标：

1. 引入 `data/repos.json` 作为仓库元数据的**唯一事实来源**（single source of truth）。
2. 用生成器脚本从 JSON 渲染 catalog 表格、README 概览表、徽章、docsify 侧边栏、CHANGELOG。
3. 用 GitHub Actions 每周自动审计并**自动提 PR**，解决快照漂移。
4. 用 docsify 将 markdown 变为可浏览、可搜索的静态站（GitHub Pages）。

## 2. 借鉴的顶级开源实践（研究结论）

- **vLLM 数据驱动范式**：`mkdocs.yaml` 中配置 `gen-files` 插件，用 `generate_examples.py`、
  `generate_argparse.py` 等脚本在构建期生成文档内容；CI 检测 docs 变更、自动打 `documentation`
  标签。→ 本设计复刻"脚本生成内容"模式。
- **awesome-list 生态**：统一表格、shields.io 徽章（分组、可点击、宁缺毋滥）、TOC、贡献规范。
- **Dependabot 式自动 PR**：自动化以"新分支 + PR"形式提出，人 review 后合并，不直接写 main。
- **文档站选型**：Material for MkDocs 已于 2025-11 进入维护模式（新项目不推荐）；Docusaurus
  需 React/JS 工程化，对纯中文 markdown 导航中心过重。选 **docsify**（零构建、纯前端、
  保留 markdown 为真源），内置全文搜索。

## 3. 目标架构

```
github-repos-hub/
├── README.md                    # 导航首页；账号概览表 + 徽章由生成器渲染
├── data/
│   └── repos.json               # ★ 唯一事实来源（手工或审计脚本维护）
├── scripts/
│   ├── generate.py              # JSON → markdown 表格/徽章/侧边栏/CHANGELOG
│   └── audit.py                 # gh api 拉取 → 刷新 repos.json
├── catalog/
│   ├── *.md                     # 8 个分类文件：手工策略段落 + 自动表格（占位符分界）
├── deep-dives/                  # 21 篇深读笔记，纯人工内容，不生成
├── index.html                   # docsify SPA 入口（根目录）
├── _sidebar.md                  # docsify 侧边栏（生成器产出）
├── _navbar.md                   # docsify 顶栏（可选，手工）
├── .nojekyll                    # 让 GitHub Pages 跳过 Jekyll
├── .github/
│   └── workflows/audit.yml      # 每周自动审计 → 自动提 PR
├── docs/superpowers/specs/      # 设计文档存放处
├── methodology.md
└── CHANGELOG.md
```

职责边界：

| 组件 | 职责 | 维护者 |
|------|------|--------|
| `data/repos.json` | 仓库元数据事实源 | 手工 + audit.py |
| `scripts/generate.py` | 由 JSON 渲染所有自动内容 | 手工 |
| `scripts/audit.py` | 从 GitHub API 刷新 JSON | 手工 |
| `catalog/*.md` 占位符外段落 | 策略文字、叙事性列表 | 手工 |
| `catalog/*.md` 占位符内表格 | 结构化数据视图 | 生成器 |
| `deep-dives/` | 深读笔记 | 手工 |
| `index.html` / `_sidebar.md` | 静态站 | 生成器（侧边栏）+ 手工（入口） |
| `audit.yml` | 每周调度 | 手工 |

## 4. 数据模型 `data/repos.json`

### 顶层结构

```json
{
  "audited_at": "2026-08-19",
  "generator_version": "0.1.0",
  "accounts": {
    "LessUp":       { "public": 31, "private": 1, "forks": 22, "note": "个人" },
    "open-infra-ai":{ "public": 7,  "private": 0, "forks": 0,  "note": "AI Infra 作品集" },
    "open-genomics":{ "public": 7,  "private": 5, "forks": 0,  "note": "生物信息与 C++ 工程" },
    "vibe-knight":  { "public": 14, "private": 1, "forks": 0,  "note": "实验性与工具" }
  },
  "repos": [
    {
      "name": "cuda-samples",
      "account": "LessUp",
      "visibility": "public",
      "property": "fork",
      "upstream": "NVIDIA/cuda-samples",
      "ahead": 26,
      "behind": 0,
      "language": "C++",
      "priority": "P1",
      "categories": ["forks-and-translations"],
      "notes": {
        "forks-and-translations": "CUDA 特性官方示例；只跑 0_Introduction、2_Concepts_and_Techniques、矩阵乘法相关样例"
      },
      "resume": false,
      "links_ok": true,
      "links": { "url": "https://github.com/LessUp/cuda-samples", "status": 200 }
    }
  ],
  "retired": [
    {
      "old": "LessUp/sgemm-optimization",
      "status": "404",
      "note": "主页移除展示；SGEMM 主题由 SGEMM_CUDA 与 open-infra-ai/cuda-foundations 覆盖"
    }
  ]
}
```

### 字段定义

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 仓库名（不含 owner） |
| `account` | 是 | 所属账号/组织：LessUp / open-infra-ai / open-genomics / vibe-knight |
| `visibility` | 是 | 仅 `public`（`repos[]` 只含公开仓库，私有仓库名称不落库，见下方约束） |
| `property` | 是 | original / fork / translation / org-project / migrated / retired |
| `upstream` | 否 | 仅 fork/translation：`owner/repo` 上游地址 |
| `ahead` / `behind` | 否 | 仅 fork：compare API 快照，审计日有效 |
| `language` | 否 | 主语言（GitHub API `language` 字段） |
| `priority` | 否 | P0–P3 / 无。见 methodology.md |
| `categories` | 是 | 所属分类文件 slug 数组，一个仓库可属多个分类（如 fq-compressor） |
| `notes` | 否 | **按分类的对象** `{slug: 说明文字}`。跨分类仓库各分类说明不同（如 fq-compressor：original-projects 下是"简历用法"、hpc-and-transferable 下是"能力信号"）。校验：`categories` 必须与 `notes` 的 key 集一致（除非某分类表格无说明列） |
| `resume` | 否 | 是否简历可用 |
| `links_ok` | 否 | 链接有效性布尔 |
| `links` | 否 | 审计时采集的链接 URL 与 HTTP 状态 |

### 分类 slug 与文件映射

| slug | 文件 | 自动表格范围 |
|------|------|-------------|
| `lessup-owned` | catalog/lessup-owned.md | 9 个原创公开仓库全表自动 |
| `forks-and-translations` | catalog/forks-and-translations.md | 22 个 fork 全表自动 |
| `organizations` | catalog/organizations.md | open-infra-ai 仓库表自动（7 行）；open-genomics/vibe-knight 叙事段落手工 |
| `original-projects` | catalog/original-projects.md | open-infra-ai 与 open-genomics 两张表自动；vibe-knight 列举段手工（note 承载证据文字） |
| `ai-infra` | catalog/ai-infra.md | **全手工**（P0 表为"项目组 + 多仓库合并列"分组叙事，数据化收益低，见 §8） |
| `hpc-and-transferable` | catalog/hpc-and-transferable.md | 主表格自动；Fork/已删除叙事行保留手工 |
| `tools-and-unrelated` | catalog/tools-and-unrelated.md | LessUp 个人表自动；vibe-knight/open-genomics 分组列举保留手工 |
| `retired-and-migrated` | catalog/retired-and-migrated.md | 全手工（历史记录，见 §8 决策） |

**私有仓库约束**（遵循 methodology.md）：`repos[]` **只含公开仓库**。私有仓库
**名称与描述不得出现在 `repos.json` 或任何渲染输出**（JSON 在公开仓库内，同样属于公开文档），
仅以 `accounts` 中的计数体现（如 `"private": 1`）。

## 5. 生成器 `scripts/generate.py` 规格

Python 3、无第三方依赖（标准库 json/re/urllib 即可，便于在任何环境与 Actions 中运行）。

### 占位符协议

每个 catalog 文件内的自动表格包裹在成对标记之间：

```html
<!-- AUTO:start <slug> -->
（生成表格）
<!-- AUTO:end <slug> -->
```

- 生成器定位每对标记，仅替换标记**之间**的内容。
- 标记之外（策略文字、叙事列表、标题）绝不触碰。
- 若文件缺失某对标记，生成器**报错并退出非零**（防止静默丢失自动区）。

### 渲染职责

1. **catalog 表格**：按 §4 映射，从 `repos[categories 含 slug]` 渲染 markdown 表格。
   表头由生成器按分类定义，单元格从 JSON 字段取值，说明列取 `notes[slug]`，仓库名渲染为链接
   `[name](https://github.com/{account}/{name})`。
2. **README 账号概览表**：从 `accounts` 渲染。
3. **README 徽章行**：渲染 shields.io 静态徽章（见 §7）。
4. **docsify `_sidebar.md`**：渲染侧边栏——分类清单 + 从 deep-dives 目录文件列表生成
   `deep-dives/*.md` 链接（自动感知新增/删除笔记）。
5. **CHANGELOG 追加**：在 `[Unreleased]` 下追加/合并"数据快照更新"条目（见 §6 格式）。
6. **README 审计日期**：从 `audited_at` 渲染。

### 校验与幂等

- 生成后对每个文件做一致性检查：占位符配对完整、无字段缺失、`visibility: private` 的
  仓库名未出现在任何输出。
- `--check` 模式：不写文件，仅输出 diff 摘要并退出非零（供 CI 断言"已生成"）。
- 相同输入 → 相同输出（确定性），便于 diff。

## 6. 审计脚本 `scripts/audit.py` + GitHub Actions

`audit.py` 复用 methodology.md 已验证的命令：

| 数据 | 命令 |
|------|------|
| 账号/组织仓库清单 | `gh repo list {owner} --limit 100`、`gh api orgs/{org}/repos?per_page=100` |
| Fork 上游 | `gh api repos/{owner}/{repo}` → `parent.full_name` |
| ahead/behind | `gh api repos/{upstream}/compare/{branch}...{owner}:{repo}:{branch}` |
| 贡献者审计 | `gh api repos/{repo}/contributors`（仅记录，不自动改 resume 判定） |
| 链接有效性 | HTTP 状态码 + `Location`（urllib/requests） |

行为：

1. 读取现有 `repos.json` 作为基线。
2. 拉取实时数据，更新 `audited_at`、`visibility`、`ahead/behind`、`links_ok`、账号统计。
3. 与基线对比：**有变化** → 更新 JSON + 调用 `generate.py` 重渲染 + 追加 CHANGELOG 条目 →
   工作流创建分支并开 PR；**无变化** → 不产生提交，干净退出。
4. **audit.py 只更新结构化数据**（`audited_at`/`visibility`/`ahead`/`behind`/`links_ok`/账号统计），
   **绝不覆盖 `notes`、`priority`、`resume`、`categories`** 等人工判断字段。
5. 无 `gh` 可用或 API 失败时：打印差异报告并退出非零（不半途覆盖 JSON）。

### `audit.yml` 规格

```yaml
name: weekly-audit
on:
  schedule:
    - cron: "7 9 * * 1"        # 每周一 09:07 UTC（避开整点，GitHub 调度友好）
  workflow_dispatch: {}        # 支持手动触发
permissions:
  contents: write              # 创建分支/提交
  pull-requests: write         # 开 PR
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python3 scripts/audit.py        # 更新 repos.json + 渲染 + CHANGELOG
      - name: Open PR if changed
        run: |
          if git diff --quiet; then echo "no changes"; exit 0; fi
          BRANCH="audit/$(date +%Y%m%d)"
          git checkout -b "$BRANCH"
          git add -A && git commit -m "chore: weekly audit data refresh"
          git push origin "$BRANCH"
          gh pr create --base main --head "$BRANCH" \
            --title "chore: weekly audit refresh" --fill
```

说明：PR 由人 review 后合并（Dependabot 式）；`workflow_dispatch` 保留手动触发能力。
`gh` 使用 `GITHUB_TOKEN`（公开仓库只读 API 即可，无需额外密钥）。

## 7. README 徽章设计

由生成器渲染 shields.io 静态徽章（不依赖动态 JSON endpoint，避免第三方实时读取）：

```
![审计日期](https://img.shields.io/badge/审计-2026--08--19-4c9) 
![仓库总数](https://img.shields.io/badge/仓库-32-4c9)
![公开](https://img.shields.io/badge/公开-31-blue) 
![Fork](https://img.shields.io/badge/Fork-22-orange)
![文档站](https://img.shields.io/badge/文档站-docsify-8A2BE2)
```

原则（来自徽章研究）：数量少、分组、可点击（链接到相关文件）、避免刷屏。徽章放 README
顶部标题下，与目录结构区块相邻。

## 8. 关键设计决策记录

| 决策 | 选择 | 理由 |
|------|------|------|
| 维护模式 | 占位符混合模式 | 表格自动、策略文字保留手工判断；全 JSON 驱动会把策略藏进数据层，维护体验差 |
| 数据模型 | 一个仓库多 `categories` | fq-compressor 等跨分类仓库（original-projects + hpc-and-transferable） |
| 私有仓库 | `repos[]` 只含公开仓库 | methodology.md：私有仓库名称/描述不进入公开文档；JSON 在公开仓库内同属公开文档 |
| 站点位置 | 根目录 index.html + Pages 根发布 | docsify 官方推荐，路径干净 |
| CHANGELOG | 生成器自动追加数据快照条目 | 保留数据历史；Keep a Changelog 风格 |
| retired-and-migrated | 全手工 | 历史映射记录是"过程叙事"非结构化数据，强行 JSON 化收益低 |
| ai-infra | 全手工 | P0 表为"项目组 + 多仓库合并列"分组叙事，且 P1–P3 全为策略文字；数据化收益低 |
| 站点技术 | docsify | MkDocs Material 已进维护模式；Docusaurus 过重 |
| 审计频率 | 每周一非整点 + workflow_dispatch | ahead/behind 变化慢，一周一次足够；避免刷屏 PR |
| 自动 PR | 新分支 + PR，不直写 main | Dependabot 式，人 review 后合并，安全可回滚 |

## 9. 一致性 / 校验规则

- `generate.py --check` 在 CI（或本地）断言生成结果与已提交文件一致，防手工/生成脱节。
- `visibility: private` 名称不得出现在任何渲染输出（含 README、catalog、sidebar）。
- 占位符标记必须配对；缺失即报错。
- deep-dives 内容不被生成器触碰（只读目录文件名生成 sidebar 链接）。

## 10. 风险与回滚

| 风险 | 缓解 |
|------|------|
| 生成器误伤手工段落 | 占位符分界 + 生成器只替换标记之间内容；先本地 `--check` 验证 diff |
| forks-and-translations.md 数据曾被手动修正 | 以 `repos.json` 为准重建；audit.py 首次运行重新验证 |
| 静态站失败 | markdown 永远可用；index.html 独立于文档内容，可随时移除 |
| 自动 PR 噪音 | 每周一次 + 无变化即退出；PR 可关闭/合并由人决定 |
| Action 权限 | permissions 最小化（contents: write + pull-requests: write） |

## 11. 实施顺序

1. 创建 `data/repos.json`：从现有 8 个分类文件迁移全部仓库数据（含跨分类）。
2. 编写 `scripts/generate.py`（占位符渲染、README、sidebar、CHANGELOG、--check）。
3. 改造 8 个 catalog 文件为占位符混合模式。
4. 本地运行 `generate.py --check` 对比 diff，确认手工段落无损。
5. 配置 docsify：`index.html`、`.nojekyll`、中文搜索；验证 `_sidebar.md` 生成。
6. 编写 `scripts/audit.py` + `.github/workflows/audit.yml`。
7. README 顶部徽章 + 快速导航区升级；CHANGELOG 记录本次结构性变更。
8. 本地端到端演练：改一个 ahead 值 → 重渲染 → diff 正确；手动 `workflow_dispatch` 试跑。
9. 提交并开启 GitHub Pages（Settings → Pages → Deploy from branch, root）。

## 12. 非目标（YAGNI）

- 不重写 deep-dives 内容，不将其纳入 JSON。
- 不做多语言版本、不做版本化文档（docusaurus 式 versioning）。
- 不自动修改 `resume` 判定与优先级策略（那是人的判断，audit.py 只提供数据）。
- 不引入外部徽章服务依赖（全部 shields.io 静态徽章，由生成器渲染）。
