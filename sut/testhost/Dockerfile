# SSH test host for the networking (phase 5) and remote run (phase 8) exercises.
FROM ubuntu:24.04

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      openssh-server sudo ca-certificates curl jq git less nano rsync \
      iproute2 iputils-ping traceroute dnsutils netcat-openbsd tcpdump \
      python3 python3-venv \
 && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/bash tester \
 && usermod -aG sudo tester \
 && mkdir -p /run/sshd

COPY entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh

EXPOSE 22
ENTRYPOINT ["/entrypoint.sh"]
