# Changelog
本项目所有重要迭代变更记录，格式遵循 Keep a Changelog 规范，版本采用语义化版本。
> 说明：v0.1.0 为项目初创阶段，早期开发未走PR流程；v0.2.0 开始规范化分支+PR合并管理。

## [Unreleased]
### Added
- 数据库接入，小说素材与生成剧本持久化存储
- 前端页面对接LLM解析接口

## [v0.4.0] - 2026-06-06
### Added
- 新增剧本YAML结构化生成接口 `/api/generate-script`
- 支持自动清理大模型输出的markdown代码块标记
- 内置YAML语法校验，解析失败返回明确错误信息

### Fixed
- 统一方法名为 `generate_text()`，解决YAML生成调用不匹配问题
- 修复 `generate_script_yaml` 方法缩进错误，正确归属类内
- 实现标准单例模式，全局仅初始化一次客户端
- 将 `split_text()` 分片函数封装到 `DoubaoClient` 类内
- 规范 `yaml` 库导入位置，符合Python编码规范

## [v0.3.0] - 2026-06-05
### Docs
- 标准化项目Changelog文档，统一语义化版本格式
- 补齐v0.1.0、v0.2.0迭代记录，梳理后续迭代开发规划
- 无业务代码改动，仅文档维护优化

## [v0.2.0] - 2026-06-05（#1 PR已合并｜LLM底层模块）
### Added
- 新增 backend/llm.py：封装DoubaoClient单例客户端，对接火山方舟豆包Seed-1.6 API
- 实现长篇小说智能分段算法，优先按段落分割，单段上限3000字符，保障语义完整
- 引入python-dotenv管理环境密钥，.env配置文件加入.gitignore，杜绝密钥泄露
- 固定模型temperature=0.3，约束大模型输出格式统一，方便后端结构化解析
- 新增 test_llm.py 自测用例，完善接口连通、超长文本分片全量自测
- 更新 requirements.txt，补充项目第三方依赖包

### Changed
- 优化项目.gitignore配置，屏蔽密钥、缓存、IDE配置文件

## [v0.1.0] - 2026-06-05（无PR，项目骨架搭建）
### Added
- 搭建项目前后端目录分层结构，初始化backend基础工程目录
- 配置项目基础运行环境、初始依赖清单
- 完成项目基础配置、目录分层规划，奠定整体项目架构