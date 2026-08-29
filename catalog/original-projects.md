# 组织下的原创项目（含贡献者审计）

审计日期：2026-08-19。贡献者数据来自 GitHub contributors API；仅 holtwood（含 bot）
的项目可表述为个人主导。**这是简历"项目经历"的候选池。**

## open-infra-ai — AI Infra 作品集（P0，简历主线）

贡献者审计：全部仓库仅 holtwood（+ CI/dependabot bot）。

<!-- AUTO:start original-projects -->
| 项目 | 定位与证据 | 简历用法 |
|---|---|---|
| [aicl-lab](https://github.com/open-infra-ai/aicl-lab) | 五仓 landing 页、计划与面试证据包唯一权威源 | 讲述入口 |
| [cuda-foundations](https://github.com/open-infra-ai/cuda-foundations) | CUDA 算子工程学习路径，SGEMM 到可复用推理组件（原 cuda-kernel-academy） | Kernel 主项目之一 |
| [triton-fused-ops](https://github.com/open-infra-ai/triton-fused-ops) | Triton 算子库（RMSNorm+RoPE/SwiGLU/FlashAttention/SGEMM）+ torch.library 注册 | Kernel 主项目之一 |
| [cuflash-attn](https://github.com/open-infra-ai/cuflash-attn) | 从零 CUDA C++ FlashAttention 前后向（FP16/BF16 WMMA），含 grid.y 越界修复与 causal 跳过优化 | Kernel 主项目之一 |
| [tiny-llm](https://github.com/open-infra-ai/tiny-llm) | CUDA 原生 C++ 推理引擎：GGUF 加载、W8A16 量化、分页 KV 策略 1；TPOT ≈ 6.1 ms/token（本机实测，RTX 3060 Laptop）；170 tests | 推理系统主项目 |
| [paged-infer](https://github.com/open-infra-ai/paged-infer) | PagedAttention 分页 KV + Continuous Batching 控制面（Rust）；3 并发 e2e 与 llama.cpp greedy 对齐（诚实记录量化差异） | 与 tiny-llm 组成推理系统主项目 |
<!-- AUTO:end original-projects -->

性能数字的硬件/版本/命令口径见各仓 README 与 [aicl-lab](https://github.com/open-infra-ai/aicl-lab) 证据包，此处不复制。

## open-genomics — 生物信息与 C++ 工程（P0 辅助 / P2）

贡献者审计：fq-compressor、fastq-tools 等 contributors 仅 holtwood（micos-2024 另有 dependabot）。

<!-- AUTO:start original-projects-genomics -->
| 项目 | 定位 | 简历用法 |
|---|---|---|
| [fq-compressor](https://github.com/open-genomics/fq-compressor) | C++23 高性能 FASTQ 压缩：3.97x 压缩比、O(1) 随机访问、oneTBB 并发流水线、CI/Sanitizer | C++ 工程质量辅助项目 |
| [fastq-tools](https://github.com/open-genomics/fastq-tools) | FASTQ 质控工具：零拷贝 I/O、TBB 流水线 | C++ 工程辅助 |
| [minibwa-rust](https://github.com/open-genomics/minibwa-rust) | Rust 重写 BWA 序列比对核心 | 系统能力辅助 |
| [fq-compressor-rust](https://github.com/open-genomics/fq-compressor-rust) | fq-compressor 的 Rust 版本 | 辅助 |
| [micos-2024](https://github.com/open-genomics/micos-2024) | 宏基因组综合分析平台（猛犸杯 2024 参赛项目） | 历史项目 |
| [wiki-bioinfo](https://github.com/open-genomics/wiki-bioinfo) | 中文生物信息知识库 | 社区贡献展示 |
| [awesome-bioinfo-algorithms](https://github.com/open-genomics/awesome-bioinfo-algorithms) | 算法知识库 + CLI 维护工具 | 低优先级 |
<!-- AUTO:end original-projects-genomics -->

## vibe-knight — 实验性与工具项目（P2/P3）

贡献者审计：抽查 compress-kit contributors 仅 holtwood；组织仅一名成员。
与 AI Infra 主线弱相关，仅在对应话题中使用：

- [compress-kit](https://github.com/vibe-knight/compress-kit)（C++/Go/Rust 跨语言压缩算法与二进制验证，P2）
- [cudaimg](https://github.com/vibe-knight/cudaimg)（CUDA 图像处理，P2）
- [webrtc-signaling](https://github.com/vibe-knight/webrtc-signaling) / [webrtc-demo](https://github.com/vibe-knight/webrtc-demo)（Go 实时系统背景）
- 其余（bookmarks-manager、bookmarks-cleaner、graph-viewer、mind-gym、meta-human、yolo-toys、utop、chatroom、brave-sync-notes、awesome-compression）为工具/应用实验，P3，不进入 AI Infra 简历主线。
