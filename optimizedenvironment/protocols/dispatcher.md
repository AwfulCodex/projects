# 任务分配协议 (Task Dispatcher Protocol)

> 协议版本: 1.0.0
> 维护者: 编排器 (Orchestrator)
> 适用: 逻辑代理协调器 和 实施代理协调器

---

## 1. 目的 (Purpose)

本协议定义协调器如何将传入任务路由到专家代理的规则。
它确保任务被分配给最合适的专家，同时保持系统内聚性。

English summary: This protocol defines how coordinator agents route incoming tasks to
specialist agents, ensuring each task reaches the most qualified specialist while
maintaining system coherence.

---

## 2. 逻辑代理路由规则 (Logic Agent Routing Rules)

### 2.1 何时路由到 `logic-agent-architecture`

路由条件（任何一个匹配即路由）:
- 任务涉及系统设计或架构决策
- 用户问"应该怎样设计这个功能？"
- 任务涉及多个模块间的交互
- 需要评估权衡（性能 vs 可维护性，等）
- 涉及新的文件夹结构或项目布局
- 涉及依赖关系或库选择

**专家焦点**: 整体设计、跨层交互、约束权衡

### 2.2 何时路由到 `logic-agent-bugfix`

路由条件（任何一个匹配即路由）:
- 用户报告错误或"X不工作"
- 任务包含调试、诊断或根本原因分析
- 用户报告意外的行为或崩溃
- 涉及测试失败或生产问题
- 需要追踪问题到源头

**专家焦点**: 错误定位、诊断、修复策略

### 2.3 何时路由到 `logic-agent-refactor`

路由条件（任何一个匹配即路由）:
- 用户要求"整理代码"或"改进这段代码"
- 任务涉及重构、优化或现代化
- 需要改进代码清晰度、性能或测试覆盖率
- 涉及移除技术债务
- 涉及重命名、提取函数或简化逻辑

**专家焦点**: 代码质量、优化、结构改进

### 2.4 默认路由（不确定时）

如果任务不清楚属于哪个专家:
1. 路由到 `logic-agent-architecture`（最安全的默认）。
2. 架构代理确定最合适的专家并重新路由。
3. 如果需要多个专家，架构代理生成多个任务计划。

---

## 3. 实施代理路由规则 (Implementation Agent Routing Rules)

### 3.1 何时路由到 `implementation-agent-code`

任务类型:
- 文件读取、写入、编辑
- 代码修改（函数编辑、行编辑、添加导入等）
- 创建新文件或删除文件
- 修改配置文件（JSON、YAML、TOML等）
- 重命名或移动文件
- 符号提取、函数调用跟踪

**执行环境**: 文件系统 + 代码编辑工具

### 3.2 何时路由到 `implementation-agent-shell`

任务类型:
- 运行命令（npm, python, cargo, git等）
- 编译、构建、测试执行
- 安装或更新依赖
- git操作（提交、推送、分支等）
- 环境检查（检查工具版本，权限等）
- 打包或部署操作

**执行环境**: 终端/Shell + 系统命令

### 3.3 并行任务标记

如果逻辑代理在任务计划中标记步骤为可并行（`并行组: P1`），
实施代理协调器将:

1. 识别并行组。
2. 确定每个步骤的执行代理。
3. 如果两个步骤可以由不同代理执行，派发到两个代理。
4. 等待两个代理完成，合并结果。

```
步骤3a: 编辑文件A          → implementation-agent-code (并行)
步骤3b: 运行测试          → implementation-agent-shell (并行)
```

实施代理协调器同时派发两个步骤，等待两个结果，然后进行步骤4。

### 3.4 默认路由（不确定时）

如果操作类型不清楚:
1. 首先尝试 `implementation-agent-code`（大多数操作都是文件操作）。
2. 如果代理报告"这不是文件操作"，重新路由到 `implementation-agent-shell`。

---

## 4. 协调器职责 (Coordinator Responsibilities)

### 逻辑代理协调器 (`logic-agent`)

- 解析用户输入。
- 应用路由规则（第2.1-2.4章）。
- 派发到适当的逻辑专家。
- 合并多个专家输出（如果需要）。
- 生成最终任务计划供实施代理使用。

### 实施代理协调器 (`implementation-agent`)

- 接收逻辑专家的任务计划。
- 识别步骤的执行代理。
- 识别并行执行机会。
- 派发步骤到代码或shell专家。
- 等待所有步骤完成。
- 生成最终执行结果供翻译代理使用。

---

## 5. 协调器与专家的消息格式 (Message Format: Coordinator ↔ Specialist)

所有消息使用标准格式（见 `protocols/message-format.md`），
带有以下添加字段用于路由:

```
【消息】
发: [coordinator-id]
收: [specialist-id]
型: [任务 | 结果]
...

【路由元数据】
路由原因: [列举匹配的路由规则]
是否可重路由: [是 | 否]
```

---

## 6. 错误与重路由 (Errors & Re-routing)

如果专家无法完成分配的任务:

```
【错误报告】
任ID: [task-id]
原因: "此任务应该由X代理处理，不是由我"
建议重路由: [specialist-id]
```

协调器收到此错误后:
1. 向该专家确认（通常协调器是正确的）。
2. 如果专家坚持，重路由到建议的专家。
3. 记录重路由事件以改进路由规则。

---

## 7. 路由规则冲突 (Routing Conflicts)

如果一个任务符合多个专家的条件（例如，既涉及架构又涉及错误修复）:

**优先级**（从高到低）:
1. **错误优先** — 如果任务是"修复错误"，首先路由到 `logic-agent-bugfix`。
2. **架构其次** — 如果任务涉及设计决策，路由到 `logic-agent-architecture`。
3. **重构最后** — 如果任务仅是优化，路由到 `logic-agent-refactor`。

**例外**: 如果错误修复涉及大规模架构变更，
由 `logic-agent-bugfix` 生成初始修复计划，然后由 `logic-agent-architecture`
重新审视后续步骤。

---

## 8. 统计与优化 (Statistics & Optimization)

协调器应追踪:
- 每个专家处理的任务数。
- 重路由发生频率。
- 专家完成时间。

每月审查这些数据以改进路由规则。如果某个规则导致频繁的
重路由（> 5%），更新此协议。
