# Reading List

Each phase document tells you what to read and when. This document lists all sources in one place.

## ISTQB documents

Download them from istqb.org. They are free. Keep them in the local `syllabi/` directory. Do not add them to git.

| Document | Phase |
|---|---|
| CTFL syllabus v4.0.1, and the CTFL sample exams | 2–4 |
| CTAL-TAE syllabus v2.0, and the CTAL-TAE sample exam | 7–9 |
| CT-TAS syllabus v1.0, and the CT-TAS sample exam | 10 |
| ISTQB glossary (glossary.istqb.org) | All |
| ISTQB "Exam Structures and Rules" | Before each exam |
| CT-PT, CT-SEC, CT-MAT, CT-UT, CT-GenAI, CT-AI, CTAL-TA, CTAL-TTA, CTAL-TM syllabi | 11 (optional) |

## Testing books

| Book | Use it for | Phase |
|---|---|---|
| Kaner, Bach, and Pettichord, *Lessons Learned in Software Testing* | Short lessons about the work of a tester | 2 |
| Lee Copeland, *A Practitioner's Guide to Software Test Design* | Test techniques with many examples | 3 |
| Elisabeth Hendrickson, *Explore It!* | Exploratory testing, charters, heuristics | 3 |
| Glenford Myers, Corey Sandler, and Tom Badgett, *The Art of Software Testing*, 3rd edition | A classic about test design and the psychology of testing | 3 |
| Gojko Adzic, *Specification by Example* | Examples as acceptance criteria (ATDD, BDD) | 3, 7 |
| Lisa Crispin and Janet Gregory, *Agile Testing* and *More Agile Testing* | Testing in Agile teams, the testing quadrants | 2, 4 |
| Rex Black, *Managing the Testing Process* | Test management, risk, reports | 4 |

## Test automation books

| Book | Use it for | Phase |
|---|---|---|
| Brian Okken, *Python Testing with pytest*, 2nd edition | pytest: fixtures, parametrization, plugins | 1, 6 |
| Dorothy Graham and Mark Fewster, *Experiences of Test Automation* | Case studies of real test automation projects | 7, 10 |
| Robert C. Martin, *Clean Code* | Maintainable code. The CTAL-TAE syllabus refers to it. | 7 |
| Martin Fowler, *Refactoring*, 2nd edition | Improve existing code safely | 9 |
| Jez Humble and David Farley, *Continuous Delivery* | Deployment pipelines | 8 |
| Mike Cohn, *Succeeding with Agile* | The test automation pyramid | 10 |

## Programming

| Source | Use it for | Phase |
|---|---|---|
| The official Python tutorial (docs.python.org/3/tutorial) | Python from the beginning | 1 |
| Eric Matthes, *Python Crash Course*, 3rd edition | Python from the beginning, with projects | 1 |
| Luciano Ramalho, *Fluent Python*, 2nd edition | Python in depth. Use it later. | 1, 7 |
| Freeman and Robson, *Head First Design Patterns*, 2nd edition | OOP principles and design patterns (Java examples) | 1, 7 |
| The documentation of uv, ruff, and mypy (docs.astral.sh, mypy.readthedocs.io) | The tools of the course | 1 |

For Java, C#, or TypeScript, ask the mentor for the matching sources.

## Linux

| Source | Use it for | Phase |
|---|---|---|
| William Shotts, *The Linux Command Line* (free, linuxcommand.org) | The shell and shell scripts | 0 |
| Pro Git (free, git-scm.com/book) | git | 0 |
| The `man` pages | Each command | 0, 5 |
| Julia Evans, zines (wizardzines.com) | Short, visual explanations of the command line and networking | 0, 5 |

## Networking

| Source | Use it for | Phase |
|---|---|---|
| Kurose and Ross, *Computer Networking: A Top-Down Approach* | Networking from the application layer down | 5 |
| MDN Web Docs, "An overview of HTTP" (developer.mozilla.org) | HTTP | 5, 6 |
| RFC 1918 (private addresses), RFC 9110 (HTTP semantics) | Reference | 5 |
| RFC 6455 (WebSocket), RFC 6749 (OAuth 2.0), RFC 9700 (OAuth 2.0 Security Best Current Practice) | Reference | 6 |

## Tool documentation

| Tool | Address | Phase |
|---|---|---|
| pytest | docs.pytest.org | 1, 6–9 |
| requests | requests.readthedocs.io | 6 |
| Playwright for Python | playwright.dev/python | 6–9 |
| jsonschema | python-jsonschema.readthedocs.io | 6 |
| responses | github.com/getsentry/responses | 6 |
| WireMock | wiremock.org/docs | 6 |
| websockets | websockets.readthedocs.io | 6 |
| Postman, Insomnia, Bruno | The documentation of each tool | 6 |
| pytest-bdd | pytest-bdd.readthedocs.io | 7 |
| Docker and Docker Compose | docs.docker.com | 0, 5, 8 |
| GitHub Actions | docs.github.com/actions | 8 |
| Pact | docs.pact.io | 8, 11 |
| mutmut | mutmut.readthedocs.io | 9 |
| Locust | docs.locust.io | 11 |
| OWASP | owasp.org | 11 |

## Articles

| Article | Phase |
|---|---|
| Martin Fowler, "PageObject" (martinfowler.com) | 6 |
| Martin Fowler, "Eradicating Non-Determinism in Tests" (martinfowler.com) | 6, 9 |
| Ham Vocke, "The Practical Test Pyramid" (martinfowler.com) | 4, 10 |
