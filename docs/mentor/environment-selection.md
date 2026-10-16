# Environment Selection

This document tells the AI mentor how to help the learner select a programming language and an operating system, and how to adapt the course to the selection. The learner makes the decision. The mentor suggests.

## When to do the selection

| Situation | Action |
|---|---|
| During the first assessment (step 4) | Do the selection. |
| The "Environment" section of the profile is empty or says "Not selected" | Do the selection before you give code or commands. Until then, use Python and Linux. |
| The learner wants to change the language or the OS | Do the selection again. Record the old selection in the notes. Tell the learner which code in `labs/` they must rewrite if they want to keep it. |

## Step 1: Ask

Ask these questions. Use the answers that are already in the profile, and do not ask them again.

1. Which programming language do you want to use? If you do not know: do you know a language already? Which language does your team or your target employer use?
2. Which operating system does your computer use? Can you install software (WSL2, Docker)?
3. Is the computer a company computer with restrictions?

## Step 2: Suggest

**Language** (use `docs/languages.md`):

1. If the learner names a language from the table, accept it. Tell them the fit with the documents.
2. If the learner does not program, recommend Python.
3. If the learner knows Java, C#, or TypeScript well, recommend that language. They then learn testing, not a new language.
4. If the learner's team uses a language, recommend that language.
5. If the learner names a language that is not in the table, tell them which tools are missing, and suggest the nearest supported language.

**Operating system** (use `docs/environment.md`):

1. Linux: use it as it is.
2. Windows: recommend WSL2 with Ubuntu for all course work. If WSL2 is blocked, the learner can use Windows with PowerShell for phases 1–4 and 6–10, but phase 0 needs a Linux shell (a virtual machine or a container), and phase 5 needs Linux tools. Tell the learner the extra effort.
3. macOS: use the macOS terminal for most work, and an Ubuntu container or virtual machine for phase 0.

## Step 3: Record

Fill in the "Environment" section of `learner/profile.md`:

- The language and its version
- The OS, and how the learner gets a Linux shell (native, WSL2, virtual machine, container)
- The editor
- The Docker setup (Docker Engine, Docker Desktop, OrbStack, Colima)
- The tool stack from `docs/languages.md` for the language: project tool, test framework, HTTP client, browser automation, BDD tool, linter, type checker
- Restrictions (for example a company proxy or blocked software)

## Translate the course to the environment

In every session, if the environment in the profile is not the reference environment (Python on Ubuntu):

1. Read the phase document as usual.
2. Before you give the learner a code example or a command, translate it to the learner's environment:
   - **Code:** use the tool in the same row of `docs/languages.md`. Keep the same test design and the same structure. Use the idioms of the language, not Python written in a different syntax.
   - **Commands:** on macOS, use the BSD options or Homebrew. On Windows without WSL2, give PowerShell commands.
   - **Paths and files:** `pyproject.toml` becomes `build.gradle.kts`, `pom.xml`, `*.csproj`, or `package.json`. `tests/` becomes the conventional test directory of the language.
3. If a tool has no equal in the learner's language, tell the learner. Suggest an alternative exercise that teaches the same concept.
4. Phase 0 (Linux) and phase 5 (networking) do not change with the language. They change only with the OS.
5. If the translation of a phase is large, suggest a topic document in `docs/topics/` for the language (for example `java-phase-6.md`). Other learners with the same language can use it.

For the reference environment, use the documents as they are.
