# 已撤销/已迁移仓库与失效链接记录

审计日期：2026-08-19。方法：对主页与文档中出现的每个仓库 URL 做 HTTP 状态 +
301 Location 检查，并用 `gh api repos/...` 核对当前归属。

## 已删除仓库（主页曾展示，现已 404）

| 旧地址 | 状态 | 处理 |
|--------|------|------|
| holtwood/sgemm-optimization | 404，无重定向 | 主页移除展示；SGEMM 主题由 SGEMM_CUDA（Fork+中文注释）与 open-infra-ai/cuda-foundations 覆盖 |
| holtwood/the-art-of-hpc-zh | 404，无重定向 | 主页移除展示（HPC 教材中文翻译，已放弃） |
| holtwood/cursor-rules | 404，无重定向 | 主页移除展示 |
| holtwood/awesome-claude-skills-zh | 404，无重定向 | 主页移除展示 |

## 迁移后靠 GitHub 自动重定向工作的链接（5 个）

| 旧地址（holtwood/…） | 301 目标（规范地址） |
|--------------------|--------------------|
| fq-compressor | open-genomics/fq-compressor |
| fastq-tools | open-genomics/fastq-tools |
| micos-2024 | open-genomics/micos-2024 |
| awesome-bioinfo-algorithms | open-genomics/awesome-bioinfo-algorithms |
| awesome-compression | vibe-knight/awesome-compression |

## 迁移后重定向失效、需改写为新地址的链接

| 主页旧链接 | 实际所在 | 处理 |
|-----------|---------|------|
| holtwood/wiki-bioinfo | open-genomics/wiki-bioinfo | 主页改用规范地址 |
| holtwood/compress-kit | vibe-knight/compress-kit | 同上 |
| holtwood/bookmarks-cleaner | vibe-knight/bookmarks-cleaner | 同上 |
| holtwood/graph-viewer | vibe-knight/graph-viewer | 同上 |
| holtwood/meta-human | vibe-knight/meta-human | 同上 |
| holtwood/mind-gym | vibe-knight/mind-gym | 同上 |
| holtwood/yolo-toys | vibe-knight/yolo-toys | 同上 |
| holtwood/webrtc | vibe-knight/webrtc-demo（信令服务器另在 webrtc-signaling） | 同上 |

## 组织改名

旧组织名 `aicl-lab` → 现组织名 `open-infra-ai`。旧 URL（如
`github.com/aicl-lab/cuda-foundations`）当前靠 GitHub 301 重定向工作，
所有文档应改用 `open-infra-ai` 规范地址。
