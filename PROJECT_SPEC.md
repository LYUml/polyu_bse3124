# BSE3124 电气设计执行声明

更新日期：2026-11-07。本文定义项目目标、输入、工具、数据约束、执行顺序和验收标准。它是后续工作的执行入口；课程原题优先于本文。06_Research/background/WORKFLOW.md 保留详细背景。

## 当前执行优先级

最终文件只有04_Design_Outputs/submission/BSE3124_Final.pdf和04_Design_Outputs/cad/BSE3124_Final.dwg。可编辑答案位于submission/source，入口main.tex，编译build.ps1。按用户要求以Task1、Task2、Task3为连续部分，各任务图纸紧随答案。过程版本与临时文件已清理；历史通过Git恢复。校核记录为submission/VALIDATION.md、data/final_manifest.json和data/native_final_gate.json。

保持课程作业深度：未知现场/厂家参数须明确为假设、性能要求或适用条件，不宣称实测或认证。保留统一数据和可复核计算。

## 项目目标与边界

交付建筑全栋负荷估算、首层变压器房及主低压开关房布置，以及一个办公室的照明、动力、MCB 图、进出线最大需求电流和电缆选择。建筑为10个标准层加首层，每标准层三个租户。所选租户采用Office 1。

2026-11-08复审修订：当前使用唯一Final答案和DWG，入口为04_Design_Outputs/submission/README.md，条件化验收和修订证据见VALIDATION.md。原v03全部通过表述已被复审限定。现场/厂家条件仍按答案明确假设，不宣称现场认证。1000 kW 是题目给定的冷负荷；电力负荷需要系统COP及相应功率因数依据。未量取的面积、设备功率、电缆路径和规范条文不能作为已知值填入答案。

## 已配置与验证边界

| 项目 | 配置 | 验证与限制 |
|---|---|---|
| AutoCAD | 本机 Windows AutoCAD 2027 | 当前工作副本BSE3124_Final.dwg；交付副本BSE3124_Final.dwg已由AutoCAD2027 Core Console原生复开，961个登记对象无缺失；六张交付图已逐页目检。六布局均由保存的Final原生复开重出；机房详图纸空间视口已修复 |
| LaTeX | 本机用户目录MiKTeX，XeLaTeX/pdfLaTeX/texify | 已实测中英文、数学、表格与交叉引用；作业答案原生编译并逐页目检 |
| Python | 项目 `.venv`，Python 3.12 | 包依赖检查通过；从本机Codex附带Python建立，迁移电脑须重建环境 |
| AutoCAD MCP | U-C4N/Autocad-MCP，1.8.0，提交 `6f6a538255ca9f885232e845ac32f10b4433fe3e` | 源码在 `05_Tools/autocad-mcp`；安装 COM、DXF 和PDF渲染依赖；stdio初始化、工具列表和system_about查询实测通过 |
| Codex 接入 | `.codex/config.toml`，服务 `bse3124_autocad` | 使用 COM，禁止自动启动CAD，只允许输出目录文件路径；新会话加载后仍须确认工具出现 |
| DXF | ezdxf，随MCP安装 | 合成三圆样例用于工具测试，不是办公室布灯成果 |
| QA skill | `.agents/skills/autocad-dwg-redraw` | 项目级安装，下一轮可发现；只在需要剖析/核对DWG时使用，不默认重绘底图 |
| 官方资料 | `03_Technical_References/Official` | EMSD两份PDF已下载；CLP四份PDF现已手动取得并保留于Official，SHA256见04_Design_Outputs/data/official_reference_manifest.json；旧403记录属于下载历史 |

运行环境和原件SHA256记录在 `06_Research/verification/setup_verification.json`；软件依赖快照在 `05_Tools/requirements.lock.txt`。MCP是第三方软件，安装和冒烟验证不等于完整代码审计或AutoCAD 2027兼容认证。

## 数据与文件声明

- `01_Assignment`、`02_Building_Drawings` 内原件不改动。CAD设计使用 `04_Design_Outputs/cad/BSE3124_Final.dwg` 副本。
- `04_Design_Outputs/data/areas.csv` 保存测量面积、边界、单位和证据。
- `devices.csv` 保存设备ID、楼层、办公室、坐标、功率、功率因数、回路和来源。
- `circuits.csv` 保存DB、相别、设备关联、需求依据、设计电流、保护、电缆、路径长度、敷设方法和来源。
- `assumptions.csv` 保存所有待定和采用的假设，含状态及依据。空白代表未确定，不能按零负荷使用。
- `04_Design_Outputs/calculations` 保存计算和条文引用；`cad` 保存可编辑图；`pdf` 保存出图；`submission` 保存最终答题纸。
- 设备表是平面图和MCB图编号的共同来源。任何变更必须同步数据、图纸和计算，并保留版本。

## 规范依据声明

| 依据 | 本项目角色 | 采用规则 |
|---|---|---|
| 课程原题及答题纸 | 交付范围 | 原题包含进线及出线电缆，不能只做答题纸标题提及的进线 |
| 现有 COP215 Rev07，2012 | Task 1 指定负荷方法 | 沿用课程提供文件，记录附录/页码；不得宣称为当前最新版 |
| EMSD Wiring CoP 2025 | Task 2/3 默认候选依据 | 若课程明确指定2020，统一切换并记入假设；同一套计算不得混用表格和修正系数 |
| CLP COP101 v16 | 变压器房位置、通道和设备布置 | 下载受阻时可从官网人工获取；查到正文和配套图纸前不确定房间尺寸 |
| CLP Supply Rules及计量指南 | 供电和计量接口 | 按具体章节引用，不用概括网页代替条文 |
| BEC2024 | 照明控制及能效的补充依据 | 作业范围内使用；LPD不代替照度检查 |

规范版本和具体数值必须在计算前锁定。法规、工作守则、电力公司要求、政府工程规格及论文作用不同。建筑署规格作为补充，不自动全部列为课程强制要求。

## 执行工作流与关口

| 阶段 | 要做的工作 | 输出及通过条件 |
|---|---|---|
| 0 接入验证 | 启动AutoCAD并完成必要的首次登录；打开工作副本；通过MCP读取当前文档、图层、单位和图块。核对至少一个已知尺寸。在一个办公室放3盏测试灯、回路文字并出PDF | 保存、重开、撤销/重做行为可验证；对象可编辑；图面清晰；原件哈希一致。未通过则使用AutoLISP/脚本路线，不继续批量改图 |
| 1 底图与设计依据 | 识别首层、天花网格和家具平面，量取办公室/公共区面积；选一个办公室；查老师指定规范版本 | 面积边界可追溯；单位明确；假设逐项登记 |
| 2 Task 1 | 办公室负荷、公共服务、中央空调分别计算，避免重复；比较变压器容量；依据COP101和柜尺寸布置机房 | kW/kVA分明；COP和PF有依据；机房具有设备、检修和搬运通道；说明位置理由 |
| 3 Task 2 | 按天花和家具布灯、插座、地盒和fused spur；逐点分回路、相别；从同一回路表生成MCB图 | 图纸点数与设备表一致；所有设备有回路；布局和标注可读 |
| 4 Task 3 | 逐回路计算连接负荷、需求电流、进线汇总和相平衡；校核保护、有效载流量、压降及故障保护 | 每个规格均有公式、输入和规范表号；进线与出线均完成；结果回填图表 |
| 5 交付审核 | 检查平面图、MCB图、表格和计算一致；按原答题纸结构完成LaTeX答案，导出PDF并逐页检查 | 可编辑DWG、LaTeX源码、答案及图纸PDF和计算资料齐全；设备/回路差异0项，设计条件明确列出 |

成本比较使用线长、铜材量和保护器件数量等代理指标；没有报价不写成真实工程造价。

## 工具选择声明

采用AutoCAD＋MCP／AutoLISP＋统一CSV数据。GElectrical暂不安装：当前任务先以透明计算完成负荷和选线，若压降、短路或保护配合需要独立复核，再引入。pyautocad作为备选，避免重复维护两套COM接口。.NET插件开发skill暂不安装。arXiv论文作为方法参考，不作为规范或自动化工具已可用的证据。全部候选和链接见 `06_Research/RESOURCE_CATALOG.md`。

## 继续使用

1. 新一轮对话先读本文和AGENTS.md。项目MCP配置需要新会话加载；若没出现服务，重开工作区并检查MCP状态。
2. 手动打开AutoCAD及工作副本后，先确认当前DWG完整路径在输出目录，再进行写操作。
3. 环境检查：`.venv/Scripts/python.exe 05_Tools/verify_setup.py`。MCP冒烟检查：`.venv/Scripts/python.exe 05_Tools/smoke_mcp.py`。
4. 独立启动MCP供客户端连接可用 `05_Tools/start_autocad_mcp.ps1`；它是stdio服务，不是交互终端程序。
5. 官方PDF重试：`.venv/Scripts/python.exe 05_Tools/download_references.py`；逐项结果见 `Official/sources.json`。
6. 重建环境：`05_Tools/restore_environment.ps1 -PythonExe <Python3.12完整路径>`。源码不提交到主仓库，恢复脚本按固定提交下载；依赖快照固定本次已验证版本。项目迁移后更新MCP配置中的绝对路径。

接入配置采用项目作用域，未修改用户全局Codex设置。输出目录限制不能替代对实时AutoCAD活动文档的检查。
