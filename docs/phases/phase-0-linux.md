# Phase 0: Linux and the Command Line

**Time:** 2–3 weeks. Do this phase in parallel with phase 1.
**Prerequisites:** None.
**Environment:** A Linux shell: Ubuntu, Ubuntu in WSL2 (Windows), or an Ubuntu container or virtual machine (macOS). See [../environment.md](../environment.md).

## Goal

At the end of this phase, you can:

- Move in the Linux file system, and make, copy, move, and delete files and directories.
- Read and change file permissions and owners, and explain when to use `sudo`.
- See and stop processes, and read the logs of a service.
- Combine commands with pipes and redirection to search and count data in log files.
- Use environment variables and the `PATH`.
- Install software with the package manager.
- Write a Bash script with arguments, conditions, loops, exit codes, and error handling.
- Use git for daily work: clone, commit, branch, merge, push.

## Why a tester needs Linux

Most test environments, containers, and CI runners use Linux. A test automation engineer often must:

- Start and stop the SUT and its services.
- Read the logs of the SUT to find the cause of a failed test.
- Connect to a test host with SSH (phase 5) and run commands there.
- Write small scripts that prepare test data or start the tests.
- Understand the errors of CI jobs, which run shell commands.

## Reading

| Source | Part |
|---|---|
| William Shotts, *The Linux Command Line* (free, linuxcommand.org) | Part 1 (learning the shell) and part 4 (writing shell scripts). Use part 2 and part 3 as a reference. |
| The `man` pages | `man ls`, `man grep`, and so on. Read the "DESCRIPTION" and the options that you use. |
| Pro Git (free, git-scm.com/book) | Chapters about the basics, branches, and remote repositories |
| Julia Evans, zines about the command line (wizardzines.com) | Optional. Short and visual. |

## Topics

### 0.1 The shell and the terminal

- The **terminal** is the window. The **shell** is the program in the window that reads your commands. The course uses **Bash**. macOS uses `zsh` by default: most commands are the same.
- A command has the form `command -options arguments`. Example: `ls -l /etc`.
- Help: `man <command>`, `<command> --help`, and `type <command>` (shows whether a command is a program, a built-in, or an alias).
- Keys that save time: `Tab` (complete a name), `Up` (the last command), `Ctrl+R` (search in the history), `Ctrl+C` (stop the running command), `Ctrl+D` (end the input, or close the shell).

### 0.2 The file system and paths

- Linux has one directory tree. It starts at `/` (the root directory). There are no drive letters.
- Important directories: `/home/<user>` (your files, also `~`), `/etc` (configuration), `/var/log` (logs), `/tmp` (temporary files), `/usr/bin` (programs), `/opt` (extra software).
- An **absolute path** starts at `/`: `/home/anna/notes.txt`. A **relative path** starts at the current directory: `notes.txt`, `../other/file`.
- `.` is the current directory. `..` is the parent directory. `~` is your home directory.
- File names are case-sensitive: `Test.txt` and `test.txt` are two files.
- A file name that starts with `.` is hidden. `ls -a` shows it.

### 0.3 Files and directories

| Task | Command |
|---|---|
| Show the current directory | `pwd` |
| List files, with details and hidden files | `ls -la` |
| Change the directory | `cd <path>` |
| Make a directory (with parents) | `mkdir -p a/b/c` |
| Copy a file, a directory | `cp src dst`, `cp -r srcdir dstdir` |
| Move or rename | `mv old new` |
| Delete a file, an empty directory | `rm file`, `rmdir dir` |
| Delete a directory with its content | `rm -r dir` |
| Find files by name | `find . -name "*.log"` |
| Show a tree | `tree -L 2` |
| Show the size of a directory | `du -sh dir` |
| Show free disk space | `df -h` |

**Caution:** `rm` does not use a trash bin. A deleted file is lost. `rm -rf` deletes without questions. Read the command two times before you press `Enter`, and never run `rm -rf` with a variable that can be empty.

### 0.4 Read and edit text

| Task | Command |
|---|---|
| Show a whole file | `cat file` |
| Show a long file page by page | `less file` (`q` to quit, `/text` to search) |
| Show the first or last lines | `head -n 20 file`, `tail -n 20 file` |
| Follow a growing log file | `tail -f file` |
| Edit a file | `nano file` (easy), or `vim file` (powerful) |
| Compare two files | `diff -u a b` |

Learn the basics of `vim`: you will meet it on servers where no other editor is installed. Minimum: `i` (insert mode), `Esc` (normal mode), `:w` (write), `:q` (quit), `:q!` (quit without a save).

### 0.5 Users, groups, and permissions

- Each file has an **owner**, a **group**, and permissions for three classes: the owner (`u`), the group (`g`), and others (`o`).
- `ls -l` shows the permissions: `-rwxr-x---` means: a file, owner can read, write, execute; group can read, execute; others nothing.
- Permissions as numbers: read = 4, write = 2, execute = 1. `chmod 750 script.sh` = `rwxr-x---`.
- `chmod +x script.sh` makes a script executable. `chown user:group file` changes the owner (needs `sudo`).
- On a directory, "execute" means "can enter the directory".
- `root` is the administrator. `sudo <command>` runs one command as root. Use `sudo` only when necessary, and understand the command first.
- `id` shows your user and your groups. `whoami` shows your user name.

### 0.6 Processes and signals

- A **process** is a running program. Each process has a process ID (PID) and a parent process.
- `ps aux` lists all processes. `ps aux | grep python` finds the Python processes. `top` or `htop` shows them live.
- `kill <PID>` sends the signal `SIGTERM`: "stop, please". The program can clean up. `kill -9 <PID>` sends `SIGKILL`: the kernel stops the process at once, with no cleanup. Use it only when `SIGTERM` does not work.
- `command &` runs a command in the background. `jobs`, `fg`, and `bg` control background jobs.
- **Exit code:** each command returns a number when it ends. `0` means success. Other values mean an error. `echo $?` shows the exit code of the last command. Test runners use exit codes: pytest returns `1` when a test fails, so a CI job fails.
- `lsof -i :8000` or `ss -ltnp` shows which process uses a port. (Phase 5 explains ports.)

### 0.7 Pipes, redirection, and text tools

- Each process has three standard streams: input (`stdin`, 0), output (`stdout`, 1), and error (`stderr`, 2).
- Redirection:

  | Syntax | Effect |
  |---|---|
  | `cmd > file` | Write `stdout` to a file (replace the file) |
  | `cmd >> file` | Append `stdout` to a file |
  | `cmd 2> file` | Write `stderr` to a file |
  | `cmd > file 2>&1` | Write `stdout` and `stderr` to the same file |
  | `cmd < file` | Read `stdin` from a file |

- A **pipe** `cmd1 | cmd2` sends the `stdout` of `cmd1` to the `stdin` of `cmd2`.
- Text tools for log analysis:

  | Tool | Use | Example |
  |---|---|---|
  | `grep` | Find lines | `grep -i error app.log`, `grep -c`, `grep -v`, `grep -E "4[0-9]{2}"` |
  | `wc` | Count lines, words | `wc -l` |
  | `sort`, `uniq` | Sort, remove or count duplicates | `sort \| uniq -c \| sort -rn` |
  | `cut` | Cut columns | `cut -d, -f2` |
  | `awk` | Columns and simple calculations | `awk '{print $9}'` |
  | `sed` | Replace text | `sed 's/old/new/g'` |
  | `jq` | JSON | `jq -r '.status'`, `jq 'select(.level=="ERROR")'` |
  | `xargs` | Use lines as arguments | `find . -name "*.tmp" \| xargs rm` |

- The course shop writes JSON log lines (see [../../sut/README.md](../../sut/README.md)). `jq` is the best tool to read them.

### 0.8 Environment variables and the PATH

- An environment variable is a named value that a process gets from its parent. Examples: `HOME`, `USER`, `PATH`.
- `echo "$HOME"` shows a value. `env` shows all. `export NAME=value` sets a variable for the shell and its children. `NAME=value command` sets it only for one command.
- `PATH` is a list of directories, separated by `:`. The shell looks for programs in these directories, in this order. `which python3` shows which program runs.
- Tests read their configuration (for example the SUT address) from environment variables. CI systems give secrets to jobs as environment variables.
- Put permanent settings in `~/.bashrc`. Run `source ~/.bashrc` to load them in the open shell.

### 0.9 Packages, services, and logs

- **Package manager** (Ubuntu: `apt`): `sudo apt update` (get the package lists), `sudo apt install <package>`, `apt search <text>`, `sudo apt upgrade`.
- **Services** (`systemd`): a service is a program that runs in the background, for example a web server or an SSH server.

  | Task | Command |
  |---|---|
  | Show the status | `systemctl status ssh` |
  | Start, stop, restart | `sudo systemctl start ssh` (also `stop`, `restart`) |
  | Start at boot | `sudo systemctl enable ssh` |
  | Show the log of a service | `journalctl -u ssh`, `journalctl -u ssh -f`, `journalctl -u ssh --since "10 min ago"` |

- In WSL2, `systemd` is enabled by default in new installations. In a container, `systemd` usually does not run. Use a virtual machine or WSL2 for the service exercises.
- **Logs:** many programs write to `/var/log/` or to the journal. Containers write to `stdout`: use `docker compose logs <service>`.

### 0.10 Bash scripts

A script is a text file with commands. Example:

```bash
#!/usr/bin/env bash
# Wait until a URL answers with HTTP 200, or stop after a timeout.
set -euo pipefail

url="${1:?Usage: wait-for.sh <url> [timeout-seconds]}"
timeout="${2:-60}"

for ((second = 0; second < timeout; second++)); do
    if curl --silent --fail --output /dev/null "$url"; then
        echo "OK: $url answers."
        exit 0
    fi
    sleep 1
done

echo "ERROR: $url does not answer after $timeout seconds." >&2
exit 1
```

- The first line (the "shebang") selects the interpreter.
- `set -euo pipefail`: stop on an error (`-e`), stop on an unset variable (`-u`), and fail a pipeline if any command in it fails (`-o pipefail`).
- Always put variables in double quotes: `"$file"`. Without quotes, a value with spaces becomes several arguments.
- Arguments: `$1`, `$2`, `$@` (all), `$#` (count). `${1:-default}` gives a default value. `${1:?message}` stops with a message if the argument is missing.
- Conditions: `if [[ -f "$file" ]]; then ... fi`. Tests: `-f` (file exists), `-d` (directory exists), `-z` (empty string), `==`, `!=`, `-eq`, `-lt` (numbers).
- Loops: `for file in *.log; do ... done`, `while read -r line; do ... done < file`.
- Functions: `log() { echo "[$(date +%T)] $*"; }`.
- Messages for the user go to `stderr` (`>&2`). Data goes to `stdout`.
- Check each script with `shellcheck script.sh`.

### 0.11 git

- **Repository:** a directory with the full history of a project (`.git/`).
- **Commit:** a recorded version. **Branch:** a movable name for a line of commits. **Remote:** a copy on a server (for example GitHub).
- Daily commands:

  | Task | Command |
  |---|---|
  | Copy a repository | `git clone <url>` |
  | Show the state | `git status` |
  | Show the changes | `git diff`, `git diff --staged` |
  | Stage and commit | `git add <files>`, `git commit -m "Add login tests"` |
  | Show the history | `git log --oneline --graph` |
  | Make and change branches | `git switch -c feature/x`, `git switch master` |
  | Merge a branch | `git merge feature/x` |
  | Get and send changes | `git pull`, `git push` |
  | Discard local changes in a file | `git restore <file>` |

- The `.gitignore` file lists files that git does not track: virtual environments, test reports, secrets.
- Write commit messages in the imperative: "Add cart tests", not "Added cart tests".
- This course uses git for your progress. See the [main README](../../README.md), "Branches".
- Remote repositories, pull requests, undo commands, and more: read the topic [Git for testers](../topics/git-for-testers.md) before exercise 0.11.

## Exercises

Do the exercises in your Linux shell. Write the commands that you used and the results in your test journal.

### Exercise 0.1: Navigation

1. Show your current directory and your home directory.
2. Go to `/etc`. List the files that end with `.conf`. Count them.
3. Go back to your home directory in three different ways (`cd`, `cd ~`, an absolute path).
4. Find the five largest files in `/usr/bin`. (Hint: `ls -lS`, or `du` with `sort`.)

### Exercise 0.2: Files and directories

1. Make this structure with as few commands as possible: `practice/logs/2026`, `practice/data`, `practice/scripts`.
2. Make three empty files in `practice/logs/2026` with `touch`.
3. Copy `practice/logs` to `practice/logs-backup`. Rename `practice/data` to `practice/testdata`.
4. Delete `practice/logs-backup`. Explain why `rmdir` does not work here.

### Exercise 0.3: Permissions

1. Make a file `secret.txt`. Set its permissions so that only you can read and write it. Show the result with `ls -l`.
2. Make a script `hello.sh` that prints "Hello". Try to run it with `./hello.sh`. Explain the error. Fix it.
3. Explain the difference between `chmod 644` and `chmod 755`. For which files do you use each?
4. Run `sudo -l`. Explain what it shows.

### Exercise 0.4: Read text

1. Open `/etc/passwd` with `less`. Find your user. Explain the fields of the line (`man 5 passwd`).
2. Show the first 5 and the last 5 lines of `/etc/services`.
3. Find the port of the service `ssh` in `/etc/services` with `grep`.

### Exercise 0.5: Processes

1. Start `sleep 300 &`. Find its PID with `ps` and with `jobs -l`.
2. Stop it with `kill`. Show that it does not run any more.
3. Run `ls /nonexistent`, then `echo $?`. Run `ls /`, then `echo $?`. Explain the two values.
4. Start the course shop (`cd sut && docker compose up -d`). Find the process or the container that uses port 8000.

### Exercise 0.6: Log analysis

1. Start the course shop. Open `http://127.0.0.1:8000` in a browser. Search, register a user, and log in with a wrong password three times.
2. Save the log: `docker compose logs --no-log-prefix shop > shop.log`. The log also contains the health checks of Docker: a request to `/api/health` every 30 seconds. Decide whether to count them, and remove them with `grep -v` or a `jq` filter if not.
3. With pipes and text tools (`grep`, `jq`, `sort`, `uniq`, `wc`), answer these questions:
   - How many HTTP requests are in the log?
   - How many requests had a status code of 400 or more?
   - Which paths were requested most often? Show the top 5 with their counts.
   - Which events are in the log, and how many of each?
   - What is the longest request duration?
4. Write each command line in your test journal.

**Side project (optional):** make a small "log toolkit": a directory of Bash scripts that answer the questions above for any log file of the shop.

### Exercise 0.7: Environment variables

1. Show the value of `PATH`. Split it into one directory per line with `tr`.
2. Set a variable `SHOP_URL=http://127.0.0.1:8000` for one command only: `SHOP_URL=http://127.0.0.1:8000 bash -c 'echo $SHOP_URL'`. Then show that the variable is not set in your shell.
3. Add `export SHOP_URL=http://127.0.0.1:8000` to `~/.bashrc`. Load it. Show the value in a new terminal.
4. Explain why tests must read the SUT address from a variable and not from the code.

### Exercise 0.8: Packages and services

Use Ubuntu, WSL2, or a virtual machine (not a container) for this exercise.

1. Install the package `nginx` with `apt`.
2. Show the status of the service. Open `http://localhost` (or `curl -I http://localhost`).
3. Stop the service. Show that the page does not answer. Show the last 20 lines of its journal.
4. Remove the package with `sudo apt remove nginx`.

### Exercise 0.9: Bash script (main project, stage 0)

Write `labs/tas/scripts/start-sut.sh`:

1. It starts the course shop with `docker compose up -d` in the `sut/` directory. The script must work from any current directory.
2. It accepts an optional argument: the value of `SUT_DEFECTS` (default `none`).
3. It waits until `http://127.0.0.1:8000/api/health` answers, with a timeout of 60 seconds.
4. On success, it prints the version and the defect mode from the health response (use `jq`), and exits with 0.
5. On a timeout, it prints the last 20 log lines of the shop to `stderr`, and exits with 1.
6. `shellcheck` reports no problems.

Test the script: start it with the shop stopped, with the shop already running, and with Docker stopped.

### Exercise 0.10: git

1. Make a new directory with `git init`. Add a file, commit it. Change it, commit again. Show the history.
2. Make a branch, change the file there, commit, switch back, and merge the branch.
3. Make a merge conflict on purpose: change the same line on two branches, and merge. Resolve the conflict.
4. Add a `.gitignore` that ignores `*.log` and `.venv/`. Show with `git status` that a log file is ignored.

### Exercise 0.11: Remote workflow

Read the topic [Git for testers](../topics/git-for-testers.md) first. Use a new practice repository for this exercise, not the course repository: the course repository contains your learner data.

1. Make a GitHub account if you do not have one. Make a new **private** repository `git-practice` with a README file.
2. Make an SSH key and add the public key to GitHub (or use `gh auth login`). Check the connection with `ssh -T git@github.com`.
3. Clone the repository with the SSH URL. Add a file, commit it, and push it. Show the commit on the web page.
4. **Pull request:** make a branch `feature/notes`, make two small commits, and push the branch. Open a pull request. Write a comment on one line of your own change, as a reviewer would. Fix the point in a new commit and push it. Merge the pull request with "Squash and merge". Delete the branch on GitHub, then update your local `master` and delete the local branch.
5. **A teammate:** change one line of a file in the GitHub web editor, directly on `master`. Then change the same line locally, commit, and run `git pull`. Resolve the conflict and push.
6. **Undo:** do each step, and check the result with `git log --oneline` and `git status`:
   - Change the message of your last commit before you push it (`--amend`).
   - Undo your last local commit, and keep the changes (`reset --soft`).
   - Revert a commit that is already on GitHub (`revert`), and push.
   - Put unfinished changes aside with `git stash`, switch the branch, come back, and get them again.
   - Make a commit, run `git reset --hard HEAD~1`, and get the commit back with `git reflog`.
7. Make an annotated tag `v0.1` and push it. Find it on the web page.
8. Write each command and what it did in your test journal.

## Done criteria

- [ ] I can move in the file system with absolute and relative paths.
- [ ] I can read and set permissions, and explain when `sudo` is necessary.
- [ ] I can find and stop a process, and explain exit codes.
- [ ] I can answer questions about a log file with a pipeline of text tools and `jq`.
- [ ] I can set environment variables for one command and permanently.
- [ ] I can start, stop, and read the log of a service.
- [ ] My `start-sut.sh` script works, handles errors, and passes `shellcheck`.
- [ ] I can use git for commits, branches, merges, and conflicts.
- [ ] I can work with a remote repository: push, pull, a pull request with a review, and safe undo of mistakes.

## Next

[Phase 1: Programming and OOP for testers](phase-1-programming-oop.md) (in parallel), then [Phase 2: Testing fundamentals](phase-2-testing-fundamentals.md)
