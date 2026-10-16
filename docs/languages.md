# Programming Languages

This document helps you select a programming language for the course. It also lists the tools for each language. The course documents use Python. With a different language, use the tool in the same row of the tables below, or ask the AI mentor to translate.

## How to select a language

Answer these questions:

1. **Do you already know a language well?** Use it, if it is in the table below. You then learn testing, not a new language.
2. **Which language does your team or your target employer use?** Test automation code is usually in the same language as the product code, or in the language of the test team. Look at job advertisements in your region.
3. **Do you know no language?** Use Python. It has a short syntax, a very good test framework (pytest), and it is common in test automation, DevOps, and data work.

| Language | Fit with the documents | Advantages | Disadvantages |
|---|---|---|---|
| **Python** (reference) | All examples and commands are for Python | Easy to learn. pytest is powerful and short. Common for API tests, scripts, and DevOps tools. | Dynamic types: some errors show only at run time. Use type hints and mypy. |
| **Java** | The mentor translates. Very good tool support. | Very common in enterprise test automation. Strong types. Selenium, REST Assured, and JUnit are industry standards. | Longer code. Build tools (Maven, Gradle) take time to learn. |
| **C#** | The mentor translates. Very good tool support. | Common in Microsoft environments. Strong types. Playwright for .NET is very good. | Fewer test automation jobs than Java or Python in many regions. |
| **TypeScript** | The mentor translates. Very good tool support. | Playwright Test is native to TypeScript. Common for web teams. Same language as many web front ends. | Asynchronous code (`async`, `await`) everywhere. The Node.js tool chain changes fast. |

**Other languages** (Kotlin, Go, JavaScript, Ruby): the mentor can help, but some tools in the tables have no equal. The mentor tells you which exercises need a change.

**Change of language:** you can change the language later. Tell the mentor. The concepts stay the same. You rewrite the code in `labs/` only if you want to.

## Versions

Use a current version with long-term support (LTS):

| Language | Version |
|---|---|
| Python | 3.13 or newer. Use the newest stable release that pytest and Playwright support. |
| Java | A current LTS release of the JDK (for example Temurin) |
| C# | A current LTS release of .NET |
| TypeScript | A current LTS release of Node.js, and TypeScript 5 or newer |

## Tool mapping

### Project and test framework

| Purpose | Python (reference) | Java | C# | TypeScript |
|---|---|---|---|---|
| Project, dependencies, virtual environment | `uv` (`pyproject.toml`, `uv.lock`) | Gradle or Maven | `dotnet` CLI and NuGet | npm or pnpm (`package.json`) |
| Test framework and runner | pytest | JUnit (Jupiter API) | NUnit or xUnit | Playwright Test (UI and API), Vitest (unit tests) |
| Assertions | `assert` (pytest shows the values) | AssertJ, or the JUnit assertions | The assertions of the framework, or Shouldly | `expect` |
| Setup and teardown | Fixtures (`@pytest.fixture`) | `@BeforeEach`, `@AfterEach`, extensions | `[SetUp]`, `[TearDown]`, `[OneTimeSetUp]` | Fixtures, `test.beforeEach` |
| Data-driven tests | `@pytest.mark.parametrize` | `@ParameterizedTest` | `[TestCase]`, `[TestCaseSource]` | A loop over a data table, or `test.each` (Vitest) |
| Test doubles (mocks, stubs, fakes) | `unittest.mock`, `pytest-mock` | Mockito | NSubstitute or Moq | `vi.fn()` (Vitest) |

### API and UI automation

| Purpose | Python (reference) | Java | C# | TypeScript |
|---|---|---|---|---|
| HTTP client | requests | REST Assured, or `java.net.http.HttpClient` | `HttpClient` | Playwright `APIRequestContext`, or `fetch` |
| JSON schema validation | `jsonschema` | `json-schema-validator` (REST Assured module) | JsonSchema.Net | Ajv |
| Browser automation | Playwright for Python (`pytest-playwright`) | Playwright for Java, or Selenium WebDriver | Playwright for .NET | Playwright Test |
| BDD | pytest-bdd | Cucumber-JVM | Reqnroll | playwright-bdd, or Cucumber.js |
| HTTP mocks in the process | `responses` | WireMock (embedded), MockServer | WireMock.Net, RichardSzalay.MockHttp | MSW, nock |
| Stub server (service virtualization) | WireMock in a container | WireMock | WireMock.Net, or WireMock in a container | WireMock in a container, Mockoon |
| WebSocket client | `websockets` | `java.net.http.WebSocket` | `ClientWebSocket` | `ws`, or the `WebSocket` of Node.js |
| Visual comparison | Pillow, or a plugin | A plugin, or a visual testing service | A plugin, or a visual testing service | `toHaveScreenshot()` (Playwright Test) |
| Manual API tool (all languages) | Postman, Insomnia, or Bruno | | | |

### Quality and reports

| Purpose | Python (reference) | Java | C# | TypeScript |
|---|---|---|---|---|
| Linter and formatter | ruff (`ruff check`, `ruff format`) | Checkstyle, PMD, Spotless | .NET analyzers, `dotnet format` | ESLint, Prettier |
| Type checking | mypy (`--strict`) | The compiler | The compiler, with nullable reference types | `tsc --strict` |
| Code coverage | coverage.py (`pytest-cov`) | JaCoCo | coverlet | Vitest coverage (V8) |
| Mutation testing | mutmut | PIT | Stryker.NET | StrykerJS |
| Test reports | JUnit XML (`--junitxml`), Allure (`allure-pytest`), `pytest-html` | Surefire XML, Allure | TRX or JUnit logger, Allure | JUnit reporter, HTML reporter, Allure |
| Parallel runs | `pytest-xdist` | JUnit parallel execution | NUnit `[Parallelizable]`, xUnit collections | Playwright workers |

## Language concepts for OOP

Phase 1 teaches OOP. The concepts are the same in all four languages, but the syntax is different:

| Concept | Python | Java | C# | TypeScript |
|---|---|---|---|---|
| Class | `class Cart:` | `class Cart {}` | `class Cart {}` | `class Cart {}` |
| Constructor | `def __init__(self, ...)` | `Cart(...) {}` | `Cart(...) {}` | `constructor(...) {}` |
| Private member | Convention: `_name`. Not enforced. | `private` | `private` | `private` (compile time), `#name` (run time) |
| Interface | `typing.Protocol`, or an abstract base class (`abc.ABC`) | `interface` | `interface` | `interface` |
| Abstract class | `abc.ABC` with `@abstractmethod` | `abstract class` | `abstract class` | `abstract class` |
| Inheritance | `class Admin(User):` | `extends` | `: User` | `extends` |
| Property | `@property` | Getter and setter methods | `{ get; set; }` | `get` and `set` accessors |
| Data class | `@dataclass` | `record` | `record` | An `interface` or a `type` with an object literal |

## Translation rules for the mentor

See [mentor/environment-selection.md](mentor/environment-selection.md).
