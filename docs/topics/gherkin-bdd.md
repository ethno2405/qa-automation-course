# Gherkin and BDD Scenarios

**Phase:** 3 (write scenarios), 7 (automate scenarios), 8 (run them in a pipeline)
**Syllabus:** CTFL v4.0.1, section 4.5 (FL-4.5.2, FL-4.5.3: acceptance criteria and ATDD). CTAL-TAE v2.0, section 3.1.4 (BDD as an approach to automate test cases, LO TAE-3.1.4).
**Related:** [phase 3, topic 3.11](../phases/phase-3-test-design.md), [phase 7, topic 7.9](../phases/phase-7-automation-architecture.md), [phase 7, exercises 7.7 and 7.8](../phases/phase-7-automation-architecture.md)

## Summary

Gherkin is a structured, plain-language format for examples of system behavior. Each example is a scenario with Given, When, and Then steps. Business people, developers, and testers write the scenarios together (BDD). A tool such as pytest-bdd or Cucumber then connects each step to code, so that the scenarios run as automated tests and stay current as living documentation.

## Explanation

### BDD and Gherkin

- **BDD** (behavior-driven development) is a way of working, not a tool. The team discusses a user story with concrete examples before the implementation. A common form is the "three amigos" meeting: a business representative, a developer, and a tester.
- BDD has three practices: **discovery** (find the examples together), **formulation** (write them in Gherkin), and **automation** (connect the steps to code).
- **Gherkin** is the language of the formulation. A scenario in Gherkin is an acceptance criterion in the scenario-oriented format of CTFL 4.5.
- If only the testers write Gherkin, without the business, the team gets the cost of BDD without its main benefit. The CTAL-TAE syllabus names this as a disadvantage of BDD (section 3.1.4).

### Keywords

| Keyword | Purpose |
|---|---|
| `Feature` | The first keyword of the file. A name and an optional free-text description. One feature file for one feature. |
| `Rule` | Groups the scenarios of one business rule (for example one requirement). Optional. |
| `Background` | Steps that run before each scenario of the feature (or of the rule). Use it only for short, common context. |
| `Scenario` (or `Example`) | One concrete example of the behavior |
| `Scenario Outline` (or `Scenario Template`) | A scenario with placeholders `<name>`. It runs one time for each row of its `Examples` table. |
| `Examples` | The table of values for a scenario outline. The first row has the placeholder names. |
| `Given` | The context: the state of the system before the action |
| `When` | The action or event |
| `Then` | The expected outcome that a user or a system can observe |
| `And`, `But` | Continue the previous step type. They make the text easier to read. |
| `@tag` | A label on a feature, rule, scenario, or examples table. Use tags to select scenarios, for example `@smoke`. |
| `\|` (data table) | A table of data for one step |
| `"""` (doc string) | A block of text for one step, for example a JSON body or a long message |
| `#` | A comment line |

The keywords exist in many spoken languages. The line `# language: de` at the top of a file selects German keywords, for example.

### An example feature file

The example is for the course shop. It uses the requirements in [../../sut/REQUIREMENTS.md](../../sut/REQUIREMENTS.md).

```gherkin
@prices
Feature: Discounts and shipping
  Customers pay less shipping for larger orders.
  Only one discount applies to an order.

  Background:
    Given the shop is available

  Rule: The shipping cost depends on the order value (R5.8)

    @smoke
    Scenario Outline: Shipping cost around the lower limit of the order value
      Given a customer who is not a member
      When the customer puts <quantity> copies of "<book>" in the cart
      Then the subtotal is <subtotal> EUR
      And the shipping cost is <shipping> EUR

      Examples:
        | book                               | quantity | subtotal | shipping |
        | The State Machine Garden           | 1        | 24.99    | 4.99     |
        | The Boundary Hunter                | 2        | 25.00    | 2.99     |
        | The Pyramid and the Ice Cream Cone | 1        | 49.99    | 2.99     |

  Rule: The coupon BOOKS5 needs a subtotal of 30.00 EUR or more (R5.4)

    Scenario: The coupon BOOKS5 is valid at a subtotal of exactly 30.00 EUR
      Given a customer who is not a member
      And the customer has these books in the cart:
        | book                         | quantity |
        | Exploring Without a Map      | 2        |
        | Decision Tables for Everyone | 2        |
      When the customer enters the coupon "BOOKS5"
      Then the discount is 5.00 EUR with the name "BOOKS5"
```

Read the numbers: the subtotal of the second scenario is 2 × 5.00 + 2 × 10.00 = 30.00 EUR. This is the lowest subtotal where `BOOKS5` is valid, so the discount is 5.00 EUR.

The example does not show all boundary values and all rules. It shows the syntax. Your own test design in phase 3 must cover all partitions, boundaries, and rules.

### Rules for good scenarios

1. **Describe behavior, not the user interface.** Write what the user wants and what the system does, not which fields and buttons the user uses. This is a **declarative** style. Steps with clicks, selectors, and URLs are an **imperative** style. They break when the page changes, and the business cannot read them.

   | Imperative (avoid) | Declarative (prefer) |
   |---|---|
   | `When I type "2" in "#quantity"` | `When the customer puts 2 copies of "The Boundary Hunter" in the cart` |
   | `And I click the button "Add to cart"` | |
   | `Then I see "2.99" in the element "#shipping"` | `Then the shipping cost is 2.99 EUR` |

2. **One scenario, one behavior.** One `When`, then the `Then` steps for it. A second `When` usually means a second scenario.
3. **Given is a state, When is an action, Then is an outcome.** "Given the customer clicks Login" is an action in the wrong place: write "Given a logged-in customer".
4. **Then must be observable and exact.** "Then the order works" and "Then the discount is correct" cannot fail in a useful way. Write the value: "Then the discount is 5.29 EUR".
5. **Use concrete examples.** Real values make the rule clear and show the boundaries. Use the test techniques of phase 3 to select them: the rows of an `Examples` table are equivalence partitions and boundary values, or the columns of a decision table.
6. **Leave out incidental details.** Write only the data that matters for the rule. The user name and the password of the customer do not matter for a shipping rule: hide them in the step definition.
7. **Each scenario is independent.** A scenario must not need the result of a different scenario. Put the necessary state in its `Given` steps.
8. **Write in the language of the business.** Use the words of the domain ("member", "coupon", "order value"), the same word for the same thing in all scenarios, and the third person ("the customer"), not "I", when there is more than one role.
9. **Keep scenarios short.** 3 to 7 steps is a good size. A long scenario usually tests more than one behavior, or contains incidental details.
10. **The scenario name tells the rule.** "Shipping cost at the boundaries of the order value" is better than "Test 3".

### Step definitions with pytest-bdd

pytest-bdd connects each step text to a Python function. The functions are normal pytest code: they can use fixtures.

```python
# tests/features/test_discounts.py
import uuid
from typing import Any

from pytest_bdd import given, parsers, scenarios, then, when

from shoptest.api.client import ShopApi

scenarios("discounts.feature")


def book_id(api: ShopApi, title: str) -> int:
    items = api.request("GET", "/api/products", params={"q": title}).json()["items"]
    return next(item["id"] for item in items if item["title"] == title)


@given("the shop is available")
def shop_is_available(api: ShopApi) -> None:
    assert api.request("GET", "/api/health").json()["status"] == "ok"


@given(parsers.re(r"a customer who (?P<membership>is|is not) a member"))
def customer(api: ShopApi, membership: str) -> None:
    name = f"u{uuid.uuid4().hex[:12]}"
    member = membership == "is"
    assert api.register(name, "secret123", f"{name}@example.test", 30, member).status_code == 201
    assert api.login(name, "secret123").status_code == 200


@given("the customer has these books in the cart:")
def books_in_cart(api: ShopApi, datatable: list[list[str]]) -> None:
    header, *rows = datatable
    for row in rows:
        line = dict(zip(header, row, strict=True))
        body = {"product_id": book_id(api, line["book"]), "quantity": int(line["quantity"])}
        assert api.request("POST", "/api/cart/items", json=body).status_code == 201


@when(parsers.parse('the customer puts {quantity:d} copies of "{book}" in the cart'), target_fixture="cart")
def put_in_cart(api: ShopApi, quantity: int, book: str) -> dict[str, Any]:
    body = {"product_id": book_id(api, book), "quantity": quantity}
    response = api.request("POST", "/api/cart/items", json=body)
    assert response.status_code == 201, response.text
    return response.json()


@when(parsers.parse('the customer enters the coupon "{code}"'), target_fixture="cart")
def enter_coupon(api: ShopApi, code: str) -> dict[str, Any]:
    return api.request("GET", "/api/cart", params={"coupon": code}).json()


@then(parsers.parse("the subtotal is {amount} EUR"))
def subtotal_is(cart: dict[str, Any], amount: str) -> None:
    assert cart["subtotal"] == amount


@then(parsers.parse("the shipping cost is {amount} EUR"))
def shipping_is(cart: dict[str, Any], amount: str) -> None:
    assert cart["shipping"] == amount


@then(parsers.parse('the discount is {amount} EUR with the name "{name}"'))
def discount_is(cart: dict[str, Any], amount: str, name: str) -> None:
    assert (cart["discount"], cart["discount_name"]) == (amount, name)
```

- `scenarios("discounts.feature")` makes one pytest test for each scenario and each row of an `Examples` table. The path is relative to the test module.
- **Parsers:** a plain string must match the step text exactly. `parsers.parse` uses `{name}` and `{name:d}` (a whole number). `parsers.re` uses a regular expression with named groups.
- **Scenario outlines:** pytest-bdd puts the values of the row into the step text before it matches the steps. So the step definitions use normal parsers, not the `<placeholder>` names.
- **Shared state:** a step with `target_fixture="cart"` stores its return value as the fixture `cart`. Later steps of the same scenario get it as a parameter. Do not use global variables: they break when tests run in parallel.
- **Data tables and doc strings:** a step function gets a data table with the parameter `datatable` (a list of rows, each a list of strings), and a doc string with the parameter `docstring`.
- **Tags become pytest markers.** Run `uv run pytest -m smoke` to run only the scenarios with `@smoke`. Register the markers in `pyproject.toml`, so that pytest does not warn:

  ```toml
  [tool.pytest.ini_options]
  markers = ["smoke: fast checks of the most important functions", "prices: price rules"]
  ```

- **Keep the steps thin.** A step definition calls the business logic layer (API clients, flows, page objects) and asserts. It contains no locators, no URLs, and no long logic (phase 7, topic 7.8). The example uses `ShopApi` directly. In your TAS, move `book_id` and the cart actions into the `Shop` facade of phase 7.
- **Reuse steps.** Use the same step text for the same action in all feature files. Before you write a new step, look for an existing one. Put shared step definitions in a `conftest.py`, so that all feature test modules find them.

### Where scenarios run

- Scenarios are not a test level. A scenario can run against the API (fast, stable) or against the UI (slow, closer to the user). The step definitions decide this. Run most business rules through the API, and only a few user journeys through the UI.
- In the pipeline (phase 8), use tags to select suites: `@smoke` in each push, all scenarios in the nightly run.
- Publish the results with the scenario names. Then the report is living documentation: the business can see which rules the system meets today.

## Example

A bad scenario and a rewrite:

```gherkin
Scenario: Test 2
  Given I am on "/login"
  When I type "anna" and "secret123" and click "Log in"
  And I add 2 of book 2 and go to the cart
  Then I see "0.00"
```

Problems: the name tells nothing; the steps describe the UI (imperative); the user name and password are incidental details; there are two actions; "I see 0.00" does not say what is 0.00.

```gherkin
Scenario: An order value of exactly 25.00 EUR has the low shipping cost
  Given a customer who is not a member
  When the customer puts 2 copies of "The Boundary Hunter" in the cart
  Then the shipping cost is 2.99 EUR
```

## Common mistakes

| Mistake | Result | Fix |
|---|---|---|
| Imperative steps with selectors and URLs | Many scenarios break when the page changes. The business cannot read them. | Declarative steps. The locators stay in the page objects. |
| More than one `When` in a scenario | A failure does not tell which behavior failed. | One behavior for each scenario. |
| A vague `Then` ("works", "is correct") | The scenario cannot fail for a wrong value. | An exact, observable outcome. |
| Scenarios that depend on other scenarios | Random order and parallel runs fail. | Each scenario sets its own context in `Given`. |
| A long `Background` | The reader must look in two places to understand a scenario. | Keep it to 1–3 short steps, or put the steps in the scenarios. |
| Many similar scenarios with different values | Long files, duplicated steps | A `Scenario Outline` with an `Examples` table |
| Too many near-identical step texts ("add a book", "put a book", "adds the book") | Many step definitions for one action | One wording for one action. Search the existing steps first. |
| Logic, locators, or HTTP calls in step definitions | Duplication. Hard to maintain. | Call the business logic layer. |
| Only positive scenarios | Negative cases and boundaries are missing. The CTAL-TAE syllabus names this as a disadvantage of BDD. | Add scenarios from the test techniques of phase 3. |
| Testers write Gherkin alone | The cost of BDD without the shared understanding | Write the scenarios with the business and the developers. |

## Sources

- Cucumber documentation, "Gherkin Reference" (cucumber.io/docs/gherkin/reference)
- pytest-bdd documentation (pytest-bdd.readthedocs.io): scenarios, step arguments, data tables, doc strings, tags
- Seb Rose and Gáspár Nagy, *The BDD Books: Discovery* and *Formulation*
- Gojko Adzic, *Specification by Example*
- CTFL v4.0.1, section 4.5. CTAL-TAE v2.0, section 3.1.4.
