# 组织仓库概览与贡献审计

审计日期：2026-08-19。方法：`gh api orgs/{org}/repos` + `repos/{repo}/contributors` 逐仓核对。

## open-infra-ai（AI Infra 作品集，7 个公开仓库）

组织成员：LessUp、Lumkai、TideTree。**但全部 7 个仓库的代码贡献者仅为 LessUp
（另含 dependabot[bot]/github-actions[bot]）**，因此下列仓库可以如实表述为
"个人主导开发"的组织仓库。

| 仓库 | 语言 | License | 贡献者 | 定位 |
|------|------|---------|--------|------|
| [aicl-lab](https://github.com/open-infra-ai/aicl-lab) | Markdown | - | LessUp | 五仓作品集 landing 页与计划/面试材料唯一权威源 |
| [cuda-foundations](https://github.com/open-infra-ai/cuda-foundations) | C++ | MIT | LessUp + CI bot | L1：CUDA 算子工程学习路径（原 cuda-kernel-academy） |
| [triton-fused-ops](https://github.com/open-infra-ai/triton-fused-ops) | Python | MIT | LessUp | L2：Triton 算子库 + torch.library 注册 |
| [cuflash-attn](https://github.com/open-infra-ai/cuflash-attn) | CUDA | MIT | LessUp | L3：CUDA C++ FlashAttention 前后向（WMMA） |
| [tiny-llm](https://github.com/open-infra-ai/tiny-llm) | C++ | MIT | LessUp | L4：CUDA 原生 C++ 推理引擎（GGUF/W8A16/分页 KV） |
| [paged-infer](https://github.com/open-infra-ai/paged-infer) | Rust | MIT | LessUp | L4：PagedAttention 分页 KV + Continuous Batching 控制面 |
| [.github](https://github.com/open-infra-ai/.github) | - | - | - | 组织级配置 |

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
