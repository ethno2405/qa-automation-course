# Contributing

Did you find an error in the course? Thank you. Please send the fix as a pull request (PR). Then all learners get it.

Errors can be wrong facts, wrong commands, broken links, unclear text, code examples that fail, or a defect of the course shop that the course does not plan. The course shop has some defects on purpose (the seeded defects). They are not errors. If you are not sure, ask your AI mentor, or open an issue.

With an AI mentor, say for example: `I think exercise 3.5 has an error. Help me open a pull request with the fix.` The mentor follows `AGENTS.md`, "Errors in the course". Without a mentor, do the steps below.

## Steps

1. **Save your own work first.** Commit your learner data and code on your track branch.
2. **Make a fix branch from `master`**, never from your track branch. Your track branch contains personal data.

   ```sh
   git switch master
   git pull
   git switch -c fix/<short-name>
   ```

3. **Make the fix.** Keep it small: one error for each PR. Check the fix: run the changed code or command, and check the links.
4. **Commit only the files of the fix.** Never commit files in `learner/`, `labs/`, or `.github/workflows/`. Write the commit message as one line in the imperative, for example `Fix the shipping boundary in exercise 3.5`.
5. **Push the branch to your fork.** Make a fork on GitHub first if you do not have one (the "Fork" button, or `gh repo fork --remote --remote-name fork`).

   ```sh
   git push -u fork fix/<short-name>
   ```

6. **Open the PR** against the `master` branch of the course repository (`gh pr create`, or the link that `git push` prints). Write:
   - what was wrong, and where;
   - how you found it;
   - the fix;
   - how you checked the fix.
7. **Go back to your track branch.** To use the fix now, merge it: `git switch track/<YYYY-MM-DD>`, then `git merge fix/<short-name>`. When the course repository has the fix, `git merge master` brings it as usual.

## Rules

- Do not put personal data in a PR: no profile, no progress, no learner code, no names of other people.
- Write in ASD-STE100 Simplified Technical English, as the rest of the course (see `AGENTS.md`, "Writing style").
- Do not copy text from the ISTQB syllabi. Refer to the syllabus section and the learning objective.
- Do not describe the seeded defects of the course shop in documents that learners read before the exercises.
- If you change the course shop (`sut/`), run its smoke tests and start it with `docker compose up -d --build --wait`.

## Issues

If you do not know the correct fix, open an issue. Describe the error, the steps to see it, and the expected result.
