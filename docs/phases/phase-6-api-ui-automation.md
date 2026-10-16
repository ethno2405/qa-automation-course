# Phase 6: API and Web Test Automation

**Time:** 6–7 weeks
**Prerequisites:** Phase 1 (programming), phase 3 (test design), phase 5 (HTTP). Phase 4 is recommended.
**Syllabus:** None directly. This phase gives the practice for CTAL-TAE (phases 7–9): GUI and API testing, testability, test fixtures, design patterns (TAE-3.1.5).
**Environment:** `labs/tas/` from stage 0, the course shop, Playwright for Python (see [../software-setup.md](../software-setup.md)).

## Goal

At the end of this phase, you can:

- Build an API test suite with an HTTP client, fixtures, test data, and parametrized tests from your test design.
- Validate API responses against a schema.
- Build a UI test suite with Playwright: locators, auto-waits, web-first assertions, traces.
- Apply the page object pattern.
- Make tests independent, repeatable, and safe to run in parallel.
- Find and remove the causes of flaky tests.
- Use a manual API tool, test doubles for HTTP services, and network interception in UI tests.
- Run UI tests on several browsers, and compare screenshots with baselines.
- Test WebSocket events and OAuth 2.0 token access.

## Reading

| Source | Part |
|---|---|
| requests documentation (requests.readthedocs.io) | "Quickstart", "Advanced usage": sessions, timeouts |
| Playwright for Python documentation (playwright.dev/python) | "Getting started", "Writing tests", "Locators", "Assertions", "Auto-waiting", "Trace viewer", "Test generator" |
| Brian Okken, *Python Testing with pytest*, 2nd edition | The chapters about fixtures, parametrization, and plugins |
| Martin Fowler, "PageObject" (martinfowler.com/bliki/PageObject.html) | All |
| Martin Fowler, "Eradicating Non-Determinism in Tests" (martinfowler.com) | All |
| The OpenAPI document of the shop (`http://127.0.0.1:8000/docs`) | All endpoints |
| Playwright for Python documentation | "Network" (routes and mocks), "Screenshots", "Browsers" |
| The documentation of `responses`, WireMock, and `websockets` | The basic usage pages |
| RFC 6749 (OAuth 2.0), sections 1, 4.4, and 5; RFC 9700 (OAuth 2.0 Security Best Current Practice) | Overview |
| RFC 6455 (the WebSocket protocol), section 1 | Overview |

## Topics

### 6.1 The project and its configuration

- Work in `labs/tas/`. Add the dependencies:

  ```sh
  uv add --dev pytest requests jsonschema pytest-playwright pytest-xdist pytest-randomly
  uv run playwright install --with-deps chromium
  ```

- Configuration comes from the environment (see `AGENTS.md`, "Code conventions"). One settings object reads it:

  ```python
  # src/shoptest/core/config.py
  import os
  from dataclasses import dataclass


  @dataclass(frozen=True)
  class Settings:
      shop_url: str
      admin_password: str
      timeout_seconds: float


  def load_settings() -> Settings:
      return Settings(
          shop_url=os.environ.get("SHOP_URL", "http://127.0.0.1:8000").rstrip("/"),
          admin_password=os.environ["ADMIN_PASSWORD"],
          timeout_seconds=float(os.environ.get("HTTP_TIMEOUT", "10")),
      )
  ```

- Put local values in `.env` (ignored by git) and dummy values in `.env.example`. Run with `uv run --env-file .env pytest`.

### 6.2 What an API test checks

| Check | Example |
|---|---|
| Status code | `201` for a new user, `422` for a user name with 2 characters |
| Body content | The total of the cart is `"52.98"` |
| Body structure | The response matches the schema (topic 6.5) |
| Headers | `content-type: application/json`, `x-request-id` is present |
| Side effects | After an order, the stock is lower and the cart is empty (check with a second request) |
| Error messages | The response has an `error` field and a `details` entry for each field that is not valid |
| Non-functional | The response time is less than 500 ms (R7.1). No password in the response (R7.4). |

Test positive and negative cases. Negative API tests (wrong types, missing fields, unknown IDs, no token, a token of a different user) find many defects, because UIs usually prevent these inputs.

### 6.3 An API client class

Do not repeat URLs, headers, and timeouts in each test. Put them in a class (OOP from phase 1: encapsulation):

```python
# src/shoptest/api/client.py
from typing import Any

import requests


class ShopApi:
    """Thin client for the course shop API. It does not assert: tests assert."""

    def __init__(self, base_url: str, timeout_seconds: float = 10) -> None:
        self._base_url = base_url
        self._timeout = timeout_seconds
        self._session = requests.Session()

    def request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        return self._session.request(method, f"{self._base_url}{path}", timeout=self._timeout, **kwargs)

    def register(self, username: str, password: str, email: str, age: int, member: bool = False) -> requests.Response:
        body = {"username": username, "password": password, "email": email, "age": age, "member": member}
        return self.request("POST", "/api/users", json=body)

    def login(self, username: str, password: str) -> requests.Response:
        response = self.request("POST", "/api/auth/login", json={"username": username, "password": password})
        if response.status_code == 200:
            self._session.headers["Authorization"] = f"Bearer {response.json()['token']}"
        return response
```

- Always set a **timeout**. Without it, a test can wait forever when the SUT hangs.
- The client returns the response. The test decides what is correct. Then the same client works for positive and negative tests.

### 6.4 Test data and fixtures

- Each test makes its own data. Use unique names, so that tests do not collide:

  ```python
  # tests/conftest.py
  import uuid

  import pytest

  from shoptest.api.client import ShopApi
  from shoptest.core.config import Settings, load_settings


  @pytest.fixture(scope="session")
  def settings() -> Settings:
      return load_settings()


  @pytest.fixture
  def api(settings: Settings) -> ShopApi:
      return ShopApi(settings.shop_url, settings.timeout_seconds)


  @pytest.fixture
  def user(api: ShopApi) -> dict[str, str]:
      """A new registered user. The api fixture is logged in as this user."""
      name = f"u{uuid.uuid4().hex[:12]}"
      password = "secret123"
      assert api.register(name, password, f"{name}@example.test", 30).status_code == 201
      assert api.login(name, password).status_code == 200
      return {"username": name, "password": password}
  ```

- **Fixture scope:** `function` (default, new for each test), `module`, `session`. A wider scope is faster but shares state. Share only data that no test changes.
- **The reset endpoint and parallel runs:** `POST /api/admin/reset` resets the whole shop. If tests run in parallel (`pytest -n 4`), a reset in one test deletes the users of the other tests. Use the reset only at the start of a run, or in tests that run alone. Prefer unique data.
- **Shared data that tests change:** the stock of a book is shared by all users. A test that checks the stock after an order must not assume an exact stock value, unless it owns the book. Check the change (before and after), or use a book that only this test buys.

### 6.5 Schema validation

- A **schema** describes the structure of a response: field names, types, required fields. A schema check finds changes in the API contract.
- The shop publishes an OpenAPI document. Its schemas are JSON Schema, so you can use them directly:

  ```python
  # src/shoptest/core/schemas.py
  from functools import cache
  from typing import Any

  import jsonschema
  import requests


  @cache
  def openapi(base_url: str) -> dict[str, Any]:
      spec: dict[str, Any] = requests.get(f"{base_url}/openapi.json", timeout=10).json()
      return spec


  def validate(base_url: str, instance: Any, schema_name: str) -> None:
      spec = openapi(base_url)
      schema = {"$ref": f"#/components/schemas/{schema_name}", "components": spec["components"]}
      jsonschema.validate(instance, schema)
  ```

- The CTAL-TAE syllabus names schema validation as a way to improve API tests (chapter 8).

### 6.6 Data-driven API tests from your test design

Use `pytest.mark.parametrize` for the test cases of phase 3. Give each case an ID, so that the report shows which case failed:

```python
@pytest.mark.parametrize(
    ("age", "expected_status"),
    [
        pytest.param(15, 422, id="age-15-below-lower-boundary"),
        pytest.param(16, 201, id="age-16-lower-boundary"),
        pytest.param(17, 201, id="age-17-above-lower-boundary"),
        pytest.param(119, 201, id="age-119-below-upper-boundary"),
        pytest.param(120, 201, id="age-120-upper-boundary"),
        pytest.param(121, 422, id="age-121-above-upper-boundary"),
    ],
)
def test_registration_age_boundaries(api: ShopApi, age: int, expected_status: int) -> None:
    name = f"u{uuid.uuid4().hex[:12]}"

    response = api.register(name, "secret123", f"{name}@example.test", age)

    assert response.status_code == expected_status, response.text
```

Put `response.text` in the assertion message. When the test fails, the report shows the error from the shop.

### 6.7 UI automation with Playwright

- Playwright controls a real browser (Chromium, Firefox, WebKit). pytest-playwright gives the fixtures `page`, `context`, and `browser`.
- Set the base URL from the settings:

  ```python
  # tests/ui/conftest.py
  import pytest

  from shoptest.core.config import Settings


  @pytest.fixture(scope="session")
  def base_url(settings: Settings) -> str:
      return settings.shop_url
  ```

- **Locators** find elements. Prefer, in this order:
  1. `page.get_by_role("button", name="Log in")`: the way users and assistive technology see the page.
  2. `page.get_by_label("User name")`, `page.get_by_text(...)`.
  3. `page.get_by_test_id("cart-count")`: the `data-testid` attributes of the shop. Stable when the layout changes.
  4. CSS or XPath only when nothing else works. Never long paths such as `div > div:nth-child(3) > span`.
- **Web-first assertions** wait until the condition is true, or until the timeout:

  ```python
  from playwright.sync_api import Page, expect


  def test_search_finds_the_linux_book(page: Page) -> None:
      page.goto("/products")

      page.get_by_test_id("search-input").fill("Linux")
      page.get_by_role("button", name="Search").click()

      expect(page.get_by_test_id("product-row")).to_have_count(1)
      expect(page.get_by_test_id("product-row")).to_contain_text("The Linux Shell Diaries")
  ```

- Useful options: `--headed` (show the browser), `--slowmo 500`, `--browser firefox`, `--tracing retain-on-failure`, `--screenshot only-on-failure`. Open a trace with `uv run playwright show-trace <file>`.
- **Codegen** records your actions as code: `uv run playwright codegen http://127.0.0.1:8000`. Use it to find locators, not as the final test code (CTAL-TAE section 3.1.4 lists the disadvantages of capture and playback).

### 6.8 Waits and synchronization

- A UI changes after the action: a request goes to the server, a script updates the page. A test that checks too early fails. A test that waits a fixed time is slow and still fails when the system is slower.
- **Never use `time.sleep()` or `page.wait_for_timeout()` to wait for the SUT.**
- Playwright waits automatically before actions (the element must be visible, enabled, and stable) and in `expect` assertions.
- Use `expect(locator).to_have_text(...)` in place of `assert locator.inner_text() == ...`. The first one waits. The second one reads one time.
- Test your waits: start the shop with `SUT_SLOW_UI=1 SUT_LATENCY_MS=800`. A correct test still passes, only slower.

### 6.9 The page object pattern

- A **page object** is a class for one page (or one component, such as the header). It contains the locators and the actions of the page. Tests use the page objects, not the locators.
- When the page changes, you change one class. The CTAL-TAE syllabus explains this pattern in section 3.1.5.

  ```python
  # src/shoptest/ui/pages/login_page.py
  from playwright.sync_api import Page


  class LoginPage:
      def __init__(self, page: Page) -> None:
          self.page = page
          self.username = page.get_by_test_id("username-input")
          self.password = page.get_by_test_id("password-input")
          self.submit = page.get_by_test_id("login-button")
          self.error = page.get_by_test_id("login-error")

      def open(self) -> "LoginPage":
          self.page.goto("/login")
          return self

      def log_in(self, username: str, password: str) -> None:
          self.username.fill(username)
          self.password.fill(password)
          self.submit.click()
  ```

  ```python
  def test_wrong_password_shows_an_error(page: Page, user: dict[str, str]) -> None:
      login = LoginPage(page).open()

      login.log_in(user["username"], "wrong-password-1")

      expect(login.error).to_have_text("The user name or the password is wrong.")
  ```

- **Rules:** page objects contain no assertions (the test asserts). Page objects expose actions in the language of the user ("log in", "add to cart"), not of the HTML ("click button 3"). A component (for example the header with the cart count) is its own class, and pages contain it (composition).

### 6.10 Fast setup through the API

- UI tests are slow. Do the setup through the API, and use the UI only for the behavior under test.
- Example: log in through the API, and give the session cookie to the browser:

  ```python
  from playwright.sync_api import BrowserContext


  def log_in_browser(context: BrowserContext, base_url: str, token: str) -> None:
      context.add_cookies([{"name": "session", "value": token, "url": base_url}])
  ```

- Also put books in the cart through the API before a UI test of the cart page.

### 6.11 Flaky tests

- A **flaky test** passes and fails without a change in the code or the test. It destroys trust in the suite.
- Common causes and fixes:

  | Cause | Fix |
  |---|---|
  | Fixed waits, or no wait | Web-first assertions, polling with a timeout |
  | Shared test data, order dependency | Unique data for each test, no reset during parallel runs |
  | Random data that sometimes hits a boundary | Control the random data, or record the seed |
  | Time and dates | Do not depend on the current time, or control it (for example `SUT_LOCK_MINUTES`) |
  | Environment (slow host, network) | Correct timeouts, health check before the run |
  | Animations, scroll position | Playwright actionability checks, stable locators |

- Find order dependencies with pytest-randomly: when it is installed, each run uses a random order and prints the seed. Repeat an order with `--randomly-seed=<seed>`. Find shared-state problems with `pytest -n 4` (parallel).
- An automatic rerun of failed tests (for example `pytest-rerunfailures`) hides flaky tests. If you use it, report each rerun, and fix the cause.

### 6.12 Manual API tools

- Tools such as **Postman**, **Insomnia**, and **Bruno** send HTTP requests from a user interface. Testers use them to explore an API, to reproduce a defect, and to share a request with a developer.
- Main features:
  - **Collections:** saved requests in folders.
  - **Environments and variables:** `{{baseUrl}}`, `{{token}}`. The same collection runs against different environments.
  - **Scripts:** a script before a request (for example to make unique data), and test scripts after it (assertions on the status and the body, and saving values such as a token into a variable).
  - **A command-line runner:** for example Newman or the Postman CLI for Postman, `bru run` for Bruno, `inso` for Insomnia. A collection can then run in a pipeline.
- **Version control:** Bruno saves each request as a text file, so the collection goes into git. Postman and Insomnia can export a collection as JSON. Some tools synchronize collections to the cloud of the vendor: read the terms and the security settings of your company.
- **Secrets:** do not put passwords or tokens in a collection that you share or commit. Use local environment values or secret variables.
- **Code or tool?** A tool is fast for exploration. A regression suite in code (topics 6.3–6.6) is easier to review, to refactor, and to combine with UI tests and test data. Many teams use both.

### 6.13 Test doubles for HTTP services

- A system often calls other services: a payment provider, a shipping service, an exchange rate service. In a test, the real service can be unavailable, slow, expensive, or impossible to make fail on purpose.
- A **test double for an HTTP service** answers in place of the real service. Two common levels:

  | Level | Tool examples | Use |
  |---|---|---|
  | In the process: replace the HTTP library | `responses` (for requests), `respx` (for httpx), MSW or nock (JavaScript) | Component tests of your own HTTP client code. Very fast, no network. |
  | A stub server on the network | WireMock (a container), Mockoon, Prism (from an OpenAPI document) | System and integration tests of a system that calls the service. Also called **service virtualization**. |

- A stub server can also simulate faults: slow answers, HTTP 500, a reset connection, broken JSON. You can then test timeouts, retries, and error messages.
- **Risk:** a stub can drift away from the real service. Then the tests pass, and production fails. Contract tests (phase 8, topic 8.5) find this drift.
- **Example: a component test of your own API client with `responses`.** The shop does not run for this test:

  ```python
  # tests/core/test_shop_api_client.py
  import responses

  from shoptest.api.client import ShopApi


  @responses.activate
  def test_login_adds_the_bearer_token_to_later_requests() -> None:
      responses.post("http://shop.test/api/auth/login", json={"token": "abc", "username": "anna"})
      responses.get("http://shop.test/api/cart", json={"items": []})
      api = ShopApi("http://shop.test")

      api.login("anna", "secret123")
      api.request("GET", "/api/cart")

      assert responses.calls[1].request.headers["Authorization"] == "Bearer abc"
  ```

- **Example: a WireMock stub.** WireMock reads JSON mapping files from the directory `mappings/`:

  ```json
  {
    "request": { "method": "GET", "urlPath": "/rates", "queryParameters": { "from": { "equalTo": "EUR" } } },
    "response": {
      "status": 200,
      "headers": { "Content-Type": "application/json" },
      "jsonBody": { "from": "EUR", "to": "USD", "rate": 1.08 }
    }
  }
  ```

  A response with `"fixedDelayMilliseconds": 3000` is slow. A response with `"fault": "CONNECTION_RESET_BY_PEER"` breaks the connection. Read the WireMock documentation ("Stubbing", "Simulating faults") for all options.

### 6.14 Network interception in UI tests

- Playwright can intercept the requests of the page. A test can then answer a request itself, change it, or stop it:

  | Method | Effect |
  |---|---|
  | `page.route(pattern, handler)` | Sends each matching request to the handler |
  | `route.fulfill(status=..., json=...)` | Answers with your own response. The server gets no request. |
  | `route.abort()` | Stops the request, as if the network fails |
  | `route.continue_()` | Sends the request to the server without a change |
  | `page.expect_response(pattern)` | Waits for a response, so that the test can check it |

- **Use it for** states that are difficult to make with the real SUT: server errors, network failures, empty lists, very long texts. Also to check the request that the page sends.
- **Do not overuse it.** A UI test with all requests mocked does not test the integration with the server. Keep most UI tests against the real SUT, and use interception for the error states.
- **Example:** R4.8 requires an error message when the removal of a book fails. The fixture `cart_with_one_book` logs the browser in and puts one book in the cart through the API (topic 6.10):

  ```python
  # tests/ui/test_cart_errors.py
  from playwright.sync_api import Page, Route, expect


  def test_server_error_on_removal_shows_a_message(page: Page, cart_with_one_book: None) -> None:
      def fail_deletes(route: Route) -> None:
          if route.request.method == "DELETE":
              route.fulfill(status=500, json={"error": "Internal server error."})
          else:
              route.continue_()

      page.route("**/api/cart/items/*", fail_deletes)
      page.goto("/cart")

      page.get_by_test_id("remove-button").click()

      expect(page.get_by_test_id("cart-message")).to_have_text("Internal server error.")
      expect(page.get_by_test_id("cart-row")).to_have_count(1)
  ```

### 6.15 Cross-browser testing

- Users have different browsers. Playwright has three browser engines: **Chromium** (Chrome, Edge), **Firefox**, and **WebKit** (the engine of Safari). It can also use the installed Chrome or Edge (`--browser-channel chrome`).
- Install the engines: `uv run playwright install --with-deps firefox webkit`.
- Run one suite on several browsers: `uv run pytest tests/ui --browser chromium --browser firefox --browser webkit`. Each test then runs one time for each browser, and the test ID shows the browser.
- Typical differences: form controls (for example date and number fields), fonts and layout, timing, keyboard behavior, and browser-specific defects in the SUT.
- **Cost:** three browsers make the UI suite three times longer. A common strategy: the full UI suite on one browser in each pipeline run, and a smoke subset on all browsers (for example every night).

### 6.16 Visual regression testing

- A **visual test** compares a screenshot with an approved **baseline** image. It finds changes that functional assertions do not see: a broken layout, a hidden button, wrong colors, overlapping text.
- **Sources of false failures:** different fonts and font rendering on different operating systems, dynamic data (dates, user names, random content), animations, the cursor, and the viewport size.
- **Rules:**
  - Make the baselines and run the comparisons in the same environment, for example the same Playwright container image.
  - Use a fixed viewport, disable animations, and mask dynamic areas: `page.screenshot(path=..., animations="disabled", mask=[locator])`.
  - Use a small tolerance for anti-aliasing.
  - A change of a baseline is a decision. A person reviews the new image before it becomes the baseline.
- **Tools:** Playwright Test (TypeScript) has a built-in assertion `toHaveScreenshot()`. In Python, write a small comparison with Pillow, or use a plugin. There are also commercial visual testing services.
- **Example:** a simple comparison with Pillow:

  ```python
  # src/shoptest/core/visual.py
  from pathlib import Path

  from PIL import Image, ImageChops


  def changed_ratio(actual: Path, baseline: Path, diff: Path, tolerance: int = 16) -> float:
      """Return the part of the pixels that changed more than the tolerance. Save a diff image."""
      with Image.open(actual) as new, Image.open(baseline) as old:
          if new.size != old.size:
              raise AssertionError(f"The size changed from {old.size} to {new.size}.")
          delta = ImageChops.difference(new.convert("RGB"), old.convert("RGB")).convert("L")
      changed = delta.point(lambda value: 255 if value > tolerance else 0)
      changed.save(diff)
      return changed.histogram()[255] / (changed.width * changed.height)
  ```

### 6.17 WebSocket testing

- A **WebSocket** is a connection that stays open after an HTTP handshake (status `101 Switching Protocols`). The server and the client can both send messages at any time. Addresses start with `ws://`, or `wss://` with TLS. RFC 6455 defines the protocol.
- Applications use WebSockets for live data: notifications, chat, prices, status changes. The course shop sends order events (R9).
- **What to test:** the authentication of the connection, the format and the schema of each message, the order of the messages, the time until a message arrives, that a user gets only their own data, and the behavior when the connection closes.
- **Event-based waits:** a test that waits for an event is faster and more reliable than a test that polls the status again and again. The CTAL-TAE syllabus names a subscription to the events of the SUT as the best wait mechanism (section 8.1.2). Always use a timeout.
- **Example** with the `websockets` package:

  ```python
  # tests/api/test_order_events.py
  import json

  from websockets.sync.client import connect

  from shoptest.api.client import ShopApi
  from shoptest.core.config import Settings


  def test_paying_an_order_sends_a_status_event(api: ShopApi, user: dict[str, str], settings: Settings) -> None:
      token = api.login(user["username"], user["password"]).json()["token"]
      api.request("POST", "/api/cart/items", json={"product_id": 5, "quantity": 1})
      url = settings.shop_url.replace("http", "ws", 1) + f"/api/ws/orders?token={token}"

      with connect(url, open_timeout=5) as events:
          assert json.loads(events.recv(timeout=5))["event"] == "subscribed"
          order = api.request("POST", "/api/orders").json()
          assert json.loads(events.recv(timeout=5))["event"] == "order_placed"

          api.request("POST", f"/api/orders/{order['id']}/pay")
          event = json.loads(events.recv(timeout=5))

      assert (event["order_id"], event["old"], event["new"]) == (order["id"], "NEW", "PAID")
  ```

- A token in a URL can appear in the logs of servers and proxies. Browsers send the session cookie in place of it. Prefer `wss://` in real systems.
- Playwright can also observe the WebSockets of a page (`page.on("websocket", ...)`).

### 6.18 OAuth 2.0 and token-based API access

- **OAuth 2.0** (RFC 6749) lets a client get an **access token** from an **authorization server**, and use it at a **resource server** (the API). The token has a **scope** (what the client may do) and an expiry time.
- **Grants** (ways to get a token):

  | Grant | Use |
  |---|---|
  | Authorization code with PKCE | A user logs in at the authorization server in a browser. For web, mobile, and desktop applications. |
  | Client credentials | A system calls an API for itself, without a user. Machine-to-machine. |
  | Refresh token | Get a new access token without a new login |

  The older "password" and "implicit" grants are not recommended any more (OAuth 2.0 Security Best Current Practice, RFC 9700).
- The client sends the token in the header `Authorization: Bearer <token>`. Some tokens are JSON Web Tokens (JWT) with readable claims. The course shop uses opaque tokens: random strings without content.
- **What to test** (the course shop: R8):
  - The token request: the correct grant, each client authentication method, the response fields, the `Cache-Control: no-store` header.
  - The error responses of RFC 6749, section 5.2: wrong credentials, missing parameters, an unsupported grant, a wrong scope.
  - **Least privilege:** each action that the scope permits works, and each action that it does not permit fails with 403.
  - **Expiry:** a token works before its expiry and fails after it. Use a short lifetime in the test environment (`SUT_OAUTH_TOKEN_SECONDS`).
  - No token, secret, or password in logs, URLs, or test reports.
- **In the TAS:** a token provider class gets a token, keeps it, and gets a new one shortly before the expiry. Tests then never use an expired token by accident.
- Get a token with requests. The client ID and the secret come from the configuration, not from the code:

  ```python
  response = requests.post(
      f"{settings.shop_url}/api/oauth/token",
      data={"grant_type": "client_credentials"},
      auth=(client_id, client_secret),
      timeout=10,
  )
  token = response.json()["access_token"]
  ```

## Exercises

All code goes in `labs/tas/` (main project, stage 2). Start with a simple structure: `src/shoptest/api/`, `src/shoptest/ui/pages/`, `src/shoptest/core/`, `tests/api/`, `tests/ui/`. Phase 7 improves the structure.

### Exercise 6.1: Setup

1. Add the dependencies of topic 6.1. Make `Settings`, `.env`, `.env.example`, and the `settings` and `api` fixtures.
2. Make `pytest` start only when the shop answers: add a session fixture that calls `/api/health` and stops the run with a clear message if the shop does not answer.
3. Update the README.

### Exercise 6.2: First API tests

1. Test `GET /api/health`, `GET /api/products` (default page size, page 3, page size 51), and `GET /api/products/1`.
2. Test a book ID that does not exist. What does R3.6 and R7.2 expect?
3. Check the headers of one response.

### Exercise 6.3: Registration and login

1. Write the `ShopApi` client (topic 6.3).
2. Automate your phase 3 test cases for R1 and R2 with `parametrize` and IDs. Include the account lock (R2.3–R2.6). Start the shop with a short lock time.
3. Check that no response contains the password (R7.4).

### Exercise 6.4: Cart and prices

1. Add the cart and order methods to the client. Add a `user` fixture and a `member` fixture.
2. Automate your BVA test cases for R4 and R5.8, and your decision table for R5.2–R5.7. Calculate the expected values in the test data, not with the same formula as the shop.
3. Check the side effects: the stock after an order, the empty cart.

### Exercise 6.5: Order status

1. Automate your all-transitions test cases from phase 3 (R6.5). Use an `admin` fixture for `ship` and `deliver`.
2. Check R6.6 (stock back after cancel) and R6.7 (a user does not see the orders of a different user).

### Exercise 6.6: Schema validation

1. Write `validate()` (topic 6.5). Validate the responses of the products, cart, and order endpoints.
2. Change one schema name on purpose, and show that the test fails with a clear message.

### Exercise 6.7: First UI tests

1. Use `playwright codegen` to explore the login and the search. Read the generated locators. Rewrite them with the preferred locators of topic 6.7.
2. Write UI tests for: a successful login, a failed login, the search, and the pagination.
3. Run them with `--headed`, then headless. Make one test fail on purpose and open its trace.

### Exercise 6.8: Page objects

1. Write page objects for the login page, the catalog, the product page, and the cart page, and a component object for the header.
2. Write UI tests for: add a book to the cart (check the cart count), remove a book from the cart (check the cart count and the total), apply a coupon, and place an order.
3. Do the login and the cart setup through the API (topic 6.10) where the test does not test the login.

### Exercise 6.9: A manual API tool

1. Install Postman, Insomnia, or Bruno. (Bruno saves the collection as files that you can commit.)
2. Make a collection for the shop: health, register, log in, add to cart, read the cart, place an order, pay. Use an environment with the variable `baseUrl`.
3. In the login request, add a script that saves the token in a variable. Use the variable in the `Authorization` header of the next requests.
4. Add test scripts: the status code and one field of the body for each request. Make the user name unique with a script or a dynamic variable.
5. Run the collection from the command line with the runner of the tool. Export or save the collection in `labs/tas/api-collection/`. Check that no password or token is in the files.
6. Compare the collection with your pytest suite: what is easier in each one?

### Exercise 6.10: Test doubles for HTTP services

1. Add `responses`. Write component tests for your `ShopApi` client that do not need the shop: the login adds the bearer header, a timeout is set on each request, an error response goes back to the test without a change.
2. The shop team plans a currency feature: the shop will call an exchange rate service, but the service is not ready. Write a small `RateClient` class with a method `rate(source, target) -> Decimal`. It raises `RateServiceError` for a server error, a timeout, and an answer that is not valid JSON.
3. Start WireMock in a container (read the WireMock Docker documentation for the image and the port). Write mappings for: a normal answer, a slow answer (longer than the timeout of the client), HTTP 500, a reset connection, and a broken body.
4. Test `RateClient` against each mapping.
5. Explain how a contract test (phase 8) can protect these tests when the real service exists.

### Exercise 6.11: Network interception in UI tests

1. Test R4.8 with `page.route`: a server error on the removal of a book, and a network failure (`route.abort()`). Check the message, the cart rows, and the cart count.
2. Mock an error response for "Add to cart" (for example HTTP 422 with an error text). Check that the product page shows the text.
3. Use `page.expect_response` to check the request that the product page sends when you add 3 copies: the method, the path, and the JSON body.
4. Explain which risks these tests cover, and which risks they do not cover because the server is mocked.

### Exercise 6.12: Cross-browser testing

1. Install Firefox and WebKit for Playwright.
2. Run your UI suite on Chromium, Firefox, and WebKit. Record the results and the duration for each browser.
3. For each failure, decide: a defect in the shop, a defect in the test, or a real difference between browsers. Fix the tests where necessary.
4. Mark a smoke subset of UI tests that must run on all browsers. Explain your selection and the cost.

### Exercise 6.13: Visual regression testing

1. Write the comparison function of topic 6.16 and a fixture that compares a screenshot with a baseline in `tests/ui/baselines/`. If the baseline does not exist, the fixture saves the screenshot as the new baseline and marks the test as skipped with a message.
2. Write visual tests for the catalog, a product page, and the cart. Mask the dynamic areas (for example the user name).
3. Run each test 5 times. Fix the causes of false failures.
4. Change the CSS of the shop in your working copy (for example a margin in `sut/app/static/style.css`), and restart the shop. Show the diff image. Restore the file with `git restore sut/`.
5. Explain why the baselines must come from the same environment as the test runs.

### Exercise 6.14: WebSocket testing

1. Add the `websockets` package. Write the test of topic 6.17.
2. Test each requirement of R9: the rejection without a valid token (R9.2), the first message (R9.3), the events of a new order and of each status change (R9.4), no events from the orders of other users (R9.5), and the time limit of 1 second (R9.6).
3. Test that the administrator gets the events of all orders.
4. Rewrite one test of exercise 6.5 that waits for a status change: wait for the event in place of a poll of `GET /api/orders/{id}`. Compare the duration.

### Exercise 6.15: OAuth 2.0

1. Test the token endpoint against R8: both client authentication methods, the response fields and headers, and each error of R8.7.
2. Test the permissions of the scope (R8.6): the API client can read all orders, ship, and deliver. Pay and cancel fail with 403.
3. Start the shop with `SUT_OAUTH_TOKEN_SECONDS=5`. Test that a token works before its expiry and fails with 401 after it. (This is the one place where a wait for a time is correct: the test waits for a time limit, not for the SUT.)
4. Write a `TokenProvider` class: it gets a token, keeps it, and gets a new one 30 seconds before the expiry. Give it the clock as a dependency (phase 1, topic 1.9), so that a unit test can control the time without a wait. Test it with `responses` and a fake clock.
5. Use the `TokenProvider` in an `api_client` fixture for the shipping service. Check the test logs: no token and no secret appears.

### Exercise 6.16: Robust and complete (main project, stage 2)

1. Run the full suite in random order (pytest-randomly) and in parallel: `uv run pytest -n 4`. Run it three times. Fix all failures that come from the test design.
2. Run the UI suite 5 times with `SUT_SLOW_UI=1 SUT_LATENCY_MS=800`. Fix each failure.
3. Run the full suite against `SUT_DEFECTS=none`: all tests pass. Then against `SUT_DEFECTS=all`: list the failed tests. Read each failure message: does it tell you the failure without a look at the code?
4. Check the acceptance criteria of stage 2 in [../projects/test-automation-solution.md](../projects/test-automation-solution.md).

**Side project (optional):** build a small API suite for a public practice API that permits automated tests (for example restful-booker). Read the terms of the site first. Do not send many requests.

## Done criteria

- [ ] My API suite covers R1–R6 with the test cases of phase 3, with parametrized tests and IDs.
- [ ] My API tests validate the response schemas.
- [ ] My UI tests use preferred locators, web-first assertions, and no fixed waits.
- [ ] My UI tests use page objects without assertions.
- [ ] My tests pass in random order and in parallel.
- [ ] My UI tests pass 5 times in sequence with the slow UI and latency on.
- [ ] I can explain the causes of flaky tests and how to remove them.
- [ ] I can build and run an API collection in a manual API tool without secrets in the files.
- [ ] I can test my own HTTP client code with `responses`, and a client of an unavailable service with WireMock stubs and faults.
- [ ] I can test UI error states with network interception, and I can explain its limits.
- [ ] I can run UI tests on Chromium, Firefox, and WebKit, and select a cross-browser subset.
- [ ] I can run visual comparisons with stable baselines, masks, and a tolerance.
- [ ] I can test WebSocket events with timeouts, and use an event in place of polling.
- [ ] I can test an OAuth 2.0 client credentials flow: errors, scopes, and expiry.
- [ ] Stage 2 of the main project is complete.

## Next

[Phase 7: Test automation architecture](phase-7-automation-architecture.md)
