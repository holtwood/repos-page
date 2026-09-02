#!/usr/bin/env python3
"""generate.py 的单元测试：占位符替换、缺失占位符、跨分类 notes、确定性、私有约束。"""
import importlib.util
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
    "accounts": {"holtwood": {"public": 31, "private": 1, "forks": 22}},
    "repos": [
        {"name": "cuda-samples", "account": "holtwood", "visibility": "public",
         "property": "fork", "upstream": "NVIDIA/cuda-samples", "ahead": 26, "behind": 0,
         "language": "C++", "priority": "P1", "categories": ["forks-and-translations"],
         "notes": {"forks-and-translations": "说明A"}, "resume_level": "低"},
        {"name": "fq-compressor", "account": "open-genomics", "visibility": "public",
         "property": "org-project", "language": "C++", "priority": "P0",
         "categories": ["original-projects", "hpc-and-transferable"],
         "notes": {"original-projects": {"position": "证据", "resume": "辅助"},
                   "hpc-and-transferable": {"signal": "C++23", "usage": "辅助"}}},
        # --- 精选区(render_featured)测试仓库:追加在末尾,不动 repos[0] ---
        {"name": "ai-infra-interview-prep", "account": "holtwood", "visibility": "public",
         "property": "original", "language": "Markdown", "resume_level": "中",
         "categories": ["lessup-owned"],
         "notes": {"lessup-owned": "12 周 AI Infra 转行计划"}},
        {"name": "repos-db", "account": "holtwood", "visibility": "public",
         "property": "original", "language": "Markdown", "resume_level": "低",
         "categories": ["lessup-owned"],
         "notes": {"lessup-owned": "本仓库"}},
        {"name": "tiny-llm", "account": "open-infra-ai", "visibility": "public",
         "property": "org-project", "language": "C++", "priority": "P0",
         "contributors": "holtwood", "categories": ["original-projects"],
         "notes": {"original-projects": {"position": "CUDA 推理引擎", "resume": "主线"}}},
        {"name": "minibwa-rust", "account": "open-genomics", "visibility": "public",
         "property": "org-project", "language": "Rust", "priority": "P0",
         "categories": ["original-projects"], "notes": {}},
        {"name": "cudaimg", "account": "vibe-knight", "visibility": "public",
         "property": "org-project", "language": "CUDA", "priority": "P2",
         "categories": ["hpc-and-transferable"]},
        {"name": "some-org-proj", "account": "open-infra-ai", "visibility": "public",
         "property": "org-project", "language": "Python", "priority": "P0",
         "contributors": "Lumkai", "categories": ["original-projects"]},
    ],
    "retired": [],
}

# 1. 占位符替换：只换标记之间，手工段保留
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "t.md"
    p.write_text("标题\n\n<!-- AUTO:start forks-and-translations -->\n旧表\n"
                 "<!-- AUTO:end forks-and-translations -->\n\n手工段落", encoding="utf-8")
    repos = [r for r in FIXTURE["repos"] if "forks-and-translations" in r["categories"]]
    table = generate.render_table(repos, generate.CATEGORY_CONFIG["forks-and-translations"])
    out = generate.replace_placeholders(p, "forks-and-translations", table)
    check("占位符内被替换", "旧表" not in out and "NVIDIA" in out)
    check("手工段落保留", "手工段落" in out and "标题" in out)

# 2. 缺失占位符 → 报错（SystemExit）
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "t.md"
    p.write_text("无占位符内容", encoding="utf-8")
    try:
        generate.replace_placeholders(p, "forks-and-translations", "x")
        check("缺失占位符报错", False)
    except SystemExit:
        check("缺失占位符报错", True)

# 3. 跨分类对象 notes：original-projects 取 position/resume
fq = [r for r in FIXTURE["repos"] if r["name"] == "fq-compressor"][0]
row = generate.render_row(fq, generate.CATEGORY_CONFIG["original-projects"])
check("对象 notes 取 position/resume", "证据" in row and "辅助" in row, row)

# 4. 确定性：相同输入 → 相同输出
repos = [r for r in FIXTURE["repos"] if "forks-and-translations" in r["categories"]]
t1 = generate.render_table(repos, generate.CATEGORY_CONFIG["forks-and-translations"])
t2 = generate.render_table(repos, generate.CATEGORY_CONFIG["forks-and-translations"])
check("渲染确定性", t1 == t2)

# 5. 私有仓库约束：repos[] 无私有仓库（数据层保证）；渲染路径无 private 分支输出
check("无私有仓库分支", not any(r.get("visibility") == "private" for r in FIXTURE["repos"]))

# 6. 字符串 notes：单列说明正常
srow = generate.render_row(FIXTURE["repos"][0],
                           generate.CATEGORY_CONFIG["forks-and-translations"])
check("字符串 notes 渲染", "说明A" in srow and "26/0" in srow, srow)

# 7. 多占位符文件：只替换目标 slug，其他占位符原样保留（回归测试）
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "t.md"
    p.write_text("<!-- AUTO:start original-projects -->\n表A\n"
                 "<!-- AUTO:end original-projects -->\n\n"
                 "<!-- AUTO:start original-projects-genomics -->\n表B\n"
                 "<!-- AUTO:end original-projects-genomics -->", encoding="utf-8")
    out = generate.replace_placeholders(p, "original-projects-genomics", "新表B")
    check("多占位符只替换目标",
          "新表B" in out and "表A" in out and "\n表B\n" not in out, out)

# --- 精选区(render_featured) ---
REPO_BY_NAME = {r["name"]: r for r in FIXTURE["repos"]}

# T-A. is_featured 门槛：original 需 resume 高/中；org-project 需 P0 且 contributors 缺失或含 holtwood；fork 排除
expect_featured = {
    "ai-infra-interview-prep": True,   # original resume 中
    "repos-db": False,             # original resume 低
    "tiny-llm": True,                  # org P0 contributors=holtwood
    "minibwa-rust": True,              # org P0 无 contributors 字段 → 通过
    "fq-compressor": True,             # org P0 无 contributors 字段 → 通过
    "cudaimg": False,                  # org P2
    "some-org-proj": False,            # org P0 但 contributors=Lumkai
    "cuda-samples": False,             # fork
}
check("is_featured 门槛",
      all(generate.is_featured(REPO_BY_NAME[n]) == exp
          for n, exp in expect_featured.items()))

# T-B. 精选去重与确定性：两调输出相等，且仓库名无重复
feat1 = generate.render_featured(FIXTURE)
feat2 = generate.render_featured(FIXTURE)
check("精选确定性", feat1 == feat2)
import re as _re
names_in_feat = _re.findall(r"\[([^\]]+)\]\(https://github\.com/", feat1)
check("精选去重", len(names_in_feat) == len(set(names_in_feat)), names_in_feat)

# T-C. 精选排序：open-infra-ai 先于 open-genomics，先于 holtwood
def _row_account(name):
    # 行形如 | [name](https://github.com/acct/name) | lang | acct | tagline |
    line = next(l for l in feat1.splitlines() if f"[{name}](https://github.com/"
                in l and l.startswith("| ["))
    return line.split("|")[3].strip()

check("精选排序 open-infra-ai 先于 open-genomics",
      feat1.find("tiny-llm") < feat1.find("fq-compressor"))
check("精选排序 open-genomics 先于 holtwood",
      feat1.find("fq-compressor") < feat1.find("ai-infra-interview-prep"))
check("精选排序 归属列正确", _row_account("tiny-llm") == "open-infra-ai")

# T-D. 定位回退：无 position notes 的 org P0 仓库定位列渲染为 -
row = next(l for l in feat1.splitlines() if "minibwa-rust" in l and l.startswith("| ["))
check("定位回退为 -", "| - |" in row, row)

# T-E. featured 占位符：只换标记内，手工段保留（镜像用例 #1）
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "t.md"
    p.write_text("标题\n\n<!-- AUTO:start featured -->\n旧表\n"
                 "<!-- AUTO:end featured -->\n\n手工段落", encoding="utf-8")
    out = generate.replace_placeholders(p, "featured", "新精选表")
    check("featured 占位符替换", "旧表" not in out and "新精选表" in out)
    check("featured 手工段保留", "手工段落" in out and "标题" in out)

# T-F. 无私有分支：精选区入选仓库均为 public
check("精选区无私有仓库",
      all(REPO_BY_NAME[n].get("visibility") == "public" for n in names_in_feat))

if FAILURES:
    print("\n".join(FAILURES), file=sys.stderr)
    sys.exit(1)
print("ALL TESTS PASSED")
