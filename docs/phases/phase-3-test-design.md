# Phase 3: Static Testing and Test Design

**Time:** 3–4 weeks
**Prerequisites:** Phase 2. For exercise 3.9: phase 1.
**Syllabus:** CTFL v4.0.1, chapter 3 (Static Testing) and chapter 4 (Test Analysis and Design). LOs FL-3.1.1 to FL-4.5.3. See [../certification.md](../certification.md).
**Environment:** The course shop with `SUT_DEFECTS=all` (exercises 3.4–3.8). A browser, `curl`, and the interactive API page `http://127.0.0.1:8000/docs`.

## Goal

At the end of this phase, you can:

- Explain the value of static testing, and do a review with the correct process and roles.
- Derive test cases with equivalence partitioning, boundary value analysis, decision table testing, and state transition testing, and measure their coverage.
- Explain statement testing and branch testing, and measure code coverage.
- Use error guessing, exploratory testing, and checklist-based testing.
- Write user stories and acceptance criteria with the team, and derive test cases with ATDD.
- Find the seeded defects of the course shop with these techniques (main project, stage 1).

## Reading

| Source | Part |
|---|---|
| CTFL syllabus v4.0.1 | Chapters 3 and 4. Read them completely. Chapter 4 has K3 LOs: practice them. |
| Lee Copeland, *A Practitioner's Guide to Software Test Design* | The chapters about equivalence classes, boundary values, decision tables, and state transitions |
| Elisabeth Hendrickson, *Explore It!* | The chapters about charters and heuristics |
| Gojko Adzic, *Specification by Example* | Optional. Examples as acceptance criteria. |

## Rules for the exercises

- Use only [../../sut/REQUIREMENTS.md](../../sut/REQUIREMENTS.md) and the running shop. **Do not read the code in `sut/app/` before exercise 3.9.**
- Start the shop with all seeded defects: `cd sut && SUT_DEFECTS=all docker compose up -d`. Reset the data between tests with `curl -X POST http://127.0.0.1:8000/api/admin/reset`.
- **First design, then execute.** Write all test cases of an exercise before you run the first one. A test case has: an ID, the requirement, the technique, the precondition, the input or steps, and the expected result.
- When the actual result is different from the expected result, record it. You write the defect reports in phase 4.
- Put the work in `labs/tas/docs/test-design.md` (main project, stage 1).

## Topics

### 3.1 Static testing (CTFL 3.1)

- **Static testing** examines work products without execution: reviews (by people) and static analysis (by tools, for example a linter or a type checker).
- Almost every work product can be examined: requirements, user stories, designs, code, test plans, test cases, contracts, configuration.
- **Value:** static testing finds defects early, before they cause failures. It finds defects that dynamic testing cannot find easily: ambiguous requirements, missing requirements, design problems, code that is hard to maintain, deviations from standards.
- **Static compared with dynamic testing:** static testing finds **defects** directly. Dynamic testing finds **failures**, and then the team looks for the defects. Static testing can find defects in code that never runs in a test.

### 3.2 Feedback and the review process (CTFL 3.2.1, 3.2.2)

- **Early and frequent feedback** from stakeholders prevents misunderstandings. The cost of a change is low when the change comes early.
- **Review process** (based on ISO/IEC 20246):

  | Activity | What happens |
  |---|---|
  | Planning | Define the scope, the objectives, the work product, the quality characteristics, the exit criteria, the effort, and the time |
  | Review initiation | Make sure that everybody has access to the work product and understands their role |
  | Individual review | Each reviewer examines the work product and records anomalies |
  | Communication and analysis | The team discusses the anomalies, and decides the status and the owner of each one |
  | Fixing and reporting | The author fixes the defects. The team reports the results and checks the exit criteria. |

### 3.3 Review roles and review types (CTFL 3.2.3–3.2.5)

- **Roles:** manager (decides what to review, gives resources), author (makes and fixes the work product), moderator or facilitator (runs the review meetings), scribe or recorder (records the anomalies and decisions), reviewer (does the review), review leader (owns the review: organization and people).
- **Review types**, from informal to formal:

  | Type | Main characteristics |
  |---|---|
  | Informal review | No defined process, no formal documentation. Main objective: find anomalies. |
  | Walkthrough | The author leads. Objectives: education, consensus, new ideas, find anomalies. |
  | Technical review | Technically qualified reviewers, led by a moderator. Objectives: consensus and technical decisions, find anomalies. |
  | Inspection | The most formal. A full generic process, metrics, and exit criteria. The author cannot be the review leader or the scribe. Objective: find the maximum number of anomalies. |

- **Success factors:** clear objectives and exit criteria, the correct review type, small parts of the work product, enough time, management support, training, a culture of learning without blame.

### 3.4 Test techniques: overview (CTFL 4.1)

| Category | Basis | Techniques in CTFL |
|---|---|---|
| Black-box | The specification. No knowledge of the code. | Equivalence partitioning, boundary value analysis, decision table testing, state transition testing |
| White-box | The internal structure (code) | Statement testing, branch testing |
| Experience-based | The knowledge and experience of the tester | Error guessing, exploratory testing, checklist-based testing |

Test techniques help you to find the important test conditions and to select a small number of test cases with good coverage. Use several techniques together.

### 3.5 Equivalence partitioning (CTFL 4.2.1)

- Divide the data into **partitions** (equivalence classes). The system must process all values of one partition in the same way. Test one value from each partition.
- Partitions exist for inputs, outputs, configuration, time, and internal values. Make **valid** and **invalid** partitions.
- **Example:** R1.6, the age is a whole number from 16 to 120.

  | Partition | Values | Valid? | Example test value |
  |---|---|---|---|
  | P1 | less than 16 | Invalid | 10 |
  | P2 | 16 to 120 | Valid | 40 |
  | P3 | more than 120 | Invalid | 150 |
  | P4 | not a whole number (text, decimal, empty) | Invalid | `"abc"` |

- **Coverage:** EP coverage = partitions tested / all partitions. **Each choice coverage** for several inputs: each partition of each input is used in at least one test case.
- Test invalid partitions one at a time. If one test case has two invalid values, the first error can hide the second.

### 3.6 Boundary value analysis (CTFL 4.2.2)

- BVA applies to ordered partitions. Defects often occur at the **boundaries**: `<` in place of `<=`, an index off by one.
- **2-value BVA:** for each boundary, test the boundary value and its closest neighbor in the next partition.
- **3-value BVA:** for each boundary, test the boundary value and both of its neighbors. It finds more defects, for example `==` in place of `<=`.
- **Example:** R1.6, age 16 to 120, whole numbers.

  | Boundary | 2-value BVA | 3-value BVA |
  |---|---|---|
  | Lower: 16 | 15, 16 | 15, 16, 17 |
  | Upper: 120 | 120, 121 | 119, 120, 121 |

- For money, the closest neighbor is one cent away: the boundary 25.00 has the neighbors 24.99 and 25.01.
- **Coverage:** BVA coverage = boundary values tested / all boundary values (for the selected method).

### 3.7 Decision table testing (CTFL 4.2.3)

- Use a decision table when the result depends on a **combination** of conditions.
- **Conditions** are the rows at the top. **Actions** are the rows at the bottom. Each **column** (a rule) is one combination of conditions and its actions.
- Notation: `T`/`F` (true/false), `–` (the value does not matter), `N/A` (not possible).
- Steps: list the conditions, list the actions, write all combinations, remove the combinations that are not possible, merge columns where a condition does not matter, fill in the actions from the requirements.
- **Coverage:** decision table coverage = columns tested / all feasible columns. Each column is one test case.
- A decision table often shows **gaps** in the requirements: a combination that the requirements do not describe. Ask the business. This is static testing too.

### 3.8 State transition testing (CTFL 4.2.4)

- Use it when the behavior depends on the **history**: the current state and the event.
- A **state diagram** shows states (circles or boxes) and transitions (arrows), with `event [guard condition] / action`.
- A **state table** shows each state with each event. It shows the **invalid transitions** too: an event that is not permitted in a state.
- **Coverage criteria:**

  | Criterion | Each test suite must cover | Finds |
  |---|---|---|
  | All states coverage | Each state at least one time | Unreachable states |
  | Valid transitions coverage (0-switch coverage) | Each valid transition at least one time | Wrong valid transitions |
  | All transitions coverage | Each valid transition, and each invalid transition (one invalid transition for each test case) | Transitions that must not be possible, but are |

- All transitions coverage is the minimum for safety-critical software.

### 3.9 White-box testing (CTFL 4.3)

- **Statement testing:** the coverage items are the executable statements. Statement coverage = statements executed / all statements.
- **Branch testing:** a branch is a transfer of control between two blocks of code: both outcomes of an `if`, each `case`, and the jump back of a loop. Branch coverage = branches executed / all branches.
- 100 % branch coverage gives 100 % statement coverage. The reverse is not true: an `if` without an `else` can have 100 % statement coverage with only the "true" branch.
- **Value of white-box testing:** it finds code that no test executes, and defects in code that the specification does not describe. **Limit:** it cannot find missing code: a requirement that nobody implemented.
- **Tool:** coverage.py. `uv run pytest --cov=src --cov-branch --cov-report=term-missing`.

### 3.10 Experience-based techniques (CTFL 4.4)

- **Error guessing:** predict errors, defects, and failures from experience: earlier failures, typical developer errors, failures in similar systems. A **fault attack** is a systematic list of these guesses. Examples for an API: empty body, wrong type, very long text, unknown ID, special characters, a request without authentication, two requests at the same time.
- **Exploratory testing:** design, execute, and evaluate tests at the same time, while you learn about the system. Use **session-based testing**: a time box (for example 60 minutes), a **test charter** (the mission), and session notes. A charter: "Explore <target> with <resources> to discover <information>."
- **Checklist-based testing:** use a checklist of test conditions from experience, standards, or earlier defects. Checklists must be specific and must change over time.

### 3.11 Collaboration-based approaches (CTFL 4.5)

- **User stories:** "As a <role>, I want <goal>, so that <benefit>." The **3 C's**: card (the story), conversation (the discussion), confirmation (the acceptance criteria).
- **INVEST:** a good story is Independent, Negotiable, Valuable, Estimable, Small, and Testable.
- **Acceptance criteria** define when the story is complete. Two common formats: **scenario-oriented** (Given/When/Then) and **rule-oriented** (a list of rules, or a table).
- **ATDD:** before the implementation, the team (business, developer, tester) writes examples as test cases from the acceptance criteria. The test cases start with the positive paths, then negative paths and non-functional characteristics. The test cases are in a language that the business understands. Later, they can become automated acceptance tests (phase 7, BDD).
- For the Gherkin format (Feature, Scenario, Scenario Outline, Examples) and the rules for good Given/When/Then scenarios, read the topic [Gherkin and BDD scenarios](../topics/gherkin-bdd.md). Read only the parts about the keywords and the rules for good scenarios now. The part about step definitions is for phase 7.

## Exercises

### Exercise 3.1: Review of a user story

Do an individual review of this draft. Record each anomaly with: the location, the problem, and a question or a proposal.

> **Story GIFT-1: Gift cards**
> As a customer, I want to pay with a gift card, so that I can use presents from friends.
>
> Acceptance criteria:
> 1. The customer enters the gift card number at checkout.
> 2. The gift card value is subtracted from the total.
> 3. Gift cards are valid for a long time.
> 4. If the gift card value is bigger than the total, the rest stays on the card.
> 5. The system must be fast and secure.
> 6. Gift cards can be combined with coupons.

Find at least 8 anomalies. Classify each one: ambiguous, missing, not testable, contradiction with REQUIREMENTS.md, or a question. Then rewrite the story with testable acceptance criteria.

**Side project (optional):** review a real requirements document or user story from your work, or a public one (for example an RFC or an open-source issue). Use a checklist.

### Exercise 3.2: Static analysis

1. Run `uv run ruff check` and `uv run mypy --strict` on your code from phase 1. Classify each finding: a likely defect, a maintainability problem, or a style problem.
2. Explain why each likely defect is a defect that static testing finds and dynamic testing can miss.

### Exercise 3.3: Equivalence partitions (warm-up)

For R3.2 (page size and page number) and R5.4 (coupon `BOOKS5`), list the valid and invalid partitions. Give one test value for each partition.

### Exercise 3.4: Registration (EP and BVA)

1. For R1.2 (user name), R1.4 (password), and R1.6 (age), make the partitions and the boundary values (3-value BVA for the lengths and the age).
2. Write the test cases. Calculate the EP coverage and the BVA coverage of your test cases.
3. Execute the test cases against the shop (UI or API) with `SUT_DEFECTS=all`. Record the results.

### Exercise 3.5: Shipping, quantity, and login (BVA)

1. R5.8 (shipping cost): find all boundaries of the order value. Use 3-value BVA. Find books in the catalog to build each order value (combine books and quantities). Write the expected shipping cost and total for each test case.
2. R4.2 and R4.3 (quantity): use 3-value BVA for the quantity of one add, and for the total quantity of one book in the cart.
3. R2.3 (failed logins): which number of failed logins is the boundary? Write the test cases.
4. Execute all test cases. Record the results.

### Exercise 3.6: Discounts (decision table)

1. Make a decision table for R5.2–R5.6. Conditions: the user is a member, the coupon that the user enters (none, `WELCOME10`, `BOOKS5`, unknown), and the validity of the coupon. Actions: the discount that applies, the discount amount, and the error message.
2. Remove the combinations that are not possible. Merge columns where you can.
3. Select a cart for each column, so that the discount amounts are easy to calculate. Write the expected results.
4. Add test cases for R5.7 (rounding): find a book and a discount where the discount has an exact half cent.
5. Execute all test cases. Record the results.
6. Did your table show a gap in the requirements? Write it down as a question for the business.

### Exercise 3.7: Order status and account lock (state transitions)

1. Draw the state diagram for the order status (R6.4–R6.6). Make the state table with all states and all events (`pay`, `cancel`, `ship`, `deliver`). Mark the invalid transitions.
2. Write test cases for **all transitions coverage**. Each test case covers one invalid transition at most.
3. Draw the state diagram for the login and the account lock (R2.3–R2.6). Use these states: 0, 1, and 2 failed logins, and locked. Write test cases for valid transitions coverage. (Start the shop with `SUT_LOCK_MINUTES=0.2` so that the lock ends after 12 seconds.)
4. Execute all test cases. Use the admin account for `ship` and `deliver`. Record the results.

### Exercise 3.8: Exploratory and checklist-based testing

1. Write three test charters for the course shop, for example: "Explore the cart page with removals and coupon changes to discover display errors", "Explore the API with wrong inputs to discover error handling problems", "Explore the search with different texts to discover differences from R3.3".
2. Make an error-guessing checklist for a REST API (at least 10 items).
3. Do one 45-minute session for each charter. Write session notes: what you tested, what you found, the questions, and the ideas for next time.
4. Record the failures that you found.

### Exercise 3.9: Statement and branch coverage

1. Use your `shipping_cost` and `Cart` code from phase 1. Measure the statement and branch coverage of your tests with `pytest --cov --cov-branch`.
2. Find a test suite with 100 % statement coverage and less than 100 % branch coverage. Explain why.
3. Add tests until you have 100 % branch coverage.
4. Now read `sut/app/rules.py`. Find the branches of `shipping_cost` and `quote`. Do your black-box test cases from exercises 3.5 and 3.6 cover all branches? Which branch, if any, did no black-box test case reach?

### Exercise 3.10: User story and ATDD

The business wants a new feature: "Gift wrapping costs 2.50 EUR for each book. It is free for members. The customer selects it for the whole order."

1. Write the user story. Check it against INVEST.
2. Write the acceptance criteria in both formats: rule-oriented, and Given/When/Then in Gherkin. Follow the rules for good scenarios in the topic [Gherkin and BDD scenarios](../topics/gherkin-bdd.md).
3. Derive the ATDD test cases: positive paths first, then negative paths and boundaries, then a non-functional test case.
4. Find two questions for the business that the conversation must answer.

### Exercise 3.11: Result (main project, stage 1)

1. Complete `labs/tas/docs/test-design.md`: all test cases of exercises 3.4–3.8, with a traceability table (requirement → test conditions → test cases → result).
2. Count the different failures that you found. Ask the mentor to confirm your count. Record the number in `learner/progress.md`.

## Done criteria

- [ ] I can explain the value of static testing, the review process, the roles, and the review types.
- [ ] I can derive test cases with EP and BVA (2-value and 3-value), and calculate the coverage.
- [ ] I can build a decision table, minimize it, and derive test cases.
- [ ] I can build a state diagram and a state table, and derive test cases for all states, valid transitions, and all transitions coverage.
- [ ] I can explain statement and branch coverage, and measure them with a tool.
- [ ] I can write a test charter, do a session, and write session notes.
- [ ] I can write a user story with acceptance criteria, and derive ATDD test cases.
- [ ] My test design for the course shop is complete and traceable (stage 1, part 1).

## Next

[Phase 4: Test management, tools, and the CTFL exam](phase-4-test-management.md)
