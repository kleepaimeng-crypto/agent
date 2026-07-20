# 方向 A 岗位情报库

本目录用于收集和分析中国大陆的 **Agent 应用研发 / AI 后端工程师** 岗位，服务于“Java 后端 → Agent 应用研发”的学习路线校准。

## 当前进度

- 目标：40 个有效岗位；实习/校招 20 个，1–3 年社招 20 个。
- 已由 AI 采集：25 个；实习/校招 13 个，1–3 年社招 12 个。
- 待用户补充：15 个；实习/校招 7 个，1–3 年社招 8 个。
- 方向配额：现有核心/混合 23 个、相邻对照 2 个；待补核心/混合 13 个、相邻对照 2 个。
- 数据日期：2026-07-20。

## 目录约定

```text
01-job-market/
├─ inbox/                         # 用户投放的待处理 JD
├─ raw/2026-07/                   # 一岗一张 Markdown 岗位卡
├─ normalized/
│  ├─ jobs.csv                    # 一行一个岗位
│  ├─ requirements.csv            # 一行一个技能观察
│  └─ skill_aliases.csv           # 原始术语到能力类别的映射
└─ reports/
   └─ target-role-analysis-v1.md  # 阶段报告，40 个样本后转为正式版
```

## 有效岗位标准

1. 包含公司、岗位名、城市、职责、要求、来源链接和采集日期。
2. 方向 A 核心或混合岗位应以 Agent、RAG、LLM 应用、AI 后端或相关工程落地为主要工作。
3. 纯模型训练、纯 CV/NLP 算法、数据标注、产品和销售岗位不计入样本。
4. 推理集群、GPU 优化、模型训练为主的岗位只进入 4 个相邻对照名额。
5. 同公司、近似岗位名且 JD 高度一致时，优先保留官网或更新版本。
6. 不保存招聘者姓名、电话、邮箱等个人联系方式。

## 分类与权重

- `match_score=3`：方向 A 核心岗位，`role_relevance=1.0`。
- `match_score=2`：方向 A 与全栈、算法或平台混合，`role_relevance=0.7`。
- `match_score=1`：Agent Infra / 模型工程相邻对照，`role_relevance=0.3`。
- `match_score=0`：排除，不进入正式样本。
- 职责或必备要求的 `base_weight=3`，加分项的 `base_weight=2`。
- `weighted_score = base_weight × role_relevance`。

## 公开网页材料说明

公开网页岗位卡保存完整的职责和要求含义、关键技术证据及原链接，不整页逐字复制。用户自行取得并放入 `inbox` 的材料可以保留原文，再由 AI 生成同样结构的岗位卡。

## 搜索词

- 岗位：`Agent开发工程师`、`AI Agent应用开发`、`大模型应用开发`、`LLM应用工程师`、`RAG工程师`、`AI后端工程师`、`智能体开发`。
- 能力：`Tool Calling`、`Function Calling`、`LangGraph`、`RAG`、`MCP`、`Agent Evaluation`。
- 后端：`FastAPI`、`Spring Boot`、`Spring AI`、`MySQL`、`Redis`、`Docker`。

## 用户下一步

按 `inbox/_template.md` 每批放入 5 个岗位。不要手工修改 `normalized` 下的 CSV；批次完成后通知 AI 统一去重、归类和更新报告。
