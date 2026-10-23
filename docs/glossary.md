# Glossary

The course uses the terms of the ISTQB glossary (glossary.istqb.org). This list gives short meanings in the words of the course, and the terms that are not in the ISTQB glossary (Linux, networking, tools). Add a term to this list when you find it for the first time.

| Term | Meaning |
|---|---|
| Acceptance criteria | The conditions that a work product (for example a user story) must meet to be accepted. |
| Access token | A string that a client sends to an API to prove that it may do an action. It has a scope and an expiry time. |
| API | Application programming interface. In this course usually a web API: HTTP endpoints that exchange JSON. |
| ARP | Address Resolution Protocol. Finds the MAC address for an IPv4 address in the local network. |
| ATDD | Acceptance test-driven development. The team writes acceptance tests from acceptance criteria before the implementation. |
| Baseline | In visual testing: the approved screenshot that later screenshots are compared with. |
| BDD | Behavior-driven development. The team writes examples of behavior in Given/When/Then form. A tool can execute them as tests. |
| Boundary value analysis (BVA) | A black-box test technique that tests the values at and next to the boundaries of ordered partitions. |
| Branch coverage | The percentage of branches (outcomes of decisions) that the tests executed. |
| CI/CD | Continuous integration and continuous delivery (or deployment). Each change is built, tested, and made ready for release automatically. |
| CIDR | Classless Inter-Domain Routing. The notation `/24` for the number of network bits of an IP address. |
| Confirmation testing | Testing that checks that a fix removed a defect. |
| Container | An isolated process with its own file system and network, that shares the kernel of the host. Docker runs containers. |
| Contract testing | A type of integration testing that verifies that two services agree on the interactions and data between them. |
| Correlation ID | A unique ID that goes with a request through all systems, so that logs can be connected. The course shop uses `X-Request-ID`. |
| Cross-browser testing | Running the same tests on several browsers or browser engines. |
| CT-TAS | ISTQB Certified Tester Test Automation Strategy (specialist). |
| CTAL-TAE | ISTQB Certified Tester Advanced Level Test Automation Engineering. |
| CTFL | ISTQB Certified Tester Foundation Level. |
| Decision table testing | A black-box test technique that tests the combinations of conditions and their actions. |
| Defect | A flaw in a work product. When the code with the defect executes, it can cause a failure. Also called "bug" or "fault". The course uses "defect". |
| Defect detection rate | In this course: the percentage of known (seeded) defects that a test suite detects. |
| DHCP | Dynamic Host Configuration Protocol. Gives a host its IP address, mask, gateway, and DNS servers. |
| DNS | Domain Name System. Translates names to IP addresses. |
| Equivalence partitioning (EP) | A black-box test technique that divides data into partitions that the system processes in the same way, and tests one value from each partition. |
| Error | A human action that gives a wrong result. Also called "mistake". |
| Exit code | The number that a process returns when it ends. 0 means success. |
| Exploratory testing | Testing where the tester designs, executes, and evaluates tests at the same time, while learning about the system. |
| Facade | A design pattern: a simple interface that hides complex details. |
| Failure | A wrong behavior of the system that a user or a test sees. |
| Feature file | A text file in Gherkin with one feature and its scenarios. The file extension is `.feature`. |
| Fixture | In pytest: a function that prepares data or objects for a test. In the ISTQB glossary: test fixture, the preconditions for test execution. |
| Flaky test | A test that passes and fails without a change in the code or the test. |
| Flow model | A design pattern: a facade over page objects that contains user actions across several pages. |
| Gherkin | A plain-language format for BDD scenarios with the keywords Feature, Scenario, Given, When, Then. |
| gTAA | Generic test automation architecture. An abstract design of the capabilities and interfaces of a test automation solution. |
| HTTP | Hypertext Transfer Protocol. A request-response protocol for the web and for web APIs. |
| Idempotent | An operation that has the same effect when you do it one time or many times. |
| IP address | A number that identifies a network interface on an IP network. IPv4 has 32 bits, IPv6 has 128 bits. |
| JSON | JavaScript Object Notation. A text format for structured data. |
| K-level | The cognitive level of an ISTQB learning objective: K1 remember, K2 understand, K3 apply, K4 analyze. |
| Keyword-driven testing | Test cases are tables of keywords (user actions) and data. A TAF executes them. |
| LO | Learning objective of an ISTQB syllabus, for example FL-4.2.2. |
| Locator | In UI automation: a way to find an element on a page, for example by role or by test ID. |
| MAC address | A 48-bit address of a network interface in the local network. |
| Mock | A test double that records the calls to it, so that the test can check them. |
| Mutation testing | A method that makes small changes in the code (mutants) and checks whether the tests fail. |
| NAT | Network address translation. A router replaces private addresses with its public address. |
| Network interception | In UI tests: a test catches the requests of the page and answers, changes, or stops them. |
| OAuth 2.0 | A standard (RFC 6749) for access tokens. A client gets a token from an authorization server, and uses it at an API. |
| OOP | Object-oriented programming: encapsulation, abstraction, inheritance, polymorphism. |
| OpenAPI | A standard format that describes a web API: endpoints, parameters, and schemas. |
| Page object | A design pattern: a class that represents a page and hides its locators. |
| Port | A number (0–65535) that identifies a service or a connection on a host. |
| Pull request | A request to merge a branch, with code review and automatic checks. GitLab calls it a merge request. |
| QA | Quality assurance. Activities that make sure that the process gives quality. Many companies use "QA" for testing. The ISTQB does not. |
| Quality gate | A check in a pipeline that stops the pipeline when it fails. |
| Rebase | A git operation that copies the commits of a branch on top of a different commit. The commits get new IDs. |
| Regression testing | Testing that checks that a change did not cause new defects in parts that did not change. |
| REST | Representational State Transfer. An API style where resources have URLs and HTTP methods act on them. |
| ROI | Return on investment. In CT-TAS: savings divided by investment. |
| Root cause | The basic reason for a defect. |
| Scenario outline | A Gherkin scenario with placeholders. It runs one time for each row of its Examples table. |
| Schema validation | A check that data (for example a JSON response) has the structure that a schema defines. |
| Scope | In OAuth 2.0: the actions that an access token permits. |
| Service virtualization | A stub server that simulates a service that is not available for testing. |
| Shift left | Testing earlier in the software development lifecycle. |
| Shift right | Testing after the release, in preproduction or production, with monitoring and user feedback. |
| SSH | Secure Shell. An encrypted remote terminal, file copy, and port forwarding. |
| State transition testing | A black-box test technique that tests the states of a system and the transitions between them. |
| Statement coverage | The percentage of executable statements that the tests executed. |
| Static testing | Testing without execution: reviews and static analysis. |
| Step definition | The code that a BDD tool runs for one Gherkin step. |
| Stub | A test double that returns fixed answers. |
| Subnet mask | A number that divides an IP address into a network part and a host part. |
| SUT | System under test. In this course: the course shop in `sut/`. |
| TAA | Test automation architecture. The technical design of a test automation solution. |
| TAE | Test automation engineer. |
| TAF | Test automation framework. The base of a TAS: the test harness, libraries, test scripts, and test suites. |
| Tag | In git: a fixed name for one commit, for example a release version `v1.4.0`. |
| TAS | Test automation solution. The complete solution: the TAF, tools, test suites, and their configuration. |
| TCP | Transmission Control Protocol. A reliable, connection-oriented transport protocol. |
| TDD | Test-driven development. Write a failing test first, then the code, then refactor. |
| Test basis | The documents and knowledge that test analysis and test design use, for example requirements. |
| Test case | A set of preconditions, inputs, actions, and expected results, made for a test condition. |
| Test condition | A testable aspect of a component or system, identified as a basis for testing. |
| Test double | An object that replaces a real dependency in a test: stub, fake, mock, spy. |
| Test pyramid | A model with many small, fast tests at the bottom and few large, slow tests at the top. |
| Testability | How easily a system can be tested: observability, controllability, architecture transparency. |
| Testware | All work products of testing: plans, test cases, scripts, data, reports. |
| TLS | Transport Layer Security. Encrypts a connection and proves the identity of the server with a certificate. |
| Token (AI model) | The unit of text that an AI model reads and writes. A token is a part of a word. The usage limits and the price of an AI agent depend on the number of tokens. See [token-usage.md](token-usage.md). |
| Traceability | The links between the test basis, test cases, test results, and defects. |
| UDP | User Datagram Protocol. A transport protocol without connections or delivery guarantee. |
| Visual regression testing | Testing that compares screenshots with approved baselines to find unwanted visual changes. |
| WebSocket | A connection (RFC 6455) that stays open after an HTTP handshake. Both sides can send messages at any time. |
| WSL2 | Windows Subsystem for Linux, version 2. Runs Linux on Windows in a light virtual machine. |
