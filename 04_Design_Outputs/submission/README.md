# Group 1 交付入口

最终答案是 [BSE3124_Answer_Sheets_v04.pdf](BSE3124_Answer_Sheets_v04.pdf)，共19页，已经填写组员信息。前5页保留老师原模板，随后8页为技术续页，最后6页为首层总图、机房详图、配电图、照明平面、动力平面及新增安装详图。A3图纸请按实际大小打印。

可编辑图纸是 [assignment_submission_v02.dwg](../cad/assignment_submission_v02.dwg)，用AutoCAD2027打开。交付布局为TASK1-GROUND-OVERVIEW、TASK1-ROOM-REVIEW、TASK2-DB-SCHEMATIC、TASK2-LIGHTING-PLAN、TASK2-POWER-PLAN、DESIGN-DETAILS；其他布局是历史工作内容。LaTeX源码在[latex_v04/main.tex](latex_v04/main.tex)，运行同目录build.ps1可从公共数据重建PDF。MiKTeX安装在本机用户目录，未放入项目。

验收逐项记录在[REVISION_V04.md](REVISION_V04.md)，文件哈希与检查入口在[revision_v04_manifest.json](../data/revision_v04_manifest.json)。旧版本、候选计算和试验出图属于过程记录；最终采用值以v04答案、devices.csv、circuits.csv及下面的计算入口为准。

## 怎么计算、为什么这样选

Task1先用三个办公室的图注面积，明确假设其为UFA，再按10层和COP215Rev07的0.16kVA/m²得到1644.8kVA。1000kW冷负荷通过冷吨及1.85kW/TR参考折算为526.039kW电功率，再除假设PF0.90得到584.488kVA。公共服务按五部电梯的aggregate allowance计200kVA；对公共空调重复项给出0–200kVA界限。两供电区系数1.1后取上限2672.216kVA，选两台1500kVA预留。计算入口是[task1_load_summary.py](../calculations/task1_load_summary.py)。位置选首层外围，以便外部搬运、缩短LV接口并与楼梯/电梯核心分开；设备尺寸、门、通道和通风条件在答案与详图明确区分为假设或规范要求。

Task2按天花网格和房间边界布置92块面板，采用60块22W及32块28W，共2216W；分成七个照明回路及七个手动开关。九个地盒、三个双位插座和一个设备预留点全部标注回路，每个动力点有13A熔断限制。P1–P4采用环路，其余采用放射回路；茶水间与办公室回路分开。设备编号与回路归属共用[devices.csv](../data/devices.csv)和[circuits.csv](../data/circuits.csv)，避免图纸与计算各填一套。

Task3从各回路和相别汇总需求，照明90%，插座按最大回路100%加其余50%，P7设备预留独立100%，最大相48.909A。选源端C63及4芯35mm²铜缆加16mm²CPC，校核修正载流量；再逐一核对15条出线的保护、载流量、全程压降、故障切断和CPC能量。环路用两端供电网络求分流，不把一个环腿误当完整32A放射电缆。入口为[office_design_demand.py](../calculations/office_design_demand.py)、[incoming_cable_design.py](../calculations/incoming_cable_design.py)、[fault_protection_design.py](../calculations/fault_protection_design.py)。规范表号、计算条件和公式在PDF的Task3及公共JSON中列明。

## 怎么画、怎么核对

原始DWG和作业文件保留不改，设计写入版本副本。已用已知尺寸、600mm天花格和三灯样板确认单位/比例；最终图是AutoCAD原生对象，可编辑。灯、插座、路径、DB及注释分层保存，布局视口锁定比例；底图调淡，设计标注保持清楚。绘图脚本在calculations中以draw_开头，带重复执行保护，不能把它们当普通计算脚本反复运行。

最终核对包含：112个组件一对一分回路、92个灯标签、15条回路路径、两条进线路径、15行配电表和六张交付布局；940个登记对象经AutoCAD2027原生复开读取，未丢失。PDF逐页渲染目检，原件哈希保持一致。现场/厂家未知参数均作为明确的课程设计条件，不能把这些条件理解为实测或产品认证。

## 文件归档

旧答案、旧DWG、试验出图、QA图片和恢复备份统一移至[archive/2026-11-07](../archive/2026-11-07/README.md)。原始资料、当前公共数据、最终文件及其哈希均未改变。逐文件搬移清单见data/folder_cleanup_20261107.json；历史图纸中的旧文件名可在此归档找到。
