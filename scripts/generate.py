#!/usr/bin/env python3
"""GitHub Repos Hub 生成器：repos.json -> catalog 表格 / README / _sidebar / CHANGELOG。

用法：
  python3 scripts/generate.py                        # 全量渲染（写文件）
  python3 scripts/generate.py --check                # 只检查差异，有差异退出 1
  python3 scripts/generate.py --changelog "数据快照更新（2026-08-21）"  # 渲染并追加 CHANGELOG

只替换 <!-- AUTO:start <slug> --> 与 <!-- AUTO:end <slug> --> 标记之间的内容，
标记之外（策略文字、叙事段落）绝不触碰。私有仓库名称不出现在任何输出。
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


def repo_link(r):
    return f"[{r['name']}](https://github.com/{r['account']}/{r['name']})"


def upstream_link(r):
    return f"[{r['upstream']}](https://github.com/{r['upstream']})"


def ahead_behind(r):
    return f"{r.get('ahead', 0)}/{r.get('behind', 0)}"


def note(slug, key=None):
    """返回 (repo -> str) 取值函数：字符串 notes 直接取，对象 notes 取指定 key。"""
    def _f(r):
        v = r.get("notes", {}).get(slug, "")
        if isinstance(v, dict):
            return v.get(key, "") if key else ""
        return v if isinstance(v, str) else ""
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
        "cols": [repo_link, note("original-projects", "position"),
                 note("original-projects", "resume")],
    },
    "original-projects-genomics": {
        "title": "open-genomics — 生物信息与 C++ 工程（P0 辅助 / P2）",
        "headers": ["项目", "定位", "简历用法"],
        "cols": [repo_link, note("original-projects", "position"),
                 note("original-projects", "resume")],
    },
    "hpc-and-transferable": {
        "title": "HPC 与可迁移能力项目",
        "headers": ["项目", "能力信号", "使用建议"],
        "cols": [repo_link, note("hpc-and-transferable", "signal"),
                 note("hpc-and-transferable", "usage")],
    },
    "tools-and-unrelated": {
        "title": "LessUp 个人",
        "headers": ["仓库", "说明"],
        "cols": [repo_link, note("tools-and-unrelated")],
    },
}

# 全手工分类（无占位符）：ai-infra、retired-and-migrated


def load_data():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def repos_for_slug(data, slug):
    """返回某分类（渲染 slug）对应的仓库列表。"""
    base = slug.replace("-genomics", "")
    if slug == "original-projects-genomics":
        return [r for r in data["repos"] if base in r["categories"]
                and r["account"] == "open-genomics"]
    if slug == "original-projects":
        return [r for r in data["repos"] if base in r["categories"]
                and r["account"] != "open-genomics"]
    return [r for r in data["repos"] if base in r["categories"]]


def render_row(repo, config):
    return "| " + " | ".join((col(repo) or "-") for col in config["cols"]) + " |"


def render_table(repos, config):
    header = "| " + " | ".join(config["headers"]) + " |"
    sep = "|" + "|".join(["---"] * len(config["headers"])) + "|"
    rows = "\n".join(render_row(r, config) for r in repos)
    return "\n".join([header, sep, rows])


def replace_in_text(text, slug, table):
    """在内存文本中替换 slug 占位符之间的内容；缺失占位符则报错退出。

    只替换与 slug 同名的占位符对；文件中其他占位符对原样保留。
    """
    marker = f"<!-- AUTO:start {slug} -->"
    if marker not in text or f"<!-- AUTO:end {slug} -->" not in text:
        print(f"ERROR: 缺少占位符 {slug}", file=sys.stderr)
        sys.exit(1)
    def _repl(m):
        if m.group(1) != slug:
            return m.group(0)
        return f"{marker}\n{table}\n<!-- AUTO:end {slug} -->"
    new, n = PLACEHOLDER_RE.subn(_repl, text)
    if n == 0:
        print(f"ERROR: 占位符 {slug} 未匹配", file=sys.stderr)
        sys.exit(1)
    return new


def replace_placeholders(path, slug, table):
    """从磁盘读文件并替换 slug 占位符（供测试/单文件使用）。"""
    return replace_in_text(Path(path).read_text(encoding="utf-8"), slug, table)


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


MANUAL_SIDEBAR = {
    "ai-infra": "AI Infra 优先级与阅读范围",
    "retired-and-migrated": "已撤销/已迁移仓库与失效链接",
}


def render_sidebar(data):
    lines = ["- [🏠 首页](README.md)", "", "- **catalog**"]
    for slug in ["lessup-owned", "forks-and-translations", "organizations",
                 "original-projects", "ai-infra", "hpc-and-transferable",
                 "tools-and-unrelated", "retired-and-migrated"]:
        cfg = CATEGORY_CONFIG.get(slug)
        title = cfg["title"] if cfg else MANUAL_SIDEBAR[slug]
        lines.append(f"  - [{title}](catalog/{slug}.md)")
    lines += ["", "- **deep-dives**"]
    for p in sorted((CATALOG.parent / "deep-dives").glob("*.md")):
        if p.name == "README.md":
            continue
        lines.append(f"  - [{p.stem}](deep-dives/{p.name})")
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
    new = text[:insert_at] + f"- {message}\n" + text[insert_at:]
    CHANGELOG.write_text(new, encoding="utf-8")


def catalog_slugs_by_file():
    """按文件名分组渲染 slug：catalog/original-projects.md 对应两个 slug。"""
    grouped = {}
    for slug in CATEGORY_CONFIG:
        fn = f"{slug.replace('-genomics', '')}.md"
        grouped.setdefault(fn, []).append(slug)
    return grouped


def check(root=ROOT):
    """渲染到内存并与磁盘比对；返回差异文件列表（无差异为 []）。"""
    data = load_data()
    diffs = []

    for fn, slugs in catalog_slugs_by_file().items():
        f = root / "catalog" / fn
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8")
        for slug in slugs:
            table = render_table(repos_for_slug(data, slug), CATEGORY_CONFIG[slug])
            text = replace_in_text(text, slug, table)
        if text != f.read_text(encoding="utf-8"):
            diffs.append(str(f))

    readme_path = root / "README.md"
    if readme_path.exists():
        text = readme_path.read_text(encoding="utf-8")
        for slug, table in (("accounts", render_accounts_table(data)),
                            ("badges", render_badges(data))):
            if f"<!-- AUTO:start {slug} -->" in text:
                text = replace_in_text(text, slug, table)
        if text != readme_path.read_text(encoding="utf-8"):
            diffs.append(str(readme_path))

    side = root / "_sidebar.md"
    if side.exists() and side.read_text(encoding="utf-8") != render_sidebar(data) + "\n":
        diffs.append(str(side))

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

    # 全量渲染 catalog（按文件分组，内存中依次替换各 slug 后一次写入）
    for fn, slugs in catalog_slugs_by_file().items():
        f = CATALOG / fn
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8")
        total = 0
        for slug in slugs:
            repos = repos_for_slug(data, slug)
            table = render_table(repos, CATEGORY_CONFIG[slug])
            text = replace_in_text(text, slug, table)
            total += len(repos)
        f.write_text(text, encoding="utf-8")
        print(f"rendered: {f.name} ({total} rows)")

    # README：概览表 + 徽章（内存连续替换）
    readme = README.read_text(encoding="utf-8")
    for slug, table in (("accounts", render_accounts_table(data)),
                        ("badges", render_badges(data))):
        if f"<!-- AUTO:start {slug} -->" in readme:
            readme = replace_in_text(readme, slug, table)
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
