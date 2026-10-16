# Software Setup

This document tells you which tools to install and how to do a check of each tool. The commands are for Ubuntu (the reference OS) and for Ubuntu in WSL2. Notes for macOS are at the end. For Java, C#, or TypeScript, see [languages.md](languages.md), or ask the AI mentor for the exact setup.

You do not need all tools on the first day. The table shows the phase where you need each tool first.

## 1. Install the tools

| Tool | Phase | Purpose |
|---|---|---|
| Git | 0 | Version control |
| Basic shell tools: `curl`, `jq`, `tree`, `nano` or `vim`, `shellcheck` | 0 | Downloads, JSON on the command line, file trees, text editors, script checks |
| A text editor, for example VS Code | 0 | Editor |
| `uv` and Python 3.13 or newer | 1 | Python versions, projects, virtual environments, dependencies |
| Network tools: `iproute2`, `iputils-ping`, `traceroute`, `dnsutils`, `netcat-openbsd`, `tcpdump`, `openssh-client` | 5 | Phase 5 exercises |
| Wireshark (optional) | 5 | Graphical packet analysis |
| Docker Engine and Docker Compose | 0 (to run the SUT) | Containers for the SUT and the CI jobs |
| Playwright browsers (Chromium; later Firefox and WebKit) | 6 | Browser automation, cross-browser tests |
| A manual API tool: Postman, Insomnia, or Bruno | 6 | API exploration and collections |
| WireMock (a container image, no installation) | 6 | A stub server for HTTP services |
| GitHub account, and the GitHub CLI `gh` (optional) | 0 | Remote repositories, pull requests (exercise 0.11), CI pipelines (phase 8) |

### Shell tools

```sh
sudo apt update
sudo apt install -y git curl jq tree nano vim shellcheck build-essential
```

### Network tools (phase 5)

```sh
sudo apt install -y iproute2 iputils-ping traceroute dnsutils netcat-openbsd tcpdump openssh-client
```

### Python with uv

Install `uv` with the official installer. Read the script first if you want to know what it does.

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Open a new terminal. Then install Python:

```sh
uv python install 3.13
```

`uv` keeps its Python versions separate from the Python of the OS. Do not change or remove the system Python of Ubuntu: many system tools need it.

### Docker

Follow the official guide "Install Docker Engine on Ubuntu" on docs.docker.com. It installs Docker Engine and the Compose plugin. Then let your user run Docker without `sudo`:

```sh
sudo usermod -aG docker "$USER"
```

Log out and log in again. **Note:** members of the `docker` group have root rights on the computer. Do this only on your own computer.

On Windows, you can also install Docker Desktop with the WSL2 back end. See [environment.md](environment.md).

### A text editor

You can use any text editor. Examples: VS Code, PyCharm, Sublime Text, `nano`, or `vim`. The course recommends VS Code, because it is free and has good support for Python, Playwright, and WSL2.

Without a graphical desktop (in a container, on a server, or through SSH), use `nano` or `vim` in the terminal. You can also edit the files on your host computer with a graphical editor, if the directory is mounted in the container or shared with the virtual machine.

### VS Code

If you use VS Code, install it from code.visualstudio.com. Install these extensions:

- **Python** and **Pylance** (Microsoft)
- **Ruff** (Astral)
- **Playwright Test for VS Code** (Microsoft), optional for Python
- **WSL** (Microsoft), only on Windows
- **Docker** or **Container Tools** (Microsoft), optional

### Playwright browsers (phase 6)

Playwright needs its own browser builds. Install them inside a lab project:

```sh
uv add --dev pytest-playwright
uv run playwright install --with-deps chromium
```

`--with-deps` installs the system libraries. It asks for your `sudo` password.

## 2. Do a check of the tools

Run these commands in a new terminal. Each command must print a version or a result.

```sh
git --version
curl --version
jq --version
shellcheck --version
uv --version
uv run --python 3.13 python --version
docker --version
docker compose version
docker run --rm hello-world
```

In phase 5, also run:

```sh
ip -brief address
ping -c 2 127.0.0.1
dig +short example.com
ssh -V
```

## 3. Configure git

```sh
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch master
git config --global pull.rebase false
```

On Windows with WSL2, configure git inside Ubuntu. Line endings: the repository has a `.gitattributes` file. Do not change `core.autocrlf` inside WSL2.

## 4. Start the SUT

```sh
cd sut
docker compose up -d --build
curl -s http://127.0.0.1:8000/api/health
```

The last command must print `{"status":"ok", ...}`. See [../sut/README.md](../sut/README.md).

## macOS notes

- Install Homebrew from brew.sh. Then install the tools: `brew install git jq tree shellcheck uv`.
- Install Docker Desktop, OrbStack, or Colima. With Colima: `brew install colima docker docker-compose`, then `colima start`.
- Network tools: macOS has `ping`, `traceroute`, `dig`, `nc`, `ssh`, and `tcpdump`. It does not have `ip` and `ss`. Use `ifconfig`, `netstat -an`, and `lsof -i`, or run the Linux tools in an Ubuntu container.
- macOS uses BSD versions of `sed`, `date`, and `find`. Some options are different. In phase 0, use an Ubuntu virtual machine (recommended) or an Ubuntu container. A container has limits: no Docker, no browser, and a different `127.0.0.1`. See [environment.md](environment.md), section "macOS".
