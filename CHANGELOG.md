# Changelog

本项目所有重要迭代变更记录，格式遵循 Keep a Changelog 规范，版本采用语义化版本。

> 说明：v0.1 为项目初创阶段，早期开发未走PR流程；v0.2 开始规范化分支+PR合并管理。

## [v0.2] - 2026-06-05（#1 PR已合并｜LLM底层模块）

### Added

- 新增 backend/llm.py：封装DoubaoClient单例客户端，对接火山方舟豆包Seed-1.6 API
- 实现长篇小说智能分段算法，优先按段落分割，单段上限3000字符，保障语义完整
- 引入python-dotenv环境密钥，.env加入.gitignore，杜绝密钥泄露
- 固定temperature=0.3，约束大模型输出格式统一
- 新增 test_llm.py 自测用例
- 更新 requirements.txt 依赖

### Changed

- 优化项目.gitignore配置

## [v0.1] - 2026-06-05（无PR，项目骨架搭建）

### Added

- 搭建项目前后端目录结构
- 初始化backend基础工程
- 完成项目基础配置

## [Unreleased]（待开发）

### Todo

- 剧本YAML结构化生成模块开发
- 前端页面对接LLM解析接口
- 数据库接入，小说素材持久化存储