# QA Automation Course

A self-study course in software testing and test automation. You learn the testing fundamentals, test design, test automation architecture, and test automation strategy. The course follows the ISTQB path: Foundation Level (CTFL), Test Automation Engineering (CTAL-TAE), and Test Automation Strategy (CT-TAS). You also learn programming with object-oriented programming (OOP), Linux, and networking basics. You build a real test automation solution for a practice web shop.

- **For:** anyone who wants to work as a tester or a test automation engineer. You do not need to know how to program. Phase 1 teaches programming from the beginning.
- **Environment:** a computer that can run Docker. You select your programming language and your operating system. The documents use Python on Linux (Ubuntu). You can use Java, C#, or TypeScript, and Windows or macOS: the AI mentor adapts the course to your selection. See [docs/languages.md](docs/languages.md) and [docs/environment.md](docs/environment.md).
- **Cost:** all tools are free. The ISTQB exams have a fee. See [docs/certification.md](docs/certification.md).
- **Time:** approximately 10 months for phases 0–10 at 6–8 hours per week. Phase 11 is open-ended.

You can use the course alone, or with an AI coding agent as your mentor. The mentor assesses your knowledge, adapts the explanations to your background, reviews your work, prepares you for the exams, and tracks your progress.

## Quick start with an AI mentor

1. Clone the repository:

   ```sh
   git clone https://github.com/ethno2405/qa-automation-course.git
   cd qa-automation-course
   ```

2. Open an AI coding agent in the repository root. The agent must be able to read and write files and run commands. Examples: Claude Code (`claude`), OpenAI Codex CLI, GitHub Copilot in agent mode, Cursor, Gemini CLI. The agent reads its instructions from [AGENTS.md](AGENTS.md) (Claude Code reads [CLAUDE.md](CLAUDE.md), which imports `AGENTS.md`).

3. Type the first prompt:

   ```
   Start the course.
   ```

4. The mentor offers three assessment modes. Select one:

   | Mode | Time | Content |
   |---|---|---|
   | Quick | ~5 minutes | Questions about your background only |
   | Standard | ~15–20 minutes | Background questions and a short adaptive quiz |
   | Full | ~45 minutes | Background questions, a longer quiz, and practical items (code reading, test design, a subnet calculation) |

5. The mentor asks for your programming language and your operating system. If you do not know, it uses Python and Linux.

6. The mentor makes your track branch, `track/<YYYY-MM-DD>`, with the start date in the name (for example `track/2026-10-16`). It saves your profile and your progress in the `learner/` directory on this branch. Then it tells you where to start.

In each later session, open the agent in the repository root and type `Continue the course.` The agent has no memory of earlier sessions. It finds your track branch, and reads your profile and progress from `learner/`.

## The practice application

The course has its own system under test (SUT): a small web shop with a web UI, a REST API, and a test host that you connect to with SSH. It runs in Docker on your computer. The SUT has seeded defects that you can switch on. You find them with test design techniques, and later your automated tests must find them. See [sut/README.md](sut/README.md).

```sh
cd sut
docker compose up -d
```

Then open `http://127.0.0.1:8000`.

## Your data

- The `learner/` directory contains `profile.md` (background, levels, environment, preferences, mentor observations) and `progress.md` (position, completed work, exams, notes, the newest session log entries). Older session log entries go to `session-log-archive.md`.
- The `labs/` directory contains your code.
- You can read and edit all files. The mentor uses the content that it finds.

### Branches

The `master` branch is the course baseline. It contains only the course documents and the SUT. Each learner has a track branch `track/<YYYY-MM-DD>` that contains the course documents, the SUT, the learner data, and the code of one learner. The date is the start date. The branch name contains no personal data.

| Branch | Content |
|---|---|
| `master` | Course documents and `sut/` |
| `track/<YYYY-MM-DD>` | Course documents, `sut/`, `learner/`, `labs/`, and your CI workflow in `.github/workflows/` (from phase 8) |

- At the end of each session, the mentor asks whether you want to commit your data and code. It commits only on your track branch.
- On `master`, the file `learner/.gitignore` ignores all files in `learner/`, so the files cannot go to `master` by accident. When the mentor makes a track branch, it clears this file in the first commit of the branch. After that, git tracks the learner data on the branch.
- The mentor pushes only when you agree, and only to a remote that you own (for example your fork), or to a remote where the owner permits track branches.
- **Your profile contains personal data.** All persons who can read the remote can read your track branch. If the course repository is public, push your track branch to a private repository (see "Share your data with git").
- Never merge a track branch into `master`.

### Get course updates

The course documents change on `master`. To get the changes on your track branch, merge `master`:

```sh
git switch master
git pull                       # if master has a remote
git switch track/<YYYY-MM-DD>
git merge master
```

A track branch does not change the course documents or the SUT, so the merge has no conflicts.

### Share your data with git

**Private repository** (do this one time if the course repository is public):

1. Make a new, empty, private repository, for example on GitHub. GitHub does not permit a private fork of a public repository.
2. Add the private repository as a second remote: `git remote add private <url>`.

Push `master` to `origin`. Push your track branches to `private`. To share a track with a different person, give that person access to the private repository. If the course repository is private, you do not need a second remote. Use `origin` in place of `private` in the commands below.

**Send** (from the old clone or computer):

1. End the session with `Save my progress and end the session.` The mentor updates your data and offers to commit it.
2. Push your track branch: `git push -u private track/<YYYY-MM-DD>`.

**Receive** (in the new clone, or for a different person):

1. Clone the course repository. Add the private remote (`git remote add private <url>`), and fetch: `git fetch private`.
2. Switch to the track branch: `git switch track/<YYYY-MM-DD>`. Git makes a local branch from `private/track/<YYYY-MM-DD>`.
3. Start the agent and type `Continue the course.` The mentor continues from the "Current position" in `progress.md`.

To see all track branches, run `git branch -a --list "track/*" "*/track/*"`.

**Before you switch branches,** commit your changes. If `learner/` contains files other than `.gitignore` on `master` (local data from an older version of the course), copy the directory to a safe location first. A checkout can overwrite ignored files and does not give a warning.

**Partial data:**

| The branch contains | Result |
|---|---|
| `profile.md` and `progress.md` | The mentor continues where you stopped. |
| Only `progress.md` | The mentor looks for an earlier version in the git history. If there is none, it keeps your position and offers a short assessment to rebuild your profile. |
| Only `profile.md` | The mentor looks for an earlier version in the git history. If there is none, it asks for your current phase and completed exercises, and makes a new progress file. |
| Nothing | The mentor asks whether you started before. If not, it starts a new assessment. |

**Course version:** the progress file refers to phase and exercise numbers. If you merge a different version of the course documents, the mentor checks the position and corrects it with you.

## Start from scratch

The easiest way: make a new track branch from `master`. Your old branch does not change.

```sh
git switch -c track/<YYYY-MM-DD> master   # use the date today
echo "# Track learner data on this branch." > learner/.gitignore
git add -- learner/.gitignore
git commit -m "Track learner data on this branch"
```

**With the mentor:**

```
Reset the course. I want to start from scratch.
Reset only my progress.
Delete my code in labs/ and start phase 6 again.
```

The mentor asks what to reset (profile, progress, code, or all), shows what it will delete, and offers a backup. It deletes nothing before you confirm. It resets only a track branch, never `master`. The backup is a git tag `<branch>/backup-<date>`, for example `track/2026-10-16/backup-2026-11-02`.

**Without the mentor** (run in the repository root, on your track branch):

Bash:

```sh
git tag "$(git branch --show-current)/backup-$(date +%F)"   # optional backup of committed data and code
git rm -r -q --ignore-unmatch -- learner/profile.md learner/progress.md labs   # delete profile, progress, and code
rm -rf learner/profile.md learner/progress.md labs   # delete the remaining local files
git commit -m "Remove learner data to start the course again"
```

PowerShell:

```powershell
git tag "$(git branch --show-current)/backup-$(Get-Date -Format yyyy-MM-dd)"   # optional backup of committed data and code
git rm -r -q --ignore-unmatch -- learner/profile.md learner/progress.md labs   # delete profile, progress, and code
Remove-Item -Recurse -Force learner/profile.md, learner/progress.md, labs -ErrorAction SilentlyContinue   # delete the remaining local files
git commit -m "Remove learner data to start the course again"
```

Uncommitted changes are lost. Commit them before the reset if you want to keep them in the backup tag. Skip the `git commit` command if the branch had no committed learner files.

## Example prompts

### First session

```
Start the course.
Start the course. Use the quick assessment.
Start the course. I am a manual tester. I want to learn automation with Java on Windows.
```

### Each session

```
Continue the course.
What is my next step?
Summarize my progress.
Save my progress and end the session.
Commit my code in labs/.
```

### Learn a topic

```
Explain boundary value analysis at my level.
Explain the TCP three-way handshake with a diagram.
Compare Python classes with the language that I know best.
Why must a page object not contain assertions?
What is the difference between a subnet mask of /24 and /26?
```

### Exercises

```
I finished exercise 3.4. Here are my boundary values for the shipping cost. Check them.
Give me a hint for exercise 5.6. Do not give the solution.
I am blocked on exercise 6.3. Show me the full solution and explain it.
```

### Code review

```
Review my code in labs/phase-6-api-ui.
Review my page objects against the course conventions.
Is my test suite independent of the test order?
```

### Debugging

```
My Playwright test passes on my computer but fails in CI. Help me find the cause step by step.
I cannot connect to the test host with SSH. What do I check first?
Here is the output of curl -v: ... Why does the API return 401?
```

### Quizzes, reviews, and exams

```
Quiz me on phase 2.
I completed phase 4. Do the phase review.
Am I ready for the CTFL exam?
Which CTAL-TAE learning objectives are weak for me?
Re-assess my networking knowledge.
```

### Profile and progress

```
Mark exercise 0.4 as done.
Update my profile: I now prefer full solutions.
I passed the CTFL exam today. Update my progress.
I want to change my language to TypeScript.
Reset the course. I want to start from scratch.
```

### Errors in the course

```
I think exercise 3.5 has an error. Help me open a pull request with the fix.
The command in topic 5.7 does not work on my computer. Is this an error in the course?
```

### Environment and setup

```
Help me choose a programming language for test automation.
I use Windows. Help me install WSL2 and Docker.
The SUT does not start. Help me find the cause.
Help me install the tools for phase 6.
```

## Use fewer tokens

An AI agent has usage limits, or a price for each token. To use fewer tokens, keep sessions short: do one topic or one exercise in one session, then start a new session. The mentor gives you one tip at the start of each session. All tips are in [docs/token-usage.md](docs/token-usage.md).

## Found an error in the course?

Send the fix as a pull request, so that all learners get it. With the AI mentor, say `Help me open a pull request with the fix.` The mentor makes a fix branch from `master` (never from your track branch, which contains personal data), and helps you push it to your fork and open the pull request. Without a mentor, follow [CONTRIBUTING.md](CONTRIBUTING.md). If you do not know the correct fix, open an issue.

## Use the course without an AI mentor

Start with [docs/README.md](docs/README.md). It has the roadmap, and each phase document has its reading, exercises, and done criteria.

## Repository

| Path | Content |
|---|---|
| [AGENTS.md](AGENTS.md) | Instructions for the AI mentor |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to send a fix for an error in the course |
| [docs/](docs/) | Course documents |
| [docs/mentor/](docs/mentor/) | Assessment and teaching instructions for the AI mentor |
| [sut/](sut/) | The practice application (system under test) |
| `labs/` | Your code (created during the course, only on your track branch) |
| `learner/` | Your profile and progress (only on your track branch). On `master`, only `.gitignore`. |
| `learner-backup-<date>/` | Local backups of learner data (not committed) |

## License

[MIT](LICENSE). The ISTQB syllabi, the ISTQB glossary, and the sample exams are the property of the ISTQB. Download them from istqb.org. Do not add them to the repository.
