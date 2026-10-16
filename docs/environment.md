# Environment

This document helps you select an operating system (OS) for the course. It also gives the computer requirements. The course documents use Ubuntu Linux. With a different OS, ask the AI mentor to translate the commands, or use the notes below.

## Computer requirements

| Item | Minimum | Recommended |
|---|---|---|
| CPU | 64-bit, 4 cores, hardware virtualization enabled in the firmware settings (Intel VT-x or AMD-V; Apple silicon has it) | 8 cores |
| RAM | 8 GB | 16 GB. Docker, a browser, and an editor use much memory together. |
| Free disk space | 30 GB | 60 GB |
| Network | Internet access to install tools and container images | |
| Rights | Administrator rights to install software | |

If your computer is a company computer, ask your IT department whether you can install WSL2, Docker, and Python. Some companies block them.

## How to select an operating system

| OS | Fit with the documents | How you get a Linux shell for phase 0 | Notes |
|---|---|---|---|
| **Linux** (reference: Ubuntu LTS, 24.04 or newer) | All commands are for Ubuntu | You have it | Other distributions work. On Fedora, use `dnf` in place of `apt`. On Arch, use `pacman`. The mentor translates. |
| **Windows 11** | Very good with WSL2 | WSL2 with Ubuntu | **Recommended for Windows:** do all course work inside WSL2. Then all commands in the documents work as they are. |
| **macOS** | Good. The terminal is Unix, but some tools are different. | An Ubuntu container or virtual machine | macOS uses BSD versions of some tools (`sed`, `date`, `find`), and `ifconfig` in place of `ip`. The mentor shows the differences. |

If you are not sure, use Linux. If you must use Windows, use WSL2.

**Why Linux:** most servers, containers, and CI runners use Linux. Test environments run on Linux. A test automation engineer must read logs, start services, and connect to test hosts on Linux.

## Linux (reference)

Install Ubuntu LTS on the computer, or in a virtual machine (for example VirtualBox, VMware Workstation, or GNOME Boxes). A dual boot is also possible. Then follow [software-setup.md](software-setup.md).

## Windows with WSL2

WSL2 (Windows Subsystem for Linux, version 2) runs a real Linux kernel in a light virtual machine. You get a full Ubuntu system in a Windows terminal.

- Install it with `wsl --install` in an administrator PowerShell. This installs Ubuntu by default.
- Keep your course files in the Linux file system (for example `~/qa-automation-course`), not in `/mnt/c/...`. File access across the two systems is slow, and file permissions do not work correctly there.
- Use VS Code with the "WSL" extension. VS Code then runs its tools inside Ubuntu.
- Docker: install Docker Desktop with the WSL2 back end, or install Docker Engine directly in Ubuntu. Docker Desktop needs a paid subscription in large companies. Read the Docker license terms.
- Browsers for Playwright: Playwright installs its own browsers inside Ubuntu. WSLg (included in Windows 11) shows the browser windows.

## macOS

- Use the Terminal app (or iTerm2) with `zsh` or `bash`. Install the tools with Homebrew.
- Docker: install Docker Desktop, OrbStack, or Colima. Read the license terms of each tool.
- Phase 0 needs a Linux shell. Use one of these options:
  - An Ubuntu container: `docker run -it --rm ubuntu:24.04 bash`. Good for most exercises. Data in the container is lost when it stops, unless you mount a directory.
  - A virtual machine with Ubuntu: Multipass, UTM, or Parallels. Good for the exercises with services (`systemd`) and users.
- On Apple silicon (M-series CPUs), use container images for `arm64`. The course SUT images build for your CPU automatically.

## A cloud virtual machine (optional)

A small Linux virtual machine at a cloud provider gives you a real remote host for the SSH and networking exercises in phases 5 and 8. It costs money. The course does not need it: the SUT has a local SSH test host.

## Record your selection

The AI mentor records your OS, your Linux access method, and your language in the "Environment" section of `learner/profile.md`. Without a mentor, write them in your progress file.
