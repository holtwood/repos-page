# AI Infra 视角：优先级与阅读范围

原则：**"行业重要性"与"是否完整读源码"分开评价**。三个月内不做任何大仓全仓通读。

## P0 — 个人作品集与面试主线（原创，不新建）

| 项目组 | 仓库 | 证据形态 |
|--------|------|---------|
| 推理系统主项目 | open-infra-ai/tiny-llm + paged-infer | 模型加载、量化、KV Cache、分页内存、调度、Serving、端到端差分验证 |
| Kernel 主项目 | open-infra-ai/cuda-foundations + cuflash-attn + triton-fused-ops | CUDA/Triton/FlashAttention、差分测试、Benchmark、性能分析 |
| C++ 工程辅助 | open-genomics/fq-compressor | CI、Sanitizer、并发流水线 |

## P1 — 选择性动手学习（Fork，只读相关模块）

SGEMM_CUDA、cuda-samples、cuda-course、extension-cpp、Triton-Puzzles、
nano-vllm、mini-sglang、lectures（详见 [forks-and-translations.md](forks-and-translations.md)）。

## P2 — 架构与实现参考（行业价值高，三个月内只产出"五个一"）

flash-attention、flashinfer、vllm、sglang、TensorRT-LLM、triton、LightLLM。

每个 P2 仓库只形成：

1. 一张架构图
2. 一条关键调用链
3. 两到三个核心数据结构
4. 一个可运行实验
5. 五个面试问题

（产出落在 [ai-infra-interview-prep](https://github.com/holtwood/ai-infra-interview-prep) 的对应周文件，
仓库本身不修改。）

## P3 — 按需或低优先级

minGPT、LLM-Workshop、dataflowr-notebooks、tutorials（Triton Inference Server）、ompi、tvm。

- TVM 仅在明确投递 ML Compiler 岗时提升为主线，否则保持选修。
- 非 AI Infra 项目（生物信息、工具类）见 [original-projects.md](original-projects.md)、
  [tools-and-unrelated.md](tools-and-unrelated.md)，不进入 12 周核心路线。
