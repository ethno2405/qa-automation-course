# Phase 7: Test Automation Architecture

**Time:** 4 weeks
**Prerequisites:** Phase 6. The CTFL certificate is required before the CTAL-TAE exam.
**Syllabus:** CTAL-TAE v2.0, chapter 1 (Introduction and Objectives for Test Automation), chapter 2 (Preparing for Test Automation), chapter 3 (Test Automation Architecture), and chapter 4 (Implementing Test Automation). LOs TAE-1.1.1 to TAE-4.3.1. See [../certification.md](../certification.md).
**Environment:** `labs/tas/` from stage 2, the course shop.

## Goal

At the end of this phase, you can:

- Explain the advantages, disadvantages, and limits of test automation, and how it fits different SDLC models.
- Analyze an SUT, select tools for it, and present the findings of a tool evaluation.
- Explain testability, and the test environments where test automation runs.
- Explain the generic test automation architecture (gTAA) and its capabilities.
- Design a test automation solution, and structure a test automation framework in layers.
- Apply the approaches to automate test cases: structured scripting, data-driven, keyword-driven, BDD.
- Apply the OOP and SOLID principles and the design patterns of the syllabus: facade, singleton, page object, flow model.
- Plan a pilot, analyze the deployment risks, and keep a TAS maintainable.

## Reading

| Source | Part |
|---|---|
| CTAL-TAE syllabus v2.0 | Chapters 1–4. Read them completely. |
| Robert C. Martin, *Clean Code* | The chapters about names, functions, and comments. The syllabus refers to this book in section 4.3. |
| Dorothy Graham and Mark Fewster, *Experiences of Test Automation* | Optional. Case studies from real projects. |
| pytest-bdd documentation (pytest-bdd.readthedocs.io) | "Quick start", scenarios, step arguments |
| Python `logging` HOWTO (docs.python.org) | The basic and the advanced tutorial |

## Topics

### 7.1 Purpose of test automation (TAE 1.1)

- Test automation uses tools to set up and control test execution, to execute tests, and to compare actual results with expected results.
- **Advantages:** more tests in each build, tests that a human cannot execute (real-time responses, remote or parallel testing), more complex tests, faster execution, fewer human errors, better use of test resources, faster feedback, better reliability checks, and the same execution in each test cycle.
- **Disadvantages:** extra cost (people, hardware, training), an initial investment, the time to develop and maintain the TAS, the need for clear objectives, rigid tests that do not adapt well when the SUT changes, and new defects in the test code itself.
- **Limits:** not all manual tests can be automated. An automated test checks only what it is programmed to check. It can check only results that a machine can interpret, with an automated test oracle.

### 7.2 Test automation in the SDLC (TAE 1.2.1)

| SDLC model | Test automation |
|---|---|
| Waterfall | The TAS is built in parallel with or after the implementation. Tests run mainly in the verification phase. |
| V-model | Each test level can have its own TAF: component, integration, system, acceptance. |
| Agile | The team decides together. Code reviews, pair programming, and frequent automated runs. The goal is **in-sprint automation**: the tests for a story are automated in the same sprint. |

### 7.3 Tool selection for an SUT (TAE 1.2.2)

- First analyze the SUT and the project requirements. UI software and web services need different tool features.
- Consider the cost: a commercial tool or an open-source solution with custom code.
- Consider the team: testers without programming skills can use low-code or no-code tools. Technical testers gain when the test language matches the SUT language: they can debug with the developers and share knowledge.

### 7.4 Testability and test environments (TAE 2.1)

- **Testability** is a non-functional requirement of the SUT. The architect designs it, often with the TAE. Aspects:
  - **Observability:** the SUT shows what happens inside, so that tests can compare actual and expected results.
  - **Controllability:** the SUT has interfaces to control it: UI elements, function calls, protocols, switches.
  - **Architecture transparency:** the documentation shows the components and interfaces clearly.
- **Course shop example:** `data-testid` attributes (accessibility and test identifiers), environment variables (`SUT_LOCK_MINUTES`, `SUT_TEST_MODE`), the reset endpoint (controllability), JSON logs with request IDs, and the OpenAPI document (observability and transparency).
- **Environments:**

  | Environment | Typical automated tests |
  |---|---|
  | Local development | Component tests, white-box checks in the IDE, some GUI and API tests |
  | Build (CI agent) | Component and component integration tests, static analysis. No deployment. |
  | Integration | A release candidate with its real neighbors. Full black-box API and UI suites. Monitoring starts here. |
  | Preproduction | Close to production. Non-functional tests (for example performance), user acceptance testing. |
  | Production | Monitoring, and testing in production practices: canary release, blue/green deployment, A/B testing. |

### 7.5 Analyze the SUT and evaluate tools (TAE 2.2)

- **Requirements for the TAS** (with the stakeholders): which test activities to automate, which test levels and types, which roles and skills, which products and their lifetime, which SUT technologies, the test data (availability and quality), and how to emulate parts that you cannot reach (for example third-party systems, with test doubles).
- **Tool evaluation:** make a **comparison table**: tools in the columns, requirements in the rows, with the properties and priorities in the cells. Requirements: language and IDE, configuration (environments, run settings), test data management, test types, reports, integration with CI/CD and other tools, scalability, maintainability, compatibility, and reliability.
- One tool rarely meets all requirements. Present the proposal to the stakeholders for approval.

### 7.6 The generic test automation architecture (TAE 3.1.1)

```
     Project management     Test management     Configuration management
            ▲                      ▲                      ▲
            │ progress             │ test case mapping    │ pipelines, environments, testware
 ┌──────────┴──────────────────────┴──────────────────────┴────────┐
 │                       Test automation solution                   │
 │  Test generation (optional): test cases from a model            │
 │  Test definition: test cases, test data, test libraries          │
 │  Test execution: run the tests, test logs, test reports         │
 │  Test adaptation: adaptors for the SUT interfaces (API, GUI, ...)│
 └──────────────────────────────┬──────────────────────────────────┘
                                │ SUT interface
                                ▼
                       System under test
```

- The **gTAA** is an abstract design. It shows the interfaces of a TAS to the SUT, project management, test management, and configuration management, and the capabilities that a TAA must cover.
- **Capabilities:** test generation (optional, for example with model-based testing), test definition (high-level and low-level tests, separate from the SUT and the tools), test execution (run, log, report), and test adaptation (adaptors for the APIs, protocols, and services of the SUT).
- **Your TAS:** pytest is the test execution capability. Your test files and data files are the test definition. `ShopApi` and the page objects are the test adaptation.

### 7.7 Design a TAS (TAE 3.1.2)

The test automation architecture (TAA) is the technical design of the TAS. It covers: the selection of tools and libraries, plugins and components to develop, the connectivity requirements (firewalls, databases, URLs, mocks and stubs, message queues, protocols), the connection to test management and defect management tools, and version control.

### 7.8 Layers of a TAF (TAE 3.1.3)

The test automation framework (TAF) is the base of the TAS: the test harness (test runner), test libraries, test scripts, and test suites. The syllabus describes three layers. Keep the number of layers low.

| Layer | Content | In your TAS |
|---|---|---|
| Test scripts | The test cases and test suites. They call the business logic layer. **No direct calls to the core libraries.** | `tests/` |
| Business logic | The libraries that depend on the SUT: test steps, user flows, API calls. They use or extend the core libraries. | `src/shoptest/api/`, `src/shoptest/ui/` |
| Core libraries | The libraries that do not depend on the SUT. They can be used in other projects with the same technology. | `src/shoptest/core/`: configuration, HTTP session with logging, waits, data factories, schema validation |

A good test: "If the course shop is replaced by a different shop, which code stays?" The core libraries stay. The business logic changes.

### 7.9 Approaches to automate test cases (TAE 3.1.4)

| Approach | Description | Main advantage | Main disadvantage |
|---|---|---|---|
| Capture/playback | A tool records manual actions as a script | Easy to start | Hard to maintain and scale; depends on the SUT version |
| Linear scripting | Scripts without own libraries | Easy to start, easy to change | Hard to maintain and scale |
| Structured scripting | Reusable libraries of steps and user journeys | Easy to maintain, scale, and adapt | Needs programming skills and an initial investment |
| TDD | Developers write a failing test first (red, green, refactor) | Better code structure and testability | Takes time to learn; done badly, it gives false confidence |
| Data-driven testing | Structured scripts read their test data from files | New tests with new data only; test analysts can add tests | Needs test data management |
| Keyword-driven testing | Test cases are tables of keywords (user actions) with data | Business people can write tests | Keywords are complex to build and maintain |
| BDD | Given/When/Then scenarios in feature files, executed by a tool | Better communication; scenarios are specification and tests | Teams often use it without the business; complex steps are hard to debug |

For the Gherkin syntax, good scenario style, and step definitions with pytest-bdd, read the topic [Gherkin and BDD scenarios](../topics/gherkin-bdd.md).

### 7.10 Design principles and patterns (TAE 3.1.5)

- Test automation is software development. The OOP principles (encapsulation, abstraction, inheritance, polymorphism) and the SOLID principles (phase 1, topics 1.5–1.10) apply.
- **Facade:** a simple interface that hides the details. The tests see only what they need. Example: a `Shop` facade with `shop.register_member()`, `shop.buy(book, quantity)`, which uses the API clients.
- **Singleton:** one instance of a class. It is often used for the driver that communicates with the SUT. In pytest, a session-scoped fixture gives the same effect without a global variable.
- **Page object model:** one class for each page. A change of the page needs a change in one place (phase 6, topic 6.9).
- **Flow model:** a facade over the page objects. It contains the user actions that use several pages (for example "check out with a coupon"). The tests use the flows. The steps can be reused in many tests.

  ```python
  # src/shoptest/ui/flows/checkout_flow.py
  class CheckoutFlow:
      def __init__(self, page: Page) -> None:
          self._product = ProductPage(page)
          self._cart = CartPage(page)

      def buy(self, product_id: int, quantity: int, coupon: str | None = None) -> OrderPage:
          self._product.open(product_id).add_to_cart(quantity)
          cart = self._cart.open()
          if coupon:
              cart.apply_coupon(coupon)
          return cart.place_order()
  ```

### 7.11 Pilot and deployment (TAE 4.1)

- A **pilot** is short, but its result can change the direction of the project. Define its scope first: the languages, the tools (commercial or open-source), the test levels, the selected test cases, and the development approach.
- Build several small prototypes to compare approaches. Check the progress regularly to find risks early.
- Integrate the pilot into the CI/CD pipeline early. It shows problems in the SUT, the TAS, and the tool integration.
- Also evaluate the non-technical aspects: the knowledge of the team, the team structure, licenses and organization rules, the planned test types and levels.
- At the end, the TAEs and the test managers evaluate the success and decide.

### 7.12 Deployment risks (TAE 4.2)

- Environment risks: firewall openings, resource utilization (CPU, memory), network connections and their reliability. For mobile tests on real devices: power, battery, network, access to the SUT.
- Technical risks:
  - **Packaging:** testware needs version control and a repository, the same as the SUT.
  - **Logging:** use log levels. Fatal (stop the run), Error (the test fails), Warn (unexpected, but the test continues), Info (basic information), Debug (details for investigation), Trace (even more details).
  - **Test structuring:** the test harness and its test fixtures control the environment and the test data, set preconditions and postconditions, and group test cases into test suites. Fixtures make tests repeatable and atomic.
  - **Updating:** automatic updates of agents and devices can break a run. Plan the configuration and the updates.

### 7.13 Maintainability (TAE 4.3)

- Follow the clean code principles: meaningful names, a logical project structure, no hardcoded values, few parameters, short methods, logging, design patterns where they help, and a focus on testability.
- Avoid hardcoded data: use data-driven testing, and constants for values that rarely change.
- Use static analysis and a code formatter (ruff, mypy).
- Use an agreed branching strategy in version control (feature, release, and fix branches). See the topic [Git for testers](../topics/git-for-testers.md).

## Exercises

All code goes in `labs/tas/` (main project, stage 3).

### Exercise 7.1: Advantages and limits

For the course shop, list 5 test conditions that are good candidates for automation, and 3 that are not (or that are difficult). Explain each one with the advantages, disadvantages, and limits of topic 7.1.

### Exercise 7.2: SUT analysis and tool evaluation

**Side project:** a tool evaluation report.

1. Write the requirements for a TAS for the course shop (topic 7.5): test activities, levels, types, roles, technologies, test data, parts to emulate.
2. Compare three tool sets in a comparison table: (a) Python with pytest, requests, and Playwright; (b) your choice of a second programming stack (for example Java with JUnit, REST Assured, and Selenium); (c) a low-code or no-code tool of your choice. Use at least 8 requirements, with priorities.
3. Write a one-page proposal for the stakeholders.

### Exercise 7.3: Testability review

1. List the testability features of the course shop. Classify each one: observability, controllability, or architecture transparency.
2. Propose three new testability features that would make your tests faster or more reliable. Explain the benefit of each.

### Exercise 7.4: Restructure into layers

1. Restructure `labs/tas/` into the three layers of topic 7.8. Move the configuration, the HTTP session, the waits, and the schema validation into `core/`. Keep the API clients, the page objects, and the flows in the business logic layer.
2. Add a check that test scripts do not import `shoptest.core` directly (for example a small test that reads the imports, or a ruff rule for banned imports).
3. Write `labs/tas/docs/architecture.md` with a diagram of the layers and the gTAA capabilities of your TAS.

### Exercise 7.5: Facades and the flow model

1. Write a `Shop` facade over the API clients for the test setup (for example `shop.new_member()`, `shop.cart_with(book_id, quantity)`).
2. Write a `CheckoutFlow` (topic 7.10) and use it in the UI tests.
3. Explain where your TAS uses a singleton effect, and why a session fixture is better than a global variable.

### Exercise 7.6: Data-driven tests

1. Move the boundary value test data of R1, R4, and R5.8 into CSV files in `tests/data/`.
2. Read them in a parametrize helper, with an ID column.
3. Add a new test case only with a new CSV line. Show that it runs.

### Exercise 7.7: Gherkin style review

Read the topic [Gherkin and BDD scenarios](../topics/gherkin-bdd.md) first. A colleague wrote this feature file:

```gherkin
Feature: Tests

  Background:
    Given I open "http://localhost:8000/login"
    And I type "anna" in the field "#username"
    And I type "secret123" in the field "#password"
    And I click the button "Log in"

  Scenario: Test 1
    When I go to "/products/2"
    And I type "2" in "quantity-input"
    And I click "add-to-cart"
    And I go to "/cart"
    Then I see "50.00"
    And I see "0.00"
    When I type "BOOKS5" in "coupon-input"
    And I click "Apply"
    Then I see "45.00"
    And I see "2.99"

  Scenario: Test 2
    When I click "Place the order"
    Then the order works

  Scenario: Member discount
    Given a member
    Then the discount is correct
```

1. List each problem. For each problem, name the rule of the topic that it breaks. Find at least 10 problems.
2. Find the scenario that depends on a different scenario. Explain what happens when the scenarios run in random order or in parallel.
3. Find the business rules that the colleague wanted to test. Name the requirements (R-numbers in `sut/REQUIREMENTS.md`).
4. Rewrite the file: a good feature name and description, one `Rule` for each business rule, declarative steps, one behavior for each scenario, exact outcomes, and a `Scenario Outline` where several scenarios differ only in their values.
5. Give your rewrite to the mentor for a review.

### Exercise 7.8: BDD

1. Add pytest-bdd. Write a feature file `tests/features/discounts.feature` with at least 5 scenarios for R5.2–R5.6. Use a scenario outline with an examples table for the decision table. Use one data table.
2. Write the step definitions. The steps call the business logic layer. Put the steps that more than one feature file uses in a `conftest.py`.
3. Add the tags `@smoke` and `@prices`, and register them as markers. Run only the smoke scenarios with `pytest -m smoke`.
4. Run the feature against `SUT_DEFECTS=all`. Read each failure message: does it name the rule and the expected value?
5. Show the feature file to a non-technical person. Can they read it? Change the wording with their feedback.

### Exercise 7.9: Keyword-driven testing (small)

1. Define 5 keywords for the shop (for example `register member`, `add to cart`, `apply coupon`, `check total`).
2. Write a small interpreter that runs a test case from a CSV table of keywords and arguments.
3. Compare the effort and the readability with the BDD scenarios.

### Exercise 7.10: Logging and evidence

1. Configure Python `logging` with levels. Log each HTTP request (method, URL, status, duration, request ID) at the Debug level, and each test step at the Info level.
2. Send a unique `X-Request-ID` with each request.
3. Save a screenshot and a Playwright trace for each failed UI test.
4. Make a test fail. From the test log, find the matching log line of the shop.

### Exercise 7.11: Pilot plan and risks

Write a pilot plan of one page for the introduction of your TAS in a fictional team: the scope, the tools, the selected test cases, the timeline, the check points, the non-technical aspects, and a table of deployment risks with their mitigations.

## Done criteria

- [ ] I can explain the advantages, disadvantages, and limits of test automation, and in-sprint automation.
- [ ] I can analyze an SUT and present a tool evaluation in a comparison table.
- [ ] I can explain observability, controllability, and architecture transparency, and the test environments.
- [ ] I can draw the gTAA and map my TAS to its capabilities.
- [ ] My TAS has three layers, and the test scripts do not call the core libraries.
- [ ] I can explain each approach of topic 7.9, and I used structured scripting, data-driven testing, and BDD.
- [ ] I can write declarative Gherkin scenarios with one behavior each, and find the problems in bad scenarios.
- [ ] I used the facade, page object, and flow model patterns, and I can explain the singleton pattern.
- [ ] I can write a pilot plan and analyze deployment risks.
- [ ] My logs connect a failed test to the log of the SUT (stage 3 complete).

## Next

[Phase 8: CI/CD, environments, and reporting](phase-8-ci-cd-reporting.md)
