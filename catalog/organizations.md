# 组织仓库概览与贡献审计

审计日期：2026-08-19。方法：`gh api orgs/{org}/repos` + `repos/{repo}/contributors` 逐仓核对。

## open-infra-ai（AI Infra 作品集，7 个公开仓库）

组织成员：LessUp、Lumkai、TideTree。**但全部 7 个仓库的代码贡献者仅为 LessUp
（另含 dependabot[bot]/github-actions[bot]）**，因此下列仓库可以如实表述为
"个人主导开发"的组织仓库。

<!-- AUTO:start organizations -->

<!-- AUTO:end organizations -->

> 旧组织名 `aicl-lab` 的 URL（如 `github.com/aicl-lab/xxx`）目前依赖 GitHub 301
> 重定向工作，规范地址应使用 `open-infra-ai`。

## open-genomics（生物信息与 C++ 工程，7 公开 + 5 私有）

组织成员：仅 LessUp。

公开仓库（7 个）：micos-2024、fastq-tools、awesome-bioinfo-algorithms、
fq-compressor、wiki-bioinfo、minibwa-rust、fq-compressor-rust，
详见 [original-projects.md](original-projects.md)。另有 5 个私有仓库，信息不公开。
其中 fq-compressor / fastq-tools / minibwa-rust 是 C++/Rust 工程质量与
生物信息背景的核心证据。

## vibe-knight（实验性与工具项目，14 公开 + 1 私有）

组织成员：仅 LessUp。公开仓库以工具和应用实验为主（WebRTC、书签工具、
压缩算法、CUDA 图像处理等），详见 [original-projects.md](original-projects.md)。
与 AI Infra 主线弱相关，个别（compress-kit、cudaimg）可作为辅助证据。
