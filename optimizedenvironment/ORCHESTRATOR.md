# ORCHESTRATOR — System Root

## Overview

This is a modular multi-agent system. The Orchestrator reads this file first to understand
agent topology, file locations, and startup sequence before dispatching work.

## Agent Registry

### Coordinator Layer
| Agent ID             | Role                           | Steering File                              |
|----------------------|--------------------------------|--------------------------------------------|
| `logic-agent`        | Routes tasks to specialists    | `agents/logic/steering.md`                 |
| `implementation-agent` | Routes tasks to specialists    | `agents/implementation/steering.md`        |

### Logic Specialists (Chinese internal)
| Agent ID                     | Role                           | Steering File                                  |
|------------------------------|--------------------------------|------------------------------------------------|
| `logic-agent-architecture`   | Architectural decisions        | `agents/logic/variants/architecture.md`        |
| `logic-agent-bugfix`         | Bug analysis & diagnosis       | `agents/logic/variants/bugfix.md`              |
| `logic-agent-refactor`       | Refactoring & optimization    | `agents/logic/variants/refactor.md`            |

### Implementation Specialists (Chinese internal)
| Agent ID                     | Role                           | Steering File                                  |
|------------------------------|--------------------------------|------------------------------------------------|
| `implementation-agent-code`  | File editing, code ops        | `agents/implementation/variants/code.md`       |
| `implementation-agent-shell` | Command execution, system ops  | `agents/implementation/variants/shell.md`      |

### Language Boundary (English)
| Agent ID             | Role                           | Steering File                              |
|----------------------|--------------------------------|--------------------------------------------|
| `translator-agent`   | Chinese → English translation  | `agents/translator/steering.md`            |
| `user-facing-agent`  | User communication (English)   | `agents/user-facing/steering.md`           |

## File Index

```
optimizedenvironment/
├── ORCHESTRATOR.md                         ← You are here
├── agents/
│   ├── logic/
│   │   ├── steering.md                     ← Logic Coordinator authority file
│   │   └── variants/
│   │       ├── architecture.md             ← Logic Agent: Architecture Specialist
│   │       ├── bugfix.md                   ← Logic Agent: Bug Analysis Specialist
│   │       └── refactor.md                 ← Logic Agent: Refactor Specialist
│   ├── implementation/
│   │   ├── steering.md                     ← Implementation Coordinator authority file
│   │   └── variants/
│   │       ├── code.md                     ← Implementation Agent: Code Specialist
│   │       └── shell.md                    ← Implementation Agent: Shell Specialist
│   ├── translator/
│   │   └── steering.md                     ← Translator Agent authority file
│   └── user-facing/
│       └── steering.md                     ← User-Facing Agent authority file
├── protocols/
│   ├── dispatcher.md                       ← Task routing rules to specialists
│   ├── internal-comms.md                   ← Chinese internal message protocol
│   ├── message-format.md                   ← Canonical message schema
│   └── workflow.md                         ← Agent orchestration workflow
└── shared/
    ├── glossary.md                         ← Bilingual term glossary
    └── constraints.md                      ← System-wide rules & constraints
```

## Startup Sequence

1. Read `ORCHESTRATOR.md` (this file) — build agent registry and file map.
2. Load `shared/constraints.md` — apply system-wide rules before any agent runs.
3. Load `protocols/internal-comms.md` — enforce Chinese internal protocol.
4. Load `protocols/dispatcher.md` — understand task routing rules.
5. Load `protocols/workflow.md` — understand task handoff and state machine.
6. Instantiate each agent with its steering file loaded as system context.
7. Route incoming user request to `logic-agent` (coordinator) as the entry point.

## Dispatch Rules

- All new user requests → `logic-agent` (coordinator) first.
- `logic-agent` routes to specialists based on `protocols/dispatcher.md` rules:
  - Architecture/design questions → `logic-agent-architecture`
  - Bug/error analysis → `logic-agent-bugfix`
  - Refactoring/optimization → `logic-agent-refactor`
- Specialist output (Chinese task plan) → `implementation-agent` (coordinator).
- `implementation-agent` routes to specialists for parallel execution:
  - Code edits, file ops → `implementation-agent-code`
  - Shell commands, system ops → `implementation-agent-shell`
- Any implementation specialist output (Chinese result) → `translator-agent`.
- Translator Agent output (English) → `user-facing-agent`.
- `user-facing-agent` is the **only** agent allowed to write to the user.
- Any agent may route an error message back to `logic-agent` for replanning.

## Authority Hierarchy

Steering files > Protocol files > Shared files > Orchestrator defaults.
If a steering file contradicts a protocol file, the steering file wins for
that agent's behavior. Conflicts that affect multi-agent flow must be resolved
by the Orchestrator via `protocols/workflow.md`.

## Language Boundary

```
User ─── English ──► user-facing-agent
                          │
                    translator-agent
                          │
         ┌────── Chinese ────────┐
         ▼                       ▼
   logic-agent             implementation-agent
   (coordinator)           (coordinator)
    │    │    │             │    │
    ▼    ▼    ▼             ▼    ▼
  arch  bug refactor    code  shell
  agent agent agent    agent agent
```

**Internal Chinese communication is mandatory** — all coordinator-to-specialist and
specialist-to-translator routing uses Chinese messages. See `protocols/internal-comms.md`
and `protocols/dispatcher.md`.
