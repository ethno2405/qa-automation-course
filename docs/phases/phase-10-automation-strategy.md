# Phase 10: Test Automation Strategy, and the CT-TAS Exam

**Time:** 3 weeks, plus the exam
**Prerequisites:** Phase 9 (recommended), phase 4. The CTFL certificate is required before the CT-TAS exam.
**Syllabus:** CT-TAS v1.0, chapters 1–6. LOs CT-TAS-1.1.1 to CT-TAS-6.2.1. See [../certification.md](../certification.md).
**Environment:** Your TAS and its data from phase 9. A spreadsheet program for the ROI calculation.

## Goal

At the end of this phase, you can:

- Define the objectives of a test automation strategy and judge its chance of success.
- Compare ownership models and licensing models by their cost.
- Select a test automation distribution across test levels for an SUT architecture, with shift left and shift right.
- Fit test automation into sequential, Agile, and DevOps lifecycles.
- Decide which tests to automate, and which tests are difficult to automate.
- Define a deployment strategy for a TAS, with its risks, components, and dependencies.
- Calculate the return on investment (ROI), and select metrics for decisions.
- Plan the transition from manual testing to test automation and to continuous testing.
- Pass the CT-TAS exam.

## Reading

| Source | Part |
|---|---|
| CT-TAS syllabus v1.0 | Chapters 1–6. Read them completely. |
| CT-TAS sample exam (istqb.org) | All questions |
| Mike Cohn, *Succeeding with Agile* | Optional. The chapter about the test automation pyramid. |
| Dorothy Graham and Mark Fewster, *Experiences of Test Automation* | Optional. The case studies about strategy and ROI. |

## Topics

### 10.1 Objectives and success factors (CT-TAS 1.1)

- A test automation strategy defines: the purpose, the risks, the scope, the stakeholders, the tools, the test automation architecture (TAA), and the environments.
- **Typical objectives:** better test efficiency, broader and deeper coverage, better quality of the SUT, lower total cost and shorter time to market, tests that manual testers cannot do, shorter test execution time, more frequent tests.
- **Technical success factors:** the testability of the SUT; a defined, achievable, and current strategy; a clear TAA; and a TAF that is easy to use, documented, and maintainable, with test reporting, easy troubleshooting, a correct test environment, documented and traceable automated test cases, current tests, clear deployment and execution plans, retirement of old tests, and good exception handling.
- Not all factors are necessary, and rarely all are present. Analyze which factors exist and which are missing before you start. A pilot helps.
- **Investment criteria** for a candidate project: the cost of introduction (people, hardware, training), the current phase of the SDLC (earlier gives more value), the planned duration (a short project may not repay the investment), and the maintenance cost. A test architect or test manager owns this decision.

### 10.2 Cost of ownership and licenses (CT-TAS 2.1)

| Ownership model | Advantages | Risks |
|---|---|---|
| In-house solution (on open-source or commercial tools) | All costs, risks, and governance inside the organization. No vendor contract. | Needs the right TAEs (hire or train). |
| Vendor solution | Easy to adopt if a piloted tool already meets the requirements. The vendor trains the testers. | Tool defects and new features need negotiation with the vendor and take time. |
| Outsourcing | No hiring, no hardware or software to buy. | Needs measurable expectations and metrics in the contract. |

| Licensing model | Main characteristic |
|---|---|
| Open-source | No license or maintenance fees. Community support. Can usually be changed. |
| Per user or per machine | Efficient when the number of long-term TAEs is known. Volume discounts. |
| Floating | Shared licenses, counted by concurrent use. |
| Runtime | Pay for execution time, for example on cloud browser grids or device farms. |

- **Strategy factors:** time constraints (the first and most important cost factor), the number and expertise of the TAEs, test hardware, tool licenses, adaptability, maintenance, platform support (web, desktop, mobile), CI/CD support, test management integration and reporting. Cloud resources on demand can reduce cost, but machines that keep running can cost more than own hardware.

### 10.3 Roles and skills (CT-TAS 2.2)

- **TAEs:** strong programming and technical architecture skills, knowledge of SDLCs and of the SUT architecture, and the ability to work with test analysts and other stakeholders. 100 % automation is not possible, so TAEs must help prioritize the most valuable test conditions through risk assessment.
- **At least one strong subject matter expert** (for example a test lead, architect, or business analyst) who knows the business domain and the test objectives, and drives the concept and the roadmap. Team management and soft skills to train and motivate the team.

### 10.4 Test automation distributions (CT-TAS 3.1)

- The **test automation pyramid** (Mike Cohn): unit (ISTQB: component), service, and UI levels. The service level contains component integration tests (with test doubles), contract tests, and API tests.
- Draw the **current state** (how many tests at each level, manual or automated) and the **target state**.

  | Distribution | Shape | Effect |
  |---|---|---|
  | Pyramid | Many component tests, fewer service tests, few UI tests | Balanced, fast, stable. Often the target. |
  | Ice cream cone | Inverted pyramid: most tests at the UI level | Costly, defects found late (few component tests) |
  | Hourglass | Many tests at the top and the bottom, few service tests | Integration defects. Move UI tests to the API level where the business logic has APIs. |
  | Umbrella | Almost only UI tests | Slow feedback, high maintenance. If lower tests are not possible, optimize the UI suite. |

- **The SUT architecture** changes the realistic target. Microservices permit API and contract tests. Mainframes (terminal emulation, batch jobs) often permit only tests through batch jobs, databases, and the GUI. A realistic step (for example from umbrella to hourglass) is better than an impossible target.
- **Shift left:** start bottom-up. Low code coverage shows missing component tests. Then improve their quality (TDD, workshops on test techniques). Component tests for UI and API code with test doubles. Contract tests find defects in underlying services early. An API call graph shows the consumers and producers of each API.
- **Shift right:** testing after the release, in preproduction or production, with monitoring and real user feedback. Goals: understand user preferences, support canary releases and dark launches, find production defects early, expand the scope of automation, increase coverage. Test automation with observability helps to decide quickly between a full release and a rollback.

### 10.5 Test automation in different lifecycles (CT-TAS 3.2)

| Lifecycle | Test automation |
|---|---|
| Waterfall | The test phase comes late, so automation starts late. Long cycles give few runs and late feedback: lower ROI. |
| V-model | Test design starts early, but the TAS implementation still comes late. Better ROI than waterfall, lower than Agile. |
| Agile | Goal: **in-sprint test automation**. The automation tasks are part of the exit criteria of each user story. An immature team first reaches in-sprint testing, with automation one sprint behind. |
| DevOps | End-to-end delivery with automated build, integration, test, and deployment. **Continuous testing** through feedback loops. Focus on lower-level tests (component, component integration, contract) without real data and services. Different suites run at each stage (local, pull request, merge, deployment). Manual effort goes to exploratory testing and user feedback. |

### 10.6 Which tests to automate (CT-TAS 3.3)

- **Suitability criteria:** technically possible; the team can do it; adequate ROI; value of frequent runs; the test type and suite (smoke, regression, confirmation); repeatable; easy to maintain when the SUT changes; covers frequent business workflows; reuse of steps and data with other tests.
- **Only test automation can:** run tests that take too long manually; synchronize test execution; give results inside a pipeline; parse large log files for defects; give precise timing; run permutations across many operating systems, browsers, devices, locations, or configurations; run a large volume of executions or data; do non-functional tests that need automated monitoring or very many users (stress, reliability).
- **Difficult to automate:** subjective look and feel across platforms; processes with much human decision (for example a loan application that agents check); technical restrictions (for example OS-level messages outside the SUT); long time dependencies that cannot be shortened (for example a two-hour session timeout without a way to change the time).

### 10.7 Planning and deployment (CT-TAS 4.1, 4.2)

- **Time to market:** test automation shortens the test cycle, especially for regression testing. **Quality gates** based on automated tests speed up the deployment, because defects are found earlier. Parallel execution and shift left reduce the time further.
- **Confirmation tests:** defects can come back in later releases. An automated confirmation test has a narrow scope. Add it to the regression suite. Run it on many platforms at low cost.
- **Operationally relevant scenarios** (for operational acceptance testing): static code analysis, end-to-end tests, failover tests, backup and restore tests, performance tests, review of the operational documentation, security tests, and monitoring of service level agreements in production with reused automated tests.
- **Deployment strategy:** the test environments (the same scripts run in each environment with only a changed URL), the tools (for example access to a license server in each environment), access to the SUT (parameters for users and credentials), test script storage (a repository with configuration management), and data provisioning (avoid static data; preload it, or create it with setup scripts, each with advantages and disadvantages).
- **Risks:** technical (too many abstractions, test data tables that are too large to migrate, dependencies on OS libraries that are not in all environments), project (staffing, unplanned maintenance after SUT updates, delays, nonstandard UI objects, outdated test cases), and failure points (migration to a different environment, deployment to production, forgetting that the automation is software that needs tests).
- **Mitigation:** the TAS has its own SDLC, configuration management, and documented features. A documented, versioned deployment procedure. For the **first deployment**: plan enough execution time, and use test fixtures for the preconditions. For a **maintenance deployment**: test the new TAS version before you use it (new functions, the suite runs, reports are sent, no performance problems).

### 10.8 Environment components and dependencies (CT-TAS 4.3)

- **Components:** the SUT (whole or in parts: API, web interface, database), the platform (cloud, network, virtual machines, containers), test cases and test suites, tools, and the TAF (driver scripts, libraries, templates, data provisioning scripts, documentation, tutorials). Do not make the environment too complex: you then fix the TAF more than you test.
- **Infrastructure dependencies:** host machines, the network, the platform, software dependencies (for example a language version), and the access to the SUT (for example the browser type and version).
- **Data and interfaces:** API (the order of calls and the correlation of data in a business process), database interface (check data, stored procedures), interface compatibility (contract testing: consumer-driven, provider-driven, bidirectional).

### 10.9 Return on investment (CT-TAS 5.1)

- **ROI = Savings / Investment.** The syllabus uses time units. Convert costs to time with a rate, or times to costs with labor rates.
- **Savings** come from tests that run in much less time than manually: the time of a manual run, the time of an automated run, the number of test cases, and the number of test runs.
- **Investment:** the setup time, the average development time of a script, the number of scripts, the average maintenance time, the execution time, the percentage of failed scripts (they need analysis), the number of test cases, and the number of test runs.
- **Example (a course model, with assumptions):**

  | Assumption | Value |
  |---|---|
  | Test cases (N) | 200 |
  | Manual execution time for each test case | 10 minutes |
  | Automated execution and result check for each test case | 1 minute |
  | Setup of the TAS | 80 hours |
  | Development time for each script | 1 hour |
  | Maintenance and failure analysis for each run | 4 hours |

  After k runs: Savings = k × 200 × (10 − 1) min = 30 k hours. Investment = 80 + 200 × 1 + 4 k = 280 + 4 k hours.
  ROI ≥ 1 when 30 k ≥ 280 + 4 k, so k ≥ 10.8. The investment returns after **11 regression runs**. With one regression run in each two-week sprint, this is about 22 weeks.
- **Rules:** if the project ends before the break-even point, manual testing is cheaper. The investment depends much on the execution time: tests at the correct level of the pyramid improve the ROI. Count only the runs that would also happen manually as savings. Extra runs (for example nightly) give faster feedback, which is a benefit that this simple model does not show.

### 10.10 Metrics and decisions (CT-TAS 5.2, 5.4)

- Metrics show whether the TAS suits the project, whether it adapts to new test conditions, and how maintainable it is. Collect them automatically.

  | Metric | Meaning |
  |---|---|
  | Pass-fail ratio | Tests passed / tests failed |
  | Ratio of failures to defects | How many automated tests fail for one defect. Many failures for one defect show a design problem in the tests. Also track the reason: sub-system, whole system, test data, infrastructure. |
  | Execution time | Including the build of the TAS. Important when the suite grows. |
  | Number of automated test cases | Shows progress, but not coverage |
  | Functional coverage | Requirements covered by automated tests |
  | Code coverage | Code executed by the component tests |

- **Decisions from reports:** find trends and root causes, move effort to maintenance or to TAF improvements, add TAS capabilities, increase shift left and shift right, expand functional coverage, focus on defect clusters, advise developers and the SDLC process, and change the reports themselves.

### 10.11 Organization and project (CT-TAS 5.3)

- **Organization:** the development policies and practices, existing test automation projects (reuse before you build), the subject matter experts, the availability of test environments (do not disturb other teams), and existing tools and licenses (use them to reduce cost).
- **Project characteristics:** the domain (regulations, standards), the platforms, the programming language and technology stack (prefer the language of the developers), the maturity (number of test cases, pipelines, testers; a greenfield project gets an incremental, minimum-viable-product roadmap), stakeholder buy-in (show risks, benefits, milestones, testability needs), team knowledge (a competency and skill matrix), test management support and budget, and the quality characteristics of ISO/IEC 25010.

### 10.12 Transitions (CT-TAS 6.1, 6.2)

- **From manual testing to test automation:** start with regression testing. Expect higher costs during the transition, because manual and automated testing run at the same time. Then move manual effort to exploratory testing. Watch: functional overlap (make reusable components, for example a login flow), data sharing (one source for shared test data), test interdependency (for example an order ID that later tests need), test execution preconditions (analyze them first, and automate their creation), functional coverage (automated manual tests are not all possible tests), and executable tests (fix a manual test before you automate it).
- **From test automation to continuous testing:** run the suites right after each change. Update the test suites, the stubs and drivers, and the infrastructure for the new TAS. Analyze the risks and benefits of TAS defects. Write release notes with the known defects. Extend the pipeline with tests right after the deployment.
- **Evaluation of assets and practices:** track the hours to develop the TAS, the hours to fix it, and the time saved. **Warning sign:** the TAS maintenance time is greater than the manual testing time. For a first deployment: code coverage, a requirements traceability matrix, a consistent infrastructure, a configuration management strategy, development guidelines, and automated preconditions. For updates: evaluate new tools, optimize, modularize, share reusable components, collect evidence, remove functional overlap, automate more manual tests, improve test design and test data, and keep all suites on the latest TAS version.

### 10.13 CT-TAS exam preparation

- Read the whole syllabus again. Many questions are about decisions in a scenario: "Which approach is best for this organization?"
- Practice the K3 LOs: the ROI calculation (CT-TAS-5.1.1), shift left and shift right (CT-TAS-3.1.3), DevOps preparation (CT-TAS-3.2.3), organizational and project analysis (CT-TAS-5.3.1, 5.3.2), and the evaluation of assets (CT-TAS-6.2.1).
- Do the official sample exam with the time limit. Ask the mentor for the exam readiness check.

## Exercises

All documents go in `labs/tas/docs/` (main project, stage 6). The fictional company for the exercises: **BookBridge Ltd.** sells the course shop as a product to 30 small bookstores. It has 12 developers in 2 Scrum teams, 3 manual testers, 1 TAE (you), a release every 6 weeks, a manual regression test of 600 test cases that takes 5 tester-days, and about 40 % of the customer defect reports are regressions.

### Exercise 10.1: Objectives and success factors

1. Write 5 measurable objectives of test automation for BookBridge.
2. Make a table of the technical success factors (topic 10.1). For each factor, write whether it exists, is partly present, or is missing at BookBridge (use the course shop and your TAS as the facts). Name the 3 most important gaps.

### Exercise 10.2: Ownership and licenses

Compare three options for BookBridge: (a) extend your open-source TAS in-house, (b) buy a commercial low-code tool with per-user licenses, (c) outsource the automation. Use the factors of topic 10.2, with estimated costs for 2 years. Recommend one option with reasons.

### Exercise 10.3: Distribution and shift left or right

1. Count the tests of your TAS by level (component, API, UI). Draw the distribution.
2. BookBridge has 600 manual UI regression test cases, 150 developer unit tests, and no API tests. Name the shape. Define a realistic target state for 6 months and for 18 months.
3. Write a roadmap with 6–8 backlog items for the shift left, and 2–3 items for the shift right (with the course shop health endpoint and logs as the monitoring base).

### Exercise 10.4: Suitability

Take 15 test cases from your phase 3 test design. For each one, apply the criteria of topic 10.6, and decide: automate at the API level, automate at the UI level, keep manual, or remove. Name two test conditions of the shop that only automation can test, and two that are difficult to automate.

### Exercise 10.5: ROI

1. Use your own data from phase 9: the number of tests, the execution time, the hours that you spent to build and maintain the TAS, and the failure analysis time. Estimate the manual execution time of the same tests.
2. Build the ROI model of topic 10.9 in a spreadsheet. Find the break-even run. Show a chart of savings and investment over the runs.
3. Do the same for BookBridge with its numbers. Change one assumption at a time (maintenance time, number of runs) and show how the break-even point moves.

### Exercise 10.6: Test automation strategy (main project, stage 6)

Write `labs/tas/docs/automation-strategy.md` for BookBridge (4–8 pages). Cover:

1. Purpose, objectives, scope, and stakeholders (CT-TAS chapter 1)
2. Resources: ownership, licenses, roles, skills, and a skill matrix (chapter 2)
3. The target distribution, the approach for the SUT architecture, shift left and shift right, the lifecycle fit, and the selection criteria for automation (chapter 3)
4. The deployment strategy, the environments and components, the risks and their mitigations (chapter 4)
5. The ROI, the metrics, and the reports for each stakeholder group (chapter 5)
6. The transition plan from manual testing to continuous testing, and the evaluation process (chapter 6)

Use the data from your TAS where possible. Ask the mentor for a review.

### Exercise 10.7: Decisions from a report

The mentor (or you) invents a test automation report for BookBridge after 3 months: the pass-fail ratio, the failures for each defect, the execution time trend, the functional coverage, and the maintenance hours. Analyze it, and write 5 decisions with their reasons for the management.

### Exercise 10.8: CT-TAS exam

1. Do the official CT-TAS sample exam with the time limit. Record the score in `learner/progress.md`.
2. Do the exam readiness check with the mentor.
3. Book and take the exam. Record the result.

## Done criteria

- [ ] I can define the objectives of a test automation strategy and judge its success factors and investment criteria.
- [ ] I can compare ownership and licensing models by cost and risk.
- [ ] I can name a test distribution, define a realistic target, and plan shift left and shift right.
- [ ] I can explain test automation in waterfall, V-model, Agile (in-sprint), and DevOps (continuous testing).
- [ ] I can decide which tests to automate, and name tests that only automation can do and tests that are difficult to automate.
- [ ] I can define a deployment strategy with its risks, mitigations, components, and dependencies.
- [ ] I can calculate the ROI and the break-even point, and select metrics for decisions.
- [ ] I can plan the transition from manual testing to continuous testing.
- [ ] My test automation strategy for BookBridge is complete (stage 6).
- [ ] I passed the CT-TAS exam (if this is in my plan).

## Next

[Phase 11: Beyond](phase-11-beyond.md)
