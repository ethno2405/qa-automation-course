# Certification

This document describes the three ISTQB certifications of the course and maps each learning objective (LO) to a phase. ISTQB is the International Software Testing Qualifications Board.

## The certification path

```
CTFL (Foundation Level)  ──►  CTAL-TAE (Advanced Level, Test Automation Engineering)
        │
        └────────────────►  CT-TAS (Specialist, Test Automation Strategy)
```

| Certificate | Syllabus | Phases | Entry requirement |
|---|---|---|---|
| **CTFL**: Certified Tester Foundation Level | CTFL v4.0.1 | 2, 3, 4 | None |
| **CTAL-TAE**: Certified Tester Advanced Level Test Automation Engineering | CTAL-TAE v2.0 | 6, 7, 8, 9 | The CTFL certificate |
| **CT-TAS**: Certified Tester Test Automation Strategy (Specialist) | CT-TAS v1.0 | 10 | The CTFL certificate |

The CTAL-TAE syllabus covers the engineering work: how to build, run, and improve a test automation solution. The CT-TAS syllabus covers the strategy work: why, where, and how much to automate in a project or an organization. The course does CTAL-TAE first, because the strategy is easier to understand when you have built a solution.

The ISTQB also recommends practical experience before the advanced and specialist exams. The course gives you this experience with the main project. Read section 0 of each syllabus for the recommendations.

## Get the syllabi

1. Download these documents from istqb.org ("Certifications"). They are free.
   - The syllabus of each certificate
   - The sample exam questions and answers of each certificate
   - The "Exam Structures and Rules" document
   - The ISTQB glossary (glossary.istqb.org)
2. Put the PDF files in a directory `syllabi/` in the repository root. Git ignores this directory. Do not commit the files: they are copyrighted.
3. Do a check of the version number on the first page of each syllabus. If it is newer than the version in the table above, tell the AI mentor. The mentor compares the LO list of the new syllabus with this document.

## Exams

- You take the exam with an exam provider that ISTQB or a member board accredits. Many providers have online exams with a remote proctor.
- All three exams have multiple-choice questions. The CTFL exam has 40 questions, takes 60 minutes, and needs 26 of 40 points (65 %). Candidates who take the exam in a language that is not their native language usually get 25 % more time.
- For the CTAL-TAE and CT-TAS exams, the questions have different point values, and the duration is longer. Read the current values in the "Exam Structures and Rules" document. Do not trust a value from a website or a course: the values change with new syllabus versions.
- The exam fee depends on the country and the provider. Ask the provider.
- **K-levels:** each LO has a cognitive level. K1 = remember, K2 = understand, K3 = apply, K4 = analyze. K3 and K4 questions give scenarios, and you must apply or analyze. Practice them with exercises, not only by reading.

## Exam preparation in the course

| Exam | Phase | Preparation |
|---|---|---|
| CTFL | 4 | Read the syllabus completely. Do the official sample exams with a time limit. The mentor does the exam readiness check (`mentor/assessment.md`). |
| CTAL-TAE | 9 | Same, plus a review of your TAS against each chapter. |
| CT-TAS | 10 | Same, plus your strategy document as a case study. |

**Rule for exam answers:** the exam asks for the syllabus view, not the view of your company or your favorite blog. When the two are different, learn both, and answer with the syllabus view.

## LO mapping: CTFL v4.0.1

The LO text is a short summary in the words of this course. Read the exact text in the syllabus.

| LO | K | Summary | Phase |
|---|---|---|---|
| FL-1.1.1 | K1 | Typical test objectives | 2 |
| FL-1.1.2 | K2 | Testing compared with debugging | 2 |
| FL-1.2.1 | K2 | Why testing is necessary | 2 |
| FL-1.2.2 | K1 | Testing and quality assurance | 2 |
| FL-1.2.3 | K2 | Root cause, error, defect, and failure | 2 |
| FL-1.3.1 | K2 | The seven testing principles | 2 |
| FL-1.4.1 | K2 | Test activities and tasks | 2 |
| FL-1.4.2 | K2 | Context and the test process | 2 |
| FL-1.4.3 | K2 | Testware | 2 |
| FL-1.4.4 | K2 | Traceability | 2 |
| FL-1.4.5 | K2 | Roles in testing | 2 |
| FL-1.5.1 | K2 | Generic skills for testing | 2 |
| FL-1.5.2 | K1 | The whole team approach | 2 |
| FL-1.5.3 | K2 | Independence of testing | 2 |
| FL-2.1.1 | K2 | The SDLC and its effect on testing | 2 |
| FL-2.1.2 | K1 | Good testing practices in all SDLCs | 2 |
| FL-2.1.3 | K1 | Test-first approaches (TDD, ATDD, BDD) | 2 |
| FL-2.1.4 | K2 | DevOps and testing | 2 |
| FL-2.1.5 | K2 | Shift left | 2 |
| FL-2.1.6 | K2 | Retrospectives and process improvement | 2 |
| FL-2.2.1 | K2 | Test levels | 2 |
| FL-2.2.2 | K2 | Test types | 2 |
| FL-2.2.3 | K2 | Confirmation testing and regression testing | 2 |
| FL-2.3.1 | K2 | Maintenance testing and its triggers | 2 |
| FL-3.1.1 | K1 | Work products for static testing | 3 |
| FL-3.1.2 | K2 | The value of static testing | 3 |
| FL-3.1.3 | K2 | Static testing compared with dynamic testing | 3 |
| FL-3.2.1 | K1 | Early and frequent stakeholder feedback | 3 |
| FL-3.2.2 | K2 | Activities of the review process | 3 |
| FL-3.2.3 | K1 | Roles in reviews | 3 |
| FL-3.2.4 | K2 | Review types | 3 |
| FL-3.2.5 | K1 | Success factors for reviews | 3 |
| FL-4.1.1 | K2 | Black-box, white-box, and experience-based techniques | 3 |
| FL-4.2.1 | K3 | Equivalence partitioning | 3 |
| FL-4.2.2 | K3 | Boundary value analysis | 3 |
| FL-4.2.3 | K3 | Decision table testing | 3 |
| FL-4.2.4 | K3 | State transition testing | 3 |
| FL-4.3.1 | K2 | Statement testing | 3 |
| FL-4.3.2 | K2 | Branch testing | 3 |
| FL-4.3.3 | K2 | The value of white-box testing | 3 |
| FL-4.4.1 | K2 | Error guessing | 3 |
| FL-4.4.2 | K2 | Exploratory testing | 3 |
| FL-4.4.3 | K2 | Checklist-based testing | 3 |
| FL-4.5.1 | K2 | Collaborative user story writing | 3 |
| FL-4.5.2 | K2 | Options for acceptance criteria | 3 |
| FL-4.5.3 | K3 | ATDD | 3 |
| FL-5.1.1 | K2 | Test plan: purpose and content | 4 |
| FL-5.1.2 | K1 | The tester in iteration and release planning | 4 |
| FL-5.1.3 | K2 | Entry criteria and exit criteria | 4 |
| FL-5.1.4 | K3 | Test effort estimation | 4 |
| FL-5.1.5 | K3 | Test case prioritization | 4 |
| FL-5.1.6 | K1 | The test pyramid | 4 |
| FL-5.1.7 | K2 | The testing quadrants | 4 |
| FL-5.2.1 | K1 | Risk level from likelihood and impact | 4 |
| FL-5.2.2 | K2 | Project risks and product risks | 4 |
| FL-5.2.3 | K2 | Product risk analysis and test scope | 4 |
| FL-5.2.4 | K2 | Responses to product risks | 4 |
| FL-5.3.1 | K1 | Test metrics | 4 |
| FL-5.3.2 | K2 | Test reports | 4 |
| FL-5.3.3 | K2 | Communication of the test status | 4 |
| FL-5.4.1 | K2 | Configuration management | 4 |
| FL-5.5.1 | K3 | Defect reports | 4 |
| FL-6.1.1 | K2 | Types of test tools | 4 |
| FL-6.2.1 | K1 | Benefits and risks of test automation | 4 |

## LO mapping: CTAL-TAE v2.0

| LO | K | Summary | Phase |
|---|---|---|---|
| TAE-1.1.1 | K2 | Advantages and disadvantages of test automation | 7 |
| TAE-1.2.1 | K2 | Test automation in different SDLC models | 7 |
| TAE-1.2.2 | K2 | Select test automation tools for an SUT | 7 |
| TAE-2.1.1 | K2 | Infrastructure configuration for test automation | 7 (and 8) |
| TAE-2.1.2 | K2 | Test automation in different environments | 7 (and 8) |
| TAE-2.2.1 | K4 | Analyze an SUT to find the right test automation solution | 7 |
| TAE-2.2.2 | K4 | Technical findings of a tool evaluation | 7 |
| TAE-3.1.1 | K2 | Capabilities of a test automation architecture (gTAA) | 7 |
| TAE-3.1.2 | K2 | Design of a test automation solution | 7 |
| TAE-3.1.3 | K3 | Layers of a test automation framework | 7 |
| TAE-3.1.4 | K3 | Approaches to automate test cases | 7 |
| TAE-3.1.5 | K3 | Design principles and design patterns | 1 (OOP), 6, 7 |
| TAE-4.1.1 | K3 | Pilot and deployment of test automation | 7 |
| TAE-4.2.1 | K4 | Deployment risks and their mitigation | 7 |
| TAE-4.3.1 | K2 | Maintainability of a test automation solution | 7 |
| TAE-5.1.1 | K3 | Test automation at different test levels in pipelines | 8 |
| TAE-5.1.2 | K2 | Configuration management for testware | 8 |
| TAE-5.1.3 | K2 | Test automation dependencies for an API infrastructure | 8 |
| TAE-6.1.1 | K3 | Data collection from the TAS and the SUT | 8 |
| TAE-6.1.2 | K4 | Analysis of TAS and SUT data to understand test results | 8 |
| TAE-6.1.3 | K2 | Test progress reports | 8 |
| TAE-7.1.1 | K3 | Verification of the test automation environment | 9 |
| TAE-7.1.2 | K2 | Correct behavior of a test script or test suite | 9 |
| TAE-7.1.3 | K2 | Unexpected results of test automation | 9 |
| TAE-7.1.4 | K2 | Static analysis for test automation code | 9 |
| TAE-8.1.1 | K3 | Improve test cases from data analysis | 9 |
| TAE-8.1.2 | K4 | Analyze a deployed TAS and recommend improvements | 9 |
| TAE-8.1.3 | K3 | Restructure testware after SUT changes | 9 |
| TAE-8.1.4 | K2 | Opportunities for test automation tools | 9 |

## LO mapping: CT-TAS v1.0

| LO | K | Summary | Phase |
|---|---|---|---|
| CT-TAS-1.1.1 | K2 | Objectives and relevance of test automation | 10 |
| CT-TAS-1.1.2 | K2 | Technical success factors of a test automation project | 10 |
| CT-TAS-1.1.3 | K2 | Investment criteria to select projects for test automation | 10 |
| CT-TAS-2.1.1 | K2 | Cost of ownership of alternative technical solutions | 10 |
| CT-TAS-2.1.2 | K2 | Licensing models of test automation tools | 10 |
| CT-TAS-2.1.3 | K2 | Factors for a test automation strategy | 10 |
| CT-TAS-2.2.1 | K2 | Roles and skills for test automation | 10 |
| CT-TAS-3.1.1 | K2 | Test automation distributions across test levels | 10 |
| CT-TAS-3.1.2 | K2 | Test automation approach from the SUT architecture | 10 |
| CT-TAS-3.1.3 | K3 | Shift left and shift right with test automation | 10 |
| CT-TAS-3.2.1 | K2 | Test automation in legacy SDLC models | 10 |
| CT-TAS-3.2.2 | K2 | Test automation in Agile development | 10 |
| CT-TAS-3.2.3 | K3 | Test automation in DevOps and continuous testing | 10 |
| CT-TAS-3.3.1 | K2 | Criteria for the suitability of tests for automation | 10 |
| CT-TAS-3.3.2 | K2 | Challenges that only test automation can address | 10 |
| CT-TAS-3.3.3 | K2 | Test conditions that are difficult to automate | 10 |
| CT-TAS-4.1.1 | K2 | Test automation and a shorter time to market | 10 |
| CT-TAS-4.1.2 | K2 | Test automation to verify reported defects | 10 |
| CT-TAS-4.1.3 | K2 | Operationally relevant scenarios | 10 |
| CT-TAS-4.2.1 | K2 | A test automation deployment strategy | 10 |
| CT-TAS-4.2.2 | K2 | Test automation risks in deployment | 10 |
| CT-TAS-4.2.3 | K2 | Mitigation of deployment risks | 10 |
| CT-TAS-4.3.1 | K2 | Test automation components in the test environment | 10 |
| CT-TAS-4.3.2 | K2 | Infrastructure components and dependencies | 10 |
| CT-TAS-4.3.3 | K2 | Test data and interface requirements | 10 |
| CT-TAS-5.1.1 | K3 | Return on investment (ROI) of a test automation solution | 10 |
| CT-TAS-5.2.1 | K2 | Classification of test automation metrics | 10 |
| CT-TAS-5.3.1 | K3 | Organizational considerations | 10 |
| CT-TAS-5.3.2 | K3 | Project characteristics and test automation objectives | 10 |
| CT-TAS-5.4.1 | K2 | Decisions from test report data | 10 |
| CT-TAS-6.1.1 | K2 | From manual testing to test automation | 10 |
| CT-TAS-6.1.2 | K2 | From test automation to continuous testing | 10 |
| CT-TAS-6.2.1 | K3 | Evaluation of test automation assets and practices | 10 |

## Topics outside the syllabi

Phases 0, 1, and 5 (Linux, programming, networking) and most of phase 6 (the tools) are not in the three syllabi. The syllabi expect that a test automation engineer can program and can work with environments. The CTAL-TAE syllabus names the OOP principles, the SOLID principles, and design patterns (LO TAE-3.1.5). Phase 1 teaches them.

## Other ISTQB certificates

The course does not prepare for these certificates, but phase 11 touches their topics: CTAL-TA (Test Analyst), CTAL-TTA (Technical Test Analyst), CTAL-TM (Test Management), CT-PT (Performance Testing), CT-SEC (Security Testing), CT-MAT (Mobile Application Testing), CT-UT (Usability Testing), CT-GenAI (Testing with Generative AI), CT-AI (AI Testing). See istqb.org for the full list.
