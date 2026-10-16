# Git for Testers

**Phase:** 0 (basics and remote work), 7 (branching strategies), 8 (pipelines, tags, `git bisect`)
**Syllabus:** CTFL v4.0.1, section 5.4 (configuration management, FL-5.4.1). CTAL-TAE v2.0, section 4.3 (branching strategy, LO TAE-4.3.1) and section 5.1.2 (configuration management for testware, LO TAE-5.1.2).
**Related:** [phase 0, topic 0.11 and exercises 0.10–0.11](../phases/phase-0-linux.md), [phase 7, topic 7.13](../phases/phase-7-automation-architecture.md), [phase 8, topic 8.4 and exercise 8.9](../phases/phase-8-ci-cd-reporting.md)

## Summary

Git records the history of files, so that a team can work in parallel, review changes, and go back to any earlier version. Test automation code is code: it needs version control the same as the SUT. A tester also uses git to find when a test or the SUT changed, to connect testware versions to SUT versions, and to find the commit that caused a regression.

## Explanation

### The model

```
working tree  ──git add──►  staging area  ──git commit──►  local repository  ──git push──►  remote repository
     ▲                                                          │    ▲                          │
     └──────────── git restore / git switch ────────────────────┘    └──────── git fetch ───────┘
```

- **Working tree:** the files that you edit.
- **Staging area (index):** the changes that go into the next commit. `git add` puts changes there. `git restore --staged <file>` takes them out again.
- **Commit:** a recorded version of all tracked files, with an author, a date, a message, and the ID of its parent commit. The commit ID is a hash, for example `3f2a9c0`.
- **Branch:** a movable name that points to a commit. A new commit moves the current branch forward. `HEAD` is the commit that you have now.
- **Remote:** a copy of the repository on a server, usually named `origin`. `origin/master` is your local record of the `master` branch on the remote, from the last `fetch`.

### Remote work

| Task | Command |
|---|---|
| Copy a remote repository | `git clone <url>` |
| Show the remotes | `git remote -v` |
| Get the new commits without a change to your branches | `git fetch` |
| Get the new commits and merge them into the current branch | `git pull` (= `fetch` + `merge`) |
| Send a new branch, and connect it to the remote branch | `git push -u origin feature/cart-tests` |
| Send more commits on a connected branch | `git push` |
| Delete a remote branch | `git push origin --delete feature/cart-tests` |
| Compare your branch with the remote | `git status` (after `git fetch`), `git log --oneline origin/master..HEAD` |

**Authentication to GitHub:**

- **SSH key** (recommended): make a key with `ssh-keygen -t ed25519`, and add the **public** key (`~/.ssh/id_ed25519.pub`) in GitHub under "Settings", "SSH and GPG keys". Check it with `ssh -T git@github.com`. Use the SSH clone URL `git@github.com:<owner>/<repository>.git`. Phase 5, topic 5.10 explains SSH keys in detail.
- **HTTPS with a token:** GitHub does not accept your account password for git. Use the GitHub CLI (`gh auth login`), or a personal access token with a limited scope and an expiry date.
- Never put a token or a private key in a repository, a script, or a CI log.

### Pull requests and code review

A **pull request** (PR; GitLab says "merge request") asks the team to merge a branch. It is the place for code review and for automatic checks.

1. Make a branch from the current `master`: `git switch -c feature/cart-tests`.
2. Commit small, complete steps. Push the branch.
3. Open the pull request (in the web page, or `gh pr create`). Write what changed, why, and how you tested it.
4. The CI pipeline runs on the pull request. Its result is a quality gate (phase 8).
5. Reviewers comment, request changes, or approve. You answer each comment, and push new commits to the same branch.
6. Merge when the checks pass and the reviewers approve. Delete the branch.

**Merge options** in the web page:

| Option | Result |
|---|---|
| Merge commit | All commits of the branch, and a merge commit |
| Squash and merge | One new commit with all changes of the branch. A clean history on `master`. |
| Rebase and merge | The commits of the branch, copied on top of `master`. A straight history. |

**Review of test code:** check what the test case checks, not only the style. Questions for a review: Can this test fail? Does its name say what it checks? Does it depend on other tests or on fixed waits? Does it contain a password or a URL? Is the expected value from the requirement, or copied from the actual output of the SUT?

### Undo changes

| Situation | Command | Safe after a push? |
|---|---|---|
| Discard the changes in a file in the working tree | `git restore <file>` | Yes (only local). **The changes are lost.** |
| Take a file out of the staging area | `git restore --staged <file>` | Yes |
| Change the message or content of the last commit | `git commit --amend` | **No.** It makes a new commit ID. |
| Undo the last commit, keep its changes staged | `git reset --soft HEAD~1` | **No** |
| Undo the last commit, keep its changes in the working tree | `git reset HEAD~1` | **No** |
| Undo the last commit and **discard** its changes | `git reset --hard HEAD~1` | **No.** Uncommitted changes are lost too. |
| Undo a commit that is already on the remote | `git revert <commit>` | **Yes.** It makes a new commit with the reverse change. |
| Put unfinished work aside | `git stash push -m "half done"`, later `git stash pop` | Yes (only local) |
| Find a commit that you "lost" (for example after `reset --hard`) | `git reflog`, then `git switch -c rescue <commit>` | Yes (only local) |

**Rule:** do not rewrite commits that other people already have (`amend`, `reset`, `rebase` on a pushed branch). Use `revert` for shared history. If you must rewrite your own pushed branch, use `git push --force-with-lease`, never `--force`.

**A secret in a commit:** a commit with a password stays in the history, also after a new commit removes the password. Change the password at once (it is now known), then ask for help to clean the history.

### Merge and rebase

- `git merge master` (on your branch) joins the two histories with a merge commit. The history shows what really happened.
- `git rebase master` (on your branch) copies your commits on top of the newest `master`. The history is straight, but the commits get new IDs.
- Use rebase only on your own branch before other people use it. `git pull --rebase` updates your branch without merge commits.
- A conflict can occur in both cases. Resolve it in the files, `git add` the files, then `git merge --continue` or `git rebase --continue`. `git merge --abort` and `git rebase --abort` go back to the state before.

### Branching strategies

| Strategy | How it works | Fits |
|---|---|---|
| Feature branches (GitHub flow) | Short branches from `master`, merged through pull requests. `master` is always releasable. | Most teams, continuous delivery |
| Trunk-based development | Very short branches (hours to a day), or commits directly to the main branch. Unfinished features hide behind feature toggles. | Teams with strong automated tests and CI |
| Git Flow | `develop`, `feature/*`, `release/*`, and `hotfix/*` branches | Products with planned releases and several supported versions |
| Release branches | A branch for each release version, for fixes of that version | Products with old versions in maintenance |

The CTAL-TAE syllabus recommends an agreed branching strategy with branches for features, releases, and fixes (section 4.3.1). The test strategy must say which suites run on which branch (phase 8).

### Git for test work

- **Where the testware lives:** in the repository of the SUT (tests change with the code in the same pull request), or in its own repository (one TAS for several systems). In its own repository, record which testware version tests which SUT version.
- **Tags for versions:** `git tag -a v1.4.0 -m "Testware for shop release 1.4.0"`, then `git push origin v1.4.0`. A tag marks the exact testware for a release (CTAL-TAE section 5.1.2).
- **Find when something changed:**

  | Question | Command |
  |---|---|
  | Which commits changed this file? | `git log --oneline -- tests/ui/pages/cart_page.py` |
  | What did each commit change in it? | `git log -p -- <file>` |
  | Which commit added or removed this text? | `git log -S "add-to-cart" --oneline` |
  | Who last changed each line, and in which commit? | `git blame <file>` |
  | What is in this commit? | `git show <commit>` |

- **Find the commit that caused a regression:** `git bisect` (next section).
- **Do not commit** test reports, screenshots, traces, virtual environments, and `.env` files. Keep them out with `.gitignore`. The CI system stores reports as artifacts.

### Find a regression with `git bisect`

A test passed in an old version and fails now. Somewhere between them, one commit broke it. `git bisect` does a binary search: it checks out a commit in the middle, you say "good" or "bad", and it halves the range again. For 1000 commits, it needs about 10 steps.

```sh
git bisect start
git bisect bad                 # the current commit is bad
git bisect good v1.3.0         # this tag (or commit) was good
# git checks out a commit in the middle. Test it, then:
git bisect good                # or: git bisect bad
# ... repeat until git names the first bad commit ...
git bisect reset               # go back to where you started
```

**Automatic:** give `git bisect run` a command. Exit code 0 means good. Exit codes 1–127 mean bad, except 125, which means "cannot test this commit, skip it".

```sh
git bisect start HEAD v1.3.0
git bisect run uv run pytest tests/api/test_shipping.py
git bisect reset
```

For a SUT regression, the test command must use the same version of the tests in each step. If the tests are in the same repository as the SUT, copy the test file to a place outside the repository first, and run that copy.

### Practice repository for `git bisect`

This script makes a small repository with 20 commits. One commit, at a random position, breaks a shipping rule. Copy the script to `labs/phase-8-ci/make-bisect-practice.sh` and run it in a Linux shell.

```bash
#!/usr/bin/env bash
# Make a practice repository with 20 commits. One commit breaks the shipping rule.
set -euo pipefail

dir="${1:-bisect-practice}"
if [[ -e "$dir" ]]; then
    echo "ERROR: $dir exists already." >&2
    exit 1
fi
mkdir "$dir"
cd "$dir"
git init -q
git config user.name "Practice"
git config user.email "practice@example.test"
echo "__pycache__/" > .gitignore

cat > shop.py <<'PY'
def shipping_cost(order_value: float) -> float:
    if order_value < 25.00:
        return 4.99
    if order_value >= 50.00:
        return 0.00
    return 2.99
PY

cat > check.py <<'PY'
from shop import shipping_cost

assert shipping_cost(24.99) == 4.99
assert shipping_cost(25.00) == 2.99
assert shipping_cost(50.00) == 0.00, "50.00 must have free shipping"
print("OK")
PY

git add .
git commit -q -m "Add the shipping cost rule"

broken=$((RANDOM % 19 + 2))
for step in $(seq 2 20); do
    echo "Change $step" >> CHANGES.txt
    if [[ $step -eq $broken ]]; then
        sed -i 's/>= 50.00/> 50.00/' shop.py
    fi
    git add .
    git commit -q -m "Update the change log, step $step"
done

echo "The repository $dir has 20 commits. One of them breaks check.py."
```

## Example

A tester finds a failed UI test after a weekend with 40 merged pull requests:

```sh
git log -S "data-testid=\"add-to-cart\"" --oneline      # which commit changed the button?
git bisect start HEAD release-1.3                       # or bisect the SUT with the failing test
git bisect run ./run-one-test.sh                        # a script that starts the SUT and runs one test
```

The result names one commit. The tester reads it with `git show`, and writes a defect report with the commit ID, or fixes the locator in the page object if the change was intended.

## Common mistakes

| Mistake | Result | Fix |
|---|---|---|
| Work directly on `master` | No review, no pull request checks, conflicts with other people | A short branch for each change |
| Huge commits with many unrelated changes | Hard to review, hard to revert, `git bisect` finds a large commit | Small commits, each with one purpose |
| Messages such as "fix" or "wip" | The history does not explain anything | One line in the imperative that says what and why: "Wait for the cart count after removal" |
| `git push --force` on a shared branch | Other people lose commits | `git revert`, or `--force-with-lease` on your own branch only |
| `git reset --hard` with uncommitted work | The work is lost | `git stash` first. `git reflog` finds lost commits, not lost uncommitted changes. |
| A password or token in a commit | The secret is public in the history | Change the secret at once. Use environment variables and the CI secret store. |
| A new `git bisect start` before `git bisect reset` of the last search | The new search starts from a commit in the middle, and names a wrong commit | Always end a search with `git bisect reset`. `git bisect log` shows a search that is still open. |
| Test reports and virtual environments in the repository | A large repository, merge conflicts in generated files | `.gitignore`, CI artifacts |
| Expected values copied from the SUT output into a test in the same pull request as the SUT change | The test confirms the defect | Take expected values from the requirement. Review test changes and code changes separately. |

## Sources

- Pro Git (free, git-scm.com/book): "Git Basics", "Git Branching", "Git Tools" (stashing, rewriting history, debugging with git: `blame` and `bisect`)
- GitHub documentation (docs.github.com): "About pull requests", "Connecting to GitHub with SSH", "Managing your personal access tokens"
- The `man` pages: `git-bisect`, `git-reset`, `git-revert`, `git-rebase`
- CTFL v4.0.1, section 5.4. CTAL-TAE v2.0, sections 4.3.1 and 5.1.2.
