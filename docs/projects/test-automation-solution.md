# Project: Test Automation Solution for the Course Shop

The test automation solution (TAS) is the main project of the course. It starts as a small project with one test in phase 1. It ends as a layered, measured test automation solution with a CI pipeline and a strategy in phase 10. Each stage adds features to the work from the previous stage. Do not start again from zero.

The CTAL-TAE syllabus uses the terms test automation solution (TAS), test automation framework (TAF), and test automation architecture (TAA). This project uses the same terms.

## Final system

```
                   labs/tas/
 ┌──────────────────────────────────────────────────────────┐
 │ Test scripts        tests/api  tests/ui  tests/features  │  ◄── test data (tests/data/*.csv)
 │        │                                                 │
 │        ▼                                                 │
 │ Business logic      src/shoptest/api   (API clients)     │
 │                     src/shoptest/ui    (page objects,    │
 │                                         flows)           │
 │        │                                                 │
 │        ▼                                                 │
 │ Core libraries      src/shoptest/core  (configuration,   │
 │                     HTTP session, logging, test data     │
 │                     factories, waits)                    │
 └────────┬─────────────────────────────────┬───────────────┘
          │ HTTP (API)                      │ Browser (Playwright)
          ▼                                 ▼
     Course shop (sut/, Docker)  ◄──────────┘
          ▲
          │ SSH: run the suite on the test host (stage 4)
     CI pipeline (GitHub Actions): lint, type check, API tests, UI tests, reports
```

## Directory layout (Python reference)

```
labs/tas/
  README.md               How to install, start the SUT, and run the tests
  pyproject.toml          Project, dependencies, pytest, ruff, and mypy settings
  uv.lock
  .env.example            Example configuration (no real passwords)
  src/shoptest/
    core/                 SUT-independent: config, HTTP session, logging, data factories
    api/                  SUT-dependent: API clients for users, catalog, cart, orders
    ui/                   SUT-dependent: page objects and flows
  tests/
    conftest.py           Fixtures
    api/                  API test scripts
    ui/                   UI test scripts
    features/             BDD feature files (stage 3)
    data/                 Data files for data-driven tests (stage 3)
  scripts/                Shell scripts: start the SUT, wait for health, run on the test host
  docs/                   Test plan, test design, defect reports, strategy
```

For a different language, use the conventional layout of the language. Keep the three layers.

## Stage 0: Skeleton (phases 0–1)

**Features**

- A project in `labs/tas/` with a `pyproject.toml`, pytest, ruff, and mypy.
- A Bash script `scripts/start-sut.sh` that starts the SUT and waits until `/api/health` answers, with a timeout (phase 0, exercise 0.9).
- One test that calls `/api/health` and checks the status.
- A `README.md` with the commands.

**Acceptance criteria**

- [ ] `uv run pytest` passes on a fresh clone after the steps in the README.
- [ ] `uv run ruff check` and `uv run mypy src` report no problems.
- [ ] `scripts/start-sut.sh` exits with an error message if the SUT does not answer within 60 seconds.

## Stage 1: Test design (phases 3–4)

**Features**

- `docs/test-design.md`: test conditions and test cases for R1–R6 with the techniques of phase 3. Each test case has an ID, the requirement, the technique, the preconditions, the steps, and the expected result.
- `docs/defects/`: one defect report for each failure that you found (phase 4, topic 4.9).
- `docs/test-plan.md`: a short test plan for the shop (phase 4).
- A traceability table: requirement → test conditions → test cases → defect reports.

**Acceptance criteria**

- [ ] Each requirement R1–R6 has at least one test condition.
- [ ] The test cases for R1.2, R1.6, R4.2, and R5.8 use boundary value analysis. R5.6 uses a decision table. R6.5 and R2.3–R2.6 use state transition testing.
- [ ] Each defect report can be reproduced from its steps alone.

## Stage 2: API and UI suites (phase 6)

**Features**

- API tests for registration, login, catalog, cart, prices, and orders, from the test cases of stage 1.
- Schema validation of the API responses against the OpenAPI document.
- UI tests for login, search, add to cart, remove from cart, and checkout, with page objects.
- Fixtures that make test users and test data through the API, and reset the SUT.
- Configuration from environment variables (`SHOP_URL`, `ADMIN_PASSWORD`).
- Component tests of the API client with HTTP mocks (`responses`).
- UI tests for the error states of R4.8 with network interception.
- Tests for the order events (R9) over the WebSocket, and for the API client access with OAuth 2.0 (R8), with a token provider.
- A smoke subset of UI tests that runs on Chromium, Firefox, and WebKit. Visual tests for three pages.

**Acceptance criteria**

- [ ] All tests pass against `SUT_DEFECTS=none`.
- [ ] The tests pass in random order (pytest-randomly) and in parallel (`pytest -n 4`).
- [ ] No test uses `time.sleep()`. No test passes against `SUT_SLOW_UI=1` only by luck: run the UI suite 5 times with `SUT_SLOW_UI=1` and `SUT_LATENCY_MS=800`, with no failure.
- [ ] Against `SUT_DEFECTS=all`, at least 6 test cases fail, each with a clear message.
- [ ] No test waits for an order status by polling: the tests use the order events.
- [ ] No token, secret, or password appears in the test code, the logs, or the reports.

## Stage 3: Framework (phase 7)

**Features**

- Three layers: test scripts, business logic, core libraries (CTAL-TAE section 3.1.3). Test scripts do not call the core libraries directly.
- Design patterns: page object, flow model (a facade over the page objects), and a facade over the API clients.
- Data-driven tests: the boundary value test cases of stage 1 come from a CSV file.
- BDD: at least 5 scenarios in Gherkin for the price rules (R5), with pytest-bdd.
- Logging: each test logs its steps and the HTTP requests with the `X-Request-ID`. A failed UI test saves a screenshot and a Playwright trace.
- A short architecture document `docs/architecture.md` with a diagram of the layers.

**Acceptance criteria**

- [ ] A change of one locator needs a change in one file only.
- [ ] A new boundary value test case needs only a new line in a CSV file.
- [ ] From a failed test, you can find the log line of the SUT with the request ID.

## Stage 4: Pipeline (phase 8)

**Features**

- A GitHub Actions workflow: lint and type check, start the SUT with Docker Compose, API tests, UI tests, publish JUnit XML and an HTML or Allure report as artifacts.
- Quality gate: the pipeline fails when a test fails, or when ruff or mypy reports a problem.
- A script `scripts/run-remote.sh` that copies the TAS to the test host with `rsync` over SSH, runs the API tests there against `http://shop:8000`, and copies the report back.
- Secrets (the admin password) come from the secret store of the CI system.

**Acceptance criteria**

- [ ] A push to the branch starts the pipeline. A failed test makes the pipeline fail.
- [ ] The pipeline report shows the test results without a download of files.
- [ ] `scripts/run-remote.sh` works with SSH key authentication. No password is in the repository.

## Stage 5: Verified and measured (phase 9)

**Features**

- Metrics: number of tests by level, duration, pass rate, flaky rate over 10 runs, defect detection rate.
- Flaky test detection: run the suite 10 times (`pytest --count=10` or a loop), and list the tests with different results.
- Defect detection rate: run the suite against each seeded defect alone, and record which defects the suite detects.
- Mutation testing of the core libraries with mutmut.
- A verification checklist for the test environment.
- An improvement report `docs/improvements.md` with the results and the next steps.

**Acceptance criteria**

- [ ] The suite detects all 10 seeded defects.
- [ ] The flaky rate over 10 runs is 0 %.
- [ ] The improvement report gives at least 3 improvements with data.

## Stage 6: Strategy (phase 10)

**Features**

- `docs/automation-strategy.md`: a test automation strategy for a fictional company that sells the course shop as a product (phase 10, exercise 10.6).
- A business case with an ROI calculation.
- A roadmap for the move from manual testing to continuous testing.

**Acceptance criteria**

- [ ] The strategy covers the topics of CT-TAS chapters 1–6.
- [ ] The ROI calculation shows all assumptions and the break-even point.
- [ ] The strategy uses data from your own TAS (stage 5) where possible.
