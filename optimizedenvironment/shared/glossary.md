# 双语术语表 (Bilingual Glossary)

> 版本: 1.0.0
> 适用: 所有代理 (All agents)
> 目的: 确保中英文术语一致性，减少翻译歧义

---

## 使用规则 (Usage Rules)

- 所有代理在使用技术术语时必须参照本表。
- 翻译代理在转换中英文时以本表为权威参考。
- 用户界面代理必须使用英文列中的标准术语。
- 内部代理使用中文列中的标准术语。
- 若某概念在本表中无对应项，内部消息中保留英文原词。

---

## A — 代理与架构 (Agents & Architecture)

| 中文               | English                        | 说明                          |
|--------------------|--------------------------------|-------------------------------|
| 代理               | agent                          | 自主执行任务的模型实例         |
| 编排器             | orchestrator                   | 协调所有代理的控制层           |
| 逻辑代理           | Logic Agent                    | 分析与规划代理                 |
| 实施代理           | Implementation Agent           | 执行操作的代理                 |
| 翻译代理           | Translator Agent               | 语言边界代理                   |
| 用户界面代理       | User-Facing Agent              | 用户通信代理                   |
| 转向文件           | steering file                  | 定义代理行为的权威配置文件     |
| 工作流             | workflow                       | 代理执行的操作序列             |
| 并行执行           | parallel execution             | 同时运行多个步骤               |
| 任务计划           | task plan                      | 逻辑代理生成的结构化指令       |
| 任务状态           | task status                    | 任务当前阶段                   |
| 升级               | escalation                     | 将问题提交给人工干预           |

---

## B — 操作状态 (Operation Status)

| 中文     | English         | 说明                     |
|----------|-----------------|--------------------------|
| 成功     | success         | 操作按预期完成           |
| 失败     | failure         | 操作未能完成             |
| 部分完成 | partial         | 部分步骤完成             |
| 等待中   | pending         | 等待依赖或确认           |
| 进行中   | in progress     | 当前正在执行             |
| 已跳过   | skipped         | 步骤被有意跳过           |
| 已取消   | cancelled       | 操作被用户取消           |
| 超时     | timed out       | 超过允许的时间限制       |

---

## C — 错误类型 (Error Types)

| 中文     | English              | 说明                         |
|----------|----------------------|------------------------------|
| 权限错误 | permission error     | 访问被拒绝                   |
| 语法错误 | syntax error         | 代码格式无效                 |
| 超时错误 | timeout error        | 操作超过时间限制             |
| 意外状态 | unexpected state     | 系统处于不可预测的状态       |
| 协议错误 | protocol violation   | 违反通信协议                 |
| 配置错误 | configuration error  | 设置无效或缺失               |
| 文件未找到 | file not found     | 目标文件不存在               |
| 网络错误 | network error        | 外部连接失败                 |

---

## D — 文件与代码操作 (File & Code Operations)

| 中文     | English           | 说明                       |
|----------|-------------------|----------------------------|
| 读取     | read              | 获取文件内容               |
| 写入     | write             | 创建新文件                 |
| 编辑     | edit              | 修改现有文件               |
| 删除     | delete            | 移除文件                   |
| 重命名   | rename            | 更改文件名                 |
| 执行     | execute / run     | 运行命令或脚本             |
| 提交     | commit            | git提交                    |
| 推送     | push              | 推送到远程仓库             |
| 分支     | branch            | git分支                    |
| 合并     | merge             | 合并代码分支               |
| 差异     | diff              | 代码变更对比               |
| 路径     | path              | 文件或目录路径             |
| 目录     | directory         | 文件夹                     |
| 依赖     | dependency        | 软件依赖关系               |

---

## E — 消息与通信 (Messages & Communication)

| 中文       | English              | 说明                         |
|------------|----------------------|------------------------------|
| 消息       | message              | 代理间的通信单元             |
| 消息头     | message header       | 消息元数据部分               |
| 消息体     | message body         | 消息内容部分                 |
| 发送者     | sender               | 消息来源代理                 |
| 接收者     | receiver             | 消息目标代理                 |
| 优先级     | priority             | 消息处理紧急程度             |
| 时间戳     | timestamp            | 消息创建时间                 |
| 路由       | routing              | 消息传递路径                 |
| 澄清       | clarification        | 消除歧义的请求               |
| 确认       | confirmation         | 批准操作的用户回复           |

---

## F — 优先级与约束 (Priority & Constraints)

| 中文     | English      | 说明                     |
|----------|--------------|--------------------------|
| 高优先级 | high priority | 需要立即处理            |
| 中优先级 | medium priority | 标准处理顺序          |
| 低优先级 | low priority  | 可延迟处理              |
| 紧急     | urgent        | 比高优先级更紧迫        |
| 约束条件 | constraints   | 限制操作范围的规则      |
| 破坏性操作 | destructive operation | 不可轻易撤销的操作 |
| 不可逆   | irreversible  | 无法撤销的操作          |
| 令牌     | token         | LLM处理的文本单元       |
| 令牌优化 | token optimization | 减少处理成本的策略 |
