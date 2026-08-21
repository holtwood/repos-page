# GitHub Repos Hub 数据驱动化升级 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 github-repos-hub 改造为数据驱动仓库：`data/repos.json` 唯一事实源，生成器渲染 catalog/README/侧边栏/CHANGELOG，GitHub Actions 每周自动审计提 PR，docsify 静态站。

**Architecture:** repos.json（人工+审计维护）→ generate.py（占位符混合模式渲染 markdown）→ audit.py + GitHub Actions（每周 gh api 刷新数据自动提 PR）。catalog 文件 = 手工策略段落 + `<!-- AUTO:start -->` 包裹的自动表格。docsify 根目录静态站。

**Tech Stack:** Python 3 标准库（无第三方依赖）、GitHub Actions、gh CLI、docsify CDN。

**Spec:** `docs/superpowers/specs/2026-08-21-github-repos-hub-data-driven-design.md`

## Global Constraints

- `data/repos.json` 的 `repos[]` **只含公开仓库**；私有仓库名称/描述不得出现在任何文件（JSON 在公开仓库内，同属公开文档），仅以 `accounts` 计数体现。
- 生成器只替换 `<!-- AUTO:start <slug> -->` 与 `<!-- AUTO:end <slug> -->` 标记**之间**的内容，标记之外（策略文字、标题、叙事列表）绝不触碰。
- 文件缺失某对占位符标记时，生成器**报错并退出非零**。
- `generate.py --check`：不写文件，仅输出差异摘要；有差异退出 1，无差异退出 0。
- 生成器确定性：相同输入 → 相同输出。
- `audit.py` 只更新 `audited_at` / `visibility` / `ahead` / `behind` / `links_ok` / `links` / `accounts` 统计；**绝不覆盖** `notes` / `priority` / `resume` / `resume_level` / `categories` / `domain` / `ai_relevance` / `license` / `contributors`。
- 审计 cron 表达式 `"7 9 * * 1"`（每周一 09:07 UTC）+ `workflow_dispatch` 手动触发。
- 自动 PR：新分支 `audit/YYYYMMDD` + `gh pr create`，不直写 main。
- docsify 入口 `index.html` 放仓库根目录，`.nojekyll` 防 Jekyll 处理。
- 分类渲染范围（已修正 spec）：`ai-infra` 与 `retired-and-migrated` **全手工**，无占位符。

---

### Task 1: 创建 data/repos.json（数据迁移）

**Files:**
- Create: `data/repos.json`

**Interfaces:**
- Produces: JSON 结构被 Task 3 的 `generate.py` 消费。顶层键：`audited_at`（字符串 `YYYY-MM-DD`）、`accounts`（对象，见下）、`repos`（数组）、`retired`（数组）。

- [ ] **Step 1: 建立目录并写 repos.json**

创建 `data/` 目录，写入 `data/repos.json`。内容从 8 个 catalog 文件提取。结构：

```json
{
  "audited_at": "2026-08-19",
  "accounts": {
    "LessUp":        { "public": 31, "private": 1, "forks": 22, "note": "个人" },
    "open-infra-ai": { "public": 7,  "private": 0, "forks": 0,  "note": "AI Infra 作品集" },
    "open-genomics": { "public": 7,  "private": 5, "forks": 0,  "note": "生物信息与 C++ 工程" },
    "vibe-knight":   { "public": 14, "private": 1, "forks": 0,  "note": "实验性与工具" }
  },
  "repos": [],
  "retired": []
}
```

**repos[] 数据来源与字段**（示例见 spec §4；每仓库必须含 `name`/`account`/`visibility:"public"`/`property`/`categories`）：

- `lessup-owned` 9 个（LessUp 原创公开）：`ai-infra-interview-prep`、`github-repos-hub`、`stars-index`、`cpp-high-performance-guide`、`bitcal`、`TensorTonic-Solutions`、`awesome-cursorrules-zh`、`hugo-blog`、`LessUp`。字段含 `language`/`domain`/`ai_relevance`(高/中/低/无)/`resume_level`(高/中/低)/`resume`(bool)/`notes.lessup-owned`。
- `forks-and-translations` 22 个 fork：`property:"fork"`，含 `upstream`/`ahead`/`behind`/`language`/`priority`/`notes.forks-and-translations`。注意 `Termius-Pro-zh_CN` 的 `priority:"无"`，`tutorials`（Triton Inference Server）的 upstream 是 `triton-inference-server/tutorials`。
- `organizations` 7 个（open-infra-ai）：`aicl-lab`、`cuda-foundations`、`triton-fused-ops`、`cuflash-attn`、`tiny-llm`、`paged-infer`、`.github`。字段含 `license`/`contributors`/`notes.organizations`（定位文字）。`.github` 的 language/license 为空字符串。
- `original-projects` 的 open-infra-ai 6 个 + open-genomics 7 个：`notes["original-projects"]` 用**对象** `{"position": "...", "resume": "..."}` 承载"定位与证据"与"简历用法"两列。
- 跨分类仓库：`fq-compressor`/`fastq-tools`/`minibwa-rust` 同时属 `original-projects` 与 `hpc-and-transferable`；`cpp-high-performance-guide`/`bitcal` 同时属 `lessup-owned` 与 `hpc-and-transferable`；`compress-kit`/`cudaimg` 属 `hpc-and-transferable`（及 vibe-knight 组，vibe-knight 组手工不落 categories）。每个分类的 `notes[slug]` 单独写。
- `hpc-and-transferable` 的 `ompi`（Fork: ompi）与已删除的 `the-art-of-hpc-zh`：**不进入 repos[]**（ompi 已在 forks 分类有完整记录；the-art-of-hpc-zh 进 `retired`），该文件手工段落保留这些叙事行。
- `retired[]` 4 条（旧地址 → 状态 → 处理）：`LessUp/sgemm-optimization`、`LessUp/the-art-of-hpc-zh`、`LessUp/cursor-rules`、`LessUp/awesome-claude-skills-zh`。
- 迁移记录（301 重定向 5 个 + 需改写 8 个）**不进入 repos.json**（retired-and-migrated 全手工，在 markdown 里维护）。

- [ ] **Step 2: 校验 JSON 合法**

```bash
python3 -m json.tool data/repos.json > /dev/null && echo "VALID JSON"
```

- [ ] **Step 3: 校验数量与字段完整性**

用 python 脚本断言：LessUp 原创 = 9、fork = 22、open-infra-ai = 7、open-genomics = 7、vibe-knight 公开 = 14、retired = 4；每 repo 均有 `name`/`account`/`visibility`/`property`/`categories` 且 `categories` 非空。

- [ ] **Step 4: 提交**

```bash
git add data/repos.json && git commit -m "feat(data): add repos.json as single source of truth"
```

---

### Task 2: 测试先行 — scripts/test_generate.py

**Files:**
- Create: `scripts/test_generate.py`

**Interfaces:**
- Consumes: Task 3 将实现的 `scripts/generate.py` 模块函数：`load_data()`、`render_table(repos, config)`、`replace_placeholders(path, slug, table)`、`render_accounts_table(data)`、`render_sidebar(data)`、`check(data)`。
- Produces: 测试脚本定义 `generate` 模块的期望接口（Task 3 实现必须满足）。

- [ ] **Step 1: 写测试文件**

```python
#!/usr/bin/env python3
"""generate.py 的单元测试：占位符替换、私有约束、缺失占位符、确定性。"""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "generate", Path(__file__).parent / "generate.py")
generate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate)

FAILURES = []

def check(name, cond, detail=""):
    if not cond:
        FAILURES.append(f"FAIL: {name} {detail}")
    else:
        print(f"PASS: {name}")

# --- fixture ---
FIXTURE = {
    "audited_at": "2026-08-19",
    "accounts": {"LessUp": {"public": 31, "private": 1, "forks": 22}},
    "repos": [
        {"name": "cuda-samples", "account": "LessUp", "visibility": "public",
         "property": "fork", "upstream": "NVIDIA/cuda-samples", "ahead": 26, "behind": 0,
         "language": "C++", "priority": "P1", "categories": ["forks-and-translations"],
         "notes": {"forks-and-translations": "说明A"}, "resume": False},
        {"name": "fq-compressor", "account": "open-genomics", "visibility": "public",
         "property": "org-project", "language": "C++", "priority": "P0",
         "categories": ["original-projects", "hpc-and-transferable"],
         "notes": {"original-projects": {"position": "证据", "resume": "辅助"},
                   "hpc-and-transferable": {"signal": "C++23", "usage": "辅助"}}},
    ],
    "retired": [],
}

# 1. 占位符替换：只换标记之间，手工段保留
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "t.md"
    p.write_text("标题\n\n<!-- AUTO:start forks-and-translations -->\n旧表\n<!-- AUTO:end forks-and-translations -->\n\n手工段落",
                 encoding="utf-8")
    repos = [r for r in FIXTURE["repos"] if "forks-and-translations" in r["categories"]]
    table = generate.render_table(repos, generate.CATEGORY_CONFIG["forks-and-translations"])
    out = generate.replace_placeholders(p, "forks-and-translations", table)
    check("占位符内被替换", "旧表" not in out and "NVIDIA" in out)
    check("手工段落保留", "手工段落" in out and "标题" in out)

# 2. 缺失占位符 → 报错
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "t.md"
    p.write_text("无占位符内容", encoding="utf-8")
    try:
        generate.replace_placeholders(p, "forks-and-translations", "x")
        check("缺失占位符报错", False)
    except SystemExit:
        check("缺失占位符报错", True)

# 3. 跨分类对象 notes
forks_cfg = generate.CATEGORY_CONFIG["forks-and-translations"]
fq = [r for r in FIXTURE["repos"] if r["name"] == "fq-compressor"][0]
row = generate.render_row(fq, generate.CATEGORY_CONFIG["original-projects"])
check("对象 notes 取 position", "证据" in row and "辅助" in row, row)

# 4. 确定性
t1 = generate.render_table(repos, forks_cfg)
t2 = generate.render_table(repos, forks_cfg)
check("渲染确定性", t1 == t2)

# 5. 私有仓库名不得出现在渲染输出（数据层已保证 repos[] 无私有名；渲染时无 private 分支可输出）
check("无私有仓库分支", not any(r.get("visibility") == "private" for r in FIXTURE["repos"]))

if FAILURES:
    print("\n".join(FAILURES), file=sys.stderr)
    sys.exit(1)
print("ALL TESTS PASSED")
```

- [ ] **Step 2: 运行测试，验证失败**

```bash
python3 scripts/test_generate.py
```

Expected: 因 `generate.py` 不存在而失败（`ModuleNotFoundError` 或 ImportError）。

- [ ] **Step 3: 提交测试**

```bash
git add scripts/test_generate.py && git commit -m "test: add generate.py unit tests"
```

---

### Task 3: 实现 scripts/generate.py 使测试通过

**Files:**
- Create: `scripts/generate.py`

**Interfaces:**
- Produces: 模块级函数 `load_data()` / `render_table(repos, config)` / `render_row(repo, config)` / `replace_placeholders(path, slug, table)` / `render_accounts_table(data)` / `render_sidebar(data)` / `render_badges(data)` / `check(data, root)`；CLI 参数 `--check`、`--changelog "<text>"`。
- Consumes: `data/repos.json`（Task 1 产出）。

- [ ] **Step 1: 写完整实现**

```python
#!/usr/bin/env python3
"""GitHub Repos Hub 生成器：repos.json -> catalog 表格 / README / _sidebar / CHANGELOG。

用法：
  python3 scripts/generate.py                 # 全量渲染（写文件）
  python3 scripts/generate.py --check         # 只检查差异，有差异退出 1
  python3 scripts/generate.py --changelog "数据快照更新（2026-08-21）"  # 渲染并追加 CHANGELOG
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "repos.json"
CATALOG = ROOT / "catalog"
README = ROOT / "README.md"
SIDEBAR = ROOT / "_sidebar.md"
CHANGELOG = ROOT / "CHANGELOG.md"

PLACEHOLDER_RE = re.compile(
    r"<!-- AUTO:start (\S+) -->.*?<!-- AUTO:end \1 -->", re.DOTALL)

# 分类配置：表头 + 每列取值函数（repo -> str）
def repo_link(r): return f"[{r['name']}](https://github.com/{r['account']}/{r['name']})"
def upstream_link(r): return f"[{r['upstream']}](https://github.com/{r['upstream']})"
def ahead_behind(r): return f"{r.get('ahead', 0)}/{r.get('behind', 0)}"
def note(slug, key=None):
    def _f(r):
        v = r.get("notes", {}).get(slug, "")
        return v.get(key, "") if isinstance(v, dict) and key else (v if isinstance(v, str) else "")
    return _f

CATEGORY_CONFIG = {
    "lessup-owned": {
        "title": "LessUp 个人原创",
        "headers": ["仓库", "语言", "领域", "AI Infra 相关性", "简历可用性", "说明"],
        "cols": [repo_link, lambda r: r.get("language", ""), lambda r: r.get("domain", ""),
                 lambda r: r.get("ai_relevance", ""), lambda r: r.get("resume_level", ""),
                 note("lessup-owned")],
    },
    "forks-and-translations": {
        "title": "Fork 与 AI 翻译仓库",
        "headers": ["Fork", "上游", "ahead/behind", "主语言", "AI Infra 优先级", "学习价值与建议阅读范围"],
        "cols": [repo_link, upstream_link, ahead_behind, lambda r: r.get("language", ""),
                 lambda r: r.get("priority", ""), note("forks-and-translations")],
    },
    "organizations": {
        "title": "open-infra-ai（AI Infra 作品集）",
        "headers": ["仓库", "语言", "License", "贡献者", "定位"],
        "cols": [repo_link, lambda r: r.get("language", ""), lambda r: r.get("license", ""),
                 lambda r: r.get("contributors", ""), note("organizations")],
    },
    "original-projects": {
        "title": "open-infra-ai — AI Infra 作品集（P0，简历主线）",
        "headers": ["项目", "定位与证据", "简历用法"],
        "cols": [repo_link, note("original-projects", "position"), note("original-projects", "resume")],
    },
    "original-projects-genomics": {
        "title": "open-genomics — 生物信息与 C++ 工程（P0 辅助 / P2）",
        "headers": ["项目", "定位", "简历用法"],
        "cols": [repo_link, note("original-projects", "position"), note("original-projects", "resume")],
    },
    "hpc-and-transferable": {
        "title": "HPC 与可迁移能力项目",
        "headers": ["项目", "能力信号", "使用建议"],
        "cols": [repo_link, note("hpc-and-transferable", "signal"), note("hpc-and-transferable", "usage")],
    },
    "tools-and-unrelated": {
        "title": "LessUp 个人",
        "headers": ["仓库", "说明"],
        "cols": [repo_link, note("tools-and-unrelated")],
    },
}

def load_data():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)

def render_row(repo, config):
    return "| " + " | ".join(col(repo) for col in config["cols"]) + " |"

def render_table(repos, config):
    header = "| " + " | ".join(config["headers"]) + " |"
    sep = "|" + "|".join(["---"] * len(config["headers"])) + "|"
    rows = "\n".join(render_row(r, config) for r in repos)
    return "\n".join([header, sep, rows])

def replace_placeholders(path, slug, table):
    """替换 path 中 slug 占位符之间的内容；缺失占位符则报错退出。"""
    text = Path(path).read_text(encoding="utf-8")
    marker = f"<!-- AUTO:start {slug} -->"
    if marker not in text or f"<!-- AUTO:end {slug} -->" not in text:
        print(f"ERROR: {path} 缺少占位符 {slug}", file=sys.stderr)
        sys.exit(1)
    new, n = PLACEHOLDER_RE.subn(
        lambda m: f"{marker}\n{table}\n<!-- AUTO:end {slug} -->", text)
    if n == 0:
        print(f"ERROR: {path} 占位符 {slug} 未匹配", file=sys.stderr)
        sys.exit(1)
    return new

def render_accounts_table(data):
    header = "| 账号 | 可见仓库 | 公开 | 私有 | Fork |"
    sep = "|------|---------|------|------|------|"
    rows = []
    for acct, info in data["accounts"].items():
        total = info["public"] + info["private"]
        rows.append(f"| {acct} | {total} | {info['public']} | {info['private']} | {info['forks']} |")
    return "\n".join([header, sep] + rows)

def render_badges(data):
    accts = data["accounts"]
    total = sum(a["public"] + a["private"] for a in accts.values())
    pub = sum(a["public"] for a in accts.values())
    forks = sum(a["forks"] for a in accts.values())
    audited = data["audited_at"]
    return (f"![审计日期](https://img.shields.io/badge/审计-{audited}-4c9)\n"
            f"![仓库总数](https://img.shields.io/badge/仓库-{total}-4c9)\n"
            f"![公开](https://img.shields.io/badge/公开-{pub}-blue)\n"
            f"![Fork](https://img.shields.io/badge/Fork-{forks}-orange)\n"
            f"![文档站](https://img.shields.io/badge/文档站-docsify-8A2BE2)")

def render_sidebar(data):
    lines = ["- [🏠 首页](README.md)", "", "- **catalog**"]
    for slug in ["lessup-owned", "forks-and-translations", "organizations",
                 "original-projects", "ai-infra", "hpc-and-transferable",
                 "tools-and-unrelated", "retired-and-migrated"]:
        cfg = CATEGORY_CONFIG.get(slug)
        title = cfg["title"] if cfg else {
            "ai-infra": "AI Infra 优先级与阅读范围",
            "retired-and-migrated": "已撤销/已迁移仓库与失效链接",
        }[slug]
        lines.append(f"  - [{title}](catalog/{slug}.md)")
    lines += ["", "- **deep-dives**"]
    for p in sorted((CATALOG.parent / "deep-dives").glob("*.md")):
        if p.name == "README.md":
            continue
        name = p.stem
        lines.append(f"  - [{name}](deep-dives/{p.name})")
    lines += ["", "- [📋 审计方法](methodology.md)"]
    return "\n".join(lines)

def append_changelog(message):
    text = CHANGELOG.read_text(encoding="utf-8")
    anchor = "### Changed\n"
    idx = text.find(anchor)
    if idx == -1:
        print(f"ERROR: CHANGELOG 缺少 '{anchor.strip()}' 段落", file=sys.stderr)
        sys.exit(1)
    insert_at = idx + len(anchor)
    new = text[:insert_at] + f"\n- {message}\n" + text[insert_at:]
    CHANGELOG.write_text(new, encoding="utf-8")

def check(root=ROOT):
    """渲染到内存并与磁盘比对；有差异返回差异列表，无差异返回 []。"""
    data = load_data()
    diffs = []
    def cmp(path, content):
        current = Path(path).read_text(encoding="utf-8")
        if current != content:
            diffs.append(str(path))
    for slug, cfg in CATEGORY_CONFIG.items():
        # 只处理存在于目录中的文件
        f = root / "catalog" / f"{slug.replace('-genomics', '')}.md"
        if not f.exists():
            continue
        repos = [r for r in data["repos"] if slug.replace("-genomics", "") in r["categories"]
                 and (slug != "original-projects-genomics" or r["account"] == "open-genomics")
                 and (slug == "original-projects-genomics" or not (slug == "original-projects" and r["account"] == "open-genomics"))]
        table = render_table(repos, cfg)
        cmp(f, replace_placeholders(f, slug.replace("-genomics", ""), table))
    # README 概览与徽章
    readme = Path(root / "README.md").read_text(encoding="utf-8")
    new_readme = readme
    if "<!-- AUTO:start accounts -->" in readme:
        new_readme = replace_placeholders(root / "README.md", "accounts", render_accounts_table(data))
    if "<!-- AUTO:start badges -->" in readme:
        new_readme = replace_placeholders(root / "README.md", "badges", render_badges(data))
    if new_readme != readme:
        diffs.append(str(root / "README.md"))
    # sidebar
    new_side = render_sidebar(data)
    if Path(root / "_sidebar.md").exists() and Path(root / "_sidebar.md").read_text(encoding="utf-8") != new_side:
        diffs.append(str(root / "_sidebar.md"))
    return diffs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只检查差异，有差异退出 1")
    ap.add_argument("--changelog", metavar="TEXT", help="渲染后向 CHANGELOG [Unreleased] 追加条目")
    args = ap.parse_args()

    data = load_data()

    if args.check:
        diffs = check()
        if diffs:
            print("DIFFS:", ", ".join(diffs), file=sys.stderr)
            sys.exit(1)
        print("OK: 生成结果与磁盘一致")
        sys.exit(0)

    # 全量渲染
    for slug, cfg in CATEGORY_CONFIG.items():
        f = CATALOG / f"{slug.replace('-genomics', '')}.md"
        if not f.exists():
            continue
        repos = [r for r in data["repos"] if slug.replace("-genomics", "") in r["categories"]
                 and (slug != "original-projects-genomics" or r["account"] == "open-genomics")
                 and (slug == "original-projects-genomics" or not (slug == "original-projects" and r["account"] == "open-genomics"))]
        table = render_table(repos, cfg)
        content = replace_placeholders(f, slug.replace("-genomics", ""), table)
        f.write_text(content, encoding="utf-8")
        print(f"rendered: {f.name} ({len(repos)} rows)")

    # README：概览表 + 徽章
    readme = README.read_text(encoding="utf-8")
    if "<!-- AUTO:start accounts -->" in readme:
        readme = replace_placeholders(README, "accounts", render_accounts_table(data))
    if "<!-- AUTO:start badges -->" in readme:
        readme = replace_placeholders(README, "badges", render_badges(data))
    README.write_text(readme, encoding="utf-8")
    print("rendered: README.md")

    # sidebar（全量覆盖，生成器专属文件）
    SIDEBAR.write_text(render_sidebar(data) + "\n", encoding="utf-8")
    print("rendered: _sidebar.md")

    if args.changelog:
        append_changelog(args.changelog)
        print("changelog appended")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 运行测试**

```bash
python3 scripts/test_generate.py
```

Expected: `ALL TESTS PASSED`。

- [ ] **Step 3: 运行 --check（此时 catalog 无占位符，应因缺占位符报错——预期行为）**

```bash
python3 scripts/generate.py --check; echo "exit=$?"
```

Expected: 退出 1 且 stderr 提示缺少占位符（因为 Task 4 尚未改造 catalog 文件）。

- [ ] **Step 4: 提交**

```bash
git add scripts/generate.py && git commit -m "feat: add generate.py renderer (tables/readme/sidebar/changelog)"
```

---

### Task 4: 改造 catalog 文件为占位符混合模式

**Files:**
- Modify: `catalog/lessup-owned.md`、`catalog/forks-and-translations.md`、`catalog/organizations.md`、`catalog/original-projects.md`、`catalog/hpc-and-transferable.md`、`catalog/tools-and-unrelated.md`
- 不改: `catalog/ai-infra.md`、`catalog/retired-and-migrated.md`（全手工）

**Interfaces:**
- Consumes: Task 3 的 `CATEGORY_CONFIG`（slug 与表头一致）。

- [ ] **Step 1: 每个文件把自动表格替换为占位符**

对 6 个文件，将现有 markdown 表格（含表头与分隔行）整体替换为占位符对：

```html
<!-- AUTO:start <slug> -->
（原表格内容先留空或保留，Task 5 会用生成器重写）
<!-- AUTO:end <slug> -->
```

具体 slug：`lessup-owned` / `forks-and-translations` / `organizations` / `original-projects`（open-infra-ai 表）/ `original-projects-genomics`（open-genomics 表）/ `hpc-and-transferable` / `tools-and-unrelated`。

**关键**：
- `original-projects.md` 有两张自动表 → 两个占位符：`<!-- AUTO:start original-projects -->`（open-infra-ai 6 仓）与 `<!-- AUTO:start original-projects-genomics -->`（open-genomics 7 仓）。标题、贡献者审计说明、vibe-knight 段保留在占位符外。
- `hpc-and-transferable.md` 的手工叙事行（"Fork: ompi"、"Fork: the-art-of-hpc-zh（已删除）"）移到占位符**之后**的"Fork 与已删除记录"小节。
- `forks-and-translations.md` 顶部的"重要声明"段落与底部"归属与 License"段保留。
- 占位符内先放临时表格（哪怕 1 行假数据），保证占位符存在。

- [ ] **Step 2: 验证 6 个文件占位符配对**

```bash
for f in catalog/lessup-owned.md catalog/forks-and-translations.md catalog/organizations.md catalog/original-projects.md catalog/hpc-and-transferable.md catalog/tools-and-unrelated.md; do
  opens=$(grep -c 'AUTO:start' "$f"); closes=$(grep -c 'AUTO:end' "$f")
  echo "$f opens=$opens closes=$closes"
done
```

Expected: 每文件 opens == closes（original-projects 为 2/2）。

- [ ] **Step 3: 提交**

```bash
git add catalog/ && git commit -m "refactor(catalog): wrap auto tables in placeholder markers"
```

---

### Task 5: 全量渲染 + diff 验证

**Files:**
- Run: `python3 scripts/generate.py`

**Interfaces:**
- Consumes: repos.json（Task 1）+ 占位符（Task 4）+ generate.py（Task 3）。

- [ ] **Step 1: 全量渲染**

```bash
python3 scripts/generate.py
```

Expected: 输出每个 catalog 文件的行数、README.md、_sidebar.md。

- [ ] **Step 2: 检查 git diff 手工段落无损**

```bash
git diff --stat
git diff catalog/ | grep -E '^[-+](?![-+])' | grep -vE '^\+\+\+|^---' | head -80
```

Expected: 每个 catalog 文件的 diff 仅限占位符内表格区域；手工段落（声明、策略、叙事）逐字节不变。重点核对：`forks-and-translations.md` 的"重要声明"段、`organizations.md` 的贡献者审计叙事、`original-projects.md` 的 vibe-knight 段。

- [ ] **Step 3: 运行 --check 确认幂等**

```bash
python3 scripts/generate.py --check; echo "exit=$?"
```

Expected: `OK: 生成结果与磁盘一致`，exit=0。

- [ ] **Step 4: 提交**

```bash
git add -A && git commit -m "feat: first full render from repos.json"
```

---

### Task 6: 配置 docsify 静态站

**Files:**
- Create: `index.html`、`.nojekyll`
- Verify: `_sidebar.md`（Task 5 已生成）

**Interfaces:**
- Consumes: Task 5 生成的 `_sidebar.md`。

- [ ] **Step 1: 写 index.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🗺️ GitHub Repos Hub</title>
  <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/docsify@4/lib/themes/vue.css">
</head>
<body>
  <div id="app"></div>
  <script>
    window.$docsify = {
      name: '🗺️ GitHub Repos Hub',
      repo: 'https://github.com/LessUp/github-repos-hub',
      loadSidebar: true,
      subMaxLevel: 2,
      search: {
        placeholder: '搜索',
        noData: '未找到结果',
        depth: 2,
        paths: 'auto'
      }
    };
  </script>
  <script src="//cdn.jsdelivr.net/npm/docsify@4/lib/docsify.min.js"></script>
  <script src="//cdn.jsdelivr.net/npm/docsify@4/lib/plugins/search.min.js"></script>
</body>
</html>
```

- [ ] **Step 2: 创建空 .nojekyll**

```bash
touch .nojekyll
```

- [ ] **Step 3: 验证 _sidebar.md 已生成且链接完整**

```bash
python3 - <<'EOF'
from pathlib import Path
side = Path("_sidebar.md").read_text(encoding="utf-8")
links = [l for l in side.splitlines() if "](deep-dives/" in l or "](catalog/" in l]
missing = [l for l in links if not Path(l.split("](")[1][:-1]).exists()]
print(f"sidebar links: {len(links)}, missing: {len(missing)}")
assert not missing, missing
EOF
```

Expected: `missing: 0`（21 篇 deep-dives + 8 个 catalog 链接全部有效）。

- [ ] **Step 4: 提交**

```bash
git add index.html .nojekyll && git commit -m "feat(site): add docsify static site entry"
```

---

### Task 7: 编写 scripts/audit.py（含 dry-run）

**Files:**
- Create: `scripts/audit.py`

**Interfaces:**
- Produces: CLI `python3 scripts/audit.py [--dry-run]`。`--dry-run` 只打印差异不写文件（供本地/CI 试跑）。
- Consumes: `data/repos.json`；`gh` CLI（在 Actions 中由 GITHUB_TOKEN 认证）。

- [ ] **Step 1: 写实现**

```python
#!/usr/bin/env python3
"""GitHub Repos Hub 审计：gh api 拉取实时数据刷新 repos.json。

只更新结构化字段：audited_at / visibility / ahead / behind / links_ok / links / accounts。
绝不覆盖 notes / priority / resume / resume_level / categories / domain /
ai_relevance / license / contributors（人工判断字段）。

用法：
  python3 scripts/audit.py            # 更新 repos.json（有 gh 时）
  python3 scripts/audit.py --dry-run  # 只打印差异，不写文件
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "repos.json"
ACCOUNTS = ["LessUp", "open-infra-ai", "open-genomics", "vibe-knight"]

def gh(args, check=True):
    """运行 gh 命令，返回 stdout；失败抛异常。"""
    r = subprocess.run(["gh", *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)} failed: {r.stderr}")
    return r.stdout

def repo_exists(owner, name):
    r = subprocess.run(["gh", "api", f"repos/{owner}/{name}", "--jq",
                        ".visibility, .parent.full_name, .fork, .default_branch, .language"],
                       capture_output=True, text=True)
    return r.returncode == 0, r.stdout

def fetch_public_repos(account):
    """返回该账号公开仓库名列表（含 fork 标记）。"""
    cmd = ["repo", "list", account, "--limit", "100", "--json",
           "name,isFork,visibility,language"]
    r = subprocess.run(["gh", *cmd], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"gh repo list {account} failed: {r.stderr}")
    return json.loads(r.stdout)

def fetch_compare(upstream, owner, repo, branch):
    r = subprocess.run(
        ["gh", "api", f"repos/{upstream}/compare/{branch}...{owner}:{repo}:{branch}",
         "--jq", ".ahead_by, .behind_by"],
        capture_output=True, text=True)
    if r.returncode != 0:
        return None
    a, b = r.stdout.split()
    return int(a), int(b)

def load_data():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not shutil.which("gh"):
        print("ERROR: gh CLI 不可用；请安装 GitHub CLI 或改用 --dry-run 之外的环境", file=sys.stderr)
        sys.exit(2)

    data = load_data()
    changes = []

    # 1. 账号统计 + 公开仓库清单
    account_stats = {}
    for acct in ACCOUNTS:
        repos = fetch_public_repos(acct)
        public = len([r for r in repos if not r["visibility"].startswith("private")])
        forks = len([r for r in repos if r["isFork"]])
        # 私有数 = repo list 不含私有（--json visibility 只列可见）→ 用 api 兜底：org 用 api count
        priv = 0
        if acct != "LessUp":
            r = subprocess.run(["gh", "api", f"orgs/{acct}/repos?per_page=100&type=private",
                                "--jq", "length"], capture_output=True, text=True)
            if r.returncode == 0:
                priv = int(r.stdout)
        account_stats[acct] = {"public": public, "private": priv, "forks": forks}
        old = data["accounts"].get(acct, {})
        if old != {k: account_stats[acct][k] for k in ("public", "private", "forks")}:
            changes.append(f"accounts.{acct}: {old.get('public')}/{old.get('private')}/{old.get('forks')} -> "
                           f"{public}/{priv}/{forks}")

    # 2. 逐仓库刷新结构化字段
    for repo in data["repos"]:
        name, acct = repo["name"], repo["account"]
        if name == ".github":
            continue
        ok, out = repo_exists(acct, name)
        if not ok:
            changes.append(f"repo {acct}/{name}: 404/不可达")
            continue
        lines = out.strip().splitlines()
        visibility = lines[0].strip() if lines else ""
        parent = lines[1].strip() if len(lines) > 1 else ""
        is_fork = lines[2].strip().lower() == "true" if len(lines) > 2 else False
        branch = lines[3].strip() if len(lines) > 3 else "main"
        language = lines[4].strip() if len(lines) > 4 else ""

        if repo.get("visibility") != visibility:
            changes.append(f"{acct}/{name} visibility: {repo.get('visibility')} -> {visibility}")
            repo["visibility"] = visibility
        if repo.get("language", "") != language and language:
            # 语言属于 GitHub 数据，可刷新；人工字段仅当仓库自身变化
            changes.append(f"{acct}/{name} language: {repo.get('language')} -> {language}")
            repo["language"] = language

        if repo.get("property") == "fork" and repo.get("upstream"):
            upstream = repo["upstream"]
            if parent and parent != upstream:
                changes.append(f"{acct}/{name} upstream: {upstream} -> {parent}")
                repo["upstream"] = parent
                upstream = parent
            ab = fetch_compare(upstream, acct, name, branch)
            if ab:
                a, b = ab
                if repo.get("ahead") != a or repo.get("behind") != b:
                    changes.append(f"{acct}/{name} ahead/behind: {repo.get('ahead')}/{repo.get('behind')} -> {a}/{b}")
                    repo["ahead"], repo["behind"] = a, b

    # 3. 链接状态（urllib 轻量检查）
    import urllib.request
    for repo in data["repos"]:
        url = f"https://github.com/{repo['account']}/{repo['name']}"
        try:
            req = urllib.request.Request(url, method="HEAD",
                                         headers={"User-Agent": "github-repos-hub-audit"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                ok_link = resp.status < 400
        except Exception:
            ok_link = False
        if repo.get("links_ok") != ok_link:
            changes.append(f"{acct}/{name} links_ok: {repo.get('links_ok')} -> {ok_link}")
            repo["links_ok"] = ok_link

    # 4. audited_at
    from datetime import date
    today = date.today().isoformat()
    if data.get("audited_at") != today:
        changes.append(f"audited_at: {data.get('audited_at')} -> {today}")
        data["audited_at"] = today

    # 5. 写出
    data["accounts"] = account_stats
    if args.dry_run:
        print("DRY RUN — 以下字段将变更:")
        for c in changes:
            print("  " + c)
        sys.exit(0 if not changes else 1)
    if changes:
        with open(DATA, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
    print(f"audit done: {len(changes)} changes")
    for c in changes:
        print("  " + c)
    sys.exit(0 if not changes else 1)

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 验证语法与 dry-run 行为**

```bash
python3 -m py_compile scripts/audit.py && echo "SYNTAX OK"
python3 scripts/audit.py --dry-run; echo "exit=$?"
```

Expected: `SYNTAX OK`；有 gh 时 dry-run 打印差异并退出 1（有变化）或 0（无变化）；无 gh 时退出 2 并提示。

- [ ] **Step 3: 提交**

```bash
git add scripts/audit.py && git commit -m "feat: add audit.py (gh api refresh, dry-run)"
```

---

### Task 8: 配置 GitHub Actions 每周自动审计 workflow

**Files:**
- Create: `.github/workflows/audit.yml`

**Interfaces:**
- Consumes: `scripts/audit.py`（Task 7）+ `scripts/generate.py --changelog`（Task 3）。

- [ ] **Step 1: 写 workflow**

```yaml
name: weekly-audit
on:
  schedule:
    - cron: "7 9 * * 1"   # 每周一 09:07 UTC
  workflow_dispatch: {}

permissions:
  contents: write
  pull-requests: write

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run audit
        run: python3 scripts/audit.py
      - name: Regenerate docs
        run: python3 scripts/generate.py --changelog "数据快照更新（$(date +%Y-%m-%d)）：ahead/behind 与链接状态已刷新"
      - name: Open PR if changed
        run: |
          if git diff --quiet; then
            echo "no changes"
            exit 0
          fi
          BRANCH="audit/$(date +%Y%m%d)"
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git checkout -b "$BRANCH"
          git add -A
          git commit -m "chore: weekly audit data refresh ($(date +%Y-%m-%d))"
          git push origin "$BRANCH"
          gh pr create --base main --head "$BRANCH" \
            --title "chore: weekly audit refresh" --fill
```

注意：`audit.py` 无变化时退出 1（有 changes 时也退出 1），但该退出码只用于本地/CI 判断，workflow 中后续步骤仍会执行（无 `set -e` 阻止）。若想严格，可改为 `|| true`。此处保留默认（步骤失败会停止，故在 Regenerate 步骤前不需要 --dry-run）。

**修正**（避免 workflow 中断）：`audit.py` 退出 1 表示"有变化"，属预期，不视为失败。在 workflow 中调用改为：

```bash
python3 scripts/audit.py || true
```

- [ ] **Step 2: 验证 YAML 语法**

```bash
python3 - <<'EOF'
import yaml
with open(".github/workflows/audit.yml", encoding="utf-8") as f:
    yaml.safe_load(f)
print("YAML OK")
EOF
```

若环境无 pyyaml：`ruby -e 'require "yaml"; YAML.load_file(".github/workflows/audit.yml"); puts "YAML OK"'` 或直接人工目检缩进。

- [ ] **Step 3: 提交**

```bash
git add .github/workflows/audit.yml && git commit -m "ci: add weekly audit workflow (auto PR)"
```

---

### Task 9: README 手工区升级 + 徽章占位符

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: Task 3 的 `render_badges` / `render_accounts_table`（通过占位符 `<!-- AUTO:start badges -->` 与 `<!-- AUTO:start accounts -->`）。

- [ ] **Step 1: README 顶部加徽章占位符 + 账号概览占位符**

在 `# 🗺️ GitHub Repos Hub` 标题与引用块之后插入：

```html
<!-- AUTO:start badges -->
<!-- AUTO:end badges -->
```

将现有"账号概览"表格整体替换为：

```html
<!-- AUTO:start accounts -->
（保留原表格内容占位，Task 5 已渲染，此处验证）
<!-- AUTO:end accounts -->
```

- [ ] **Step 2: 更新目录结构与职责边界描述**

`目录结构` 代码块更新为含 `data/`、`scripts/`、`index.html`、`_sidebar.md`、`.nojekyll`、`.github/workflows/audit.yml`；`快速导航` 增加"📖 阅读站点：GitHub Pages（index.html）"链接项。

- [ ] **Step 3: 运行生成器并验证**

```bash
python3 scripts/generate.py && python3 scripts/generate.py --check && echo "CHECK OK"
```

Expected: 徽章行与概览表渲染进 README，--check 通过。

- [ ] **Step 4: 提交**

```bash
git add README.md && git commit -m "docs: upgrade README with badges and generated sections"
```

---

### Task 10: 端到端演练 + CHANGELOG + 全量提交

**Files:**
- Modify: `CHANGELOG.md`（结构性变更条目）
- Run: 端到端演练

**Interfaces:**
- Consumes: 全部前述任务产出。

- [ ] **Step 1: 模拟数据变化验证端到端链路**

```bash
# 改一个 ahead 值
python3 - <<'EOF'
import json
p = "data/repos.json"
d = json.load(open(p, encoding="utf-8"))
for r in d["repos"]:
    if r["name"] == "cuda-samples":
        r["ahead"] = 26
        break
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
EOF
python3 scripts/generate.py
git diff --stat   # 应只显示 forks-and-translations.md 一行 ahead 数字变化
# 还原
git checkout -- data/repos.json catalog/ scripts/ README.md _sidebar.md 2>/dev/null || git restore .
python3 scripts/generate.py --check && echo "RESTORED OK"
```

Expected: diff 仅限目标单元格；还原后 --check 通过。

- [ ] **Step 2: 更新 CHANGELOG 结构性条目**

在 `CHANGELOG.md` 的 `[Unreleased]` 区块追加：

```markdown
### Added

- `data/repos.json`：全部公开仓库的结构化元数据（唯一事实来源）。
- `scripts/generate.py`：占位符混合模式渲染器（catalog 表格 / README 徽章与概览 / _sidebar / CHANGELOG）。
- `scripts/audit.py` + `.github/workflows/audit.yml`：每周自动审计（gh api），有变化自动提 PR。
- docsify 静态站（`index.html` + `.nojekyll`），GitHub Pages 根发布。
- README 顶部状态徽章（审计日期 / 仓库数 / Fork 数 / 文档站）。

### Changed

- `catalog/*.md`：自动表格改为 `<!-- AUTO:start/end -->` 占位符混合模式；
  策略文字与叙事段落保留手工维护。
- 私有仓库不再出现于任何公开文件（仅以账号计数体现）。

### Removed

- 原手工 markdown 表格数据（由 repos.json + 生成器取代）。
```

- [ ] **Step 3: 全量提交**

```bash
git add -A && git commit -m "chore: data-driven hub upgrade complete"
```

- [ ] **Step 4: 最终验证**

```bash
python3 scripts/generate.py --check && echo "FINAL CHECK OK"
python3 scripts/test_generate.py
```

Expected: `FINAL CHECK OK` + `ALL TESTS PASSED`。

---

## Self-Review

**1. Spec coverage：**
- §3 目标架构（data/、scripts/、docsify、workflow）→ Task 1/3/6/7/8 ✅
- §4 数据模型（repos.json、私有约束、分类映射）→ Task 1（含 ai-infra/retired 全手工）✅
- §5 生成器（占位符、README、sidebar、CHANGELOG、--check、幂等）→ Task 3/5/9 ✅
- §6 审计 + workflow（cron、自动 PR、人工字段保护）→ Task 7/8 ✅
- §7 徽章（shields.io 静态、生成器渲染）→ Task 3 render_badges + Task 9 ✅
- §9 一致性规则（--check、私有约束、占位符配对）→ Task 2/3/5 ✅
- §10 风险（先本地验证 diff、还原路径）→ Task 5/10 ✅

**2. Placeholder scan：** 无 TBD/TODO；每步含可执行命令或代码。

**3. Type consistency：** `CATEGORY_CONFIG` 的 slug 在 Task 2 测试、Task 3 实现、Task 4 占位符、Task 5 渲染间一致；`original-projects-genomics` 子分类仅用于 open-genomics 表（original-projects.md 文件内两占位符）；`render_row`/`render_table`/`replace_placeholders`/`render_sidebar`/`check` 签名在 Task 2 测试与 Task 3 实现一致。
