# Assessment

This document tells the AI mentor how to assess the knowledge of a learner. The result is the learner profile, `learner/profile.md`. The mentor uses the profile in every session.

## When to assess

| Situation | Action |
|---|---|
| `learner/profile.md` does not exist | Do a full assessment: mode selection, part A, part B, environment selection, result |
| `learner/profile.md` does not exist, but `learner/progress.md` exists | Rebuild the profile. Recommend the quick mode. Keep the progress file and the current position. |
| The learner asks to re-assess one area ("Re-assess my networking knowledge") | Do part B for that area only. Update the level after the learner agrees. |
| The learner completes a phase | Do the phase review (section "Phase review") |
| The learner plans an exam, or asks "Am I ready?" | Do the exam readiness check (section "Exam readiness") |

## Rules for the assessment

- Tell the learner that the assessment is not a test. Its only purpose is to select the correct start point and the correct explanation level.
- Ask **one question at a time**. Wait for the answer.
- Tell the learner that "I do not know" is a good answer. A guess gives a wrong level.
- Ask the learner not to look up answers.
- Do not explain the correct answer during part B, unless the learner asks. Give all corrections at the end, in the result summary.
- Keep a short record of each question and the result. You write it into the profile as evidence.

## Step 1: Mode selection

Show the three modes to the learner and ask them to select one:

| Mode | Time | Content | Accuracy |
|---|---|---|---|
| **Quick** | ~5 minutes | Part A only (self-report) | Low. The mentor trusts the answers and corrects the levels later from the learner's work. |
| **Standard** | ~15–20 minutes | Part A, then 2–4 adaptive questions for each area in part B | Good for most learners |
| **Full** | ~45 minutes | Part A, then 5–8 questions for each area in part B, with the practical items | High. Use it if the learner wants an exact start point. |

If the learner does not select a mode, use **standard**.

## Step 2: Part A, self-report (all modes)

Ask these questions. You can ask related questions together in one message.

1. Which programming languages do you know? For how many years? Which one do you know best? (Or: I do not program.)
2. Do you know object-oriented programming: classes, objects, inheritance, interfaces? (no / a little / yes)
3. What is your testing experience? (none / I test as part of a different job / manual tester / automation tester / test lead) For how many years?
4. Do you have an ISTQB certificate or a different testing certificate? Which one, and which year?
5. How much do you use Linux and a terminal? (never / a little / every day)
6. How much networking do you know? (none / I know what an IP address is / I can configure networks / professional)
7. Which tools do you use: git, Docker, a CI system, an issue tracker, an API client (for example Postman)?
8. Which operating system do you use? Can you install software on the computer?
9. Which programming language do you want to use in the course? (If you do not know, the course uses Python.)
10. How many hours per week can you work on the course?
11. What is your goal? (for example: first job in testing, move from manual testing to automation, a test lead role, a certificate by a date)
12. Which ISTQB exams do you want to take, and when?
13. How do you want the mentor to help when you are blocked? (hints first, and a solution only when I ask / a full solution with an explanation)
14. How detailed must the explanations be? (short / normal / very detailed)

In **quick** mode, set the levels from the self-report with the rubric below, and mark them "self-reported". Then go to step 4.

## Step 3: Part B, knowledge check (standard and full modes)

### Adaptive rule

For each area:

1. Use the self-report to select the first question. Self-report "none" or "never" → start at level 1. Self-report "a little" or "basic" → start at level 2. Self-report "yes", "every day", or "professional" → start at level 3.
2. A correct answer → ask the next question at a higher level (or another question at level 3).
3. A wrong answer or "I do not know" → ask the next question at a lower level.
4. Stop when the level is clear. Standard mode: 2–4 questions for each area. Full mode: 5–8 questions for each area, including the practical items.
5. A partly correct answer counts as half. Ask one more question at the same level to decide.

If the learner does not program, ask only the level 1 questions of area P, in the words of the learner.

You can change the wording of a question. You can make new questions at the same level. Show code in the language that the learner knows best. The expected answers below are the minimum for "correct".

### Area P: programming and OOP

| Level | Question | Expected answer |
|---|---|---|
| 1 | What is the difference between a variable and a function? | A variable holds a value. A function is a named block of code that you can call, with parameters and a return value. |
| 1 | What does this loop print? `for i in range(3): print(i)` | `0`, `1`, `2`, each on a new line |
| 1 | What is a list (array)? How do you get its first element? | An ordered collection of values. Index 0, for example `items[0]`. |
| 2 | What is the difference between a class and an object? | A class is the definition (the type). An object is one instance of the class, with its own data. |
| 2 | What is encapsulation? Why is it useful? | The object hides its data and gives access through methods. Other code cannot put the object in a wrong state, and the inside can change without changes to the callers. |
| 2 | What happens when code raises an exception and nothing catches it? | The program stops with an error and a stack trace. |
| 2 | What is a dictionary (map)? Give one use. | A collection of key-value pairs. Example: user names to user objects, or JSON objects. |
| 3 | What is polymorphism? Give an example. | Code calls the same method on objects of different classes, and each class has its own behavior. Example: `pay()` on `CardPayment` and `InvoicePayment`. |
| 3 | When do you use composition in place of inheritance? | When the relation is "has a", not "is a", or to combine behaviors without a deep class tree. Composition is easier to change. |
| 3 | What is dependency injection? Why does it help testing? | An object gets its dependencies from outside (for example in the constructor), and does not make them. A test can give a test double. |
| 3 | What is an interface (or a protocol, or an abstract class)? | A contract: a set of methods that a class must have. Callers depend on the contract, not on one class. |

### Area Q: testing knowledge

| Level | Question | Expected answer |
|---|---|---|
| 1 | Why do we test software? | To find defects, to reduce the risk of failures, to get information about quality, and to build confidence. |
| 1 | What is the difference between a defect and a failure? | A defect is a fault in the code or a document. A failure is the wrong behavior that a user or a test sees when the defect executes. |
| 1 | What is a test case? | A set of preconditions, inputs, actions, and expected results, made for a test condition. |
| 2 | What is regression testing? | Testing to find out whether a change caused new defects in parts that did not change. |
| 2 | A field accepts an age from 18 to 65. Which values do you test with boundary value analysis? | 17, 18, 65, 66 (2-value). The 3-value method adds 19 and 64. |
| 2 | What is the difference between static testing and dynamic testing? | Static testing examines work products without execution (reviews, static analysis). Dynamic testing executes the software. |
| 2 | Name three test levels. | Component, component integration, system, system integration, acceptance. |
| 3 | What is the test pyramid? Why is it a pyramid? | Many fast, small tests at the bottom (component), fewer at the top (UI, end to end). Lower tests are faster, cheaper, and more stable. |
| 3 | A test passes and fails without a change in the code. What is it called? Name two causes. | A flaky test. Causes: timing and waits, shared test data, test order, environment problems, random data. |
| 3 | What is a page object? Why do test automation engineers use it? | A class that represents a page or a part of a page and hides its locators. When the UI changes, you change one class, not each test case. |
| 3 | What is the difference between a stub and a mock? | A stub returns fixed answers. A mock also records the calls and checks them. |

### Area L: Linux and the shell

| Level | Question | Expected answer |
|---|---|---|
| 1 | What does `cd ..` do? | It changes to the parent directory. |
| 1 | How do you see the files in a directory, with the hidden files? | `ls -a` (or `ls -la`) |
| 1 | What is the difference between an absolute path and a relative path? | An absolute path starts at `/`. A relative path starts at the current directory. |
| 2 | What does `chmod 640 file` do? | Owner: read and write. Group: read. Others: nothing. |
| 2 | How do you find all lines with "ERROR" in `app.log`? | `grep ERROR app.log` |
| 2 | What does the pipe `\|` do? | It sends the standard output of one command to the standard input of the next command. |
| 2 | How do you see the running processes? How do you stop one? | `ps aux` or `top`. `kill <PID>`. |
| 3 | What does `2>&1` do in `cmd > out.txt 2>&1`? | It sends the standard error to the same place as the standard output. Both go to `out.txt`. |
| 3 | A service does not start. Which commands do you use to find the cause? | `systemctl status <service>`, `journalctl -u <service>`, the log files of the service. |
| 3 | What does `set -euo pipefail` do in a Bash script? | Stop on an error, stop on an unset variable, and fail a pipeline if any command in it fails. |
| 3 | What is an environment variable? How do you set one for one command only? | A named value that a process gets from its parent. `NAME=value command` |

### Area N: networking

| Level | Question | Expected answer |
|---|---|---|
| 1 | What is an IP address? | A number that identifies a network interface on a network. |
| 1 | What does DNS do? | It translates names (for example `example.com`) to IP addresses. |
| 1 | What is a port? | A number that identifies a service or a connection on a host. Example: HTTPS uses port 443. |
| 2 | What does a subnet mask of `255.255.255.0` (or `/24`) mean? | The first 24 bits are the network part. The hosts are in the same network if these bits are the same. 254 usable host addresses. |
| 2 | What does DHCP do? | It gives a host an IP address, a mask, a gateway, and DNS servers automatically. |
| 2 | What is the difference between TCP and UDP? | TCP is connection-oriented and reliable (order, retransmission). UDP sends datagrams without a connection or a delivery guarantee. |
| 2 | What do the HTTP status codes 200, 404, and 500 mean? | OK. Not found. Server error. |
| 3 | How many usable host addresses has a `/26` network? Which is the broadcast address of `192.168.1.64/26`? | 62. `192.168.1.127`. |
| 3 | What happens in the TCP three-way handshake? | The client sends SYN. The server answers SYN-ACK. The client sends ACK. |
| 3 | How does SSH key authentication work, in short? | The server has the public key in `authorized_keys`. The client proves that it has the private key with a signature. The private key never leaves the client. |
| 3 | A test cannot connect to `api.test.local:8443`. Which steps do you do to find the cause? | Name resolution (`dig`), reachability (`ping`, route), port (`nc -zv` or `curl -v`), TLS (certificate), then the application. |

### Area D: developer tools

| Level | Question | Expected answer |
|---|---|---|
| 1 | What does `git commit` do? | It records the staged changes as a new version in the local repository. |
| 1 | What is a branch in git? | A movable name for a line of commits. You work on it without a change to other lines. |
| 2 | What is a container? How is it different from a virtual machine? | A process with its own isolated file system, network, and resources. It shares the kernel of the host. A virtual machine has its own kernel. |
| 2 | What is CI (continuous integration)? | Each change is merged often, and an automatic pipeline builds and tests it. |
| 2 | What does `git pull` do? | It fetches the changes from the remote and merges them into the current branch. |
| 3 | What is the difference between a Docker image and a container? | The image is the read-only template. A container is a running (or stopped) instance of an image. |
| 3 | How do two containers in the same Docker Compose project find each other? | Through the Compose network: each service name is a DNS name. |
| 3 | A test job in CI must use a password. Where do you put it? | In the secret store of the CI system, as an environment variable. Never in the repository. |

### Practical items (full mode only)

Ask 1–2 items for each area, at the level of the learner.

**P, code reading.** Find the problems (show the code in the learner's language):

```python
class Cart:
    items = []

    def add(self, item):
        self.items.append(item)
```

Expected: `items` is a class attribute. All carts share one list. Make it an instance attribute in `__init__`.

**Q, test design.** "Shipping is free for an order total of 50.00 or more. Below 50.00, shipping costs 4.99." Give the equivalence partitions and the boundary values.

Expected: partitions `< 50.00` and `>= 50.00` (and invalid: negative). Boundary values 49.99 and 50.00 (2-value). 3-value: 49.99, 50.00, 50.01.

**Q, flaky test.** Explain why this test can fail:

```python
page.click("#add-to-cart")
time.sleep(1)
assert page.inner_text("#cart-count") == "1"
```

Expected: a fixed wait. If the update takes more than 1 second, the test fails. Use an auto-waiting assertion (`expect(...).to_have_text("1")`).

**L, shell.** Write one command line that counts the lines with "ERROR" in all `.log` files in the current directory.

Expected: `grep -c ERROR *.log` (per file) or `cat *.log | grep -c ERROR` (total), or an equal command.

**N, subnet.** A host has the address `10.0.5.130/25`. Give the network address, the broadcast address, and the range of host addresses.

Expected: network `10.0.5.128`, broadcast `10.0.5.255`, hosts `10.0.5.129` to `10.0.5.254`.

**N, trace.** Show the learner a short `curl -v` output with a `401 Unauthorized` response. Ask what failed and what to check.

Expected: the connection and TLS worked. The server rejected the authentication. Check the token or the `Authorization` header.

**D, tools.** Explain the steps from a code change to a test report in a CI pipeline.

Expected: commit and push, the CI system starts a job, it gets the code, installs dependencies, starts the SUT or uses an environment, runs the tests, and publishes the results and the report.

## Level rubric

Give each area (P, Q, L, N, D) a level from 0 to 3:

| Level | Name | Description |
|---|---|---|
| 0 | None | Cannot answer level 1 questions. |
| 1 | Basic | Answers most level 1 questions. Fails most level 2 questions. |
| 2 | Working | Answers most level 2 questions. Fails most level 3 questions. |
| 3 | Strong | Answers most level 3 questions. |

In quick mode, use the self-report: "none" / "never" / "I do not program" → 0, "a little" / "I know what an IP address is" / "I test as part of a different job" → 1, "manual tester" / "I can configure networks" / "I wrote small programs" / "every day" → 2, "automation tester" / "professional" / "I use it at work" → 3. Mark these levels "self-reported".

## Learning path

Use the levels to make the learning path. Write the decisions in the profile.

| Condition | Decision |
|---|---|
| P = 0 | Phase 1 starts with topic 1.1. Plan 6–8 weeks for phase 1. Do phase 0 in parallel. |
| P = 1 | Phase 1: read topics 1.1–1.4 quickly. Do all exercises from 1.3. Plan 3–4 weeks. |
| P = 2 | Phase 1: start at topic 1.5 (OOP). Do exercises 1.5–1.10. Plan 2 weeks. |
| P = 3 | Phase 1: do exercises 1.8, 1.9, and 1.10 only. Plan 1 week. |
| Q = 0 or 1 | Do phases 2–4 completely. |
| Q = 2 | Read phase 2 quickly, and do its exercises. Do phases 3 and 4 completely. |
| Q = 3 and a CTFL certificate for syllabus v4.0 or newer | Skip phases 2–4. Do exercises 3.4–3.8 for the SUT, because the main project needs them. |
| Q = 3, no CTFL certificate | Read phases 2–4 quickly. Do the CTFL sample exams early, and fill the gaps that they show. |
| L = 0 or 1 | Do all of phase 0. Explain each command at first use. |
| L = 2 | Phase 0: read topics 0.6–0.10. Do exercises 0.5–0.9. |
| L = 3 | Phase 0: do exercise 0.9 only. |
| N = 0 or 1 | Do all of phase 5. Draw a diagram for each protocol. |
| N = 2 | Phase 5: read topics 5.2, 5.8, and 5.10–5.12. Do exercises 5.2, 5.5, 5.7, and 5.8. |
| N = 3 | Phase 5: do exercises 5.7 and 5.8 only. |
| D = 0 or 1 | Teach git and Docker in phase 0, before the first SUT start (exercise 0.5). Do exercises 0.10 and 0.11 with the topic `docs/topics/git-for-testers.md`. Spend extra time in phase 8. |
| No CTFL certificate, and the learner wants CTAL-TAE or CT-TAS | Tell the learner that the CTFL certificate is required before these exams. |
| Fewer than 4 hours per week | Tell the learner to double the phase times in `docs/README.md`. |

## Step 4: Environment selection

Do the environment selection in `docs/mentor/environment-selection.md`. Use the answers from part A (questions 1, 8, and 9). If the learner does not select, record Python and Linux (with WSL2 on Windows).

## Step 5: Result

1. Write `learner/profile.md` from `docs/templates/profile-template.md`. Fill in all sections. Put the evidence for each level (the questions and the results).
2. Show the learner a summary: the level of each area, the environment, the learning path, the exam plan, and the corrections for the questions that they answered wrong.
3. Ask the learner whether the summary is correct. Change the profile if the learner disagrees with good reasons.
4. If `learner/progress.md` does not exist, create it from `docs/templates/progress-template.md`. Set the start date to today. Fill in the planned exams.
5. If `learner/progress.md` already existed before the assessment, do not change the current position. Tell the learner their next step from the progress file. Otherwise, tell the learner the first step of their learning path.

## Phase review

When the learner says that they completed a phase:

1. Ask 3–5 questions from the "Done criteria" list of the phase. Use questions that need an explanation, not a yes or no.
2. Ask for evidence of the practical criteria: test design documents, defect reports, command output, code and test results in `labs/`, or a CI run.
3. If the learner meets all criteria, mark the phase "Done" in `learner/progress.md`.
4. If some criteria are not met, tell the learner which ones, and suggest the exercises to repeat.
5. If the results show that a level in the profile changed, propose the new level to the learner. Change it after the learner agrees. Add the review to the "Assessment history" in the profile.
6. Give the learner the phase summary: their performance in the phase, their gaps, what to improve, and a short description of the next phase. See `docs/mentor/mentoring.md`, "Overviews and summaries". Write a one-line result in the "Notes" column of the phase in `learner/progress.md`.

## Exam readiness

When the learner plans an exam, or asks whether they are ready:

1. Ask whether the learner has the current syllabus and the official sample exam (see `docs/certification.md`). If not, tell them to download them.
2. Make a list of the LOs of the exam from `docs/certification.md`. Ask 1–2 questions for each chapter, at the K-level of the LOs. For K3 and K4 LOs, give a short scenario. Do not say that your questions are official exam questions.
3. Ask the learner to do one official sample exam with the time limit of the exam. Ask for the score and the wrong answers.
4. For each wrong answer, find the LO and explain the syllabus view.
5. Give a result:

   | Result | Condition | Recommendation |
   |---|---|---|
   | Ready | Sample exam score at least 75 %, and no chapter with more than one third of its questions wrong | Book the exam. |
   | Almost ready | Sample exam score 65–75 %, or one weak chapter | Repeat the weak chapters. Do a second sample exam. |
   | Not ready | Sample exam score below 65 % | Repeat the phases of the weak chapters before you book. |

   The 75 % threshold is a course recommendation, not an ISTQB rule. It gives a safety margin above the pass mark.
6. Record the result in the "Exams" table of `learner/progress.md`. After the exam, ask for the result and record it. Do not record the exam questions: they are confidential.
