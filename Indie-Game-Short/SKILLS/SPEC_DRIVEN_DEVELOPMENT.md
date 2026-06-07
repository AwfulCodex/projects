# Spec-Driven Development

This project uses **spec-driven development**: every feature starts with a detailed specification written by Claude Opus before any implementation begins.

## Philosophy

Specs are the bridge between ideas and code. They force clarity on:
- What the feature actually does
- Why it matters
- How it fits the game
- What success looks like
- Technical constraints and edge cases

**Specs prevent**: vague requirements, scope creep, rework, decision paralysis, and implementation surprises.

## The Workflow

### 1. Create a Spec (Opus)

When you want to develop a new feature, create a spec first:

```powershell
./spec-generator.ps1 "Feature Title" "What you want to build"
```

This uses Claude Opus to generate a comprehensive spec. You'll be asked:
- **Audience**: Who uses this?
- **Scope**: How big is it? (single level, full system, menu flow, etc.)

**Output**: Markdown file in `spec/inprogress/[feature-name].md`

### 2. Review & Refine the Spec

Read the generated spec. Ask yourself:
- Is this clear?
- Are the acceptance criteria measurable?
- Are dependencies listed?
- Does it solve the actual problem?

**Edit the spec directly** if you need to adjust scope, clarify mechanics, or add constraints.

### 3. Implement Against the Spec (Sonnet)

Once the spec is locked:
1. Move it to review or keep iterating
2. When ready, call Claude on implementation tasks referencing the spec
3. Use `claude-sonnet-4-6` for implementation work (cheaper, still capable)
4. **Test against acceptance criteria** in the spec

### 4. Complete the Spec

When implementation is done and tested:

```powershell
./spec-complete.ps1 "feature-name"
```

This moves the spec to `spec/completed/` and marks it as complete.

## Spec Structure

Every spec includes these sections:

| Section | Purpose |
|---------|---------|
| **Overview** | What is this, in one paragraph? |
| **Core Mechanics** | How does it work? What can the player do? |
| **Requirements** | What must be true for this to function? |
| **Acceptance Criteria** | How do we know it's done? (testable) |
| **Technical Considerations** | Architecture, assets, complexity, tech choices |
| **Edge Cases** | What breaks this? What's unusual? |
| **Dependencies** | What does this depend on? |
| **Implementation Notes** | Tips for building it |

## Key Rules

1. **Specs come first** — No implementation without a spec
2. **Opus for specs** — Specs are always generated with Claude Opus for quality
3. **Sonnet for implementation** — Implementation uses Sonnet (cheaper, fast)
4. **Acceptance criteria are testable** — "User can do X" not "system is good"
5. **Edit specs before implementing** — Specs are living documents until locked
6. **Reference specs during implementation** — Keep the spec open while coding

## When to Create a New Spec

- New game mechanic (combat, crafting, dialogue, etc.)
- New system (save/load, UI flow, progression, etc.)
- New level/area with different design requirements
- Major refactor that changes how something works
- Cross-system feature (something that touches multiple systems)

**Don't** create a spec for:
- Bug fixes (just fix and test)
- Small UI tweaks (just update)
- Code cleanup (no spec needed)
- One-line changes

## Example Workflow

```
1. User: "I want a combo system"
   → ./spec-generator.ps1 "Combo System" "Chain attacks for bonus damage"

2. Claude (Opus): Generates detailed spec with mechanics, requirements, edge cases

3. User: Reviews spec, asks for tweaks
   → Edit spec/inprogress/combo-system.md
   → Re-run generator or manually refine

4. User: "OK, locked. Implement this."
   → Claude (Sonnet): Implements feature following spec

5. User: Playtests, finds it works per acceptance criteria
   → ./spec-complete.ps1 "combo-system"

6. Spec moves to spec/completed/ as reference for future work
```

## Tips for Good Specs

- **Be specific**: "Player can combo up to 5 hits" not "combo system exists"
- **List edge cases**: What if player hits nothing? Misses? Chains to self?
- **Technical notes matter**: "Requires networked update every 100ms" is important
- **Reference existing mechanics**: "Like X but with Y twist"
- **Keep it short**: 1-2 pages, not a novel
- **Make criteria testable**: "Health bar updates in real-time" not "health is good"

## Directories

- `spec/inprogress/` — Specs being written or refined (not yet implemented)
- `spec/completed/` — Specs that have been implemented (historical record)

## Tools

- `spec-generator.ps1` — Create new specs with Opus
- `spec-complete.ps1` — Mark specs as done

## Integrating with Claude Code

When asking Claude for implementation help:

1. **Reference the spec**: "Implement the Combo System (see spec/inprogress/combo-system.md)"
2. **Use Sonnet**: Model will be set to Sonnet for implementation
3. **Test against criteria**: "Make sure it meets acceptance criteria in the spec"
4. **Update spec if needed**: If implementation reveals new edge cases, update the spec

---

**Core principle**: A good spec makes implementation straightforward. If implementation is confusing, the spec wasn't clear enough.
