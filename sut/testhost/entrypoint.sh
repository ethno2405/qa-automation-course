#!/usr/bin/env bash
# Prepare the user "tester" and start the SSH server.
set -euo pipefail

echo "tester:${TESTHOST_PASSWORD:-tester}" | chpasswd

# Copy the public keys of the learner, if the file exists.
if [[ -f /ssh-keys/authorized_keys ]]; then
  install -d -m 700 -o tester -g tester /home/tester/.ssh
  install -m 600 -o tester -g tester /ssh-keys/authorized_keys /home/tester/.ssh/authorized_keys
fi

ssh-keygen -A
exec /usr/sbin/sshd -D -e
