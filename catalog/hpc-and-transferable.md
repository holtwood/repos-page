# HPC 与可迁移能力项目

这些项目不直接属于 LLM Infra，但支撑"性能工程"的通用叙事（C++、并发、
SIMD、压缩、实时系统），在面试中作为背景与辅助证据使用。

| 项目 | 能力信号 | 使用建议 |
|------|---------|---------|
| [open-genomics/fq-compressor](https://github.com/open-genomics/fq-compressor) | C++23、oneTBB 并发流水线、CI/Sanitizer、O(1) 随机访问数据结构 | C++ 工程质量辅助项目（P0 辅助） |
| [open-genomics/fastq-tools](https://github.com/open-genomics/fastq-tools) | 零拷贝 I/O、流水线设计 | 辅助 |
| [open-genomics/minibwa-rust](https://github.com/open-genomics/minibwa-rust) | Rust 系统编程、算法重写 | 辅助 |
| [cpp-high-performance-guide](https://github.com/LessUp/cpp-high-performance-guide) | C++20 性能工程、SIMD、内存优化、基准测试 | 辅助；内容可作面试复习材料 |
| [bitcal](https://github.com/LessUp/bitcal) | C++23、AVX2 位运算 | 低优先级 |
| [vibe-knight/compress-kit](https://github.com/vibe-knight/compress-kit) | 跨语言压缩算法与二进制级验证 | 低优先级 |
| [vibe-knight/cudaimg](https://github.com/vibe-knight/cudaimg) | CUDA 图像处理 | 可作 CUDA 广度证据 |
| Fork: ompi | MPI/分布式通信理论学习参考 | P3，仅通信话题引用 |
| Fork: the-art-of-hpc-zh（已删除） | HPC 教材中文翻译 | 已移除，见 [retired-and-migrated.md](retired-and-migrated.md) |
