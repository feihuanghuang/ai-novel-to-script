# 林中箱庭项目文档

*七牛云 × XEngineer 暑期实训营 · 第三批次  第三项 参赛作品*

一款 AI 辅助剧本创作工具，将小说自动转换为结构化 YAML 格式分镜头短剧剧本。

![c3c4659d238b778c2af02d371d2365a2](image/c3c4659d238b778c2af02d371d2365a2.png)

## 演示视频

https://www.bilibili.com/video/BV1caE86BEDG/?vd_source=f8ecc52d3a26cc68573e861e1e7abce7#reply116710082349305## 项目演示
<iframe 
  src="//player.bilibili.com/player.html?bvid=BV1caE86BEDG&p=1&high_quality=1&danmaku=0" 
  width="100%" 
  height="450" 
  scrolling="no" 
  border="0" 
  frameborder="no" 
  framespacing="0" 
  allowfullscreen="true">
</iframe>



## 项目简介

本项目实现小说自动转结构化短剧剧本，内置标准化 Prompt 统一输出格式，自动生成标题、剧情简介、场景、镜头、画面、台词 / 音效。 目前已接入 豆包、DeepSeek、通义千问 三大平台共 9 款主流大模型，支持自由切换，兼容 OpenAI 标准调用协议。

核心能力：

- 小说一键生成标准分镜头剧本（YAML）
- 多平台大模型无缝切换，同平台密钥通用
- 剧本在线编辑、一键复制、文件下载、历史记录管理
- 完善输入校验、异常捕获、防重复提交
- 前端视觉美化，支持 PC / 手机局域网访问

## 项目架构

```Plain
NovelToScript/
├── backend/
│   └── llm.py                  # 三大平台大模型客户端统一封装
├── static/
│   └── index.html              # 前端主页面
├── database.py                 # 数据库模型 & 连接管理
├── main.py                     # 项目入口、接口、服务启动
├── requirements.txt            # 项目依赖
├── .gitignore                  # 忽略密钥、缓存、IDE 文件
├── CHANGELOG.md                # 版本迭代日志（Keep a Changelog 规范）
└── README.md                   # 本文件
```

## 技术栈

| 层     | 技术                                                         |
| ------ | ------------------------------------------------------------ |
| 前端   | 原生 HTML / CSS / JavaScript                                 |
| 后端   | Python + FastAPI + SQLAlchemy + OpenAI SDK + PyYAML + python-dotenv |
| 数据库 | SQLite（开箱即用，无需额外部署）                             |
| 大模型 | 火山方舟豆包、DeepSeek、阿里云通义千问                       |

## 已接入模型列表（共 9 款）

### 1. 豆包（字节火山方舟）

- doubao-seed-2.0-pro
- doubao-seed-2.0-lite
- doubao-seed-2.0-mini

### 2. DeepSeek（深度求索）

- deepseek-v4-pro
- deepseek-v4-flash
- deepseek-r1-0528

### 3. 通义千问（阿里云 DashScope）

- qwen3.7-max
- qwen3.7-plus
- qwen3.5-flash

使用说明：选择对应平台模型时，请填写该平台专属 API Key；同一平台下一套密钥可通用旗下所有模型（需账号具备对应模型权限）。

## 剧本 Schema（标准完整示例）

具体参考：剧本Schema设计文档.md

```yaml
# 全局基础信息
title: 魔主方源：春秋蝉之围       # 短剧剧本整体标题，取自小说核心剧情，作为剧本文件名、页面展示标题
summary: 正道群雄围攻方源索要春秋蝉，方源浴血对峙夕阳下  # 单集剧情一句话简介，概括核心冲突与剧情走向，用于页面简介展示

# 场次列表：按剧情时间线排序，一个剧本包含多个独立场景
scenes:
- scene_id: S01                   # 场景唯一ID，全局场景序号递增（S01、S02...），用于剧本定位、编辑、检索
  location: 山间悬崖空地           # 场景拍摄地点，明确剧情发生的物理场景
  time: 日（黄昏）                 # 场景时间属性，固定为 日/夜+具体时段，适配短剧拍摄光影逻辑

  # 镜头列表：单场景内分镜序列，按播放顺序排列，为最小拍摄单元
  shots:
  - shot_id: 1                    # 单镜头唯一ID，同场景内序号递增，区分不同分镜
    frame: 全景                   # 镜头景别：远景/全景/中景/近景/特写，规范影视镜头语言
    duration: 5                   # 镜头播放时长，单位：秒，控制短剧成片节奏
    visual: 山间空地，正道群雄持兵器围成圈，中心方源浴血而立，破袍随风飘动  # 镜头画面描述，纯视觉场景、人物、动作描写，无声音信息
    audio: 【嘈杂人声】“交出春秋蝉！”“踏破魔窟！”“罪无可恕！”  # 镜头音频内容，包含环境音效、人物群体台词

  - shot_id: 2
    frame: 近景
    duration: 3
    visual: 方源披头散发，碧绿大袍残破染血，面无表情，目光幽深如古井
    audio: 【山风声】  # 纯环境音效，烘托场景氛围，无人物台词

  - shot_id: 3
    frame: 特写
    duration: 2
    visual: 方源脚下积起的暗红血水，映着夕阳微光
    audio: 【血滴声】  # 细节音效，强化画面氛围感与沉浸感

  - shot_id: 4
    frame: 中景
    duration: 4
    visual: 几位正道人物神态各异：咆哮、冷笑、警惕眯眼、捂伤口发抖
    audio: 正道长老(愤怒):“方老魔，你别妄图反抗！” 女修(怨毒):“我要让你生不如死！”  # 带情绪标注的单人/多人台词，明确角色情绪与台词内容

  - shot_id: 5
    frame: 全景
    duration: 6
    visual: 夕阳西下，晚霞如火，群雄与方源对峙，影子被余晖拉长
    audio: 【山风声】【归鸟啼鸣】  # 多重环境音效叠加，渲染场景整体氛围
```

## 快速开始

### 方式一：一键启动（推荐）

```bash
# 1. 安装依赖
pip install -r 

# 2. 启动服务
python main.py
```

启动成功后终端会输出访问地址：

- 本地访问：http://localhost:8000
- 局域网访问：http:// 你的电脑 IP:8000

### 方式二：手机访问（同一局域网 / WiFi）

1. 电脑与手机连接同一个网络
2. 查看电脑局域网 IPv4 地址
3. 手机浏览器访问：http:// 电脑 IP:8000
4. 关闭电脑防火墙 / 安全软件，避免拦截访问

## 核心流程

选择目标大模型 → 填入对应平台 API Key → 粘贴小说内容 → 模型生成剧本 ↓ 剧本在线编辑 / 复制 / 下载 / 保存

## API 概览

| 接口                 | 请求方式 | 用途                     |
| -------------------- | -------- | ------------------------ |
| /api/generate-script | POST     | 小说转 YAML 剧本核心接口 |
| /api/scripts         | GET      | 获取全部历史剧本列表     |
| /api/scripts/{id}    | GET      | 查看单条剧本详情         |
| /api/scripts/{id}    | DELETE   | 删除指定剧本             |
| /api/scripts         | POST     | 保存剧本至数据库         |
| /api/health          | GET      | 服务健康检查             |

## 版本规范 & 迭代日志

项目采用 语义化版本号，遵循 Keep a Changelog 规范，所有迭代、新增、修改、修复均记录在 [CHANGELOG.md](CHANGELOG.md)。

- v0.1.0 ~ v0.2.0：项目骨架、LLM 底层能力搭建
- v0.3.0 ~ v0.5.0：接口完善、密钥管理、基础模型对接
- v0.6.0：前端全面视觉重构、UI 美化、交互优化
- v0.7.0：三大平台 9 款大模型完整适配（当前最新版）

## 注意事项

1. 密钥安全：请勿将 API Key 提交至公共仓库，.env 等密钥文件已加入 .gitignore
2. 网络权限：校园网 / 内网环境下，外网无法直接访问，如需外网使用可搭配内网穿透工具
3. 调用权限：API Key 需提前在对应平台控制台开通目标模型调用权限
4. 超时配置：全局接口与模型调用超时统一设置为 500s，支持超长文本生成

## License