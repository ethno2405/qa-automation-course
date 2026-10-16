# Phase 9: Verify and Improve the TAS, and the CTAL-TAE Exam

**Time:** 3 weeks, plus the exam
**Prerequisites:** Phase 8. The CTFL certificate is required before the CTAL-TAE exam.
**Syllabus:** CTAL-TAE v2.0, chapter 7 (Verifying the Test Automation Solution) and chapter 8 (Continuous Improvement). LOs TAE-7.1.1 to TAE-8.1.4. See [../certification.md](../certification.md).
**Environment:** `labs/tas/` from stage 4, its pipeline, the course shop with different `SUT_DEFECTS` values.

## Goal

At the end of this phase, you can:

- Plan and do the verification of a test automation environment.
- Check that a test suite is complete, repeatable, and not too intrusive.
- Find the cause of unexpected test results, including missing assertions.
- Use static analysis on test code.
- Measure how good your test suite is: defect detection rate, mutation score, flaky rate.
- Find improvement opportunities from data, and recommend technical improvements of a TAS.
- Restructure testware when the SUT changes.
- Pass the CTAL-TAE exam.

## Reading

| Source | Part |
|---|---|
| CTAL-TAE syllabus v2.0 | Chapters 7 and 8. Then read the whole syllabus again before the exam. |
| CTAL-TAE sample exam (istqb.org) | All questions |
| mutmut documentation (mutmut.readthedocs.io) | "Install and run", configuration |
| Martin Fowler, *Refactoring*, 2nd edition | Optional. The catalog of refactorings. |

## Topics

### 9.1 Verify the test automation environment (TAE 7.1.1)

- **Tool installation, setup, configuration:** install the TAS automatically, or from a repository, so that each environment uses the same version and configuration. Your TAS: `uv sync --locked` installs the exact versions from `uv.lock`.
- **Repeatable setup and teardown:** building and rebuilding the TAS gives no difference in its behavior, in any environment. Configuration management and documentation of the components make this possible.
- **Connectivity:** before the tests, check that the TAS can reach the internal and external systems and interfaces: log in to the servers, start the tools, check the access to the SUT, check the configuration, and check the permissions for logs and reports.
- **TAF component testing:** test the components of the TAF like any other software: functional tests, and non-functional tests (performance, resource usage, for example memory leaks). Check that the logs and reports give correct information.

### 9.2 Correct behavior of a test suite (TAE 7.1.2)

- **Composition:** each test case has an expected result, the test data exists, and the versions of the TAF and the SUT are correct.
- **New TAF features:** watch them closely the first time that test cases use them.
- **Repeatability:** the same test gives the same result each time. Move test cases with unreliable results (for example from race conditions) out of the active suite, and analyze them separately (a **quarantine**). Otherwise the team loses time on each run.
- **Intrusiveness:** a TAS that is tightly coupled to the SUT can change the behavior of the SUT (for example its performance). Failures that occur only with the TAS reduce the trust in it. Developers may ask for a manual reproduction.

### 9.3 Unexpected results (TAE 7.1.3)

- When a test fails or passes unexpectedly, do a root cause analysis: test logs, performance data, setup and teardown.
- Run a few tests in isolation. Intermittent failures are the most difficult: the defect can be in the test case, the SUT, the TAF, the hardware, or the network. Monitor the system resources. Ask a developer, an analyst, or a system engineer for help.
- **Check that all assertions are in place.** A test without an assertion (or with a weak one) passes when the SUT is wrong. Its result is inconclusive.
- **False positive:** the test reports a failure, but the SUT is correct. **False negative:** the test passes, but the SUT has a defect. False negatives are more dangerous, because nobody looks at a passed test.

### 9.4 Static analysis of test code (TAE 7.1.4)

- Static analysis finds defects and vulnerabilities in code: the SUT and the TAF. Run it in the pipeline for fast feedback (also in DevSecOps).
- The findings have severities (critical, high, medium, low). Some tools suggest fixes.
- **Test code is code.** Typical problems: a password in plain text in a test script, weak error handling, bad loops, poor library calls. Scan the test code with the same tools as the product code.
- Your TAS: `ruff check` (with the `S` security rules, `C90` complexity, `PT` pytest style), `mypy --strict`, and a secret scanner (for example gitleaks) in the pipeline.

### 9.5 Measure the test suite

These measurements are not all in the syllabus, but they answer the question "How good are my tests?" with data.

| Measurement | Question | Method |
|---|---|---|
| Defect detection rate | Does the suite find real defects? | Inject known defects, and count the defects that the suite detects. The course shop has 10 seeded defects for this. |
| Mutation score | Do the tests of a component check its behavior? | A mutation tool makes small changes (mutants) in the code, for example `<` to `<=`. A good test suite fails for each mutant ("kills" it). Score = killed mutants / all mutants. |
| Flaky rate | Can we trust a failure? | Run the suite N times without changes. Flaky rate = tests with different results / all tests. |
| Duration | Is the feedback fast? | The duration of each suite and the slowest tests (`pytest --durations=10`). |
| Coverage of the test basis | Do we test all requirements? | Requirements traceability: each requirement has automated tests. |

Code coverage of the SUT tells you which code your tests executed, not whether they checked the result. A high coverage with weak assertions has little value. The mutation score and the defect detection rate show the strength of the assertions.

### 9.6 Improvement from data (TAE 8.1.1)

- **Test histogram:** a visual report of the results of each test over many runs. It shows fragile tests to refactor or rethink.
- **AI support:** some tools detect changed locators and repair them ("self-healing"), and report the change. Check each automatic repair: it can hide a real change of the SUT.
- **Schema validation:** replace many single assertions on types and mandatory fields with one schema check. The failure message names the broken part (phase 6, topic 6.5).

### 9.7 Technical improvements of a TAS (TAE 8.1.2)

| Area | Improvement examples |
|---|---|
| Scripting | Move to a better approach (for example data-driven). Remove duplicated steps into library functions, with parameters. A recovery process: the TAS continues after a failure, and recovers the SUT where possible. |
| Waits | Hard-coded waits cause many defects. Polling with a timeout is better. Events from the SUT (with a timeout) are the best, if the SUT offers them. |
| Test execution | Run in parallel or in several environments. Split long suites into parts. Remove duplicated tests. Schedule runs. |
| Verification | One set of standard verification functions for all tests, with parameters. |
| TAA | Changes for better testability of the SUT (for example new test APIs). Expensive late: plan them early. |
| TAF | Update the core libraries with a pilot, an impact analysis, and an adoption plan for all teams. |
| Setup and teardown | Move repeated actions into fixtures. Use API calls for the preconditions of UI tests. |
| Documentation | What the code does and how to use it, the user documentation of the TAS, the test reports and logs. |

### 9.8 Restructure testware for SUT changes (TAE 8.1.3)

- **Consolidate functions** that act on the same control type (for example several functions for lists and fields) into fewer, general functions.
- **Refactor the TAA** when the SUT changes. Do not "bolt on" new features. Analyze them and change the architecture where necessary.
- Keep the **naming conventions** and standards for new code.
- **Evaluate existing test scripts:** split complex, slow tests into smaller ones. Remove tests that run rarely or never, or that have no value.

### 9.9 Other uses of test automation tools (TAE 8.1.4)

- **Environment setup and control:** use test scripts to create test data and users in a new environment, and to clean up afterwards.
- **Data aging:** keep date fields in test data up to date.
- **Screenshots and videos:** UI tools can make material for release documentation or marketing.

### 9.10 CTAL-TAE exam preparation

- Read the whole syllabus again, with the keywords of each chapter.
- K3 and K4 LOs have scenario questions: "Which architecture...", "Which improvement...", "Analyze...". Use your own TAS as the example in your head.
- Do the official sample exam with the time limit. Analyze each wrong answer with its LO.
- Ask the mentor for the exam readiness check: `Am I ready for the CTAL-TAE exam?`.

## Exercises

All work goes in `labs/tas/` (main project, stage 5).

### Exercise 9.1: Environment verification

1. Write a verification checklist for your test environment (topic 9.1): installation, versions, configuration, connectivity, permissions.
2. Automate the checklist as a "preflight" step: a script or a session fixture that runs before the tests and stops with a clear message when a check fails.
3. Run it in three environments: your computer, the CI pipeline, and the test host.

### Exercise 9.2: Test the TAF

1. Write unit tests for your core libraries: configuration loading (missing variables, defaults), the HTTP session with logging, the data factories (unique and valid values), the schema validation helper, and the CSV reader.
2. Measure the branch coverage of `src/shoptest/core/`.

### Exercise 9.3: Repeatability

1. Run the whole suite 10 times against `SUT_DEFECTS=none`, also with `SUT_SLOW_UI=1 SUT_LATENCY_MS=800` (for example `pytest --count=10` with pytest-repeat, or a loop that saves a JUnit file for each run).
2. Write a small script that reads the JUnit files and lists each test with different results. Calculate the flaky rate.
3. For each flaky test, find the root cause and fix it. Write the cause and the fix in `docs/improvements.md`.
4. Add a `quarantine` marker. Explain when you use it, and how you make sure that quarantined tests come back.

### Exercise 9.4: Defect detection rate

1. Write a script that starts the shop with one seeded defect at a time (`SUT_DEFECTS=D01`, then `D02`, ..., `D10`), runs the full suite, and records which tests fail.
2. Make a table: defect → the tests that detected it. Calculate the defect detection rate.
3. For each defect that no test detected: find the requirement, find the missing or weak test case, and add or fix it. Repeat until the rate is 10 of 10.
4. Check: each detected defect must fail with a message that points to the requirement. A test that fails with a 500 error or a timeout "detects" the defect, but it is not a good test case.
5. After this exercise, you can read [../mentor/sut-defects.md](../mentor/sut-defects.md). Compare it with your table.

### Exercise 9.5: Assertions and mutations

1. Search your tests for test functions without an assertion, and for weak assertions (for example `assert response.status_code < 500`, or `assert response.json()`). Fix them.
2. Run mutation testing (mutmut) on `src/shoptest/core/` and on your phase 1 `Cart` code. Read the surviving mutants. For each one, decide: add a test, or accept it (with a reason).
3. Explain the difference between the line coverage and the mutation score of the same code.

### Exercise 9.6: Static analysis of the test code

1. Enable the ruff rule sets `S` (security), `C90` (complexity), `PT` (pytest style), and `B` (likely bugs). Fix or justify each finding.
2. Add a secret scanner to the pipeline. Put a fake password in a test on a branch, and show that the pipeline stops.

### Exercise 9.7: SUT change

Simulate a new version of the shop. **Do not commit these changes to `sut/`.** Restore them at the end with `git restore sut/`.

1. In your working copy, change the shop: rename the `data-testid` of the "Add to cart" button, rename the JSON field `discount_name` to `discount_type` in `app/services.py` and `app/api.py`, and move the coupon field from the cart page to a new section.
2. Run your suites. Count the failures and the files that you must change.
3. Update the TAS. Then evaluate: did the layers and the page objects keep the changes in few places? What would you restructure (topic 9.8)?
4. Restore the shop.

### Exercise 9.8: Improvement report (main project, stage 5)

1. Collect the data: the number of tests by level and suite, the duration, the pass rate and the flaky rate over the last runs, the defect detection rate, the mutation score.
2. Make a test histogram (a table or a chart) of the last 10 runs.
3. Write `docs/improvements.md`: the data, at least 3 technical improvements (topic 9.7) with their expected benefit, and a priority for each.
4. Check the acceptance criteria of stage 5 in [../projects/test-automation-solution.md](../projects/test-automation-solution.md).

### Exercise 9.9: CTAL-TAE exam

1. Do the official CTAL-TAE sample exam with the time limit. Record the score in `learner/progress.md`.
2. Do the exam readiness check with the mentor.
3. Book and take the exam. Record the result.

## Done criteria

- [ ] I can plan the verification of a test automation environment, and my TAS checks its environment before the tests.
- [ ] My core libraries have their own tests.
- [ ] My suite has a flaky rate of 0 % over 10 runs, and I can explain how to handle flaky tests.
- [ ] My suite detects all 10 seeded defects with clear failure messages.
- [ ] I can explain false positives, false negatives, missing assertions, and the mutation score.
- [ ] My test code passes static analysis with security rules and a secret scan.
- [ ] I can restructure testware after an SUT change, and explain what made the change easy or difficult.
- [ ] My improvement report recommends improvements with data (stage 5 complete).
- [ ] I passed the CTAL-TAE exam (if this is in my plan).

## Next

[Phase 10: Test automation strategy, and the CT-TAS exam](phase-10-automation-strategy.md)
