# Phase 11: Beyond

**Time:** Open-ended. Each module takes 1–3 weeks.
**Prerequisites:** Phase 9. Some modules need only phase 6.
**Environment:** The course shop and your TAS. Extra tools for each module.

This phase has independent modules. Select the modules that match your goal. The table names the related ISTQB certificate, if one exists. The course does not prepare for these certificates completely, but the modules give a good start.

| Module | Topic | Related certificate |
|---|---|---|
| 11.1 | Performance testing | CT-PT |
| 11.2 | Security testing basics | CT-SEC |
| 11.3 | Accessibility testing | CT-UT (partly) |
| 11.4 | Contract testing in depth | — |
| 11.5 | Property-based testing and API fuzzing | — |
| 11.6 | SQL and databases for testers | — |
| 11.7 | Observability and resilience | — |
| 11.8 | Mobile test automation | CT-MAT |
| 11.9 | AI in testing | CT-GenAI, CT-AI |
| 11.10 | Next certificates and career | CTAL-TA, CTAL-TTA, CTAL-TM |

**Rule for all modules:** run load tests, security scans, and fuzzing **only against the course shop on your own computer**, or against systems where you have the written permission of the owner. See `AGENTS.md`, "Technical accuracy".

## 11.1 Performance testing

**Goal:** plan, run, and analyze load tests.

- Concepts: load testing, stress testing, spike testing, endurance (soak) testing, scalability testing. Response time percentiles (p50, p95, p99), throughput, error rate, resource usage. Think time, ramp-up, workload model.
- Tools: Locust (Python), k6 (JavaScript), JMeter, Gatling.
- Reading: the ISTQB CT-PT syllabus; the documentation of Locust or k6.

**Exercises:**

1. Write a workload model for the shop: the user types (visitors who search, buyers who order), their share, and their think times.
2. Write a Locust test for the model. Run it against the shop with 10, 50, and 100 users. Record p50, p95, p99, the throughput, and the error rate.
3. Check R7.1 (95 % of API requests in less than 500 ms). Find the load where the shop breaks the requirement.
4. Start the shop with `SUT_LATENCY_MS=300` and repeat. Explain the change in the percentiles.

## 11.2 Security testing basics

**Goal:** find common security defects in a web application and an API.

- Concepts: the OWASP Top 10 and the OWASP API Security Top 10. Authentication, authorization (for example access to the objects of a different user), injection, cross-site scripting (XSS), security misconfiguration, sensitive data exposure, rate limits.
- Tools: OWASP ZAP (baseline scan), your own API tests for authorization rules, a secret scanner, dependency scanners (`pip-audit`).
- Reading: the OWASP Top 10 and the OWASP Web Security Testing Guide (owasp.org); the ISTQB CT-SEC syllabus.

**Exercises:**

1. Write API tests for authorization: user A must not read, pay, or cancel the orders of user B (R6.7). A normal user must not ship (R6.5). A request without a token must fail.
2. Test the login against brute force: what does the lock (R2.3) protect, and what does it not protect? (Think about many user names with one password.)
3. Try XSS in the registration and the search: enter `<script>alert(1)</script>` as a search text. Explain why the page does not run it (template escaping).
4. Run a ZAP baseline scan against `http://127.0.0.1:8000`. Classify each finding: a real risk, a risk only in production, or a false positive.
5. Run `pip-audit` on your TAS and on `sut/requirements.txt`.

## 11.3 Accessibility testing

**Goal:** check a web page against the most important accessibility requirements.

- Concepts: WCAG 2.2 (levels A, AA, AAA), keyboard navigation, focus order, labels, contrast, alternative text, screen readers, ARIA roles.
- Tools: axe-core with Playwright (for example the `axe-playwright-python` package), the browser developer tools, a screen reader (NVDA on Windows, VoiceOver on macOS, Orca on Linux).
- Reading: WCAG 2.2 "Quick Reference" (w3.org); the accessibility pages of MDN.

**Exercises:**

1. Use the shop only with the keyboard: register, log in, search, add to cart, check out. Record each problem.
2. Add an automated axe scan to your UI tests for each page. Report the violations by severity.
3. Explain why role locators (`get_by_role`) in your tests also check a part of the accessibility.

## 11.4 Contract testing in depth

**Goal:** use consumer-driven contract tests between two services.

- Tools: Pact (pact-python), Pact Broker (optional).
- Reading: docs.pact.io, "Introduction", "How Pact works".

**Exercises:**

1. Write a small consumer (for example a Python "order summary" service that reads the cart from the shop). Write a Pact consumer test that generates the contract.
2. Verify the contract against the running shop (provider verification).
3. Change the shop locally (do not commit): rename one field. Show which test fails, and where. Compare with your schema validation and with your phase 8 contract test.

## 11.5 Property-based testing and API fuzzing

**Goal:** generate many test inputs automatically from rules.

- Tools: Hypothesis (property-based testing in Python), Schemathesis (generates API tests from an OpenAPI document).
- Reading: the Hypothesis documentation, "Quick start"; the Schemathesis documentation.

**Exercises:**

1. Use Hypothesis to test your phase 1 `shipping_cost` and `Cart`: write properties (for example "the total is never negative", "adding then removing a book gives the old cart").
2. Run Schemathesis against `http://127.0.0.1:8000/openapi.json` with `SUT_DEFECTS=all`. Which seeded defects does it find without any test design? Which does it not find? Explain why.

## 11.6 SQL and databases for testers

**Goal:** read and check data in a relational database.

- Concepts: tables, primary and foreign keys, `SELECT` with `WHERE`, `JOIN`, `GROUP BY`, `ORDER BY`, aggregate functions, `INSERT`, `UPDATE`, `DELETE`, transactions. Test data setup and checks in the database.
- Tools: SQLite (`sqlite3`), DB Browser for SQLite, a PostgreSQL container.
- Reading: the SQLite documentation, "SQL As Understood By SQLite"; any SQL tutorial for beginners.

**Exercises:**

1. Load the JSON log of the shop into a SQLite table (one row for each request).
2. Answer the questions of phase 0, exercise 0.6 with SQL. Compare with your shell pipeline.
3. Design a database schema for the shop data (users, products, carts, orders). Write SQL queries that check R6.2 and R6.6 (stock changes).

## 11.7 Observability and resilience

**Goal:** use logs, metrics, and traces for testing, and test the behavior of a system under failures.

- Concepts: the three signals (logs, metrics, traces), correlation IDs, OpenTelemetry, service level objectives. Resilience testing and chaos engineering: inject failures, observe the system, and check the recovery.
- Tools: `docker compose` (stop, pause, and disconnect containers), `tc netem` on Linux (add delay and packet loss), OpenTelemetry.

**Exercises:**

1. Make a dashboard of the shop from its logs: requests per minute, error rate, and p95 response time (for example with a script, or with Grafana and Loki in containers).
2. In the test host, add 300 ms delay and 5 % packet loss to the network with `tc qdisc add dev eth0 root netem delay 300ms loss 5%` (needs `sudo` and the `NET_ADMIN` capability for the container: add it in a local copy of `compose.yaml`, do not commit). Run your API tests from the test host. Which tests fail? Are the failures correct, or does your TAS need better timeouts?
3. Stop the shop in the middle of a test run. Check that your TAS reports an environment problem, not many separate SUT failures (phase 8, topic 8.8).

## 11.8 Mobile test automation

**Goal:** understand the differences of mobile test automation.

- Concepts: native, hybrid, and mobile web apps; emulators, simulators, and real devices; device farms; gestures; permissions; network conditions; app stores.
- Tools: Appium, Espresso (Android), XCUITest (iOS), Playwright device emulation for mobile web.
- Reading: the ISTQB CT-MAT syllabus; the Appium documentation.

**Exercises:**

1. Run your UI tests for the shop with Playwright mobile emulation (for example a phone viewport and a touch device). Fix the problems that you find in your page objects.
2. Write a short comparison: which parts of your TAS can you reuse for a native mobile app of the shop, and which parts not?

## 11.9 AI in testing

**Goal:** use AI tools in testing in a responsible way, and know how to test AI-based systems.

- **AI for testing:** generate test ideas, test data, and code drafts; summarize logs; analyze failures; self-healing locators. Risks: wrong or invented results ("hallucinations"), missing context, data privacy (do not send confidential data to external services), over-trust, and licenses of generated code. Always review the output: you remain responsible for the tests.
- **Testing AI-based systems:** non-deterministic results, test oracles for AI, bias, data quality, robustness, explainability.
- Reading: the ISTQB CT-GenAI and CT-AI syllabi.

**Exercises:**

1. Ask an AI assistant to derive boundary value test cases for R5.8 from `REQUIREMENTS.md`. Compare its result with your phase 3 design. List its errors and its useful ideas.
2. Ask an AI assistant to write a page object for the cart page. Review it against the course conventions. Record each change that you made.
3. Write a short policy for your team: when to use AI tools in testing, which data they may receive, and how to review the output.

## 11.10 Next certificates and career

- **CTAL-TA** (Test Analyst): advanced black-box test design, quality characteristics for business domains, defect prevention. Builds on phases 3 and 4.
- **CTAL-TTA** (Technical Test Analyst): white-box techniques, static and dynamic analysis, non-functional technical tests, reviews of code and architecture. Builds on phases 3, 7, and 9.
- **CTAL-TM** (Test Management): test management, risk, people, and process improvement. Builds on phases 4 and 10.
- **Portfolio:** your TAS, your strategy document, and your test design are a strong portfolio. If you make a public copy, remove all personal data first, and do not publish the seeded defect list.
- Read the ISTQB career paths in section 0.3 of the CTAL-TAE and CT-TAS syllabi.

## Done criteria

For each module that you select:

- [ ] I can explain the main concepts of the module.
- [ ] I completed the exercises of the module, and recorded the results in `labs/`.
- [ ] I can explain how the module connects to my TAS and to my test automation strategy.
