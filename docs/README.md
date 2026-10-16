# QA Automation Course

This course teaches software testing and test automation. It starts at zero for programming, Linux, and networking. It follows the ISTQB path from the Foundation Level to Test Automation Engineering and Test Automation Strategy.

## Who this course is for

- **Required:** you can use a computer, install software, and read technical English.
- **Not required:** knowledge of programming, testing, Linux, or networking. The course teaches these topics.
- **Your background changes the time for phase 1:**

  | Your background | Phase 1 time |
  |---|---|
  | You program in an object-oriented language at work | 1 week (OOP review and the test framework only) |
  | You can write small programs or scripts | 3–4 weeks |
  | You never programmed | 6–8 weeks |

The AI mentor assesses your background in the first session and saves it in `learner/profile.md`. See the [main README](../README.md) for how to start. Without an AI mentor, use the table above to plan phase 1.

The course has twelve phases. Each phase has topics, reading, exercises, and done criteria. One main project, the **test automation solution (TAS)** for the course shop, grows from phase 1 to phase 10. Three phases end with an ISTQB exam.

## How to use this course

You can use the course with an AI mentor or alone. With an AI mentor, the mentor follows [mentor/](mentor/) and tracks your progress in `learner/progress.md`. Alone, follow these steps:

1. Select your language and your operating system. Read [languages.md](languages.md) and [environment.md](environment.md). If you are not sure, use Python on Linux.
2. Install the tools in [software-setup.md](software-setup.md).
3. Read the phase document from top to bottom before you start the phase.
4. Do the reading and the exercises in the given order.
5. Do the project stage for the phase.
6. Do a check of the "Done criteria" list at the end of the phase. Go to the next phase only when all items are complete.
7. Write your notes, results, and problems in your test journal (a text file in `labs/`).
8. Record your progress in `learner/progress.md`. Copy it from [templates/progress-template.md](templates/progress-template.md).

The times assume 6–8 hours of work per week.

## Roadmap

| Phase | Document | Time | Syllabus | Main result |
|---|---|---|---|---|
| 0 | [Linux and the command line](phases/phase-0-linux.md) | 2–3 weeks (parallel to phase 1) | — | You work in a Linux shell, write Bash scripts, read logs, and use git. |
| 1 | [Programming and OOP for testers](phases/phase-1-programming-oop.md) | 1–8 weeks, depends on your background | — | You write programs with classes, and test them with a test framework. |
| 2 | [Testing fundamentals](phases/phase-2-testing-fundamentals.md) | 2 weeks | CTFL ch. 1–2 | You can explain why, when, and how to test, and where testing fits in the lifecycle. |
| 3 | [Static testing and test design](phases/phase-3-test-design.md) | 3–4 weeks | CTFL ch. 3–4 | You derive test cases with test techniques and find the seeded defects of the SUT. |
| 4 | [Test management, tools, and the CTFL exam](phases/phase-4-test-management.md) | 2–3 weeks | CTFL ch. 5–6 | You write a test plan and defect reports. **CTFL exam.** |
| 5 | [Networking basics](phases/phase-5-networking.md) | 2–3 weeks | — | You can explain IP, masks, DHCP, DNS, TCP, HTTP, and TLS, and use SSH. |
| 6 | [API and web test automation](phases/phase-6-api-ui-automation.md) | 6–7 weeks | prepares CTAL-TAE | Automated API and UI test suites for the SUT, with mocks, cross-browser and visual tests, WebSockets, and OAuth 2.0. |
| 7 | [Test automation architecture](phases/phase-7-automation-architecture.md) | 4 weeks | CTAL-TAE ch. 1–4 | A layered test automation framework with design patterns. |
| 8 | [CI/CD, environments, and reporting](phases/phase-8-ci-cd-reporting.md) | 3 weeks | CTAL-TAE ch. 5–6 | A pipeline that runs your tests in containers and publishes reports. |
| 9 | [Verify and improve the TAS, and the CTAL-TAE exam](phases/phase-9-verify-improve.md) | 3 weeks | CTAL-TAE ch. 7–8 | A measured and verified TAS. **CTAL-TAE exam.** |
| 10 | [Test automation strategy, and the CT-TAS exam](phases/phase-10-automation-strategy.md) | 3 weeks | CT-TAS ch. 1–6 | A test automation strategy and a business case. **CT-TAS exam.** |
| 11 | [Beyond](phases/phase-11-beyond.md) | Open-ended | optional | Performance, security, accessibility, contract, mobile, and AI-supported testing. |

**Parallel work:** do phase 0 in parallel with phase 1. If you already program, you can also start phases 2–4 in parallel with phases 0–1. Do phase 5 before phase 6: API tests need HTTP knowledge.

See [certification.md](certification.md) for the syllabus mapping and the exam information.

## Main project: test automation solution

The full specification is in [projects/test-automation-solution.md](projects/test-automation-solution.md).

| Stage | Phase | Features |
|---|---|---|
| 0 | 0–1 | Project skeleton. A script that starts the SUT. The first tests. |
| 1 | 3–4 | Test conditions, test cases, defect reports, and a test plan for the SUT. |
| 2 | 6 | Automated API and UI test suites with page objects. |
| 3 | 7 | Layered framework, data-driven tests, BDD scenarios, logging. |
| 4 | 8 | CI pipeline, containers, test reports, runs on a remote test host. |
| 5 | 9 | Verified TAS: metrics, flaky test detection, defect detection rate. |
| 6 | 10 | Test automation strategy and business case. |

## Documents

| Document | Content |
|---|---|
| [languages.md](languages.md) | Language comparison and the tool stack for each language |
| [environment.md](environment.md) | Operating system options and computer requirements |
| [software-setup.md](software-setup.md) | Tool setup on Linux, Windows (WSL2), and macOS |
| [certification.md](certification.md) | ISTQB syllabi, exams, and the mapping to the phases |
| [reading-list.md](reading-list.md) | Books, syllabi, courses, and documentation |
| [glossary.md](glossary.md) | Terms and abbreviations |
| [phases/](phases/) | One document for each phase |
| [projects/](projects/) | Project specifications and task documents |
| [topics/](topics/) | Detailed explanations of specific topics |
| [mentor/](mentor/) | Instructions for the AI mentor: assessment and teaching |
| [templates/](templates/) | Templates for new documents, the learner profile, and progress |
| [../sut/README.md](../sut/README.md) | The practice application |

## Reference environment

You select your language and your operating system. See [languages.md](languages.md) and [environment.md](environment.md), or ask the AI mentor for a suggestion.

- **Reference environment:** Python 3.13 or newer on Ubuntu LTS. All commands and code in the phase documents are for this environment. In a different environment, you (or the AI mentor) translate these details.
- **SUT:** the course shop in [../sut/](../sut/). It runs in Docker on all operating systems.

## General advice

1. **Design before you automate.** Automation runs the test cases that you designed. A bad test case is still bad when a tool runs it. Learn the test techniques in phase 3 well.
2. **Read the requirement two times.** Many failures in test cases come from a wrong understanding of the requirement, not from a defect in the SUT.
3. **Keep a test journal.** Write down what you tested, what you found, and what you did not test.
4. **Make each failure easy to understand.** A good test case tells you what failed and why. Use clear names, clear assertion messages, and logs.
5. **Treat test code as production code.** It needs reviews, static analysis, version control, and refactoring, the same as the SUT.
6. **Use the terminal every day.** Linux, git, and network tools are a large part of the daily work of a test automation engineer.
