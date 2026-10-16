# Phase 2: Testing Fundamentals

**Time:** 2 weeks
**Prerequisites:** None. You can do this phase in parallel with phases 0 and 1.
**Syllabus:** CTFL v4.0.1, chapter 1 (Fundamentals of Testing) and chapter 2 (Testing Throughout the Software Development Lifecycle). LOs FL-1.1.1 to FL-2.3.1. See [../certification.md](../certification.md).
**Environment:** The course shop (optional, for the exercises).

## Goal

At the end of this phase, you can:

- Explain why testing is necessary, what its objectives are, and how testing is different from debugging and from quality assurance.
- Distinguish error, defect, failure, and root cause.
- Explain the seven testing principles with examples.
- Describe the test activities, the testware, traceability, and the roles in testing.
- Explain how the software development lifecycle (SDLC) changes testing, and what test-first approaches, DevOps, and shift left are.
- Distinguish the test levels, the test types, confirmation testing, regression testing, and maintenance testing.

## Reading

| Source | Part |
|---|---|
| CTFL syllabus v4.0.1 | Chapters 1 and 2. Read them completely. |
| ISTQB glossary (glossary.istqb.org) | Look up each keyword of chapters 1 and 2. |
| Kaner, Bach, and Pettichord, *Lessons Learned in Software Testing* | Optional. Short lessons about the role of the tester. |
| Crispin and Gregory, *Agile Testing* | Optional. The chapters about the whole team approach. |

## Topics

### 2.1 What testing is (CTFL 1.1)

- Testing is more than the execution of tests. It includes planning, analysis, design, implementation, execution, and completion. Reviews of documents are also testing (static testing, phase 3).
- Typical test objectives: evaluate work products, cause failures and find defects, get the required coverage, reduce the risk of low quality, verify that requirements are met, check compliance, give information to stakeholders, build confidence, and validate that the system works for the users.
- **Verification** asks: "Did we build the system correctly, against the specification?" **Validation** asks: "Did we build the correct system, for the needs of the users?"
- **Testing and debugging:** testing shows failures (dynamic testing) or finds defects directly (static testing). Debugging finds the cause of a failure, fixes it, and checks the fix. A developer usually debugs. A tester then does confirmation testing.

### 2.2 Why testing is necessary (CTFL 1.2)

- Testing finds defects before the users find them, and it gives information for decisions (for example a release decision).
- **Testing and quality assurance (QA):** testing is a form of **quality control**: it checks the product. Quality assurance is about the **process**: it makes sure that the process prevents defects. Many companies say "QA" when they mean testing. The syllabus does not.
- **Error, defect, failure, root cause:**

  | Term | Meaning | Course shop example |
  |---|---|---|
  | Error (mistake) | A human action that gives a wrong result | A developer reads "50.00 or more" as "more than 50.00". |
  | Defect (fault, bug) | A flaw in a work product (code, document) | The code uses `>` in place of `>=`. |
  | Failure | The system does not do what it must do, when the defect executes | An order of exactly 50.00 EUR is charged shipping. |
  | Root cause | The basic reason for the error | The requirement had no example at the boundary, and nobody reviewed it. |

- A defect does not always cause a failure: the code with the defect must execute with the right data. Failures can also come from the environment (for example radiation or a full disk), not only from defects.

### 2.3 The seven testing principles (CTFL 1.3)

| Principle | Short explanation | What it means for you |
|---|---|---|
| 1. Testing shows the presence, not the absence, of defects | Tests can find defects. They cannot prove that no defects exist. | Never say "the system has no defects". Say "the tests found no failures". |
| 2. Exhaustive testing is impossible | You cannot test all inputs and all combinations. | Use test techniques (phase 3) and risk (phase 4) to select tests. |
| 3. Early testing saves time and money | A defect found early (in the requirements) costs less to fix. | Review requirements. Test as soon as code exists. |
| 4. Defects cluster together | A small number of components contains most defects. | Test more where you found defects before. |
| 5. Tests wear out | The same tests repeated find fewer new defects. | Change and add tests. Use exploratory testing. |
| 6. Testing is context dependent | A medical device and a game need different testing. | There is no single correct test approach. |
| 7. Absence-of-defects fallacy | A system without failures can still be useless for the users. | Validate the user needs, not only the specification. |

### 2.4 Test activities, testware, and traceability (CTFL 1.4)

- **Test activities:** test planning, test monitoring and control, test analysis ("what to test": test conditions), test design ("how to test": test cases), test implementation (test procedures, test data, environment), test execution, and test completion.
- The activities can overlap and repeat. In Agile, they happen in each iteration.
- **Context** changes the process: stakeholders, team skills, business domain, technical factors, project constraints, organization, SDLC, and tools.
- **Testware:** all work products of testing: test plans, risk registers, test conditions, test cases, test data, test procedures, test scripts, test logs, defect reports, test progress reports, test completion reports.
- **Traceability** links the test basis (requirements, user stories) to test conditions, test cases, test results, and defect reports. It shows the coverage, the effect of a change, and the status of each requirement. Example: R5.8 → TC-SHIP-01..06 → results → defect report DR-003.
- **Roles:** the **test management role** owns the test process and the team (planning, monitoring, completion). The **testing role** does the engineering work (analysis, design, implementation, execution). One person can have both roles.

### 2.5 Skills and the team (CTFL 1.5)

- Generic skills: testing knowledge, attention to detail, curiosity, good communication, analytical and critical thinking, technical knowledge, domain knowledge.
- **Communication:** a tester brings "bad news". Report facts, not blame. "The total is 52.98, the requirement says 52.99" is better than "the developer made the calculation wrong again".
- **Whole team approach:** everybody in the team is responsible for quality. Testers work closely with developers and business representatives. They share knowledge and help with test automation and acceptance criteria.
- **Independence of testing:** testers who did not write the code find different defects (different assumptions). Levels: the author tests, a colleague in the team tests, a separate test team tests, an external organization tests. Advantages: different view, can challenge assumptions. Disadvantages: isolation from the team, slower feedback, developers can feel less responsible.

### 2.6 Testing in the SDLC (CTFL 2.1)

- The SDLC model changes the test activities:
  - **Sequential** models (waterfall, V-model): test activities follow phases. Dynamic testing comes late. Static testing (reviews) can start early. The V-model maps each development phase to a test level.
  - **Iterative and incremental** models (Agile, for example Scrum and Kanban): each iteration delivers a working increment. Testing is continuous. Regression testing is very important. Test automation is necessary for fast feedback.
- **Good practices for all models:** each development activity has a test activity. Each test level has its own objectives. Test analysis and design start early. Testers review work products as soon as drafts exist.
- **Test-first approaches:**

  | Approach | Who | What comes first |
  |---|---|---|
  | TDD (test-driven development) | Developers | A failing unit test, then the code |
  | ATDD (acceptance test-driven development) | The team with the business | Acceptance tests from acceptance criteria, then the code (phase 3, topic 3.10) |
  | BDD (behavior-driven development) | The team with the business | Examples of behavior in "Given/When/Then", then the code (phase 7) |

- **DevOps:** development and operations work as one team, with fast feedback, CI/CD pipelines, and automated tests at each stage. Benefits for testing: fast feedback, shift left, automated regression tests, stable test environments. Risks: the pipeline needs investment, and test automation needs maintenance and skills.
- **Shift left:** do testing earlier in the SDLC. Examples: review requirements, write tests before code, run static analysis and unit tests in CI, test non-functional characteristics early.
- **Retrospectives:** the team discusses what went well and what to improve, after an iteration or a release. Testers bring data: defects found late, flaky tests, missing test environments.

### 2.7 Test levels and test types (CTFL 2.2)

- **Test levels:**

  | Level | Test object | Typical test basis | Who |
  |---|---|---|---|
  | Component testing (unit testing) | One component (a class, a function) in isolation | Detailed design, code | Developers |
  | Component integration testing | The interfaces between components | Software design, interface specifications | Developers |
  | System testing | The whole system | Requirements, use cases | Independent testers |
  | System integration testing | The interfaces to other systems and services | Interface specifications, contracts | Testers |
  | Acceptance testing | The system for its users and operations | Business requirements, user stories | Users, business, operations |

  Acceptance testing has forms: user acceptance testing (UAT), operational acceptance testing, contractual and regulatory acceptance testing, alpha testing, and beta testing.
- **Test types:**

  | Type | Question | Course shop example |
  |---|---|---|
  | Functional testing | What does the system do? | Does the cart apply the correct discount? |
  | Non-functional testing | How well does it do it? (performance, security, usability, compatibility, reliability, maintainability, portability) | Does the API answer in less than 500 ms (R7.1)? |
  | Black-box testing | Based on the specification | Test cases from REQUIREMENTS.md |
  | White-box testing | Based on the internal structure | Test cases that cover each branch of the shipping code |

  Each test type can occur at each test level.
- **Confirmation testing** checks that a fix works: run the test that failed again. **Regression testing** checks that a change did not break something else. Regression tests are the best candidates for automation, because they run very often.

### 2.8 Maintenance testing (CTFL 2.3)

- Maintenance testing tests changes to a system in operation: fixes, new features, migrations, and retirement.
- **Triggers:** a modification (fix or enhancement), an upgrade or migration of the environment (for example a new database version, a move to the cloud), and the retirement of a system (data archiving and migration).
- **Impact analysis** finds which parts of the system a change affects, and so which regression tests to run.

## Exercises

Write your answers in `labs/phase-2-fundamentals/notes.md`.

### Exercise 2.1: Error, defect, failure, root cause

For each case, name the error, the defect, the failure, and a possible root cause:

1. A shop charges a member the full price. The developer used the wrong field name for the membership flag.
2. A login page accepts a user name with a space. The requirement does not say anything about spaces.
3. A report shows the dates in the wrong format after a server moved to a different country.

### Exercise 2.2: The seven principles

For each principle, describe one real situation (from your work, or invented for the course shop) where the principle applies.

### Exercise 2.3: Test activities for the course shop

1. Read [../../sut/REQUIREMENTS.md](../../sut/REQUIREMENTS.md).
2. For the requirement group R2 (login), write what you do in each test activity: planning, analysis, design, implementation, execution, completion. Write one or two sentences for each.
3. List the testware that each activity makes.

### Exercise 2.4: Traceability

Make a traceability table for R1 (registration): requirement → test conditions (at least 2 for each requirement). Keep the table: you add test cases in phase 3.

### Exercise 2.5: Test levels and types

Classify each test. Give the test level and the test type:

1. A test checks the function `shipping_cost` with the value 49.99.
2. A test sends `POST /api/orders` and checks the response and the stock.
3. A test measures the response time of `/api/products` with 50 users.
4. A user of the business tries the checkout and says whether it is acceptable.
5. A test checks that the shop sends the order data correctly to an external payment service.
6. A test runs the old tests after a change to the discount code.

### Exercise 2.6: SDLC and shift left

The course shop team works in two-week sprints with a CI pipeline. Describe five shift-left actions for this team. For each action, name the defect type that it finds early.

### Exercise 2.7: Self-check

Do a quiz with the mentor ("Quiz me on phase 2"), or answer the chapter 1 and 2 questions of the official CTFL sample exam. Record the score.

## Done criteria

- [ ] I can explain the test objectives, and the difference between testing and debugging, and between testing and QA.
- [ ] I can distinguish error, defect, failure, and root cause with examples.
- [ ] I can explain the seven principles with examples.
- [ ] I can describe the test activities and their testware, and I made a traceability table.
- [ ] I can explain the roles in testing, the whole team approach, and the independence of testing.
- [ ] I can explain how the SDLC changes testing, and what TDD, ATDD, BDD, DevOps, and shift left are.
- [ ] I can classify tests by test level and test type, and distinguish confirmation and regression testing.
- [ ] I can explain maintenance testing and its triggers.

## Next

[Phase 3: Static testing and test design](phase-3-test-design.md)
