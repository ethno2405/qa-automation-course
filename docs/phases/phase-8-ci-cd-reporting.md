# Phase 8: CI/CD, Environments, and Reporting

**Time:** 3 weeks
**Prerequisites:** Phase 7, phase 5 (SSH), phase 0 (shell scripts)
**Syllabus:** CTAL-TAE v2.0, chapter 5 (Implementation and Deployment Strategies for Test Automation) and chapter 6 (Test Automation Reporting and Metrics). LOs TAE-5.1.1 to TAE-6.1.3. See [../certification.md](../certification.md).
**Environment:** `labs/tas/` from stage 3, Docker, a GitHub account (or a different CI system), the test host of the course shop.

## Goal

At the end of this phase, you can:

- Run your TAS in containers and in a CI pipeline.
- Place automated tests of different test levels in pipelines, and use them as quality gates.
- Manage the configuration of testware: environments, test data, and test suites.
- Explain the dependencies of API test automation, and contract testing.
- Run tests on a remote test host over SSH.
- Collect data from the TAS and the SUT, analyze failures, and separate SUT failures from TAS failures.
- Build and publish test progress reports for different stakeholders.

## Reading

| Source | Part |
|---|---|
| CTAL-TAE syllabus v2.0 | Chapters 5 and 6 |
| Docker documentation (docs.docker.com) | "Get started", "Compose file reference": `healthcheck`, `depends_on` |
| GitHub Actions documentation (docs.github.com/actions) | "Understanding GitHub Actions", "Workflow syntax", "Using secrets", "Storing workflow data as artifacts" |
| Playwright documentation | "Continuous Integration", "Docker" |
| Humble and Farley, *Continuous Delivery* | Optional. The chapters about the deployment pipeline. |
| Pact documentation (docs.pact.io) | Optional. "Introduction" to contract testing. |

## Topics

### 8.1 Containers for test automation

- A container image packs the SUT or the TAS with all dependencies. Each run starts from the same state. This supports repeatable setup and teardown (CTAL-TAE section 7.1.1).
- The course shop already runs in Docker Compose. Its `Dockerfile` has a **health check**. `docker compose up -d --wait` waits until the containers are healthy.
- The TAS can also run in a container. Playwright publishes Docker images with the browsers and their system libraries (see the Playwright "Docker" page for the current image name and tag). Use the same version as the Playwright package in your lock file.
- A TAS container in the Compose network reaches the shop at `http://shop:8000`, not at `localhost` (phase 5, topic 5.11).

### 8.2 CI/CD pipelines

- **Continuous integration (CI):** each change is merged often. A pipeline builds it and runs the tests automatically.
- **Continuous delivery:** each successful change can go to production by a manual decision. **Continuous deployment:** it goes to production automatically.
- **Parts of a pipeline:** a **trigger** (push, pull request, schedule, manual), **jobs** that run on **runners** (machines), **steps** in each job, **artifacts** (files that the pipeline keeps, for example reports), **caches**, and **secrets**.
- **Quality gate:** a check that stops the pipeline when it fails. Examples: a failed test, a linter finding, a coverage below a threshold.

### 8.3 Test levels in pipelines (TAE 5.1.1)

| Test level | Where in the pipeline |
|---|---|
| Configuration tests of the TAS | During the build of the TAS: do the files and paths that the test scripts use exist? |
| Component tests | The build step. A quality gate of the CI pipeline. |
| Component integration tests | With the component tests, in the CI pipeline |
| System integration tests | Quality gates of the continuous delivery pipeline |
| System tests | The last quality gate before the delivery of the SUT, in the continuous deployment pipeline |

Two ways to run system, system integration, and acceptance tests after a deployment:

1. **In the deployment phase**, after the deployment of the components. A failure can stop and roll back the deployment. A rerun of the tests needs a new deployment.
2. **In a separate pipeline**, triggered by the successful deployment. Different test suites can run on each deployment. The tests are not a quality gate: a rollback needs other actions. A few simple deployment checks (smoke tests) confirm that the SUT is deployed.

Pipelines also run **scheduled suites** (for example the nightly regression run, so that the team sees the quality in the morning) and **non-functional tests** (for example performance trends).

### 8.4 Configuration management for testware (TAE 5.1.2)

- **Test environment configuration:** each environment has its own URLs and credentials. Keep the configuration with the testware, or in a core library or shared repository when several TAFs use it. In your TAS: environment variables, `.env` locally, CI variables and secrets in the pipeline.
- **Test data:** it can depend on the environment and on the release. Keep it with the testware for small TAFs, or use a test data management system.
- **Test suites:** group test cases by purpose: smoke, regression, and so on. In pytest, use **markers**: `@pytest.mark.smoke`, then `pytest -m smoke`.
- **Release alignment:** use **feature toggles** in the testware to select the suites for a release or environment, or release the testware with the SUT under the same version (tags or branches). See the topic [Git for testers](../topics/git-for-testers.md) for tags and branching strategies.

### 8.5 API dependencies and contract testing (TAE 5.1.3)

- For API test automation, you need to know the **API connections** (the business logic and the relations between APIs) and the **API documentation** (parameters, headers, request and response types). The OpenAPI document of the shop is such documentation.
- **Contract testing** is a type of integration testing. It verifies that two services can communicate, and that the data that they exchange follows agreed rules. It goes further than schema validation: both sides agree on the permitted interactions, and the contract can change over time in a controlled way.
  - **Consumer-driven:** the consumer writes its expectations. The provider verifies that it meets them.
  - **Provider-driven:** the provider publishes the contract of its service.
- Advantage: defects between services show early, and their source is easy to find. Tools: for example Pact.

### 8.6 Remote execution over SSH

- Tests often run on a dedicated test host or agent: near the SUT, with the correct network access and tools.
- A simple remote run: copy the TAS with `rsync`, run the tests with `ssh`, and copy the reports back.

  ```bash
  rsync -az --delete --exclude .venv --exclude reports labs/tas/ testhost:tas/
  ssh testhost 'cd tas && SHOP_URL=http://shop:8000 ~/.local/bin/uv run pytest tests/api --junitxml=reports/api.xml'
  rsync -az testhost:tas/reports/ labs/tas/reports/remote/
  ```

- The exit code of `ssh` is the exit code of the remote command. Your script can fail when the remote tests fail.
- Verify the environment first (CTAL-TAE section 7.1.1): can the host reach the SUT, are the tools installed, are the permissions correct?

### 8.7 Data collection (TAE 6.1.1)

- **Sources:** the SUT logs (UI, API, application, web server, database), the TAF logs, the build logs, the deployment logs, production monitoring, screenshots and recordings.
- **What the TAS logs:** the test case under execution with its start and end time; the status (passed, failed, or **TAS failure**: the defect is not in the SUT); the important test steps with timing; random values or seeds; enough detail to repeat the test; screenshots and other evidence for failures.
- **What the SUT logs:** time stamps, error messages, and the configuration at startup. Each failure in the test log must be easy to find in the SUT log, and the reverse. A **correlation ID** (or trace ID) in each request makes this easy. The course shop uses `X-Request-ID`.
- **Visualization:** charts and traffic-light icons for the overall status. Managers look at summaries. Technical people drill down into the details.

### 8.8 Analysis of test results (TAE 6.1.2)

For each failed test, do these steps:

1. Did the same failure happen in earlier runs? It can be a known defect in the SUT or the TAS. A history of results helps.
2. If not known: which test case failed, and what does it test?
3. In which test step did it fail? (The TAS logs this.)
4. Compare the state of the SUT with the expected state: screenshots, API and network logs, SUT logs.
5. If the state of the SUT is wrong, write a defect report with the evidence.

If the actual and expected results match but the test failed, the defect is probably in the TAS. If many tests fail at the same time with similar errors, look for an environment outage in the SUT logs.

### 8.9 Test progress reports and dashboards (TAE 6.1.3)

- Test logs give details. A **test progress report** gives the overview: the results, the SUT version and information, and the test environment, in a format for each stakeholder.
- **Stakeholders:** management (trends, pass/fail ratio, reliability of the SUT and the TAS), operational (product owner, business: product use metrics), technical (developers, TAEs, testers: details of failures).
- **Publishing:** a website, a CI page, email, chat messages, or a test management tool. Keep the history for trend analysis.
- **Formats in your TAS:** JUnit XML (`--junitxml`, read by most CI systems), an HTML report (`pytest-html`), or Allure (`allure-pytest`, with history and trends). The GitHub Actions job summary can show a short table.

## Example: a GitHub Actions workflow

GitHub Actions reads workflows only from `.github/workflows/` in the repository root. Your TAS is in `labs/tas/`, so the workflow sets the working directory. Use the current version of each action: check the releases and the tags of each action. Most actions have a tag for the major version (for example `actions/checkout@v7`) that follows the newest release of that version. Some actions publish only full version tags (for example `astral-sh/setup-uv@v10.3.0`): a short tag such as `@v10` then fails with "unable to find version". An old major version can stop working when GitHub removes an old runtime. The workflow uses a fixed runner image (`ubuntu-24.04`), not `ubuntu-latest`: the label `ubuntu-latest` moves to a new Ubuntu version from time to time, and a test environment must not change without a decision.

```yaml
# .github/workflows/tas.yml
name: tas

on:
  push:
    paths: ["labs/tas/**", "sut/**", ".github/workflows/tas.yml"]
  schedule:
    - cron: "0 3 * * *"   # nightly regression run, 03:00 UTC
  workflow_dispatch:

jobs:
  static-analysis:
    runs-on: ubuntu-24.04
    defaults:
      run:
        working-directory: labs/tas
    steps:
      - uses: actions/checkout@v7
      - uses: astral-sh/setup-uv@v10.3.0
      - run: uv sync --locked
      - run: uv run ruff check
      - run: uv run ruff format --check
      - run: uv run mypy --strict src

  tests:
    needs: static-analysis
    runs-on: ubuntu-24.04
    env:
      SHOP_URL: http://127.0.0.1:8000
      ADMIN_PASSWORD: ${{ secrets.SHOP_ADMIN_PASSWORD }}
    steps:
      - uses: actions/checkout@v7
      - uses: astral-sh/setup-uv@v10.3.0
      - name: Start the SUT
        working-directory: sut
        run: SUT_ADMIN_PASSWORD="$ADMIN_PASSWORD" docker compose up -d --build --wait
      - name: Install the TAS
        working-directory: labs/tas
        run: |
          uv sync --locked
          uv run playwright install --with-deps chromium
      - name: API tests
        working-directory: labs/tas
        run: uv run pytest tests/api --junitxml=reports/api.xml
      - name: UI tests
        if: success() || failure()
        working-directory: labs/tas
        run: uv run pytest tests/ui --junitxml=reports/ui.xml --tracing=retain-on-failure --output=reports/playwright
      - name: SUT logs
        if: always()
        working-directory: sut
        run: docker compose logs --no-color > ../labs/tas/reports/sut.log
      - uses: actions/upload-artifact@v7
        if: always()
        with:
          name: test-reports
          path: labs/tas/reports/
```

## Exercises

All work goes in `labs/tas/` (main project, stage 4). The workflow file goes in `.github/workflows/` (see [../../AGENTS.md](../../AGENTS.md), "Track branches").

### Exercise 8.1: Containers

1. Run the shop with `docker compose up -d --wait`. Explain what `--wait` waits for.
2. Run your API tests in a container in the Compose network of the shop (for example the Playwright Python image, with your TAS mounted as a volume). Use `SHOP_URL=http://shop:8000`.
3. Explain each difference between the local run and the container run.

### Exercise 8.2: CI pipeline

1. Push your track branch to your own private remote (see the [main README](../../README.md), "Share your data with git").
2. Add the workflow of this phase, with your changes. Add the repository secret `SHOP_ADMIN_PASSWORD`.
3. Make the pipeline pass. Then break one test on purpose, push, and show that the pipeline fails and keeps the reports.

### Exercise 8.3: Test suites and schedules

1. Add the markers `smoke` and `regression` to your tests. Select 5–8 smoke tests: the most important functions, fast. In feature files, use the tags `@smoke` and `@regression`: pytest-bdd makes markers from them.
2. Change the pipeline: the smoke tests run first, and the full regression suite runs only when the smoke tests pass. The nightly run executes the full suite.
3. Add a configuration test of the TAS (TAE 5.1.1): check that all data files and configuration files that the tests use exist.

### Exercise 8.4: Configuration and secrets

1. List all configuration values of your TAS. For each one, decide: environment variable, secret, constant, or test data file.
2. Make sure that no password is in the repository. Search the history too: `git log -p | grep -i password`.
3. Run ruff with the security rules (`S` rules) on your TAS. Explain each finding.

### Exercise 8.5: Remote run over SSH

1. Install `uv` on the test host (as user `tester`).
2. Write `scripts/run-remote.sh`: copy the TAS to the test host with `rsync`, run the API tests there against `http://shop:8000`, copy the reports back, and exit with the exit code of the tests. Use your SSH configuration from phase 5. The script must pass `shellcheck`.
3. Before the run, the script verifies the environment: the test host answers, the shop answers from the test host, `uv` exists.

### Exercise 8.6: Reports

1. Produce JUnit XML and an HTML report (or Allure). Upload them as artifacts in the pipeline.
2. Add a short Markdown table to the GitHub Actions job summary (`$GITHUB_STEP_SUMMARY`): the number of tests, passed, failed, skipped, and the duration of each suite.
3. Write a one-page test progress report for a manager from the data of the last 5 pipeline runs.

### Exercise 8.7: Failure analysis

1. Make five different failures on purpose, one at a time: a SUT defect (`SUT_DEFECTS=D01`), a wrong locator in a page object, a wrong expected value in the test data, a stopped shop container in the middle of a run, and a wrong `SHOP_URL`.
2. For each failure, follow the steps of topic 8.8 with only the reports and the logs. Classify each one: SUT failure, TAS failure, or environment problem.
3. Improve your logs or reports where the classification was difficult.

### Exercise 8.8: Contract test (small)

1. As a consumer of the shop API (your UI tests and your API client), write the expectations that you depend on for `GET /api/cart`: the fields, their types, and the status codes. Store them as a contract file (JSON).
2. Write a provider verification test that checks the running shop against the contract.
3. Compare this test with the schema validation of phase 6. What can a contract do that a schema check cannot?

### Exercise 8.9: Find a regression with git

Read the sections about `git bisect` and about finding changes in the topic [Git for testers](../topics/git-for-testers.md).

1. Copy the practice script of the topic to `labs/phase-8-ci/make-bisect-practice.sh`, and run it. Do not read the history yet.
2. Run `python3 check.py`. Read the failure.
3. Find the first bad commit with a manual `git bisect`: test each commit with `python3 check.py`, and say `good` or `bad`. Count the steps. Compare the count with log2(20).
4. End the search with `git bisect reset`. Then find the same commit with `git bisect run python3 check.py`.
5. Confirm the result with `git log -S "> 50.00" -- shop.py` and `git show <commit>`.
6. In your own TAS: use `git log -S` to find the commit that added a locator of your choice, and `git blame` on a page object file. Explain what each command shows.
7. Explain how you would bisect a regression of the course shop with one failing test of your TAS, when the tests and the SUT are in the same repository. (Hint: the test must stay the same in each step.)
8. Add a `pull_request` trigger to your workflow. Explain how the pipeline then becomes a quality gate for each pull request, and how a branch protection rule (GitHub also calls it a ruleset) makes a passed pipeline necessary for a merge. Try it in your `git-practice` repository from exercise 0.11, if your GitHub plan permits protection rules for private repositories. Read the GitHub documentation for the current plans.

## Done criteria

- [ ] My TAS runs in a container against the shop in the Compose network.
- [ ] My pipeline runs static analysis, smoke tests, and the regression suite, with quality gates, on push and every night.
- [ ] I can explain where each test level belongs in a pipeline, and the two ways to test after a deployment.
- [ ] My configuration has no secrets in the repository, and different environments need only different variables.
- [ ] I can explain consumer-driven and provider-driven contract testing.
- [ ] My script runs the tests on the test host over SSH, with an environment check first.
- [ ] My pipeline publishes reports, and I can write a test progress report for different stakeholders.
- [ ] I can classify a failure as a SUT failure, a TAS failure, or an environment problem from the reports and logs (stage 4 complete).
- [ ] I can find the commit that caused a regression with `git bisect`, and the history of a line with `git log -S` and `git blame`.

## Next

[Phase 9: Verify and improve the TAS, and the CTAL-TAE exam](phase-9-verify-improve.md)
