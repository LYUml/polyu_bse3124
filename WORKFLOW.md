# BSE3124 Mini Design Assignment 工作流程

## 1. 决定与目标

**主绘图工具：Windows 上已获授权的 AutoCAD。** 保留老师提供的 DWG，直接在副本上添加电气图层。Windows 上的 AI 可通过 AutoLISP／脚本或经实测可用的 MCP 桥接操作 AutoCAD、检查图面和导出图纸；Mac 上的 AI 负责资料、计算、设计数据、脚本草稿及交叉检查。不能假定 ChatGPT 网页或客户端已经获得 AutoCAD 控制权。先用一个小样验证具体接入方式，再批量绘图。

本作业是课程设计。目标是在满足课程指定方法和香港相关技术要求的前提下，得到**可追溯、可修改、图表一致**的方案。比较成本时，先用电缆长度、规格、器件数量等估算指标；没有报价单就不把它们称为真实工程造价。

```mermaid
flowchart LR
    A[原始 DWG + COP215 + 课程文件] --> B[面积与设计假设]
    B --> C[统一设备及回路数据表]
    C --> D[负荷、电流、电缆计算]
    C --> E[AI + AutoCAD 绘图]
    D --> F[一致性和性能检查]
    E --> F
    F --> G[答题纸 + DWG + PDF]
```

## 2. 输入资料及依据

| 文件／依据 | 用途 |
|---|---|
| `BSE3124 Mini Design Assignment-2.docx`、`BSE3124 Mini Design Answer Sheets.docx` | 任务及最终填写格式 |
| `Building Layouts.dwg` | 首层和标准层绘图底图；保留原件，编辑副本 |
| `Building Layouts Layout2-1.pdf` | 标准层照明图的视觉参考 |
| `Switchboard Dimensions.pdf` | 机房布置时核对开关柜尺寸 |
| `257377810-COP-215.pdf`／`.txt` | CLP COP215《Load Assessment Procedure》，**2012 年 9 月 Rev. 07**；本项目 Task 1 的指定计算依据 |
| `../01_lec/01_4 Maximum Demand and Tariff.pdf` | 课程对负荷密度和最大需求的讲解 |
| [EMSD 电力（线路）规例工作守则](https://www.emsd.gov.hk/en/electricity_safety/publications/codes_of_practice/index.html) | 回路、保护及电缆选择的技术依据；记录实际采用的版本和条文 |
| [CLP COP101 变电站设计](https://www.clp.com.hk/en/electrical-contractors) | 变压器房、通道及主低压开关房布置参考 |
| [CLP Supply Rules](https://www.clp.com.hk/en/electrical-contractors) | 供电及计量接口参考 |

COP215 的关键条目：附录 2 的 **Office = 0.16 kVA/m²**，不含中央空调电力负荷；**40 kVA/lift 仅是公共服务参考值**，应尽可能按设备逐项评估。附录 9 把制冷量与电力负荷分开：空调电力负荷 = 制冷量 ÷ 整套系统 COP。题目给的 **1000 kW 是冷负荷**。COP215 第 07 版是课程现有材料的工作依据，不声称它是 CLP 当前最新版。

## 3. 软件和 GitHub 项目

### 主路径（推荐）

| 工具 | 是否需要 | 用法 |
|---|---|---|
| Windows AutoCAD（已有授权） | **需要** | 打开并保存原始 DWG、运行自动绘图、手动核对、导出 PDF |
| AutoLISP `.lsp` 或 AutoCAD 脚本 `.scr` | **建议** | 由 AI 根据统一数据表生成；批量建图层、放图块、回路号和文字。AutoCAD [AutoLISP](https://help.autodesk.com/cloudhelp/2024/ENU/AutoCAD-MAC-AutoLisp/files/GUID-A0E9D801-8BE9-4BF1-85E8-3807E15F3B71.htm) 和 [脚本](https://help.autodesk.com/cloudhelp/2016/ENU/AutoCAD-MAC-Core/files/GUID-DB55FE5C-6B51-40AE-AE3D-4C3A28ADC5D9.htm) 均有官方文档 |
| Python＋CSV／表格 | **建议** | 计算负荷、回路电流、候选电缆及方案指标；所有公式和取值可复核 |
| Windows AI 客户端 | **需要实测** | 首选生成并审查 AutoLISP，再在 AutoCAD 中运行；若客户端支持连接本地 MCP 服务，可测试直接读取和修改图纸。两种方式均先做小样 |

### ChatGPT／AI 接入 AutoCAD 的选择

1. **最容易落地：AI 生成 AutoLISP 或 `.scr`。** 根据统一数据表生成建图层、放符号和标注的脚本；审查代码，在 DWG 副本上加载并检查结果。AutoCAD 官方说明可在命令行运行或从文件加载 [AutoLISP](https://help.autodesk.com/cloudhelp/2026/ENU/AutoCAD-Customization/files/GUID-E6429154-36DF-4D84-8ABC-9FCA15B66158.htm)。这条路径不要求 AI 客户端直接控制 AutoCAD。
2. **需要交互操作时：MCP 桥接。** 流程为“支持 MCP 的 AI 客户端 → 本地 AutoCAD MCP 服务 → Windows COM／AutoCAD”。GitHub 项目提供桥接服务，不等于 ChatGPT 网页会自动连接；必须核对所用客户端的 MCP 支持和本机配置，并在测试图纸上验证每项操作。Windows 完整版 AutoCAD 可使用 COM；Mac 不适用 Windows COM。[AutoCAD 官方接口表](https://help.autodesk.com/cloudhelp/2026/ENU/AutoCAD-Customization/files/GUID-E6429154-36DF-4D84-8ABC-9FCA15B66158.htm)
3. **定制插件：AutoCAD .NET 插件＋OpenAI API。** 仅在脚本与现成桥接不能满足需求时考虑。插件读取指定对象、提供受控的绘图函数，模型提出调用，插件核对参数后执行。[OpenAI Docs 的函数调用说明](https://developers.openai.com/api/docs/guides/function-calling)；API 使用与 ChatGPT 订阅[分别计费](https://help.openai.com/en/articles/9039756-managing-billing-for-chatgpt-and-the-api-platform)。

AutoCAD 内置的 [Autodesk Assistant](https://help.autodesk.com/cloudhelp/2026/ENU/AutoCAD-WhatsNew/files/GUID-B4E1E636-E08E-4277-8971-910D47440116.htm) 可用于产品帮助，但它不是 ChatGPT，也不作为本作业自动绘图已经可用的证据。

### 备用／可选开源项目

| GitHub 项目 | 何时使用 | 限制 |
|---|---|---|
| [mozman/ezdxf](https://github.com/mozman/ezdxf) | 需要在 Mac 上批量生成 DXF 图层、符号或预览时 | 主路径直接编辑 DWG 时**不需要**；ezdxf 不能原生编辑 DWG |
| [LibreDWG/libredwg](https://github.com/LibreDWG/libredwg) | 需要把 DWG 转为 DXF 供开源流程使用时 | 转换后必须核对比例、文字、图块及尺寸 |
| [LibreCAD/LibreCAD](https://github.com/LibreCAD/LibreCAD) | 免费查看／修改 DXF，或主路径不可用时 | 对复杂 DWG 的兼容须用本作业图纸实测 |
| [manuvarkey/GElectrical](https://github.com/manuvarkey/GElectrical) | 要进一步交叉核对单线图、压降或短路计算时 | 不是本作业的香港规范自动判定器；结果仍需人工核对 |
| [U-C4N/Autocad-MCP](https://github.com/U-C4N/Autocad-MCP) | Windows AI 客户端支持本地 MCP，且需要交互读取／修改正在运行的 AutoCAD 时 | 项目自述有 COM 实时模式及 ezdxf 离线 DXF 模式；后者不能代替在原始 DWG 上编辑。第三方项目，安装前检查代码、依赖和命令权限 |
| [vigneshpbmenon/autocad-mcp-server](https://github.com/vigneshpbmenon/autocad-mcp-server) | 只需试验画线、圆、矩形等基础 MCP 操作时 | 项目要求 Windows 上 AutoCAD 正在运行；功能较基础，不能假定满足完整电气图出图需求 |

**目前无需克隆上述仓库。** 先做 AutoCAD 小样；只有实际遇到相应需求时才安装备用工具。DWF 可用于审阅和批注，PDF 用于提交预览；两者均不作为程序生成和修改设备的主格式。

## 4. 分阶段执行

### 阶段 0：保存底图与小样试验

1. 复制 `Building Layouts.dwg`，保留老师原件不变。
2. 在 Windows AutoCAD 确认首层、照明天花图和家具／动力图的位置、比例、单位、图层与可打印范围。
3. 先选 AutoLISP／脚本路径；若要试 MCP，先确认 Windows AI 客户端能连接本地服务，限定可操作的测试文件夹，在 AutoCAD 中打开副本，并验证“读取当前图纸信息”。不要只凭仓库 README 判定接入成功。
4. 让 Windows AI 在副本中建立一个电气图层，于一个办公室放 **3 盏测试灯**及回路号，保存 DWG、导出 PDF。若测试 MCP，再分别验证读取、写入、撤销和重新打开 DWG 后的结果。
5. 核对灯具位置、字高、线宽和打印比例；通过后才大规模自动绘图。

**关口：**原图完整；至少一个已知尺寸与 CAD 测量一致；测试灯和标注在 DWG／PDF 中均清晰、可编辑。

### 阶段 1：统一数据与设计假设

1. 量取三个办公室、标准层公共部分和首层所需面积；记录量测边界与单位。
2. 选定 Office 1／2／3 中的一个用于 Task 2、3。
3. 建立设备表：`device_id、type、floor、office、x、y、power、circuit_id、source_or_assumption`。
4. 建立回路表：`circuit_id、DB、phase、device_ids、connected_load、demand_basis、Ib、MCB、cable、length、installation_method`。
5. 把未给定的数值集中写入假设表，不在计算式或 CAD 标注中藏入“默认值”。

**关口：**所有设备 ID 唯一；所有设备有且仅有一个目标回路或明确注明不属本办公室设计范围；功率与面积均有来源或假设。

### 阶段 2：Task 1 全栋负荷与机房

1. 用 COP215 附录 2 计算办公室面积负荷；另列公共服务、中央空调及其他固定／特殊负荷，避免重复计算。
2. 根据 COP215 附录 7／9 选定中央空调系统假设，把 **1000 kW 冷负荷**换算为电力负荷。记录 COP 或 kW／tonne 取值及换算过程。
3. 汇总 assessed load，并列出变压器容量／数量的方案及余量假设。
4. 结合 COP101 与开关柜尺寸，在首层底图上提出变压器房和主低压开关房位置；检查设备、检修、搬运及电缆通道。
5. 在 Answer Sheets 写出计算、假设和位置理由。

**关口：**kW 与 kVA 不混用；办公室 ADMD 不含的中央空调已另计；公共服务的 40 kVA/lift 未被当作无条件定值；面积和机房尺寸可追溯。

### 阶段 3：Task 2 办公室平面图及 MCB 图

1. 根据天花网格及房间用途布灯；根据家具与固定设备布插座、地盒和 fused spur。
2. 给所有灯具和动力点分配回路；在图上显示设备 ID 和回路号。
3. 由同一份回路表生成配电箱 MCB 示意图，写明保护器件、相别、线径和回路用途。
4. 说明分路及保护选择依据。

**关口：**图上设备数 = 设备表数；图上回路号 = MCB 图回路号 = 回路表回路号；无设备落在墙体或不可达位置；文字不重叠。

### 阶段 4：Task 3 电流与电缆

1. 按设备与回路表计算各出线连接负荷、最大需求电流。
2. 汇总办公室配电箱进线需求；若为三相，检查各相分配。
3. 按选定的 EMSD 守则版本核对保护额定值、有效载流量、敷设／温度／成组修正及压降；必要时检查故障保护条件。记录线长假设。
4. 把最终器件和线径回填到回路表与 MCB 图。

**关口：**每条回路有可复算的公式、数值与守则表格来源；图纸和计算表规格一致；不为节约材料牺牲规范条件。

### 阶段 5：比较、审核及交付

在**满足安全与课程要求的方案之间**，比较不同回路分组、配电箱位置或电缆路径。完成 Answer Sheets，并从 AutoCAD 导出打印清晰的 PDF，保留可编辑 DWG 和计算表。

| 指标 | 如何衡量 | 目标 |
|---|---|---|
| 底图保真 | 已知尺寸、图层、文字、家具与原图逐项抽查 | 关键项目全部一致 |
| 设备覆盖 | 已绘设备数／设备表应绘设备数 | 100% |
| 回路一致 | 平面图、MCB 图、回路表、计算表的编号及规格差异 | 0 项 |
| 计算可追溯 | 有公式与来源／假设的关键数值占比 | 100% |
| 电气表现 | 各回路压降、估算损耗、相负荷分配；对照采用的守则 | 全部满足已列明的设计限值 |
| 成本代理 | 按规格统计电缆长度／铜材量、MCB 数和配电箱容量 | 在合规候选方案中较低；保留比较表 |
| 修改效率 | 改一条回路后完成图纸、表格、计算更新所需时间 | 用首个小样测基线，后续应更短 |
| 出图质量 | PDF 上重叠、越界、不可读的标注 | 0 处 |

## 5. 两台电脑之间的交接规则

- 传递**原始 DWG 的副本、统一数据表、脚本、生成的 DWG 和 PDF**。每轮修改加版本号，例如 `office1_v01`，避免两边覆盖同名文件。
- **数据表是编号和负荷的共同来源**。Windows AI 改动设备位置或回路后，必须同步回传更新的数据表或明确的改动记录；不能只改 DWG。
- 每轮从 Windows 回传 PDF 供目视检查，同时保留 DWG 供继续编辑。PDF 通过审查后，再填写最终答案纸。

## 6. 最终交付清单

- 填妥的 `BSE3124 Mini Design Answer Sheets.docx`，含 Task 1–3 的假设、计算与理由。
- 首层变压器房／主低压开关房布置图。
- 所选办公室照明布置图、动力布置图及 MCB 配电箱示意图。
- 逐回路计算表、设备及回路表、方案比较表。
- 可编辑 DWG 和供阅读／提交的 PDF；按老师最终指定格式提交。
