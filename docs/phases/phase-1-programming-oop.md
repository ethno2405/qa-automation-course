# Phase 1: Programming and OOP for Testers

**Time:** 1 week if you program in an object-oriented language at work. 3–4 weeks if you can write small programs. 6–8 weeks if you never programmed. Do this phase in parallel with phase 0.
**Prerequisites:** None.
**Environment:** Your language (reference: Python 3.13 or newer with `uv`), an editor, and a terminal. See [../software-setup.md](../software-setup.md).

## Goal

At the end of this phase, you can:

- Write programs with variables, functions, conditions, loops, collections, files, JSON, and exceptions.
- Explain and use the four OOP principles: encapsulation, abstraction, inheritance, and polymorphism.
- Use composition and dependency injection, and explain why they make code easy to test.
- Explain the SOLID principles with examples.
- Use type hints and a type checker.
- Write unit tests with pytest: assertions, fixtures, parametrized tests, and test doubles.
- Make a project with dependencies and a virtual environment.

## Why a tester needs to program

Test automation is software development. The CTAL-TAE syllabus says this directly (section 3.1.5), and it names the OOP principles, the SOLID principles, and design patterns as knowledge of a test automation engineer (LO TAE-3.1.5). A page object is a class. A test fixture is a function. A test framework is a program with layers. In this phase, you learn the programming that you need for phases 6–9.

## Reading

| Source | Part |
|---|---|
| The official Python tutorial (docs.python.org/3/tutorial) | Chapters 1–9. Use it as the main source if you never programmed. |
| Eric Matthes, *Python Crash Course*, 3rd edition | Part 1 (basics, classes, files, exceptions, testing). A good alternative to the tutorial. |
| Brian Okken, *Python Testing with pytest*, 2nd edition | The chapters about test functions, fixtures, and parametrization |
| Freeman and Robson, *Head First Design Patterns*, 2nd edition | Optional. The chapter about the first principles. Examples are in Java. |
| The pytest documentation (docs.pytest.org) | "Get started", "How to use fixtures", "How to parametrize" |

For Java, C#, or TypeScript, ask the mentor for the matching sources. See [../languages.md](../languages.md).

## Topics

### 1.1 How a program runs

- A program is a list of instructions. The Python **interpreter** reads a `.py` file and executes it from top to bottom.
- Run a file: `uv run python hello.py`. Start the interactive shell (the REPL): `uv run python`. Use the REPL to try small pieces of code.
- An error stops the program with a **traceback**. Read a traceback from the bottom: the last line names the error, the lines above show where it happened.
- Compare with compiled languages: Java and C# compile the code first, and the compiler finds type errors before the program runs. TypeScript compiles to JavaScript. Python finds most errors only when the line runs. This is why tests and type checkers (topic 1.11) are important in Python.

### 1.2 Values, variables, and control flow

- Basic types: `int` (whole numbers), `float` (decimal numbers, not exact), `str` (text), `bool` (`True`, `False`), `None` (no value).
- **Money and floats:** `0.1 + 0.2` is not exactly `0.3` in binary floating point. For prices, use `decimal.Decimal("0.10")`. The course shop uses `Decimal`. Many defects in real shops come from floats.
- Operators: `+ - * / // % **`, comparisons `== != < <= > >=`, logic `and or not`.
- Conditions: `if`, `elif`, `else`. Loops: `for item in items:`, `while condition:`, `break`, `continue`.
- `match` (Python 3.10 and newer) compares a value with patterns. It is similar to `switch` in other languages.

### 1.3 Functions and modules

- A function has a name, parameters, a body, and a return value: `def shipping_cost(order_value: Decimal) -> Decimal:`.
- Parameters can have default values and names: `search("test", page=2)`.
- A function must do one thing. A short function with a good name is easy to test.
- A **module** is a `.py` file. A **package** is a directory of modules. Use `import` to use code from a module.
- Use `if __name__ == "__main__":` for code that runs only when the file is the main program.

### 1.4 Collections, text, files, JSON, and exceptions

- **Collections:**

  | Type | Use | Example |
  |---|---|---|
  | `list` | Ordered, changeable | `[1, 2, 3]` |
  | `tuple` | Ordered, not changeable | `(200, "OK")` |
  | `dict` | Key-value pairs | `{"status": "ok"}` |
  | `set` | Unique values, no order | `{"D01", "D04"}` |

- Comprehensions: `[p for p in products if p.stock > 0]`.
- Strings: f-strings `f"Total: {total} EUR"`, `split`, `join`, `strip`, `lower`, `startswith`.
- Files: `with open(path, encoding="utf-8") as f:`. Use `pathlib.Path` for paths.
- JSON: `json.loads(text)` makes a `dict` from JSON text. `json.dumps(data)` makes JSON text. API responses are JSON.
- **Exceptions:** `raise ValueError("message")` signals an error. `try: ... except ValueError as error: ...` handles it. Catch only the exceptions that you can handle. Never write `except:` without a type: it hides defects.

### 1.5 Classes and objects

- A **class** is a type that you define. An **object** (an instance) is one value of this type, with its own data.

  ```python
  from decimal import Decimal


  class Product:
      def __init__(self, title: str, price: Decimal, stock: int) -> None:
          self.title = title
          self.price = price
          self.stock = stock

      def is_available(self) -> bool:
          return self.stock > 0


  book = Product("The Boundary Hunter", Decimal("12.50"), 20)
  print(book.is_available())  # True
  ```

- `__init__` is the constructor. `self` is the object itself. Attributes (data) and methods (functions) belong to the object.
- A `@dataclass` writes the constructor, the comparison, and the text form for you. Use it for classes that mainly hold data, for example test data.
- **Common mistake:** a mutable class attribute (`items = []` in the class body) is shared by all objects. Make attributes in `__init__`.

### 1.6 Encapsulation

- **Encapsulation:** the object protects its data. Other code changes the data only through methods, and the methods keep the data valid.
- Python has no `private` keyword. The convention is a leading underscore: `self._items`. Other code must not use it. Java, C#, and TypeScript have `private`.
- A `@property` gives read access to a value without a public attribute:

  ```python
  class Cart:
      MAX_QUANTITY = 10

      def __init__(self) -> None:
          self._lines: dict[str, int] = {}

      def add(self, title: str, quantity: int) -> None:
          if not 1 <= quantity <= self.MAX_QUANTITY:
              raise ValueError("The quantity must be from 1 to 10.")
          self._lines[title] = self._lines.get(title, 0) + quantity

      @property
      def count(self) -> int:
          return sum(self._lines.values())
  ```

- Why it helps testing: the rules are in one place. You test the rules through the public methods, not through the internal data.

### 1.7 Inheritance and polymorphism

- **Inheritance:** a class (the subclass) gets the attributes and methods of a different class (the base class), and adds or changes some. `class AdminUser(User):`.
- `super().__init__(...)` calls the constructor of the base class.
- **Polymorphism:** code calls the same method on objects of different classes, and each class has its own behavior.

  ```python
  class Discount:
      def amount(self, subtotal: Decimal) -> Decimal:
          return Decimal("0.00")


  class PercentDiscount(Discount):
      def __init__(self, rate: Decimal) -> None:
          self.rate = rate

      def amount(self, subtotal: Decimal) -> Decimal:
          return subtotal * self.rate


  class FixedDiscount(Discount):
      def __init__(self, value: Decimal) -> None:
          self.value = value

      def amount(self, subtotal: Decimal) -> Decimal:
          return min(self.value, subtotal)


  for discount in [PercentDiscount(Decimal("0.05")), FixedDiscount(Decimal("5.00"))]:
      print(discount.amount(Decimal("40.00")))
  ```

- Use inheritance for a real "is a" relation. Deep class trees are hard to change. Test automation code often has a `BasePage` class with common page methods: keep it small.

### 1.8 Abstraction: interfaces and abstract classes

- **Abstraction:** the caller sees only what it needs (the "what"), not the details (the "how").
- An **abstract base class** defines methods that subclasses must implement:

  ```python
  from abc import ABC, abstractmethod


  class PaymentProvider(ABC):
      @abstractmethod
      def pay(self, order_id: int, amount: Decimal) -> bool: ...
  ```

- A **Protocol** (`typing.Protocol`) defines an interface by its methods only. A class matches the protocol if it has the methods. No inheritance is necessary. This is "structural typing".
- In Java, C#, and TypeScript, use `interface`.
- Callers depend on the interface, not on one class. Then you can give the caller a different class, for example a test double.

### 1.9 Composition and dependency injection

- **Composition:** an object contains other objects and uses them ("has a"). Example: an `OrderService` has a `PaymentProvider`.
- Prefer composition to inheritance when you want to combine behaviors.
- **Dependency injection:** an object gets its dependencies from outside, usually in the constructor. It does not make them itself.

  ```python
  class OrderService:
      def __init__(self, payments: PaymentProvider) -> None:
          self._payments = payments

      def pay(self, order_id: int, amount: Decimal) -> str:
          return "PAID" if self._payments.pay(order_id, amount) else "PAYMENT_FAILED"
  ```

- In a test, give a **test double** in place of the real dependency:

  ```python
  class FakePayments:
      def __init__(self, result: bool) -> None:
          self.result = result
          self.calls: list[tuple[int, Decimal]] = []

      def pay(self, order_id: int, amount: Decimal) -> bool:
          self.calls.append((order_id, amount))
          return self.result


  def test_failed_payment_gives_status_payment_failed() -> None:
      service = OrderService(FakePayments(result=False))

      assert service.pay(1001, Decimal("10.00")) == "PAYMENT_FAILED"
  ```

- Types of test doubles: a **stub** returns fixed answers. A **fake** has simple working logic. A **mock** records the calls so that the test can check them. A **spy** records the calls to a real object.

### 1.10 The SOLID principles

| Principle | Meaning | Example in test automation |
|---|---|---|
| **S**ingle responsibility | A class has one reason to change. | A page object knows one page. It does not also make test data. |
| **O**pen-closed | Add behavior with new code, not by changes to tested code. | A new payment type is a new class, not a new `if` in old code. |
| **L**iskov substitution | A subclass can replace its base class without surprises. | Each subclass of `BasePage` works where the code expects a `BasePage`. |
| **I**nterface segregation | Many small interfaces are better than one large one. | A test that only reads products depends on a small `CatalogReader`, not on the full API client. |
| **D**ependency inversion | High-level code depends on abstractions, not on details. | Tests use an `ApiClient` protocol. The HTTP library is a detail behind it. |

Use the principles to make decisions, not as strict rules. Small scripts do not need all of them.

### 1.11 Type hints and static checks

- Type hints document the types: `def add(self, title: str, quantity: int) -> None:`.
- Python does not check the hints when the program runs. A **type checker** (mypy) checks them before the program runs, like a compiler.
- Run `uv run mypy --strict src`. Fix each finding.
- A **linter** (ruff) finds style problems and likely errors. A **formatter** (`ruff format`) formats the code. Run them on every change.

### 1.12 Unit tests with pytest

- A test is a function with a name that starts with `test_`, in a file with a name that starts with `test_`. pytest finds and runs them.
- Use plain `assert`. pytest shows the values when an assertion fails.
- Structure each test as **arrange, act, assert** (AAA): prepare the data, do the action, check the result.

  ```python
  import pytest


  def test_cart_count_is_sum_of_quantities() -> None:
      cart = Cart()
      cart.add("A", 2)
      cart.add("B", 3)

      assert cart.count == 5


  def test_quantity_above_ten_is_rejected() -> None:
      cart = Cart()

      with pytest.raises(ValueError):
          cart.add("A", 11)
  ```

- **Fixtures** prepare data or objects for tests. A test gets a fixture by its parameter name:

  ```python
  @pytest.fixture
  def cart() -> Cart:
      return Cart()


  def test_new_cart_is_empty(cart: Cart) -> None:
      assert cart.count == 0
  ```

- **Parametrization** runs one test with several data sets. You use it for the test techniques of phase 3:

  ```python
  @pytest.mark.parametrize("quantity", [1, 10])
  def test_valid_quantities_are_accepted(cart: Cart, quantity: int) -> None:
      cart.add("A", quantity)

      assert cart.count == quantity
  ```

- Useful commands: `uv run pytest -v` (names), `-x` (stop at the first failure), `-k cart` (select by name), `--lf` (only the last failures).
- **TDD** (test-driven development): write a failing test (red), write the code that passes it (green), then improve the code (refactor). Phase 2 and phase 7 explain TDD as a test-first approach.

### 1.13 Projects, dependencies, and virtual environments

- A **virtual environment** is a separate set of packages for one project. Projects then do not break each other.
- `uv` makes and manages it:

  ```sh
  uv init --package shoplib     # make a project with src/ layout
  cd shoplib
  uv add --dev pytest ruff mypy # add development dependencies
  uv run pytest                 # run in the virtual environment
  ```

- `pyproject.toml` lists the dependencies and the tool settings. `uv.lock` records the exact versions. Commit both. Do not commit `.venv/`.
- Pin the versions through the lock file, so that a test run today and next month uses the same packages.

## Exercises

Do the exercises in `labs/phase-1-programming/`. Write tests for each exercise from exercise 1.5 on. Use `uv`, pytest, ruff, and mypy.

### Exercise 1.1: First programs

1. Write a program that prints the numbers 1 to 30. For multiples of 3, print "Test". For multiples of 5, print "Automation". For multiples of both, print "TestAutomation".
2. Write a program that asks for an age and prints whether the person can register in the course shop (R1.6 in [../../sut/REQUIREMENTS.md](../../sut/REQUIREMENTS.md)). Handle input that is not a number.

### Exercise 1.2: Functions

1. Write `shipping_cost(order_value: Decimal) -> Decimal` for the rule R5.8 of the course shop.
2. Write `is_valid_username(name: str) -> bool` for R1.2.
3. Call each function with 5 values. Print the values and the results.

### Exercise 1.3: Collections and text

1. Save a log of the course shop to a file (see phase 0, exercise 0.6).
2. Write a program that reads the file, parses each JSON line, and prints: the number of requests for each status code, the five slowest requests, and the number of each event type.
3. Compare the results with your shell pipeline from exercise 0.6.

### Exercise 1.4: Files, JSON, and exceptions

1. Write a program that reads a CSV file of test users (`username,password,email,age`) and writes a JSON file with only the valid users (use your functions from exercise 1.2).
2. Handle these errors with a clear message: the file does not exist, a line has the wrong number of fields, the age is not a number.

### Exercise 1.5: Classes

1. Write a `Product` dataclass and a `Catalog` class with the methods `add(product)`, `find(text)`, and `page(number, size)`. The search ignores the case (R3.3). The page rules follow R3.2.
2. Write tests for each method: normal cases, an empty search, the last page, a page that does not exist.

### Exercise 1.6: Encapsulation

1. Write a `Cart` class that follows R4.2, R4.3, and R4.5. The internal data is private. Use a `@property` for the count and the subtotal.
2. Write tests for the rules. Show that other code cannot put the cart in a state that breaks the rules.

### Exercise 1.7: Inheritance and polymorphism

1. Write the discount classes `MemberDiscount`, `PercentCoupon`, and `FixedCoupon` with one common method `amount(subtotal)`.
2. Write a function `best_discount(subtotal, discounts)` that applies rule R5.6 (only the larger discount, the coupon wins at equal amounts).
3. Write tests. Use parametrization.

### Exercise 1.8: Abstraction and dependency injection

1. Define a `PriceCalculator` that gets the discount rules and a `ShippingPolicy` through its constructor.
2. Define `ShippingPolicy` as a `Protocol`. Write the real policy (R5.8) and a fake policy that always returns 0.00.
3. Test the calculator with the fake policy, and test the real policy alone. Explain why two small tests are better here than one large test.

### Exercise 1.9: pytest in depth

1. For your `Cart`: write fixtures for an empty cart and a cart with two books. Write a parametrized test for the quantities 0, 1, 10, 11.
2. Use `pytest.raises` for the rejected values. Check the error message too.
3. Write a test that uses `unittest.mock.Mock` as a spy: check that the `PriceCalculator` calls the shipping policy one time with the correct order value.
4. Run the tests with `-v`, then break the code on purpose and read the failure output.

### Exercise 1.10: SOLID review and the project skeleton (main project, stage 0)

1. Review your code from exercises 1.5–1.9 against the SOLID principles. Write one improvement for each principle, or explain why the principle does not apply. Do the improvements.
2. Make the main project skeleton in `labs/tas/`: `uv init --package shoptest`, add pytest, ruff, mypy, and requests. Add one test that calls `GET /api/health` of the course shop with requests and checks that the status is `ok`. Read the URL from the environment variable `SHOP_URL`, with the default `http://127.0.0.1:8000`.
3. Add a `README.md` with the commands. Run `ruff check`, `ruff format --check`, and `mypy --strict src` with no findings.

**Side project (optional):** write and test a `BankAccount` class (deposit, withdraw, transfer, overdraft rules), or a `ParkingGarage` class (entry, exit, fees by time). Write the tests first (TDD).

## Done criteria

- [ ] I can write programs with functions, collections, files, JSON, and exceptions.
- [ ] I can explain encapsulation, abstraction, inheritance, and polymorphism, each with an example from my code.
- [ ] I can explain when composition is better than inheritance.
- [ ] I can use dependency injection to give a test double to a class.
- [ ] I can explain the five SOLID principles with an example from test automation.
- [ ] I can write pytest tests with fixtures, parametrization, `pytest.raises`, and a mock.
- [ ] My code passes ruff and `mypy --strict`.
- [ ] The main project skeleton in `labs/tas/` runs its first test (stage 0).

## Next

[Phase 2: Testing fundamentals](phase-2-testing-fundamentals.md)
