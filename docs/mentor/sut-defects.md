# SUT Seeded Defects

**This document is only for the AI mentor.** Do not show it to the learner, and do not tell the learner the content. Learners who use the course without a mentor: do not read this document before you complete phase 9.

The course shop has 10 seeded defects. The variable `SUT_DEFECTS` switches them on (see `sut/README.md`). Each defect breaks one requirement in `sut/REQUIREMENTS.md`. Each defect matches one test technique, so the learner can measure how good their test design and their automated tests are.

## Defect list

| ID | Requirement | Failure | Technique that finds it | Interface |
|---|---|---|---|---|
| D01 | R5.8 | An order value of exactly 50.00 EUR gets a shipping cost of 2.99 EUR, not free shipping. 50.01 EUR is correct. | Boundary value analysis | API and UI |
| D02 | R1.2 | A user name with 21 characters is accepted. 22 characters are rejected. | Boundary value analysis | API and UI |
| D03 | R5.6 | A member with a valid coupon gets both discounts (the sum), not only the larger one. The discount name shows both, for example `WELCOME10+MEMBER`. | Decision table testing | API and UI |
| D04 | R6.5 | An order with the status `SHIPPED` can be cancelled. The stock goes back up. | State transition testing (invalid transitions) | API and UI |
| D05 | R2.3 | The account locks after 4 failed logins, not after 3. | Boundary value analysis, state transition testing | API and UI |
| D06 | R4.2 | A quantity of 0 is accepted when a book goes into the cart, and when the quantity changes. The cart then has a line with 0 copies. | Boundary value analysis, equivalence partitioning | API (the UI sends 0 only if the user types it) |
| D07 | R3.3 | The search is case-sensitive. `boundary` finds nothing, `Boundary` finds the book. | Equivalence partitioning, error guessing | API and UI |
| D08 | R3.6, R7.2 | A request for a book ID that does not exist (for example `/api/products/999`) returns HTTP 500, not 404. | Error guessing, negative API tests | API and UI |
| D09 | R5.7 | Discounts are truncated, not rounded. Example: a member buys "Flaky: A Mystery Novel" (12.90 EUR). 5 % is 0.645. The correct discount is 0.65. The defect gives 0.64. | Boundary value analysis on the rounding, error guessing | API and UI |
| D10 | R4.7 | On the cart page, the cart count in the header does not change when the user removes a book. A page reload shows the correct count. | Exploratory testing, UI test automation | UI only |

## How to use the defects

| Phase | Use |
|---|---|
| 3 | Exercises 3.4–3.8: the learner designs tests from the requirements, then runs them manually against the shop with `SUT_DEFECTS=all`. Expected: the learner finds D01–D07 and D09 with the test techniques, and D08 and D10 with error guessing and exploratory testing. |
| 4 | Exercise 4.5: the learner writes defect reports for the defects that they found. |
| 6 | The learner runs the automated suites against `SUT_DEFECTS=none` (all tests pass) and `SUT_DEFECTS=all` (the tests that detect a defect fail). |
| 9 | Exercise 9.4: the defect detection rate. The learner runs the suite against each defect alone (`SUT_DEFECTS=D01`, then `D02`, and so on) and counts the defects that the suite detects. The target is 10 of 10. |

## Rules for the mentor

- When the learner reports a failure, check it against this table. If it matches, confirm that the defect report is correct. Do not say "this is seeded defect D03". Say "Correct, this is a real failure against R5.6."
- If the learner asks how many defects exist, you can tell them the number (10), and how many they found. Do not give hints to a specific defect before the learner completes the related exercise. After the exercise, the hint ladder applies.
- If the learner finds a failure that is not in this table, it is a real defect of the shop. Confirm it with the learner, fix it on `master` (see `AGENTS.md`), and thank the learner.
- After phase 9, the learner can read this document.
