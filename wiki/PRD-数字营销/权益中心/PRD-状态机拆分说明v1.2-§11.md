# PRD v1.2.x §11 状态机拆分说明（wiki 同步版）

> **任务**: TASK-20260604-B7A76A28 [Demo-003] + TASK-20260604-CD84EFC6 [部署-004]（两份任务合并交付）
> **写于**: 2026-06-04 20:25（doc 接手校对 + wiki 同步）
> **兜底稿**: 派蒙 2026-06-04 18:50 写（基于 PRD v1.2.2）
> **校对**: data_community_doc 2026-06-04 20:25
> **关联 PRD**: `PRD-大额低息临价折扣v1.2.8.md`（v1.2.2 已升 v1.2.3→v1.2.4→v1.2.5→v1.2.6→v1.2.7→**v1.2.8**）
> **关联评审**: review-prd-v1.2.2.md（G5 缺口）
> **关联代码**: 
> - `apps/mkt-app/src/types/api/coupon.ts` line 124-141（CouponPackage + TODO 注释）
> - `apps/mkt-app/src/mock/coupon.ts` line 15 / 79 / 108（MockTemplate/MockPackage/MockCoupon）

---

## 0. doc 校对批注（2026-06-04 20:25）

派蒙 18:50 兜底稿**主体可交付**，但存在 **3 处事实过时/需增补**，doc 校对如下：

| # | 派蒙兜底稿位置 | 派蒙写法 | 实际事实（doc 20:25 校对） | 处置 |
|:---:|:---|:---|:---|:---|
| 1 | 全文 | 基于 PRD v1.2.2 | **PRD 已升 v1.2.8**（6/4 一天内 +0.6） | 在 wiki 同步版保留 v1.2.2 主体 + 加 §11.7 v1.2.8 增量差异表 |
| 2 | §11.1 状态机总览 | MockTemplate 5 态 / MockRecord 6 态 | mock/coupon.ts 数字对，但 **PRD v1.2.8 §11.3 写的是 9 态**（pending + received + 5 failed_xxxx + invalidated + expired，v1.2.6 失败状态机扩展）| 加 PRD 设计层 9 态 vs mock 实现层 6 态对照 |
| 3 | §11.4 MockRecord 6 态 | `received \| locked \| used \| expired \| invalid \| invalidated` | mock/coupon.ts:108 是 MockCoupon 6 态；**MockRecord 实际是 3 态**（mock/coupon.ts:62 `received \| used \| expired`）| 修正 §11.4 实体名 → MockCoupon（不是 MockRecord）|

**doc 处置原则**：
- ✅ 派蒙兜底稿事实正确部分（mock/coupon.ts 实际 grep 结果）保留
- ✅ 派蒙 §11.6 兜底说明 保留（这是派蒙 5h52min 超时 + 越界反思，不可抹）
- ✅ 派蒙 grep 错误的"MockRecord 6 态"改成 "MockCoupon 6 态"（mock/coupon.ts:108 是 MockCoupon.status）
- ✅ 加 v1.2.8 增量差异（11.3 失败状态机扩展、11.3.2 pending 超时、11.3.3 Kafka 重试、§11.5 删主动作废）

---

## §11.1 状态机总览（3 实体 + 实际态数）

| 实体 | 状态枚举（mock 实现层） | 态数 | PRD 设计层（v1.2.8） | 边界 |
|:---|:---|:---:|:---|:---|
| **MockTemplate.status** | `draft \| active \| online \| paused \| expired` | **5 态** | v1.2.8 §11.1 = 3 态（draft/online/offline）| mock 比 PRD 多 2 态（active/paused，v1.3 待去重）|
| **MockPackage.status** | `draft \| active \| inactive` | **3 态** | v1.2.8 §11.2 = 3 态（draft/active/inactive）| **完全对齐** |
| **MockCoupon.status** | `received \| locked \| used \| expired \| invalid \| invalidated` | **6 态** | v1.2.8 §11.3 = **9 态**（pending + received + 5 failed_xxxx + invalidated + expired，v1.2.6 扩展）| mock 落后 PRD 3 态（缺 pending + 5 failed）|

**Mock 实现层总态数**: 5 + 3 + 6 = **14 态**（demo 范围，2026-06-04 实际 grep）
**PRD 设计层总态数**: 3 + 3 + 9 = **15 态**（v1.2.8 含失败状态机扩展）

**5/26 教训确认**:
- ✅ 5/26 教训 #4: **types 必须声明字段, mock 引用才有类型校验**（types/api/coupon.ts line 116 InventoryBatch 已补）
- ✅ 5/26 教训变体 8: **派蒙 4 验收 + 派蒙硬规矩** — 半拆（package 3 态）+ TODO 注释指向 v1.3 = 评审级妥协方案
- ✅ Demo-001 G5 半拆: **package 收紧到 3 态，template 5 态 + coupon 6 态保持不变**

**实际 grep 验证**:
- `src/mock/coupon.ts` line 15（MockTemplate.status） = 5 态
- `src/mock/coupon.ts` line 79（MockPackage.status） = 3 态
- `src/mock/coupon.ts` line 108（MockCoupon.status） = 6 态
- `src/types/api/coupon.ts` line 141（CouponPackage.status） = 3 态 + TODO 注释

---

## §11.2 CouponPackage.status 5→3 拆分（Demo-001 G5 决策）

### 5/26 教训前 vs 教训后

| 维度 | 5/26 教训前（PRD v1.2.1 原文）| 5/26 教训后（Demo-001 v1.2.2 落地）|
|:---|:---|:---|
| **状态枚举** | `pending \| executing \| success \| partial \| failed`（5 态）| `draft \| active \| inactive`（3 态）|
| **语义** | 任务执行状态（grant task lifecycle）| 包生命周期状态（package lifecycle）|
| **触发方** | 后端 grant task runner | 前端 mock（demo 范围）|
| **粒度** | 任务级（每次发券）| 包级（包整体状态）|

### dev D1 决策依据（review-prd-v1.2.2.md G5 缺口）

- PRD §11.4 写的是**任务状态机**（5 态），但前端 demo 用的是**包状态机**（3 态）
- demo 范围没有 grant task runner，**5 态无法演示**（没有"执行中"的事件源）
- dev D1 决定: **demo 范围用 3 态**（draft/active/inactive），**5 态推到生产级**（CouponGrantTask 独立类型）
- TODO 注释指向 v1.3 dev+doc 协补 CouponGrantTask

### dev D1 types 改动

`src/types/api/coupon.ts` line 124-141:
```ts
/**
 * 券包状态（PRD §11.2）— demo 范围收紧到 3 态
 * TODO 生产级: 独立 CouponGrantTask 类型, 恢复 §11.4 5 状态
 *       (pending|executing|success|partial|failed)
 *       PRD 评审 review-prd-v1.2.2.md G5 缺口, 派 dev + doc 在 v1.3 阶段补
 */
status: 'draft' | 'active' | 'inactive'
```

### dev D1 mock 改动

`src/mock/coupon.ts` line 79:
- `MockPackage.status` 枚举收紧到 3 态
- 8 条 packageMockData 全部用新枚举（active=5, inactive=2, draft=1）
- 撤掉的 5 态: `pending` / `executing` / `success` / `partial` / `failed`

---

## §11.3 CouponGrantTask 5 态待补（生产级恢复）

### 生产级 5 态语义

| 状态 | 含义 | 触发方 | 转换 |
|:---|:---|:---|:---|
| `pending` | 任务入队 | 用户请求 / 定时任务 | → executing |
| `executing` | 任务执行中 | grant task runner | → success / partial / failed |
| `success` | 全部券发放成功 | grant task runner | 终态 |
| `partial` | 部分券发放成功 | grant task runner | 终态（含部分用户/部分批次）|
| `failed` | 全部发放失败 | grant task runner | 终态（可重试）|

### 与 CouponPackage.status 3 态的关系

| 维度 | CouponPackage.status | CouponGrantTask.status |
|:---|:---|:---|
| **对象** | 券包整体 | 单次发券任务 |
| **数量关系** | 1 包 : N 任务 | N 任务 : 1 包 |
| **状态机** | 包生命周期（草稿/启用/停用）| 任务生命周期（待执行/执行中/完成态）|
| **关注方** | 营销配置人员 | grant task runner / 运维 |

**v1.3 待补**:
- 新增 `CouponGrantTask` 类型（5 态枚举 + 任务进度字段）
- 任务状态查询接口
- 包状态与最近任务状态的聚合展示

**v1.2.8 增量影响**: 临价折扣券的"任务状态"在 v1.2.6 失败状态机扩展后，**已部分覆盖** §11.3 用户券状态机的失败路径（5 个 failed_xxxx）。这意味着 v1.3 协补 CouponGrantTask 时，**任务级的 failed 状态需要映射到用户券级的 failed_1001-1005**，**不能 1:1 简单套用**。

---

## §11.4 MockTemplate 5 态 / MockCoupon 6 态 边界确认（doc 修正派蒙措辞）

> **doc 修正**: 派蒙兜底稿 §11.4 写 "MockRecord 6 态"，实际是 `MockCoupon.status` 6 态（mock/coupon.ts:108）。
> `MockRecord.action` 只有 3 态（mock/coupon.ts:62 `received | used | expired`）。
> 派蒙 grep 时把两个不同类型混了。doc 20:25 修正。

### MockTemplate 5 态（mock/coupon.ts:15）

```ts
status: 'draft' | 'active' | 'online' | 'paused' | 'expired'
```

| 状态 | 含义 | 转换 |
|:---|:---|:---|
| `draft` | 草稿（未发布）| → active |
| `active` | 已发布（在线）| → paused / expired |
| `online` | 在线（5 态枚举重复，**v1.3 待评审去重**）| ⚠️ 与 active 重复 |
| `paused` | 暂停 | → active |
| `expired` | 过期 | 终态 |

**⚠️ 评审发现（派蒙）**: `active` 和 `online` 重复，**实际只有 4 态去重**（draft / active|online / paused / expired）。
- demo 范围接受 5 态（不强制去重）
- **v1.3 待评审**: 统一为 `active`，删除 `online` 枚举值
- **PRD v1.2.8 §11.1 实际是 3 态**（draft/online/offline），mock 比 PRD 多 active/paused —— mock 演化超前 PRD

### MockCoupon 6 态（mock/coupon.ts:108）

```ts
status: 'received' | 'locked' | 'used' | 'expired' | 'invalid' | 'invalidated'
```

| 状态 | 含义 | 转换 |
|:---|:---|:---|
| `received` | 已领取（待使用）| → locked / used / expired |
| `locked` | 已锁定（订单占用）| → used / invalidated |
| `used` | 已使用 | 终态 |
| `expired` | 已过期 | 终态 |
| `invalid` | 无效（未激活过期）| 终态 |
| `invalidated` | 已作废（用户/管理员主动）| 终态 |

**用户券实例状态机**：6 态完整，覆盖领取→使用/过期/作废全生命周期。

**vs PRD v1.2.8 §11.3（9 态）差异**:
- ❌ mock 缺 `pending`（内部态，等核心 Kafka 回执）
- ❌ mock 缺 5 个 `failed_1001-1005`（核心拒收/超时/存量作废失败/Kafka 推送失败/Kafka 消费失败）
- ✅ mock `invalidated` / `expired` 对齐 PRD
- ✅ mock `received` 对齐 PRD 激活态

### 5/26 教训守住
- ✅ **没**改 `MockTemplate.status`（5 态不动，模板状态机独立）
- ✅ **没**改 `MockCoupon.status`（6 态不动，用户券实例状态独立）
- ✅ **没**改 `MockPackage.status` 之外的 3 态（G5 半拆边界）
- ✅ **没**动 `api/coupon.js` 的 `expired`（MockCoupon 实例状态，不是 package）
- ✅ **没**做 §12.4 MA 触发信号 mock（文博砍）
- ✅ **没**做 §12.6 产品配置数组（前端用 types 常量）

---

## §11.5 状态机与 PRD v1.3 升级路径

### 现状（demo 范围 14 态 mock vs 15 态 PRD）

```
MockTemplate: 5 态（draft/active/online/paused/expired）  ← mock 演化超前 PRD
MockPackage: 3 态（draft/active/inactive）  ← 完全对齐 PRD
MockCoupon: 6 态（received/locked/used/expired/invalid/invalidated）  ← 落后 PRD 3 态
---
mock 小计: 14 态
PRD v1.2.8 小计: 15 态（v1.2.6 失败状态机扩展 +3）
```

### 待补（生产级 +5 态）

```
CouponGrantTask: 5 态（pending/executing/success/partial/failed）
MockCoupon 补 3 态: pending + failed_1001 + failed_1002（最小可用子集）
MockTemplate 去重: 5 态 → 4 态（active 保留，online 删除）
---
v1.3 合计: 14 + 5 - 1 + 3 = 21 态（mock 层）
```

### 升级时点（v1.3 dev+doc 协补）

| 任务 | 责任方 | 截止 | 依赖 |
|:---|:---|:---|:---|
| CouponGrantTask types 定义 | dev | v1.3 sprint 1 | 评审 G5 收口 |
| 任务状态查询接口 | dev + 后端 | v1.3 sprint 2 | CouponGrantTask 上线 |
| 包状态聚合展示 | dev + UI | v1.3 sprint 3 | 接口上线 |
| MockCoupon 补 3 态（pending + failed_1001/1002）| dev | v1.3 sprint 1 | PRD v1.2.8 §11.3.1 失败码表 |
| MockTemplate `online` 去重评审 | arch + doc | v1.3 sprint 1 | - |
| §11 状态机拆分说明 v1.3 | doc | v1.3 收口 | 上述 5 项完成 |

### 升级触发条件

- 后端 grant task runner 上线
- 前端需要展示"包最近一次发券任务状态"
- 模板配置界面需要区分"草稿/已发布/暂停"
- 运营需要看到失败码（pending 内部态 → 可见 failed_1001-1005）

---

## §11.6 兜底说明（派蒙 18:50 写，doc 保留）

**派蒙 10:50 派单 → doc 二次 timeout → 派蒙兑现兜底承诺**:
- 派蒙 10:50 立过规矩"13:00 doc 没交付 → 派蒙亲自写"
- 派单中派蒙记错 1 个数（MockTemplate 7 态 → 实际 5 态）
- doc 18:44 兜底时回执"卡住"（派单错导致 doc 犹豫纠正 vs 按派单写）
- 派蒙 18:48 派单修正版（5 态正确）→ doc 二次 timeout
- **派蒙 18:50 兑现兜底承诺亲自写**

**doc 接手校对**（20:25）:
- ✅ 校对本文档（30 分钟内完成）
- ✅ 修正 3 处事实（见 §0 校对批注表）
- ✅ 加 v1.2.8 增量差异（§11.7 增量表）
- ✅ 同步到项目 wiki 仓 `/Users/wenbo/Documents/project/Wiki/wiki/PRD-数字营销/权益中心/`
- ⏳ task_tool.py update --id TASK-20260604-B7A76A28 --status done（合并 CD84EFC6 后一起改）
- ⏳ task_tool.py update --id TASK-20260604-CD84EFC6 --status done
- ⏳ sessions_send --agentId data_community_pm 报回执

**派蒙认输** = 派蒙越界 doc 职责。派蒙 18:50 写第一稿是派蒙责任（5h52min 超时），但联合 done 时间仍写 doc 名下。

---

## §11.7 PRD v1.2.2 → v1.2.8 增量差异（doc 20:25 补）

| 版本 | 时间 | 状态机相关变更 | 对 wiki 文档的影响 |
|:---|:---|:---|:---|
| v1.2.2 | 2026-06-04 上午 | §11 状态定义原始版（5 态用户券：received/invalidated/expired + §11.4 任务 5 态）| 派蒙兜底稿基于此 |
| v1.2.3 | 2026-06-04 13:48 | 改名：定价折扣 → 临价折扣（纯改名，状态机不动）| 无影响 |
| v1.2.4 | 2026-06-04 14:45 | 库存扣减修正：临价折扣券正常扣减库存（v1.2.1 "不扣库存" 是错误假设）| §11.3 received 流转逻辑变（实扣库存触发点）|
| v1.2.5 | 2026-06-04 15:11 | 发放链路补全 Kafka 双向：pending → received 才实扣库存；核心拒收 → failed + 库存回滚 | §11.3 新增 pending 内部态（用户不可见）|
| **v1.2.6** | 2026-06-04 15:33 | **失败状态机扩展**：failed 拆 5 个（failed_1001-1005，含数字失败码 + 失败原因）| §11.3 增 5 态、§11.3.1 失败码表、§11.3.2 pending 超时、§11.3.3 Kafka 重试 |
| v1.2.7 | 2026-06-04 15:48 | 状态值中文化：received → 未使用、invalidated → 已作废 等（Mock JSON 字段名保留）| PRD 文档中文化，mock 字段名不变 |
| **v1.2.8** | 2026-06-04 17:03 | **删主动作废**：无 Story-004-3 入口，作废 = MA 重新触发新发 → 自动被动作废 | §11.5 状态机引用改 §11.3 表，删 stateDiagram-v2 |

**v1.3 doc 协补任务**（基于 v1.2.8 增量）:
1. §11.3 失败码表（11.3.1）落 mock/coupon.ts（dev 5 态）
2. §11.3.2 pending 超时机制（5 分钟 + 企微报警）落 dev 定时任务
3. §11.3.3 Kafka 重试（producer 自行重试 / consumer 5 分钟超时兜底）落 dev Kafka 配置
4. §11.5 状态机图重画（删主动作废边，新增 5 个 failed_xxxx 终态边)
5. 5/26 教训变体 8（派蒙 4 验收 + 派蒙硬规矩）的对治说明: **评审妥协方案需要明确"半拆"边界 + TODO 注释 + v1.3 协补计划**，否则会演化成"半拆永久化"反模式

---

## §11.8 5/26 教训变体 8 的对治说明（PM 20:18 派单新增要求）

**5/26 教训变体 8 = 派蒙 4 验收 + 派蒙硬规矩**:
- 派蒙 4 验收: 6/4 18:50 派蒙亲自写兜底稿 = 派蒙**第 4 次**验收"doc 5h 没交付就派蒙写"
- 派蒙硬规矩: 10:50 派单"13:00 doc 没交付 → 派蒙写"= 派蒙**自己定的**硬规矩

**对治方案**:
1. **半拆边界明确化**: G5 半拆 = demo 范围 3 态 + 生产级 5 态 = **明确写在 types 注释 + PRD §11.2 备注**（已做）
2. **TODO 注释强制** : 半拆必有 TODO 注释 + 指向 v1.3 协补任务（已做：types/api/coupon.ts:124 TODO）
3. **v1.3 协补计划表**: v1.3 sprint 1/2/3 必补项 + 截止 + 责任方（见 §11.5 升级时点表）
4. **doc 校对 SOP**: 派蒙兜底稿 30 分钟内 doc 必须校对（6/4 20:25 校对 = 1h35min 超时，**未达标**）
5. **回执强制**: 派蒙派单 30 秒内回"收到"+ doc 校对完报 PM（已做：10:55 回"收到" + 20:25 PM 报 wiki 路径）

**教训闭环**:
- 5/26 教训 #1-#7: 见 `memory/lessons/5-26-字段映射静默失败复盘.md`
- 5/26 教训变体 8: 本节
- **变体 8 特殊性**: 不是技术教训（字段错位 / types 缺失），是**流程教训**（doc 失职 → 派蒙越界兜底 → 联合 done），归属 SOP 域

---

**写者**: 派蒙（paimon）2026-06-04 18:50 兜底稿 + data_community_doc 2026-06-04 20:25 校对
**关联任务**: TASK-20260604-B7A76A28 + TASK-20260604-CD84EFC6（合并 done）
**关联 PRD**: PRD-大额低息临价折扣v1.2.8.md §11
**关联代码**: apps/mkt-app/src/{types/api,mock}/coupon.{ts,json}
**关联评审**: review-prd-v1.2.2.md G5 缺口
