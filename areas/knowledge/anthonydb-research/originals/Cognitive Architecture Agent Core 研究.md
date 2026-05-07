---
title: "Cognitive Architecture Agent Core 研究"
tags:
  - area/knowledge
  - collection/anthonydb-research
  - source/anthonydb
  - topic/agent-systems
  - type/original
  - wiki/af
---
# Cognitive Architecture Agent Core 研究

## Meta
- type: `deepresearch`
- domain: `research`
- spark: `on`
- created: 2026-04-06
- source: KG/raw/legacy-notes/Cognitive Architecture Agent Core 研究.md

## Content
# Cognitive Architecture Agent Core 研究

> 目标：先研究各类 cognitive architecture 的 `agent core`，并以 `Claude Code` 作为现代 agent 基准项做轻量对照。
> 范围：第一轮只深看 `Claude Code`、`0-Architecture`、`LIDA`、`ACT-R`、`Soar`、`CLARION`、`HTM`；其余架构先给最小判断。
> 说明：下面的 Python 函数都是 `execution philosophy sketch`，表达的是最小执行单元和控制逻辑，不是可直接运行的实现。

## Claude Code / Tool-Calling Agent

- `core thesis`: agent core 不是显式认知模块，而是一个 `LLM policy + tool dispatcher + conversation memory` 循环。
- `core loop`: `messages -> model response -> tool_use? -> execute tools -> append tool_result -> continue / halt`。
- `agent core`: 核心单元是一次 `model call`。模型决定是否调用工具，运行时只负责执行工具和把结果写回对话。
- `state and memory`: `messages` 就是工作记忆；工具外部系统、文件系统、API 结果构成外部环境记忆。
- `learning`: loop 本身没有原生 online learning；最多通过写消息、写文件、更新外部状态形成“经验痕迹”。
- `control logic`: `stop_reason` 决定循环是否停止；`tool_use` block 决定是否进入动作分支。
- `agent-core judgment`: Claude Code 的 core 是一个极简 `policy-action-observation append loop`，非常适合做现代 agent 基准项。

Python 抽象：

```python
def claude_code_unit(core, observation=None):
    response = core.model(
        system=core.system_prompt,
        messages=core.messages,
        tools=core.tools,
    )

    if response.stop_reason != "tool_use":
        core.messages.append(response.as_assistant_message())
        return {
            "core": core,
            "working_memory": core.messages,
            "selected_action": None,
            "environment_update": None,
            "learning_update": None,
            "control_signal": "halt",
            "output": response.text,
        }

    tool_results = []
    for tool_call in response.tool_calls:
        tool_results.append(core.run_tool(tool_call))

    core.messages.append(response.as_assistant_message())
    core.messages.append(core.as_tool_result_message(tool_results))

    return {
        "core": core,
        "working_memory": core.messages,
        "selected_action": response.tool_calls,
        "environment_update": tool_results,
        "learning_update": None,
        "control_signal": "continue",
        "output": None,
    }
```

## 0-Architecture

- `core thesis`: 不是把认知功能拆成静态模块，而是用一个会演化的 functional core 持续生成智能功能。
- `core structure`: 两层结构。底层是 `Umwelt interface layer`，直接连 `Merkwelt / Werkwelt`；上层负责高层心理功能。
- `core components`: 五个核心部件 `Perceptual / Motor / Intelligent / Emotional / Volitional`。
- `agent core`: 每个部件内部都有 functional kernel，负责三件事：发控制信号、通过新增元素/改连接推动部件演化、和其他部件交互。
- `state and memory`: `Intelligent component` 负责 mental models / symbols，也就是 `Innenwelt`；不是先验写死符号集，而是通过知觉和行动共同形成。
- `learning`: 关键不是监督学习，而是 `orienting reflex` 触发的 postnatal ontogenesis。情绪部件参与自监督学习、模式识别和类别形成。
- `control logic`: `Motor component` 在交互图里是中心总线，负责把各核心部件之间的信息流接起来；`Volitional component` 做高层协调、目标设定、资源分配。
- `why this matters`: 这条路线把 agent core 定义为“可生长的控制系统”，不是“固定模块 + 静态接口”。
- `evidence`: papers；核心描述见论文第 6 节，尤其是五核心部件与信息流部分。

Python 抽象：

```python
def zero_architecture_unit(core, world):
    sensory_state = core.perceptual.observe(world.merkwelt())
    affect_state = core.emotional.evaluate(sensory_state, core.body_state)
    inner_model = core.intelligent.update_innenwelt(
        sensory_state, affect_state, core.inner_model
    )
    intention = core.volitional.allocate(
        inner_model, affect_state, core.goals, core.resources
    )
    motor_command = core.motor.enact(intention, world.werkwelt())
    core = core.evolve_via_reflex(
        sensory_state, affect_state, inner_model, intention, motor_command
    )
    return {
        "working_memory": inner_model,
        "selected_action": motor_command,
        "environment_update": {"werkwelt_command": motor_command},
        "learning_update": "self-evolution via orienting reflex",
        "control_signal": "continue",
    }
```

## LIDA

- `core thesis`: agent core 不是单次规划器，而是一轮一轮运行的认知循环。
- `core loop`: `SensoryMemory -> PerceptualAssociativeMemory -> Workspace -> GlobalWorkspace -> ProceduralMemory -> ActionSelection -> SensoryMotorMemory -> Environment`。
- `agent core`: 真正的核心在 `GlobalWorkspace broadcast + ProceduralMemory + ActionSelection` 这一段。前面负责把感知加工成可竞争的内容，后面负责把广播结果变成可执行行为。
- `state and memory`: `PerceptualAssociativeMemory` 管感知激活与阈值传播；`Workspace` 挂当前内容；`ProceduralMemory` 存 `scheme(context -> action -> result)`。
- `learning`: 通过 detectors / codelets / broadcast / procedural schemes 不断更新候选行为。这个 sample 里 scheme 是显式配置的，但框架设计显然面向持续更新。
- `implementation reading`: 这个 community repo 不是完整框架源码，真正框架主要在 `lida-framework-v1.2b.jar`，本仓库更像一个接入环境的示例 agent。即便如此，`Agent.xml` 已经把 core pipeline 摆得很清楚。
- `agent-core judgment`: LIDA 的 core 更像 `global broadcast-driven cognitive cycle`，而不是单一 memory module 或 planner。
- `local code`: `1st Startup/notes/paper reviews/cognitive-architecture-code/lida-community/configs/Agent.xml`

Python 抽象：

```python
def lida_unit(agent, environment):
    sensory = agent.sensory_memory.sample(environment)
    percepts = agent.perceptual_associative_memory.activate(sensory)
    workspace = agent.workspace.integrate(percepts)
    coalition = agent.global_workspace.compete_and_broadcast(workspace)
    candidate_schemes = agent.procedural_memory.match(coalition)
    behavior = agent.action_selection.choose(candidate_schemes)
    action = agent.sensory_motor_memory.translate(behavior)
    world_update = environment.apply(action)
    return {
        "working_memory": workspace,
        "selected_action": action,
        "environment_update": world_update,
        "learning_update": "scheme activation / codelet update",
        "control_signal": "broadcast",
    }
```

## ACT-R

- `core thesis`: 用 buffer + production rules + declarative retrieval 构成一个时间化的认知虚拟机。
- `core loop`: 先算 context，再匹配 productions，按 activation / utility 选一条 rule，等待 production latency 后执行；如果需要知识，再去 declarative memory 按 activation 检索 chunk。
- `agent core`: `ACTR` 类本质上是一个 `ProductionSystem` 调度器。工作记忆不以大对象图出现，而是以若干 `Buffer` 的当前 chunk 出现在上下文里。
- `state and memory`: `Buffer` 是工作记忆槽位；`Memory` 是 declarative memory，支持 `request -> match -> activation ranking -> recall/fail`。
- `selection`: productions 不是命中即发，而是先竞争。`core.py` 里会计算每条 production 的 activation，过阈值后选最大值项执行。
- `learning`: 程序性部分通过 `PM*` adaptors 做 utility / reward 更新；陈述性部分通过 `DMBaseLevel / DMNoise / DMSalience / spreading` 等 adaptor 调整 chunk activation。
- `embodiment hooks`: `vision / motor / imaginal / timer` 都是外挂模块，统一挂在 ACT-R 主循环外侧。
- `agent-core judgment`: ACT-R 的 core 是“以生产规则为中心的有限工作记忆控制器”，很强调时延、检索成本和模块边界。
- `local code`: `python_actr/python_actr/actr/core.py`、`python_actr/python_actr/actr/dm.py`、`python_actr/python_actr/actr/pm.py`

Python 抽象：

```python
def actr_unit(agent):
    context = agent.buffers.to_context()
    matches = [p for p in agent.productions if p.matches(context)]
    if not matches:
        return {
            "working_memory": context,
            "selected_action": None,
            "environment_update": None,
            "learning_update": None,
            "control_signal": "wait",
        }

    selected = max(matches, key=lambda p: agent.utility(p))
    result = selected.fire(context)

    if result.requests_memory:
        chunk = agent.declarative_memory.retrieve(result.memory_query)
        agent.buffers.write(result.target_buffer, chunk)

    agent.procedural_memory.learn_from_reward(selected, result.reward)
    agent.declarative_memory.update_base_levels(result.rehearsed_chunks)
    return {
        "working_memory": agent.buffers.to_context(),
        "selected_action": selected.name,
        "environment_update": result,
        "learning_update": {
            "procedural": "utility update",
            "declarative": "base-level update",
        },
        "control_signal": "continue",
    }
```

## Soar

- `core thesis`: 用统一的 production-system kernel 驱动整个 agent，不把规划、问题求解、学习拆成完全不同的外置子系统。
- `core loop`: 围绕 `state / operator` 展开：提出 operator、评估 operator、选择 operator、应用 operator。发生 impasse 时生成 substate 继续求解。
- `agent core`: working memory 上的符号结构 + `sp { ... }` production rules + operator-based decision cycle。
- `state and memory`: 当前状态存在 working memory；程序知识由 productions 编码；长期学习通过 `chunking` 把 subgoal 求解结果编译回新规则。
- `learning`: repo 自带的 planning test 一上来就开 `chunk always`，并配置 `lhs/rhs repair`、`max-chunks`、`max-dupes`。这说明 chunking 不是附属功能，而是 core learning mechanism。
- `implementation shape`: repo 里有 `Kernel`、`SoarCLI`、Tcl/Java/Python bindings 和 tests，说明作者把 Soar 当成可嵌入式认知内核，而不是单个 demo agent。
- `agent-core judgment`: Soar 的核心不是 memory 或 planner 某一块，而是一个统一的 `operator selection + impasse + chunking` 机制。
- `local code`: `1st Startup/notes/paper reviews/cognitive-architecture-code/soar/PerformanceTests/TestAgents/mac-planning_learning.soar`、`.../soar/README.md`

Python 抽象：

```python
def soar_unit(agent, working_memory):
    working_memory = agent.elaborate(working_memory)
    proposals = agent.propose_operators(working_memory)
    evaluations = agent.evaluate_operators(working_memory, proposals)
    operator = agent.select_operator(proposals, evaluations)

    if operator is None:
        substate = agent.create_impasse_substate(working_memory)
        subresult = soar_unit(agent, substate)
        agent.chunk(subresult, into=working_memory)
        return {
            "working_memory": substate,
            "selected_action": None,
            "environment_update": None,
            "learning_update": "chunk subgoal result into productions",
            "control_signal": "subgoal",
        }

    working_memory = agent.apply_operator(working_memory, operator)
    return {
        "working_memory": working_memory,
        "selected_action": operator,
        "environment_update": working_memory,
        "learning_update": "optional chunking after impasse resolution",
        "control_signal": "continue",
    }
```

## CLARION

- `core thesis`: 明确把 agent core 分成显式层和隐式层，并允许 top-down / bottom-up 双向传播。
- `core representation`: `chunk` 是显式知识基本单位；chunk 把 top-level symbol 连到 bottom-level `(micro)features / dimension-value pairs`。
- `agent core`: 从实现上看，`ChunkStore + RuleStore + Buffer/Stack + Controller + learning components` 共同构成 core。不是一个单循环，而是一套离散事件系统。
- `control logic`: `pyClarion` 把模型定义成 `discrete event simulation`。各组件产生事件，系统按优先级推进；controller 读取当前 action key 并触发回调。
- `state and memory`: `Buffer / Stack` 负责当前状态；`ChunkStore` 维护显式 chunk；`RuleStore` 维护规则；`BaseLevel` 提供类似熟练度/可得性的 base-level activation。
- `inference`: 显式 chunk 可以走 `bottom-up` 激活，也可以从 top-level 走 `top-down` 激活；rules 被编译成权重矩阵后参与传播。
- `learning`: repo 里直接有 `TDLearning`、`BaseLevel`、rule/chunk encoding，说明这个实现把学习当成 core process，而不是外部训练脚本。
- `agent-core judgment`: CLARION 的 core 是“显式符号层 + 底层数值层 + 事件驱动控制 + 学习信号”的组合体。
- `local code`: `pyclarion/demos/introduction.ipynb`、`pyClarion/components/chunks.py`、`pyClarion/components/rules.py`、`pyClarion/structures/buffers.py`、`pyClarion/components/learning.py`

Python 抽象：

```python
def clarion_unit(agent, sensory_input, reward=0.0):
    implicit_state = agent.bottom_level.encode(sensory_input)
    explicit_chunks = agent.chunk_store.bottom_up(implicit_state)
    explicit_rules = agent.rule_store.match(explicit_chunks)
    action_scores = agent.combine(
        implicit_state, explicit_chunks, explicit_rules, agent.goal_state
    )
    action = agent.controller.select(action_scores)
    agent.base_levels.invoke(explicit_chunks, explicit_rules)
    agent.td_learning.update(action, reward)
    return {
        "working_memory": {
            "implicit": implicit_state,
            "explicit_chunks": explicit_chunks,
            "explicit_rules": explicit_rules,
        },
        "selected_action": action,
        "environment_update": action,
        "learning_update": {
            "base_level": "invoke explicit knowledge",
            "td": reward,
        },
        "control_signal": "continue",
    }
```

## HTM

- `core thesis`: intelligence core 不是 planner，而是持续在线的时空模式学习器。
- `core loop`: `encoders -> sparse distributed representations -> temporal/spatial pattern learning -> anomaly/prediction outputs`。
- `agent core`: 在 NuPIC 这个实现里，HTM 更像一个 `continuous sequence-memory core`。它处理流式输入，持续更新内部表示，并输出预测或异常分数。
- `state and memory`: memory 不是显式 chunk/rule store，而是 SDR-based temporal state。时间模式本身就是长期记忆。
- `learning`: README 直接强调 `time-based continuous learning algorithms`，核心能力是存储和召回 `spatial and temporal patterns`。
- `implementation shape`: NuPIC 里能看到 `encoders`、`swarming`、prediction/anomaly 配置，说明系统围绕“如何把流数据编码成可学习的时序状态”组织，而不是围绕任务规划。
- `agent-core judgment`: HTM 的 core 更接近 perception-memory substrate；它天然强 sequence memory，但不天然给出高层 goal/action loop。
- `local code`: `1st Startup/notes/paper reviews/cognitive-architecture-code/nupic-legacy/README.md`、`.../nupic-legacy/src/nupic/encoders/`

Python 抽象：

```python
def htm_unit(model, observation):
    sdr = model.encoders.encode(observation)
    active_columns = model.spatial_pooler.compute(sdr)
    active_cells, prediction = model.temporal_memory.step(active_columns)
    anomaly = model.anomaly_model.score(active_columns, prediction.previous)
    return {
        "working_memory": {
            "active_columns": active_columns,
            "active_cells": active_cells,
            "prediction": prediction.next,
        },
        "selected_action": None,
        "environment_update": {
            "prediction": prediction.next,
            "anomaly": anomaly,
        },
        "learning_update": "continuous temporal-memory update",
        "control_signal": "continue",
    }
```

## CELTS

- `current judgment`: narrow tutoring architecture；agent core 里情绪和学习机制占比高，但不面向通用 autonomous agent。
- `status`: 先保留在清单里，后续再补。

Python 抽象（provisional）：

```python
def celts_unit(tutor, student_state):
    diagnosis = tutor.assess(student_state)
    affect = tutor.update_emotion(diagnosis)
    lesson_move = tutor.select_instruction(diagnosis, affect)
    return {
        "working_memory": diagnosis,
        "selected_action": lesson_move,
        "environment_update": lesson_move,
        "learning_update": affect,
        "control_signal": "continue",
    }
```

## FORR

- `current judgment`: expert-knowledge driven decision architecture；core 更像规则化决策顾问系统。
- `status`: 先保留在清单里，后续再补。

Python 抽象（provisional）：

```python
def forr_unit(state, advisors):
    advice = [advisor.comment(state) for advisor in advisors]
    decision = aggregate_advice(advice)
    return {
        "working_memory": advice,
        "selected_action": decision,
        "environment_update": decision,
        "learning_update": None,
        "control_signal": "continue",
    }
```

## Sigma

- `current judgment`: 更偏统一框架 / unified theory；这轮还没拿到足够直接代码证据。
- `status`: 先保留在清单里，后续再补。

Python 抽象（provisional）：

```python
def sigma_unit(model, factors):
    beliefs = model.infer(factors)
    decision = model.choose(beliefs)
    model = model.update(beliefs, decision)
    return {
        "working_memory": beliefs,
        "selected_action": decision,
        "environment_update": decision,
        "learning_update": "belief/state update",
        "control_signal": "continue",
    }
```

## EPIC

- `current judgment`: symbolic cognitive modeling 平台；更偏实验认知任务，不像通用 agent kernel。
- `status`: 先保留在清单里，后续再补。

Python 抽象（provisional）：

```python
def epic_unit(agent, perceptual_stream):
    percepts = agent.perceive(perceptual_stream)
    cognitive_state = agent.apply_task_rules(percepts)
    motor_schedule = agent.schedule_response(cognitive_state)
    return {
        "working_memory": cognitive_state,
        "selected_action": motor_schedule,
        "environment_update": motor_schedule,
        "learning_update": None,
        "control_signal": "continue",
    }
```

## ICARUS

- `current judgment`: symbolic architecture，但 skill / concept 表示值得后看。
- `status`: 先保留在清单里，后续再补。

Python 抽象（provisional）：

```python
def icarus_unit(agent, state):
    concepts = agent.recognize(state)
    skill = agent.select_skill(concepts, agent.goals)
    outcome = agent.execute(skill, state)
    return {
        "working_memory": concepts,
        "selected_action": skill,
        "environment_update": outcome,
        "learning_update": "possible skill refinement",
        "control_signal": "continue",
    }
```

## COGNET

- `current judgment`: 面向工作环境行为模拟；core 偏任务/流程建模。
- `status`: 先保留在清单里，后续再补。

Python 抽象（provisional）：

```python
def cognet_unit(agent, context):
    situation = agent.assess_context(context)
    operator_model = agent.update_operator_model(situation)
    decision = agent.choose_next_task(operator_model)
    return {
        "working_memory": operator_model,
        "selected_action": decision,
        "environment_update": decision,
        "learning_update": "operator model update",
        "control_signal": "continue",
    }
```

## DAC-h3

- `current judgment`: developmental robotics 路线；身体、自我、主动探索都在 core 里。
- `status`: 先保留在清单里，后续再补。

Python 抽象（provisional）：

```python
def dach3_unit(agent, body, world):
    salient_state = agent.perceive(world, body)
    motive = agent.regulate_drives(salient_state)
    plan = agent.proactive_controller.select(motive, body.self_model)
    outcome = agent.enact(plan)
    return {
        "working_memory": {
            "salient_state": salient_state,
            "motive": motive,
        },
        "selected_action": plan,
        "environment_update": outcome,
        "learning_update": "developmental adaptation",
        "control_signal": "continue",
    }
```

## BBD

- `current judgment`: biologically inspired robotics 原则性架构；更偏 embodied control 设计。
- `status`: 先保留在清单里，后续再补。

Python 抽象（provisional）：

```python
def bbd_unit(agent, sensorimotor_state):
    integrated_state = agent.integrate(sensorimotor_state)
    value_signal = agent.evaluate(integrated_state)
    behavior = agent.trigger_behavior(integrated_state, value_signal)
    return {
        "working_memory": integrated_state,
        "selected_action": behavior,
        "environment_update": behavior,
        "learning_update": "adaptive tuning",
        "control_signal": "continue",
    }
```

## 第一轮结论

1. `0-Architecture`、`LIDA`、`ACT-R`、`Soar`、`CLARION`、`HTM` 六种架构，对 `agent core` 的定义其实完全不同。
2. `Soar / ACT-R` 把 core 做成显式控制循环；`LIDA` 把 core 做成认知广播循环；`CLARION` 把 core 做成双层知识与事件系统；`HTM` 把 core 做成在线时序学习底座；`0-Architecture` 则把 core 提升成会生长的 functional kernel。
3. 真正值得继续深挖代码的优先级仍然是：`Soar`、`ACT-R`、`CLARION`、`LIDA`，然后才是 `HTM`。`0-Architecture` 暂时只能从论文理解，因为还没发现作者公开代码。

## Keypoints
<!-- LLM 提取，每条是一个可连接的知识点 -->
<!-- 如果该 keypoint 在其他 node 也出现过，标注 (also in: node名) -->
- [[KP - Memory|Memory]]
- [[KP - Agent Core|Agent Core]]
- [[KP - Claude Code|Claude Code]]
- [[KP - HTM|HTM]]
- [[KP - BBD|BBD]]
- [[KP - LIDA|LIDA]]
## Links
### hints

### dive-ins
