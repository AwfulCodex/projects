# Claude Steering File — Indie Game Short

## Model Rules (Enforced)

| Task Type | Model |
|-----------|-------|
| Spec creation, brainstorming, architecture, design decisions | `claude-opus-4-8` |
| Implementation, bug fixes, refactoring, code review | `claude-sonnet-4-6` |

**Never downgrade Opus for spec tasks. Never use Haiku unless explicitly asked.**

## Project Overview

This is a short-form indie game project. Development follows a **spec-driven workflow** — every significant feature begins with a spec before any code is written.

## Spec-Driven Development

Full methodology: [SKILLS/SPEC_DRIVEN_DEVELOPMENT.md](SKILLS/SPEC_DRIVEN_DEVELOPMENT.md)

**Short version:**
1. Create spec with Opus → `./spec-generator.ps1 "Title" "Description"`
2. Review and refine in `spec/inprogress/`
3. Implement with Sonnet, referencing the spec
4. Complete spec → `./spec-complete.ps1 "name"`

**Require a spec for:** new mechanics, new systems, major refactors, cross-system features.
**Skip a spec for:** bug fixes, small tweaks, one-line changes.

## Project Structure

```
CLAUDE.md                        ← you are here
SKILLS/
  SPEC_DRIVEN_DEVELOPMENT.md     ← full spec workflow guide
spec/
  inprogress/                    ← specs under development
  completed/                     ← specs that have been implemented
spec-generator.ps1               ← create a spec (uses Opus)
spec-complete.ps1                ← mark a spec complete
```

## Claude Behavior Guidelines

- **Specs before code** — If asked to implement something significant, ask if there's a spec first
- **No unnecessary comments** — Only comment when the WHY is non-obvious
- **No over-engineering** — Don't add abstractions beyond what the task requires
- **No unsolicited refactoring** — A bug fix is just a bug fix
- **Testable acceptance criteria** — "Player can do X" not "system is good"
- **Ask before big decisions** — If scope is unclear, clarify before implementing

## Common Commands

```powershell
# Create a new spec (uses Opus)
./spec-generator.ps1 "Feature Title" "Brief description"

# Mark a spec as complete
./spec-complete.ps1 "feature-name"
```

## Environment

- Platform: Windows 11
- Shell: PowerShell
- API Key: ANTHROPIC_API_KEY environment variable
