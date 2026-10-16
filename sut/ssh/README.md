# SSH keys for the test host

Put your **public** key in a file `authorized_keys` in this directory. The test host copies it when it starts. Git ignores `authorized_keys`.

```sh
cp ~/.ssh/id_ed25519.pub sut/ssh/authorized_keys
cd sut && docker compose restart testhost
```

Never put a private key here. See phase 5, exercise 5.7.
