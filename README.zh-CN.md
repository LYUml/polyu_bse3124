# BSE3124 电气设计作业

[English](README.md) | **简体中文**

最终交付入口：[Group 1 答案、图纸及计算说明](04_Design_Outputs/submission/README.md)。

[最终答案PDF](04_Design_Outputs/submission/BSE3124_Answer_Sheets_v04.pdf) · [可编辑DWG](04_Design_Outputs/cad/assignment_submission_v02.dwg) · [逐项验收记录](04_Design_Outputs/submission/REVISION_V04.md)

[空白模板复刻](04_Design_Outputs/submission/BSE3124_Template_LaTeX.pdf)采用原版底图＋LaTeX填写；原模板文字不是重新排字，答案可编辑。

[项目执行声明](PROJECT_SPEC.md)说明配置、设计步骤、数据规则和验收条件。

| 目录 | 内容 |
|---|---|
| [01_Assignment](01_Assignment/) | 作业要求和原始答题纸 |
| [02_Building_Drawings](02_Building_Drawings/) | 原始DWG和参考图，保留不改 |
| [03_Technical_References](03_Technical_References/) | 课程资料；Official为官方规范和下载记录 |
| [04_Design_Outputs](04_Design_Outputs/) | data为统一数据表，cad为工作图，calculations为计算，pdf为出图，submission为最终交付；archive为历史输出归档 |
| [05_Tools](05_Tools/) | 工具脚本、依赖快照和第三方MCP源码 |
| [06_Research](06_Research/) | 资源目录和verification验证记录 |

常用入口：

- [资源目录](06_Research/RESOURCE_CATALOG.md)
- [环境验证](06_Research/verification/setup_verification.json)
- [MCP测试](06_Research/verification/mcp_smoke_test.json)
- [计算与绘图工作流](04_Design_Outputs/submission/README.md)（历史background/WORKFLOW.md当前缺失）

隐藏目录`.venv`为Python环境，`.codex`为项目配置，`.agents`为skill。AGENTS.md是后续AI工作规则。

工具检查在根目录运行：

```powershell
.venv/Scripts/python.exe 05_Tools/verify_setup.py
.venv/Scripts/python.exe 05_Tools/smoke_mcp.py
```

Task1–3已按2026-11-08审查结果修订，最终PDF共19页；计算通过仅限声明的课程条件，详见修订记录。历史工作图/候选计算不代表最终采用值；当前入口和条件见交付说明。

历史草稿、试验出图及恢复备份统一位于[输出归档](04_Design_Outputs/archive/2026-11-07/README.md)。当前cad目录保留版本化交付DWG与工作DWG，pdf目录只保留三张采用出图。
