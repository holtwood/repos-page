# 🗺️ GitHub Repos Hub — holtwood 项目主页

> **我的开发项目主页**：主要开发项目一览 + 全部 GitHub 仓库的盘点、分类与导航中心。
> 本仓库是仓库深读（deep-dives）的唯一事实来源；学习计划与面试准备见
> [ai-infra-interview-prep](https://github.com/holtwood/ai-infra-interview-prep)，
> AI Infra 五仓作品集见 [open-infra-ai/aicl-lab](https://github.com/open-infra-ai/aicl-lab)。

**最近审计日期：2026-08-19**（基于 GitHub API 实时数据，方法见 [methodology.md](methodology.md)）

<!-- AUTO:start badges -->
![审计日期](https://img.shields.io/badge/审计-2026-08-30-4c9) ![仓库总数](https://img.shields.io/badge/仓库-69-4c9) ![公开](https://img.shields.io/badge/公开-62-blue) ![Fork](https://img.shields.io/badge/Fork-23-orange) ![文档站](https://img.shields.io/badge/文档站-docsify-8A2BE2)
<!-- AUTO:end badges -->

## ⭐ 主要项目精选

<!-- AUTO:start featured -->
| 项目 | 语言 | 归属 | 定位 |
|---|---|---|---|
| [aicl-lab](https://github.com/open-infra-ai/aicl-lab) | Markdown | open-infra-ai | 五仓 landing 页、计划与面试证据包唯一权威源 |
| [cuda-foundations](https://github.com/open-infra-ai/cuda-foundations) | C++ | open-infra-ai | CUDA 算子工程学习路径，SGEMM 到可复用推理组件（原 cuda-kernel-academy） |
| [cuflash-attn](https://github.com/open-infra-ai/cuflash-attn) | CUDA | open-infra-ai | 从零 CUDA C++ FlashAttention 前后向（FP16/BF16 WMMA），含 grid.y 越界修复与 causal 跳过优化 |
| [paged-infer](https://github.com/open-infra-ai/paged-infer) | Rust | open-infra-ai | PagedAttention 分页 KV + Continuous Batching 控制面（Rust）；3 并发 e2e 与 llama.cpp greedy 对齐（诚实记录量化差异） |
| [tiny-llm](https://github.com/open-infra-ai/tiny-llm) | C++ | open-infra-ai | CUDA 原生 C++ 推理引擎：GGUF 加载、W8A16 量化、分页 KV 策略 1；TPOT ≈ 6.1 ms/token（本机实测，RTX 3060 Laptop）；170 tests |
| [triton-fused-ops](https://github.com/open-infra-ai/triton-fused-ops) | Python | open-infra-ai | Triton 算子库（RMSNorm+RoPE/SwiGLU/FlashAttention/SGEMM）+ torch.library 注册 |
| [fastq-tools](https://github.com/open-genomics/fastq-tools) | C++ | open-genomics | FASTQ 质控工具：零拷贝 I/O、TBB 流水线 |
| [fq-compressor](https://github.com/open-genomics/fq-compressor) | C++ | open-genomics | C++23 高性能 FASTQ 压缩：3.97x 压缩比、O(1) 随机访问、oneTBB 并发流水线、CI/Sanitizer |
| [minibwa-rust](https://github.com/open-genomics/minibwa-rust) | Rust | open-genomics | Rust 重写 BWA 序列比对核心 |
| [JadeAI](https://github.com/holtwood/JadeAI) | TypeScript | holtwood | AI 驱动的简历与求职工作台 |
| [ai-infra-interview-prep](https://github.com/holtwood/ai-infra-interview-prep) | Markdown | holtwood | 12 周 AI Infra 转行计划、能力矩阵、面试执行 |
| [cpp-high-performance-guide](https://github.com/holtwood/cpp-high-performance-guide) | C++ | holtwood | 可运行的 C++20 性能工程指南：示例、基准、VitePress 文档站 |
<!-- AUTO:end featured -->

> 完整盘点见下方各分类与[文档站](https://holtwood.github.io/repos-page/)。

## 📖 文档站与完整盘点

可搜索文档站（GitHub Pages）：**https://holtwood.github.io/repos-page/**（docsify 静态站，支持全文搜索与侧边栏导航）

完整盘点按分类：

- [holtwood 个人原创（非 Fork）公开仓库](catalog/lessup-owned.md)
- [Fork 与 AI 翻译仓库](catalog/forks-and-translations.md)
- [组织仓库概览与贡献审计](catalog/organizations.md)
- [组织下的原创项目（含贡献者审计）](catalog/original-projects.md)
- [AI Infra 优先级与阅读范围](catalog/ai-infra.md)
- [HPC 与可迁移能力项目](catalog/hpc-and-transferable.md)
- [工具类与非 AI Infra 项目](catalog/tools-and-unrelated.md)
- [已撤销/已迁移仓库与失效链接](catalog/retired-and-migrated.md)

深读笔记（21 篇）：[deep-dives/](deep-dives/) · 审计方法：[methodology.md](methodology.md)

## 账号概览

| 账号 | 可见仓库 | 公开 | 私有 | Fork |
|------|---------|------|------|------|
| holtwood（个人） | 32 | 31 | 1 | 22 |
| open-infra-ai | 7 | 7 | 0 | 0 |
| open-genomics | 12 | 7 | 5 | 0 |
| vibe-knight | 15 | 14 | 1 | 0 |

> 私有仓库信息不进入公开文档，仅说明"另有若干私有仓库未公开"。

## 目录结构

```
catalog/
  lessup-owned.md           # holtwood 个人原创（非 Fork）公开仓库
  forks-and-translations.md # 22 个 Fork：上游、ahead/behind、中文注释范围
  organizations.md          # 三个组织概览与贡献审计结论
  original-projects.md      # 组织下的原创项目（含贡献者审计）
  ai-infra.md               # AI Infra 视角：P0/P1/P2/P3 优先级与阅读范围
  hpc-and-transferable.md   # HPC 与可迁移能力项目
  tools-and-unrelated.md    # 工具类与非 AI Infra 项目
  retired-and-migrated.md   # 已删除/已迁移仓库与主页失效链接记录
deep-dives/                 # 21 个 Fork 仓库深度阅读笔记（唯一事实来源）
methodology.md              # 审计方法与字段定义
CHANGELOG.md
```

## 快速导航

- 想看**我自己的项目**（简历可用）→ [catalog/original-projects.md](catalog/original-projects.md)、[catalog/lessup-owned.md](catalog/lessup-owned.md)
- 想了解**某个 Fork 的架构与学习路径** → [deep-dives/](deep-dives/)
- 想按**学习优先级**排阅读顺序 → [catalog/ai-infra.md](catalog/ai-infra.md)
- 查**失效/迁移链接** → [catalog/retired-and-migrated.md](catalog/retired-and-migrated.md)

## 职责边界

| 仓库 | 职责 |
|------|------|
| repos-page（本仓库） | 仓库盘点、分类、导航、迁移记录、deep-dives |
| [ai-infra-interview-prep](https://github.com/holtwood/ai-infra-interview-prep) | 12 周计划、学习 TODO、能力矩阵、面试执行 |
| [open-infra-ai/aicl-lab](https://github.com/open-infra-ai/aicl-lab) | 五仓 AI Infra 技术证据与项目讲述的唯一事实来源 |
| [holtwood/LessUp](https://github.com/holtwood/LessUp) | 个人主页与成果展示 |
| [stars-index](https://github.com/holtwood/stars-index) | Star 资源分类索引（1300+ 条目） |
