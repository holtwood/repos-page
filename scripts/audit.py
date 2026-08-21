#!/usr/bin/env python3
"""GitHub Repos Hub 审计：gh api 拉取实时数据刷新 repos.json。

只更新结构化且可靠的数据：
  audited_at / accounts.public / accounts.forks /
  visibility / language / upstream / ahead / behind / links_ok

绝不覆盖人工判断字段：notes / priority / resume / resume_level /
categories / domain / ai_relevance / license / contributors。
accounts.private 数量也保留人工维护（Actions 的 GITHUB_TOKEN 无私有仓库读权限）。

用法：
  python3 scripts/audit.py            # 更新 repos.json（有变化时）
  python3 scripts/audit.py --dry-run  # 只打印差异，不写文件；有差异退出 1
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
    r = subprocess.run(["gh", *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)} failed: {r.stderr.strip()}")
    return r


def fetch_repo_list(account):
    """gh repo list -> [{name, isFork, visibility}]（visibility 为 PUBLIC/PRIVATE）。"""
    r = gh(["repo", "list", account, "--limit", "100", "--json",
            "name,isFork,visibility"])
    return json.loads(r.stdout)


def fetch_repo_meta(account, name):
    """gh api repos/{a}/{n} -> (visibility, parent_full_name, is_fork, default_branch, language)"""
    r = gh(["api", f"repos/{account}/{name}", "--jq",
            ".visibility, .parent.full_name, .fork, .default_branch, .language"],
           check=False)
    if r.returncode != 0:
        return None
    lines = r.stdout.strip().splitlines()
    return (lines[0].strip().lower() if len(lines) > 0 else "",
            lines[1].strip() if len(lines) > 1 and lines[1].strip() != "null" else "",
            lines[2].strip().lower() == "true" if len(lines) > 2 else False,
            lines[3].strip() if len(lines) > 3 and lines[3].strip() != "null" else "main",
            lines[4].strip() if len(lines) > 4 and lines[4].strip() != "null" else "")


def fetch_compare(upstream, account, name, branch):
    r = gh(["api", f"repos/{upstream}/compare/{branch}...{account}:{name}:{branch}",
            "--jq", ".ahead_by, .behind_by"], check=False)
    if r.returncode != 0:
        return None
    a, b = r.stdout.split()
    return int(a), int(b)


def load_data():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="只打印差异，不写文件；有差异退出 1")
    args = ap.parse_args()

    if not shutil.which("gh"):
        print("ERROR: gh CLI 不可用", file=sys.stderr)
        sys.exit(2)

    data = load_data()
    changes = []

    # 1. 账号统计：public/forks 可靠刷新，private 保留人工值
    for acct in ACCOUNTS:
        try:
            repos = fetch_repo_list(acct)
        except RuntimeError as e:
            print(f"WARN: {e}", file=sys.stderr)
            continue
        public = sum(1 for r in repos if r.get("visibility") == "PUBLIC")
        forks = sum(1 for r in repos if r.get("isFork"))
        old = data["accounts"].get(acct, {})
        old_stats = {k: old.get(k) for k in ("public", "private", "forks")}
        new_stats = {"public": public, "private": old.get("private", 0),
                     "forks": forks, "note": old.get("note", "")}
        if old_stats != {k: new_stats[k] for k in ("public", "private", "forks")}:
            changes.append(f"accounts.{acct}: public/forks "
                           f"{old.get('public')}/{old.get('forks')} -> {public}/{forks}")
        data["accounts"][acct] = new_stats

    # 2. 逐仓库刷新结构化字段
    for repo in data["repos"]:
        name, acct = repo["name"], repo["account"]
        if name == ".github":
            continue
        meta = fetch_repo_meta(acct, name)
        if meta is None:
            changes.append(f"{acct}/{name}: 404/不可达")
            repo["links_ok"] = False
            continue
        visibility, parent, is_fork, branch, language = meta

        if repo.get("visibility") != visibility:
            changes.append(f"{acct}/{name} visibility: "
                           f"{repo.get('visibility')} -> {visibility}")
            repo["visibility"] = visibility
        # language 仅在 JSON 为空时填充：已有的人工标注（如 Python/CUDA）不被覆盖
        if language and not repo.get("language"):
            changes.append(f"{acct}/{name} language: (空) -> {language}")
            repo["language"] = language
        if not repo.get("links_ok"):
            changes.append(f"{acct}/{name} links_ok: false -> true")
        repo["links_ok"] = True

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
                    changes.append(f"{acct}/{name} ahead/behind: "
                                   f"{repo.get('ahead')}/{repo.get('behind')} -> {a}/{b}")
                    repo["ahead"], repo["behind"] = a, b

    # 3. 仓库清单差异检测：仅 LessUp（该账号 repos[] 要求全覆盖）；
    # org 账号部分仓库设计上不入库（手工列举分类），不检测避免噪声
    listed = {}
    for acct in ["LessUp"]:
        try:
            listed[acct] = {r["name"] for r in fetch_repo_list(acct)
                            if r.get("visibility") == "PUBLIC"}
        except RuntimeError:
            listed[acct] = set()
    for acct in ["LessUp"]:
        in_json = {r["name"] for r in data["repos"] if r["account"] == acct}
        missing = listed[acct] - in_json
        extra = in_json - listed[acct]
        for name in sorted(missing):
            print(f"INFO: 新公开仓库未收录: {acct}/{name}（需人工补 categories/notes）")
        for name in sorted(extra):
            print(f"INFO: repos.json 有但 gh 未列出: {acct}/{name}（可能已删除/迁移）")

    # 4. audited_at
    from datetime import date
    today = date.today().isoformat()
    if data.get("audited_at") != today:
        changes.append(f"audited_at: {data.get('audited_at')} -> {today}")
        data["audited_at"] = today

    # 4. 写出
    if args.dry_run:
        print("DRY RUN — 以下字段将变更:")
        for c in changes:
            print("  " + c)
        sys.exit(1 if changes else 0)

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
