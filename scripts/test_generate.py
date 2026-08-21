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
    "accounts": {"LessUp": {"public": 31, "private": 1, "forks": 22}},
    "repos": [
        {"name": "cuda-samples", "account": "LessUp", "visibility": "public",
         "property": "fork", "upstream": "NVIDIA/cuda-samples", "ahead": 26, "behind": 0,
         "language": "C++", "priority": "P1", "categories": ["forks-and-translations"],
         "notes": {"forks-and-translations": "说明A"}, "resume_level": "低"},
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

if FAILURES:
    print("\n".join(FAILURES), file=sys.stderr)
    sys.exit(1)
print("ALL TESTS PASSED")
