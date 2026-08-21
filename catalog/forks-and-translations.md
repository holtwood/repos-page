# Fork 与 AI 翻译仓库

审计日期：2026-08-19。共 22 个公开 Fork。

**重要声明**：这些 Fork 均为上游开源项目的镜像 + 个人中文注释/翻译（AI 辅助完成），
**不是个人原创项目**，不得写入简历"项目经历"。ahead 提交内容为中文注释/翻译 commit
（已抽样核实：SGEMM_CUDA 与 cuda-samples 的 ahead 提交均为 `docs: 中文注释` 类 commit）。
ahead/behind 数字为 2026-08-19 GitHub compare API 快照。

<!-- AUTO:start forks-and-translations -->
| Fork | 上游 | ahead/behind | 主语言 | AI Infra 优先级 | 学习价值与建议阅读范围 |
|---|---|---|---|---|---|
| [cuda-samples](https://github.com/LessUp/cuda-samples) | [NVIDIA/cuda-samples](https://github.com/NVIDIA/cuda-samples) | 26/0 | C++ | P1 | CUDA 特性官方示例；只跑 0_Introduction、2_Concepts_and_Techniques、矩阵乘法相关样例 |
| [SGEMM_CUDA](https://github.com/LessUp/SGEMM_CUDA) | [siboehm/SGEMM_CUDA](https://github.com/siboehm/SGEMM_CUDA) | 2/0 | CUDA | P1 | SGEMM 优化阶梯（naive→WMMA）经典教程，已中文化 |
| [cuda-course](https://github.com/LessUp/cuda-course) | [Infatoshi/cuda-course](https://github.com/Infatoshi/cuda-course) | 2/0 | CUDA | P1 | CUDA 入门课程，与 cuda-samples 互补，选其一 |
| [Triton-Puzzles](https://github.com/LessUp/Triton-Puzzles) | [gpu-mode/Triton-Puzzles](https://github.com/gpu-mode/Triton-Puzzles) | 2/0 | Notebook | P1 | Triton 动手练习，第 4 周配合使用 |
| [extension-cpp](https://github.com/LessUp/extension-cpp) | [pytorch/extension-cpp](https://github.com/pytorch/extension-cpp) | 5/0 | Python | P1 | PyTorch C++ 扩展官方模板 |
| [nano-vllm](https://github.com/LessUp/nano-vllm) | [GeeeekExplorer/nano-vllm](https://github.com/GeeeekExplorer/nano-vllm) | 3/0 | Python | P1 | 极简 vLLM 复现，理解 PagedAttention 最短路径 |
| [mini-sglang](https://github.com/LessUp/mini-sglang) | [sgl-project/mini-sglang](https://github.com/sgl-project/mini-sglang) | 6/0 | Python | P1 | 紧凑版 SGLang，理解 serving 主循环 |
| [flash-attention](https://github.com/LessUp/flash-attention) | [Dao-AILab/flash-attention](https://github.com/Dao-AILab/flash-attention) | 2/2 | Python/CUDA | P2 | 只读 core 目录 FlashAttention 前向实现 |
| [flashinfer](https://github.com/LessUp/flashinfer) | [flashinfer-ai/flashinfer](https://github.com/flashinfer-ai/flashinfer) | 8/102 | Python/CUDA | P2 | Kernel 库，对照 triton-fused-ops 的 API 设计 |
| [vllm](https://github.com/LessUp/vllm) | [vllm-project/vllm](https://github.com/vllm-project/vllm) | 14/498 | Python | P2 | 只读 core scheduler、block manager、worker 主链路 |
| [sglang](https://github.com/LessUp/sglang) | [sgl-project/sglang](https://github.com/sgl-project/sglang) | 12/637 | Python | P2 | 只读 scheduler 与 router |
| [TensorRT-LLM](https://github.com/LessUp/TensorRT-LLM) | [NVIDIA/TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) | 1/363 | Python/C++ | P2 | 只读 attention/quantization 文档与 benchmark 目录 |
| [triton](https://github.com/LessUp/triton) | [triton-lang/triton](https://github.com/triton-lang/triton) | 0/68 | MLIR | P2 | 只读 python/triton 语言前端与 tutorial |
| [tvm](https://github.com/LessUp/tvm) | [apache/tvm](https://github.com/apache/tvm) | 1/20 | Python | P3 | 仅投 ML Compiler 岗时读 tensor expression 与 TE 调度 |
| [LightLLM](https://github.com/LessUp/LightLLM) | [ModelTC/LightLLM](https://github.com/ModelTC/LightLLM) | 12/8 | Python | P2 | 轻量推理框架，triton kernel 实现可对照 |
| [lectures](https://github.com/LessUp/lectures) | [gpu-mode/lectures](https://github.com/gpu-mode/lectures) | 3/0 | Notebook | P1 | GPU MODE 讲座材料，性能分析专题 |
| [dataflowr-notebooks](https://github.com/LessUp/dataflowr-notebooks) | [dataflowr/notebooks](https://github.com/dataflowr/notebooks) | 16/0 | Notebook | P3 | 深度学习课程笔记，按需查阅 |
| [LLM-Workshop](https://github.com/LessUp/LLM-Workshop) | [tylerelyt/LLM-Workshop](https://github.com/tylerelyt/LLM-Workshop) | 8/0 | Python | P3 | LLM 应用课程，与 Infra 主线弱相关 |
| [minGPT](https://github.com/LessUp/minGPT) | [karpathy/minGPT](https://github.com/karpathy/minGPT) | 5/0 | Python | P3 | GPT 最小实现，理解 Transformer 结构用 |
| [tutorials](https://github.com/LessUp/tutorials) | [triton-inference-server/tutorials](https://github.com/triton-inference-server/tutorials) | 7/1 | Python | P3 | Triton Inference Server 教程（注意与 Triton 语言区分） |
| [ompi](https://github.com/LessUp/ompi) | [open-mpi/ompi](https://github.com/open-mpi/ompi) | 13/48 | C | P3 | MPI 实现，分布式通信理论参考 |
| [Termius-Pro-zh_CN](https://github.com/LessUp/Termius-Pro-zh_CN) | [ArcSurge/Termius-Pro-zh_CN](https://github.com/ArcSurge/Termius-Pro-zh_CN) | 0/0 | Python | 无 | Termius 汉化，与 AI Infra 无关 |
<!-- AUTO:end forks-and-translations -->

各 Fork 的深度阅读笔记见 [../deep-dives/](../deep-dives/)。

**归属与 License**：所有 Fork 遵循各自上游 License；中文注释为 AI 辅助翻译成果，
在简历或主页中提及时必须标注"Fork + 中文注释"，不得表述为原创实现。
