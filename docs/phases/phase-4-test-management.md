# Phase 4: Test Management, Tools, and the CTFL Exam

**Time:** 2–3 weeks, plus the exam
**Prerequisites:** Phase 3
**Syllabus:** CTFL v4.0.1, chapter 5 (Managing the Test Activities) and chapter 6 (Test Tools). LOs FL-5.1.1 to FL-6.2.1. See [../certification.md](../certification.md).
**Environment:** The course shop, your test design from phase 3.

## Goal

At the end of this phase, you can:

- Write a test plan with entry criteria and exit criteria.
- Estimate the test effort, and prioritize test cases.
- Explain the test pyramid and the testing quadrants.
- Analyze product risks, and select the test response to each risk.
- Monitor and control the test progress, and write test progress reports and test completion reports.
- Explain how configuration management supports testing.
- Write defect reports that a developer can reproduce.
- Classify test tools, and explain the benefits and risks of test automation.
- Pass the CTFL exam.

## Reading

| Source | Part |
|---|---|
| CTFL syllabus v4.0.1 | Chapters 5 and 6. Then read the whole syllabus again before the exam. |
| CTFL sample exams (istqb.org) | All official sample exams for v4.0 |
| Rex Black, *Managing the Testing Process* | Optional. The chapters about risk and test reports. |

## Topics

### 4.1 The test plan (CTFL 5.1.1)

- A test plan describes the objectives, the resources, and the processes for a test project. It documents the means and the schedule, and it is a communication tool.
- Typical content: the context (scope, objectives, test basis), assumptions and constraints, stakeholders (roles, responsibilities), communication, the risk register, the test approach (test levels, test types, test techniques, deliverables, entry and exit criteria, independence, metrics, test data and environment requirements), the budget and the schedule.
- In Agile, the test plan is often short, and parts of it live in the team agreements and the definition of done.

### 4.2 The tester in iteration and release planning (CTFL 5.1.2)

- **Release planning:** the tester helps to write testable user stories and acceptance criteria, does risk analysis, estimates the test effort, and plans the test approach for the release.
- **Iteration planning:** the tester takes part in the detailed risk analysis of the stories, checks the testability, splits the stories into tasks (including test tasks), estimates the test effort, and finds the functional and non-functional aspects to test.

### 4.3 Entry criteria and exit criteria (CTFL 5.1.3)

- **Entry criteria** define the preconditions for an activity. Examples: the test environment is ready, the test data is available, the smoke test passes, the test basis is stable. In Agile: the **definition of ready**.
- **Exit criteria** define when an activity is complete. Examples: the planned coverage is reached, all high-priority test cases passed, no open critical defects, the defect density is low enough. Also: the time or the budget ends. In Agile: the **definition of done**.

### 4.4 Estimation (CTFL 5.1.4)

| Technique | Method |
|---|---|
| Estimation based on ratios | Use numbers from earlier projects. Example: the test effort was 40 % of the development effort. |
| Extrapolation | Measure early in the project, and extend the measurement. Example: the first 3 sprints used 6 days of testing each. |
| Wideband Delphi | Experts estimate alone, discuss the differences, and estimate again until they agree. Planning Poker is a form of it. |
| Three-point estimation | Estimate the optimistic (a), the most likely (m), and the pessimistic (b) values. E = (a + 4m + b) / 6. The standard deviation SD = (b − a) / 6. |

**Example:** a = 6 hours, m = 9 hours, b = 18 hours. E = (6 + 36 + 18) / 6 = 10 hours. SD = (18 − 6) / 6 = 2 hours. The estimate is 10 ± 2 hours.

### 4.5 Test case prioritization (CTFL 5.1.5)

- **Risk-based:** the test cases for the highest risks run first.
- **Coverage-based:** the test cases with the highest coverage run first. A variant: additional coverage, where each next test case adds the most new coverage.
- **Requirements-based:** the priority of the requirements (from the stakeholders) sets the order.
- **Dependencies** change the order: if a high-priority test case needs a low-priority test case first, run the low-priority test case first.

### 4.6 The test pyramid and the testing quadrants (CTFL 5.1.6, 5.1.7)

- **Test pyramid:** many small, fast, isolated tests at the bottom (component tests). Fewer large, slow tests at the top (end-to-end UI tests). The higher the level, the more expensive and less stable the test. The number of layers and their names can be different in different models.
- **Testing quadrants** (Brian Marick): two axes. Business-facing or technology-facing. Support the team or critique the product.

  | Quadrant | Purpose | Examples | Execution |
  |---|---|---|---|
  | Q1 | Technology-facing, support the team | Component tests, component integration tests | Automated, in CI |
  | Q2 | Business-facing, support the team | Functional tests, examples, story tests, API tests, prototypes | Manual or automated |
  | Q3 | Business-facing, critique the product | Exploratory testing, usability testing, user acceptance testing | Mostly manual |
  | Q4 | Technology-facing, critique the product | Performance, security, load, reliability tests | Mostly automated, with tools |

### 4.7 Risk management (CTFL 5.2)

- **Risk:** an event that can happen in the future and has a negative effect. **Risk level** = risk likelihood × risk impact.
- **Project risks** affect the project: organization (delays, wrong estimates), people (missing skills, conflicts), technical (scope changes, a missing test environment), suppliers (a third party does not deliver).
- **Product risks** affect the quality of the product: missing or wrong functions, wrong calculations, slow responses, security holes, bad usability.
- **Product risk analysis:** risk identification (with workshops, interviews, checklists, earlier defects), then risk assessment (likelihood and impact, as numbers or as a matrix).
- The analysis changes the **thoroughness and scope** of testing: which test levels and types, which techniques and coverage, the effort, the priority, and the order.
- **Risk control:** risk mitigation (actions to reduce the risk, for example more testing, a review, a different technique, a more independent tester) and risk monitoring (check that the actions work, and find new risks). Other responses: accept the risk, transfer it (for example to an insurance or a supplier), or have a contingency plan.

### 4.8 Monitoring, control, completion, and reports (CTFL 5.3)

- **Test monitoring** collects information about the testing. **Test control** uses it to give directions: change the priority, change the schedule, add resources, change the exit criteria.
- **Metrics:** project progress (task completion, resources, effort), test progress (test cases implemented, executed, passed and failed, test execution time), product quality (availability, response time, mean time to failure), defects (number found, fixed, defect density, defect detection percentage), risk (residual risk level), coverage (requirements, code), and cost.
- **Test progress report:** during the testing. Content: the test period, the progress against the plan, blocking factors, metrics, new and changed risks, the plan for the next period.
- **Test completion report:** at the end. Content: a summary, an evaluation against the test plan and the exit criteria, deviations from the plan, impediments, metrics, residual risks, lessons learned.
- **Communication:** select the form for the audience: verbal discussion, dashboards (for example CI dashboards, burn-down charts), electronic channels (chat, email), online documentation, formal reports. A manager needs a short status and the risks. A developer needs the details of the failures.

### 4.9 Defect management and defect reports (CTFL 5.5)

- **Defect management** is a process: log the anomaly, analyze and classify it, decide the response (fix, keep, or reject), and close it. Each anomaly gets a status: for example new, open, rejected, deferred, fixed, closed.
- An anomaly is not always a defect: it can be a wrong test case, a wrong test environment, wrong test data, or a misunderstanding of the requirements.
- A **defect report** has these objectives: give the developers the information to reproduce, analyze, and fix the defect; track the quality of the product; give ideas to improve the process.
- **Course template** (based on CTFL 5.5):

  | Field | Content |
  |---|---|
  | ID | A unique identifier, for example `DR-007` |
  | Title | A short summary of the failure: what, where, when. Example: "Shipping cost is 2.99 EUR for an order value of exactly 50.00 EUR" |
  | Date, author | |
  | Test object and environment | The SUT version (`/api/health`), the configuration (`SUT_DEFECTS`, browser, OS) |
  | Context | The test case, the test technique, the requirement (for example R5.8) |
  | Steps to reproduce | Numbered steps, with the exact data. Start from a known state (for example "reset the shop"). |
  | Expected result | From the requirement, with the reference |
  | Actual result | What you saw. Exact values. |
  | Evidence | Screenshot, HTTP request and response, log lines with the request ID |
  | Severity | The effect on the system: critical, major, minor, trivial |
  | Priority | The urgency of the fix (a business decision): high, medium, low |
  | Status | New |
  | References | Test case IDs, related defect reports |

- **Severity and priority are different.** A wrong logo on the home page has a low severity and can have a high priority. A crash in a function that nobody uses has a high severity and can have a low priority.
- Write one defect for each report. Write facts, not guesses about the code, and no blame.

### 4.10 Configuration management (CTFL 5.4)

- Configuration management (CM) identifies, controls, and tracks the versions of work products: the test object, the test basis, the testware, and the environment.
- CM makes sure that each test result refers to an exact version of the test object and the testware, and that you can reproduce a test.
- In practice: version control (git) for the code and the testware, tags for the releases, container images with version tags, and a record of the environment in each test report.

### 4.11 Test tools and test automation (CTFL 6.1, 6.2)

- **Types of test tools:** management tools (test management, requirements, defect management), static testing tools, test design and implementation tools (test data generators, model-based tools), test execution and coverage tools, non-functional testing tools (performance, security), DevOps tools (CI/CD pipelines, build tools), collaboration tools, tools for scalability and deployment standardization (virtual machines, containers), and other tools (for example spreadsheets, AI tools).
- **Benefits of test automation:** less repetitive manual work, more consistency, more objective assessment (for example coverage), easier access to information (metrics, reports), shorter test execution times, earlier defect detection, more time for testers to design new tests.
- **Risks of test automation:** unrealistic expectations, wrong estimates of the cost and effort (including maintenance), use of a tool where manual testing is better, too much trust in the tool, dependency on the tool vendor, an open-source project that stops, a tool that does not work with the development platform, a tool that does not meet regulatory or safety requirements.

### 4.12 CTFL exam preparation

- Read the whole syllabus again. Learn the keywords and their glossary definitions.
- Do the official sample exams with the real time limit. Analyze each wrong answer: find the LO and the syllabus section.
- K3 questions (EP, BVA, decision tables, state transitions, estimation, prioritization, defect reports) need practice. Repeat the phase 3 exercises with new examples.
- Read each question to the end. Watch the words "not", "best", and "most likely".
- Ask the mentor for the exam readiness check (`Am I ready for the CTFL exam?`).

## Exercises

Put the documents in `labs/tas/docs/` (main project, stage 1).

### Exercise 4.1: Test plan

Write a test plan of 1–2 pages for the course shop, release 1.0. Include the scope (in and out), the objectives, the test levels and types, the test techniques from phase 3, the entry and exit criteria, the environment, the risks (from exercise 4.4), and the deliverables.

### Exercise 4.2: Estimation

1. Estimate the effort to execute all your test cases of phase 3 manually again, with three-point estimation. Show a, m, b, E, and SD.
2. Record the real time when you do it (or in exercise 4.5). Compare it with your estimate.

### Exercise 4.3: Prioritization

1. You have time for only 15 test cases from phase 3. Select them with risk-based prioritization. Explain the order.
2. Two test cases have a dependency (for example "pay an order" needs "place an order"). Show how the dependency changes the order.

### Exercise 4.4: Risk analysis

1. List at least 8 product risks and 4 project risks for the course shop.
2. For each product risk, estimate the likelihood and the impact (1 to 5). Calculate the risk level. Sort the list.
3. For the top 3 product risks, select the test response: test levels, test types, techniques, and the thoroughness.

### Exercise 4.5: Defect reports

1. Write one defect report for each failure that you found in phase 3. Use the course template (topic 4.9). Put each report in `labs/tas/docs/defects/DR-<nnn>.md`.
2. Give each report to the mentor. The mentor reproduces each report from your steps alone.
3. Explain the severity and the priority of each report.

### Exercise 4.6: Reports

1. Write a test progress report for the middle of your phase 3 work (use real or invented numbers). Write it for a project manager: one page.
2. Write a test completion report for the course shop release 1.0. Include the metrics, the exit criteria evaluation, the residual risks, and a release recommendation.

### Exercise 4.7: Tools and test automation

1. For each tool category of topic 4.11, name one tool that you know or that you find. Name the tools of this course (pytest, Playwright, ruff, mypy, Docker, GitHub Actions) in the correct category.
2. Your manager says: "Let us automate all tests, then we do not need testers." Write an answer with the benefits and the risks of test automation.

### Exercise 4.8: CTFL exam

1. Do all official CTFL sample exams with the time limit. Record each score in `learner/progress.md`.
2. Do the exam readiness check with the mentor.
3. Book and take the exam. Record the result.

## Done criteria

- [ ] I wrote a test plan with entry and exit criteria for the course shop.
- [ ] I can use three-point estimation and the other estimation techniques.
- [ ] I can prioritize test cases by risk, coverage, and requirements, with dependencies.
- [ ] I can explain the test pyramid and the testing quadrants.
- [ ] I can do a product risk analysis and select the test response.
- [ ] I can write test progress and test completion reports for different audiences.
- [ ] My defect reports can be reproduced from their steps alone (main project, stage 1 complete).
- [ ] I can classify test tools and explain the benefits and risks of test automation.
- [ ] My sample exam scores are at least 75 %. (Course recommendation.)
- [ ] I passed the CTFL exam (if this is in my plan).

## Next

[Phase 5: Networking basics](phase-5-networking.md)
