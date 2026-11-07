# 检索资源与采用决定

检索日期：2026-11-07。项目功能来自维护者说明；本机验证结果以setup_verification.json和mcp_smoke_test.json为准。

| 资源 | 用途 | 决定 |
|---|---|---|
| [U-C4N/Autocad-MCP](https://github.com/U-C4N/Autocad-MCP) | COM实时AutoCAD及离线DXF自动化 | 已安装，固定源码提交见PROJECT_SPEC |
| [ezdxf](https://github.com/mozman/ezdxf) | DXF读写 | 已作为MCP依赖安装；不原生编辑DWG |
| [AutoCAD redraw skill](https://github.com/pengxiaoan/autocad-dwg-redraw-skill) | 原图对象剖析、重绘和核对 | 项目级安装，仅按需要使用检查功能 |
| [pyautocad](https://github.com/reclosedev/pyautocad) | Python COM封装 | 备选，未安装 |
| [GElectrical](https://github.com/manuvarkey/GElectrical) | 压降、短路和保护配合分析 | 备选，未安装，不默认判定香港合规 |
| [acad-api-skill](https://github.com/ADN-DevTech/acad-api-skill) | .NET插件开发 | 当前不需要，未安装 |
| [EMSD Wiring CoP](https://www.emsd.gov.hk/en/electricity_safety/publications/codes_of_practice/index.html) | 回路及电缆设计 | 2025英文PDF已下载 |
| [EMSD版本过渡说明](https://www.emsd.gov.hk/en/electricity_safety/new_edition_cop/new_edition_cop_electricity_wiring_regulations/) | 2020/2025版本选择背景 | 课程采用版本另行登记 |
| [CLP承办商资料入口](https://www.clp.com.hk/en/electrical-contractors) | COP101 v16正文/图纸、Supply Rules和计量指南 | 官网链接已确认，直接下载403，待获取PDF |
| [BEC与技术指引](https://www.emsd.gov.hk/beeo/en/mibec_beeo_codtechguidelines.html) | 能效、LPD和控制 | BEC2024英文PDF已下载 |
| [Cap406E](https://www.elegislation.gov.hk/hk/cap406E) | 法规背景 | 动态网页未逐条核读 |
| [建筑署一般规格2022含2025勘误](https://www.archsd.gov.hk/media/publications-publicity/general-specification-for-building-serivces/BSGS_2022_Edition_wCorr_GSBS04-2022_%28Apr2025%29.pdf) | 电气设备/安装补充参考 | 链接保存，当前未下载 |
| [SkeySpot](https://arxiv.org/abs/2508.10449) | 电气图例检测研究 | 方法参考，不安装模型 |
| [CAD-Assistant](https://arxiv.org/abs/2412.13810) | FreeCAD工具调用与反馈迭代研究 | 方法参考，不作为AutoCAD接入方案 |
| [Codex MCP官方说明](https://developers.openai.com/codex/mcp) | stdio服务配置 | 本项目配置依据 |
| [Codex项目配置官方说明](https://learn.chatgpt.com/docs/config-file/config-basic) | 项目级config.toml | 本项目配置依据 |

完整PDF直链、下载状态、文件长度及SHA256见 `03_Technical_References/Official/sources.json`。PDF已下载只表示本地可用，尚未逐条完成设计适用性审查。
