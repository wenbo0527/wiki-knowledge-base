# 📋 Templates 文档模板库

> 🕵️ 尼克·弗瑞知识资产管理
> 📅 创建时间: 2026-04-30
> 🎯 定位: 标准化文档产出，提升团队协作效率

---

## 目录结构

```
templates/
├── README.md                          ← 本文件
├── TEMPLATE_EVALUATION.md            ← 质量评价体系
├── products/                          ← 产品文档模板
│   ├── 01-PD产品域说明文档.md
│   ├── 02-EPIC说明文档.md
│   ├── 03-Feature说明文档.md
│   ├── 04-FeaturePoint清单.md
│   ├── 05-PRD模板.md
│   ├── 06-业务需求文档.md
│   └── 07-产品操作手册.md
├── technical/                        ← 技术文档模板
│   ├── 08-技术方案模板.md
│   ├── ARCH_DESIGN_TEMPLATE.md       ← 架构设计
│   └── API_SPEC_TEMPLATE.md          ← API设计
├── logs/                             ← 日志类模板
│   ├── MEETING_NOTES.md              ← 会议纪要
│   ├── CHANGE_LOG.md                  ← 变更记录
│   └── DECISION_RECORD.md            ← 决策记录
└── checklists/                       ← 检查类模板
    ├── CODE_REVIEW.md                ← 代码Review
    ├── UAT_CHECKLIST.md              ← UAT检查清单
    └── TEST_CASE.md                  ← 测试用例
```

---

## 模板分类

| 分类 | 代码 | 说明 |
|------|------|------|
| **产品域模板** | PD | 产品域说明文档 |
| **Epic模板** | EPIC | Epic说明文档 |
| **Feature模板** | FEAT | Feature说明文档 |
| **PRD模板** | PRD | 产品需求文档 |
| **技术模板** | TECH | 技术方案/架构设计 |
| **操作手册** | OPS | 产品操作手册 |
| **日志模板** | LOG | 会议纪要/变更记录 |
| **检查清单** | CHECK | 检查类模板 |

---

## 质量评价体系

详见: [TEMPLATE_EVALUATION.md](TEMPLATE_EVALUATION.md)

### 四维评价模型

| 维度 | 权重 |
|------|------|
| 完整性 | 30% |
| 可用性 | 25% |
| 规范性 | 25% |
| 实用性 | 20% |

### 入库阈值

| 分数 | 状态 |
|------|------|
| ≥85 | 🏆 最佳实践 |
| 60-84 | ✅ 标准模板 |
| 45-59 | ⚠️ 待改进 |
| <45 | ❌ 废弃 |

---

## 来源参考

模板参考: `wenbo/Documents/文档仓库/产品管理项目/架构规范/模板/`

---

*维护者: 尼克·弗瑞*
*最后更新: 2026-04-30*
