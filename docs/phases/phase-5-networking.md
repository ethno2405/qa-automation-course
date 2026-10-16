# Phase 5: Networking Basics

**Time:** 2–3 weeks
**Prerequisites:** Phase 0
**Environment:** A Linux shell with the network tools (see [../software-setup.md](../software-setup.md)), the course shop and its test host (`cd sut && docker compose up -d`).

## Goal

At the end of this phase, you can:

- Explain the TCP/IP model and how data moves through the layers.
- Calculate the network address, the broadcast address, and the host range of an IPv4 network from an address and a mask.
- Explain IPv6 addresses, MAC addresses, ARP, routing, the default gateway, and NAT.
- Explain how DHCP gives a host its network configuration, and how DNS translates names.
- Explain TCP and UDP, ports, and the TCP three-way handshake, and see them in a packet capture.
- Read and write HTTP requests and responses, and explain what TLS adds.
- Use SSH with keys, a client configuration, file copy, and port forwarding.
- Find the cause of a network failure step by step.

## Why a tester needs networking

- API tests send HTTP requests. When a test fails with "connection refused" or "certificate verify failed", you must know which layer failed.
- Test environments have many hosts, containers, ports, and names. You must configure the address of the SUT and connect to test hosts with SSH.
- Many "flaky" tests are network problems: timeouts, DNS caches, proxies.
- The CTAL-TAE syllabus expects knowledge of the connectivity requirements of a TAS: firewalls, URLs and connections, protocols (section 3.1.2).

## Reading

| Source | Part |
|---|---|
| Kurose and Ross, *Computer Networking: A Top-Down Approach* | Chapter 1 (overview), then the parts about the application layer (HTTP, DNS), the transport layer (TCP, UDP), and the network layer (IP addressing, DHCP, NAT) |
| Julia Evans, *Networking! ACK!* and *How DNS Works* zines (wizardzines.com) | Optional. Short and visual. |
| MDN Web Docs, "An overview of HTTP" (developer.mozilla.org) | All |
| The man pages: `ip`, `ss`, `dig`, `curl`, `ssh`, `ssh_config`, `tcpdump` | The options that the exercises use |
| RFC 1918 (private addresses), RFC 9110 (HTTP semantics) | Reference only |

## Topics

### 5.1 Network models

- The **TCP/IP model** has four layers. The **OSI model** has seven. People use the OSI numbers in conversation: "a layer 7 problem" means an application problem.

  | TCP/IP layer | OSI layers | Unit | Examples | Address |
  |---|---|---|---|---|
  | Application | 7, 6, 5 | Message | HTTP, DNS, SSH, DHCP | URL, host name |
  | Transport | 4 | Segment (TCP), datagram (UDP) | TCP, UDP | Port |
  | Internet | 3 | Packet | IPv4, IPv6, ICMP | IP address |
  | Link | 2, 1 | Frame | Ethernet, Wi-Fi | MAC address |

- **Encapsulation:** each layer adds its own header to the data from the layer above. An HTTP request goes into a TCP segment, into an IP packet, into an Ethernet frame. The receiver removes the headers in the reverse order.

### 5.2 IPv4 addresses and subnet masks

- An IPv4 address has 32 bits, written as four decimal numbers (octets) from 0 to 255: `192.168.1.130`.
- The **subnet mask** divides the address into a **network part** and a **host part**. Two hosts are in the same network when their network parts are the same. The mask has ones for the network bits and zeros for the host bits.
- **CIDR notation** writes the number of network bits: `/24` = `255.255.255.0`.

  | Prefix | Mask | Addresses | Usable hosts |
  |---|---|---|---|
  | /8 | 255.0.0.0 | 16 777 216 | 16 777 214 |
  | /16 | 255.255.0.0 | 65 536 | 65 534 |
  | /24 | 255.255.255.0 | 256 | 254 |
  | /25 | 255.255.255.128 | 128 | 126 |
  | /26 | 255.255.255.192 | 64 | 62 |
  | /27 | 255.255.255.224 | 32 | 30 |
  | /28 | 255.255.255.240 | 16 | 14 |
  | /30 | 255.255.255.252 | 4 | 2 |

- Usable hosts = 2^(host bits) − 2. The first address is the **network address**. The last address is the **broadcast address**.
- **Worked example:** `192.168.1.130/26`.
  1. The mask /26 = 26 ones: `11111111.11111111.11111111.11000000` = `255.255.255.192`.
  2. Only the last octet is mixed. 130 in binary = `10000010`. The mask octet = `11000000`.
  3. Network address: 130 AND 192 = `10000000` = 128. The network is `192.168.1.128`.
  4. Host bits: 6. Block size: 2^6 = 64. Broadcast: 128 + 64 − 1 = 191. The broadcast address is `192.168.1.191`.
  5. Host range: `192.168.1.129` to `192.168.1.190`. 62 usable hosts.
- **Special ranges:**

  | Range | Use |
  |---|---|
  | `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` | Private addresses (RFC 1918). Not routed on the internet. |
  | `127.0.0.0/8` | Loopback. `127.0.0.1` (`localhost`) is the computer itself. |
  | `169.254.0.0/16` | Link-local. A host gives itself such an address when DHCP fails. |
  | `0.0.0.0` | "Any address" when a server listens. "No address" in other contexts. |

- **localhost and 0.0.0.0:** a server that listens on `127.0.0.1` accepts connections only from the same computer. A server that listens on `0.0.0.0` accepts connections on all interfaces. The course shop container listens on `0.0.0.0` inside the container, and Docker publishes the port only on `127.0.0.1` of your computer.

### 5.3 IPv6

- An IPv6 address has 128 bits, written as eight groups of four hexadecimal digits: `2001:0db8:0000:0000:0000:0000:0000:0001`. Short form: remove the leading zeros, and replace one run of zero groups with `::`: `2001:db8::1`.
- `::1` is the loopback address. Addresses that start with `fe80::` are link-local. Networks usually use a `/64` prefix.
- IPv6 has no broadcast. It uses multicast. Most hosts have IPv4 and IPv6 at the same time (dual stack). `localhost` can resolve to `::1` or to `127.0.0.1`: a test that connects to `localhost` can fail if the server listens only on one of them.
- **The course shop is an example.** Docker publishes its port only on `127.0.0.1`. On some computers (for example Windows), a connection to `localhost` first tries `::1`, waits for the failure, and then uses `127.0.0.1`. Each request can then take about 0.2 seconds more. A test suite with many requests becomes much slower, and nothing fails. This is why the course uses `http://127.0.0.1:8000`. Measure it yourself: `curl -s -o /dev/null -w "%{time_total}\n" http://localhost:8000/api/health`, then the same with `127.0.0.1`.

### 5.4 Ethernet, MAC addresses, and ARP

- A **MAC address** identifies a network interface on the local network: 48 bits, written as `02:42:ac:1c:00:0a`.
- Inside one network, frames go to MAC addresses, not IP addresses. **ARP** (Address Resolution Protocol) finds the MAC address for an IPv4 address in the same network: "Who has 172.28.0.10? Tell 172.28.0.20." IPv6 uses the Neighbor Discovery Protocol (NDP) for the same purpose.
- `ip neigh` shows the ARP cache.

### 5.5 Routing, the default gateway, and NAT

- A host sends a packet directly when the destination is in its own network. For all other destinations, it sends the packet to a **router**. The **default gateway** is the router for all destinations that have no more specific route.
- `ip route` shows the routing table. `default via 192.168.1.1 dev eth0` means: send all other packets to `192.168.1.1`.
- `traceroute <host>` shows the routers on the path.
- **NAT** (network address translation): a router replaces the private source address with its public address, so that many hosts share one public address. Your home router does this. Docker does it for containers.

### 5.6 DHCP

- **DHCP** (Dynamic Host Configuration Protocol) gives a host its network configuration automatically: the IP address, the mask, the default gateway, the DNS servers, and the **lease time**.
- The four messages (**DORA**):

  | Message | From | To | Meaning |
  |---|---|---|---|
  | Discover | Client (UDP port 68, source address `0.0.0.0`) | Broadcast (UDP port 67) | "Is there a DHCP server?" |
  | Offer | Server | Client | "You can have 192.168.1.57 for 24 hours." |
  | Request | Client | Broadcast | "I take 192.168.1.57." |
  | Acknowledge | Server | Client | "Confirmed." |

- The client renews the lease before it expires. If no DHCP server answers, the host can give itself a link-local address (`169.254.x.x`): this is a sign of a DHCP problem.

### 5.7 DNS

- **DNS** (Domain Name System) translates names to addresses. The client asks a **resolver**. The resolver asks the root servers, the top-level domain servers, and the authoritative servers, and caches the answers for their **TTL** (time to live).
- **Record types:**

  | Type | Content |
  |---|---|
  | A | IPv4 address |
  | AAAA | IPv6 address |
  | CNAME | Alias to a different name |
  | MX | Mail server |
  | TXT | Text (for example domain verification) |
  | NS | The name servers of the domain |

- On Linux, `/etc/hosts` has local names. They usually win over DNS. `/etc/resolv.conf` names the resolver.
- **Tools:** `dig example.com`, `dig +short example.com AAAA`, `dig @1.1.1.1 example.com` (ask a specific server), `getent hosts example.com` (uses `/etc/hosts` and DNS, like most programs).
- Docker Compose has its own DNS server inside each network. The service name `shop` resolves to the address of the shop container.

### 5.8 TCP, UDP, and ports

- A **port** (0–65535) identifies a service or a connection on a host. A **socket** is the combination of IP address and port. A TCP connection is identified by four values: source address, source port, destination address, destination port.
- Well-known ports: 22 (SSH), 53 (DNS), 67/68 (DHCP), 80 (HTTP), 443 (HTTPS). Applications often use other ports: the course shop uses 8000.
- **TCP:** connection-oriented and reliable. It numbers the bytes, confirms them (ACK), sends lost data again, and keeps the order. Used by HTTP (up to version 2), SSH, databases.
- **UDP:** no connection, no delivery guarantee, low overhead. Used by DNS (mostly), DHCP, video, and HTTP/3 (with the QUIC protocol).
- **Three-way handshake:** the client sends `SYN`. The server answers `SYN-ACK`. The client sends `ACK`. Then the data flows. `FIN` closes a connection normally. `RST` stops it at once.
- **Error messages:**

  | Message | Meaning |
  |---|---|
  | Connection refused | The host answered with `RST`: no program listens on this port. |
  | Connection timed out | No answer: a firewall drops the packets, the host is down, or the route is wrong. |
  | No route to host | The host or a router says that the destination cannot be reached. |

- `ss -ltnp` shows the TCP ports where programs listen (`-l` listening, `-t` TCP, `-n` numbers, `-p` processes). `ss -tn` shows the open connections.

### 5.9 HTTP and TLS

- **HTTP** is a request-response protocol. A request has a method, a path, headers, and an optional body. A response has a status code, headers, and an optional body.

  ```
  POST /api/auth/login HTTP/1.1
  Host: 127.0.0.1:8000
  Content-Type: application/json
  Content-Length: 46

  {"username": "anna", "password": "secret123"}
  ```

  ```
  HTTP/1.1 200 OK
  content-type: application/json
  x-request-id: 3f2a9c01b7de

  {"token": "...", "username": "anna"}
  ```

- **Methods:** `GET` (read), `POST` (create or do an action), `PUT` (replace), `PATCH` (change a part), `DELETE` (remove). `GET`, `PUT`, and `DELETE` are **idempotent**: the same request two times has the same effect as one time.
- **Status code classes:** 1xx information, 2xx success (200 OK, 201 Created, 204 No Content), 3xx redirection (303 See Other), 4xx client error (400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 422 Unprocessable Content, 423 Locked), 5xx server error (500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable).
- **Headers:** `Content-Type`, `Accept`, `Authorization` (for example `Bearer <token>`), `Cookie` and `Set-Cookie` (sessions), `Cache-Control`, `Location`.
- **REST** style: resources have URLs (`/api/orders/1001`), and the methods act on them. JSON is the usual body format.
- **TLS** (Transport Layer Security) encrypts the connection and proves the identity of the server with a **certificate**. HTTPS = HTTP over TLS, usually on port 443.
  - A certificate contains the server name, the public key, the validity dates, and the signature of a **certificate authority (CA)**. The client trusts the certificate when a chain of signatures goes to a root CA in its trust store.
  - Common test failures: an expired certificate, a wrong host name, a self-signed certificate in a test environment, a missing intermediate certificate. Do not disable the certificate check in tests ("verify=False") to hide the problem. Add the CA of the test environment to the trust store of the tests.
- **Tools:** `curl -v` (shows the connection, the TLS handshake, the request, and the response headers), `curl -i` (response headers and body), `openssl s_client -connect host:443 -servername host` (TLS details).

### 5.10 SSH

- **SSH** (Secure Shell) gives an encrypted terminal on a remote host, and also file copy and port forwarding. The server listens on port 22 by default.
- **Host key:** the server proves its identity with a host key. The client saves the key in `~/.ssh/known_hosts` at the first connection. If the key changes later, the client shows a warning: a server was reinstalled, or an attacker is in the middle. Check the reason before you remove the old key (`ssh-keygen -R "[127.0.0.1]:2222"`).
- **Key authentication:**
  1. Make a key pair on the client: `ssh-keygen -t ed25519 -C "course"`. The private key (`~/.ssh/id_ed25519`) stays on the client. Protect it with a passphrase. The public key (`~/.ssh/id_ed25519.pub`) can go anywhere.
  2. Put the public key in `~/.ssh/authorized_keys` on the server (`ssh-copy-id` does this).
  3. At login, the client proves with a signature that it has the private key. The private key never leaves the client.
- **`ssh-agent`** keeps the unlocked key in memory, so that you type the passphrase one time.
- **Client configuration** (`~/.ssh/config`):

  ```
  Host testhost
      HostName 127.0.0.1
      Port 2222
      User tester
      IdentityFile ~/.ssh/id_ed25519
  ```

  Then `ssh testhost` is enough.
- **Commands:** `ssh testhost 'uname -a'` (run one command), `scp file testhost:/tmp/` (copy), `rsync -av dir/ testhost:dir/` (synchronize), `ssh -L 9000:shop:8000 testhost` (**local port forwarding**: port 9000 on your computer goes through the SSH connection to `shop:8000`, as the test host sees it).
- **Security:** never share or commit a private key. Use one key for each computer. Disable password login on real servers.

### 5.11 Docker networking

- Docker Compose makes a **bridge network** for each project. The course shop network is `shopnet` with the subnet `172.28.0.0/24` (see [../../sut/README.md](../../sut/README.md)).
- Containers in the same network reach each other by the service name (`shop`, `testhost`) through the Docker DNS server.
- **Port publishing** (`127.0.0.1:8000:8000`) connects a port of your computer to a port of the container. Inside the network, containers use the container port directly, without publishing.
- `localhost` inside a container is the container itself, not your computer. This is a common error in test configurations: a test in a container must use `http://shop:8000`, not `http://localhost:8000`.
- Commands: `docker network ls`, `docker network inspect course-shop_shopnet`, `docker compose exec testhost bash`.

### 5.12 Network troubleshooting method

Go from the bottom layer to the top. Stop at the first step that fails.

| Step | Question | Tool |
|---|---|---|
| 1. Name | Does the name resolve to the correct address? | `getent hosts <name>`, `dig <name>` |
| 2. Address and route | Is the address reachable? Is the route correct? | `ip route get <address>`, `ping`, `traceroute` |
| 3. Port | Does a program listen, and does the firewall permit the connection? | `nc -zv <host> <port>`, `ss -ltnp` on the server |
| 4. TLS | Is the certificate valid for the name? | `curl -v`, `openssl s_client` |
| 5. Application | Is the request correct? What does the server log say? | `curl -v`, the server logs with the request ID |

Note: some hosts block `ping` (ICMP). A failed `ping` does not always mean that the host is down.

## Exercises

Write the commands, the output (shortened), and your explanation in `labs/phase-5-networking/notes.md`.

### Exercise 5.1: Your network configuration

1. Show your interfaces and addresses with `ip -brief address`. Name the loopback interface and your main interface. Give the address and the prefix of each.
2. Show your routing table. Name your default gateway.
3. Find your DNS resolver (`resolvectl status`, or `/etc/resolv.conf`).
4. Calculate the network address and the broadcast address of your main network.
5. On WSL2 or in a virtual machine: explain why your Linux address is different from the address of the host computer.

### Exercise 5.2: Subnet calculations

Show each step in binary, as in topic 5.2.

1. `10.0.5.130/25`: network, broadcast, host range, number of hosts.
2. `172.16.47.200/20`: network, broadcast, host range, number of hosts.
3. Are `192.168.10.62/26` and `192.168.10.66/26` in the same network? Why?
4. A test lab needs 4 networks with at least 50 hosts each. Divide `192.168.20.0/24`. Give the four networks in CIDR notation.
5. Which prefix gives at least 500 usable hosts with the fewest addresses?
6. Write a Python function `network_info(cidr: str)` that returns the network, broadcast, first host, last host, and number of hosts. Test it with pytest against your manual results. Then compare it with the `ipaddress` module of Python.

### Exercise 5.3: DHCP

1. Find the lease of your main interface: on Ubuntu with NetworkManager, `nmcli device show`; with `systemd-networkd`, `networkctl status`. Find the lease time, the DHCP server, the gateway, and the DNS servers that DHCP gave.
2. Draw the DORA sequence for your computer, with the source and destination addresses and ports of each message.
3. Optional, only in a virtual machine: capture a DHCP exchange with `sudo tcpdump -n -i <interface> port 67 or port 68` while you renew the lease. Find the four messages.

### Exercise 5.4: DNS

1. Use `dig` to find the A, AAAA, MX, and NS records of a public domain (for example `example.com` or `wikipedia.org`). Explain the TTL in the answer.
2. Use `dig +trace example.com`. Explain each step.
3. In the test host (`docker compose exec testhost bash`), resolve `shop` and `testhost`. Find the DNS server that the container uses (`cat /etc/resolv.conf`). Explain the result.
4. In the test host, add a line to `/etc/hosts` that sends `shop` to a wrong address (use `sudo`). Show that `curl http://shop:8000/api/health` fails. Explain the error. Remove the line.

### Exercise 5.5: TCP handshake capture

1. Open two SSH sessions to the test host (or two `docker compose exec testhost bash` terminals).
2. In the first one, start a capture: `sudo tcpdump -n -i eth0 host shop and port 8000`.
3. In the second one, run `curl -s http://shop:8000/api/health`.
4. In the capture, find the three packets of the handshake (flags `[S]`, `[S.]`, `[.]`), the data, and the close (`[F.]`). Write the source and destination ports. Explain why the client port is a large random number.
5. Run `curl http://shop:8001/`. Capture it. Find the `RST`. curl reports "Couldn't connect to server". Other tools report "Connection refused". Explain why the connection fails.

### Exercise 5.6: HTTP by hand

1. In the test host, connect with `nc -C shop 8000`. (`-C` sends the line end `CR LF` that HTTP requires.) Type an HTTP request by hand:

   ```
   GET /api/health HTTP/1.1
   Host: shop

   ```

   (End with an empty line.) Explain each line of the response.
2. On your computer, do the full flow with `curl -v`: register a user (`POST /api/users`), log in (`POST /api/auth/login`), and read the cart with the token (`GET /api/cart` with the header `Authorization: Bearer <token>`).
3. Make one request for each of these status codes: 201, 204, 401, 404, 409, 422. Explain each one.
4. Send your own `X-Request-ID` header. Find the request in the shop log with `docker compose logs shop | grep <id>`.

### Exercise 5.7: SSH

1. Connect to the test host with the password: `ssh -p 2222 tester@127.0.0.1`. Explain the host key question at the first connection.
2. Make an ed25519 key pair with a passphrase. Put the public key in `sut/ssh/authorized_keys`, and restart the test host. Log in with the key. Show with `ssh -v` which authentication method was used.
3. Add a `Host testhost` entry to `~/.ssh/config`. Run a command on the test host without an interactive session.
4. Copy a file to the test host with `scp`, and a directory with `rsync`.
5. Rebuild the test host (`docker compose up -d --build --force-recreate testhost`) and connect again. Explain the warning. Fix it correctly.
6. Use local port forwarding: forward port 9000 on your computer to `shop:8000` through the test host. Open `http://localhost:9000/api/health`. Draw the path of the request.

### Exercise 5.8: Troubleshooting

Ask the mentor to break the environment in one of the ways below without telling you which one, or ask a friend. (Without a mentor: write each change on a card, mix the cards, and take one.) For each case, use the method of topic 5.12, and write each step and its result.

| Change | Command (do not read before the exercise) |
|---|---|
| A | `docker compose stop shop` |
| B | In the test host: `echo "172.28.0.99 shop" \| sudo tee -a /etc/hosts` |
| C | `docker network disconnect course-shop_shopnet course-shop-shop-1` |
| D | Use the URL `https://shop:8000/api/health` in the test |
| E | Use the URL `http://localhost:8000/api/health` inside the test host |

After each case, restore the environment (`docker compose down && docker compose up -d`).

### Exercise 5.9: TLS

1. Run `curl -v https://example.com`. Find the TLS version, the certificate subject, the issuer, and the expiry date in the output.
2. Run `openssl s_client -connect example.com:443 -servername example.com </dev/null`. Find the certificate chain.
3. Run `curl https://expired.badssl.com/` and `curl https://wrong.host.badssl.com/` (badssl.com is a public site for this kind of test). Explain each error.
4. Explain why `verify=False` in a test is dangerous, and what to do in place of it.

**Side project (optional):** write a Bash or Python script `netcheck` that does the five steps of topic 5.12 for a URL, and prints the first step that fails.

## Done criteria

- [ ] I can explain the TCP/IP model and encapsulation.
- [ ] I can calculate the network, broadcast, and host range of an IPv4 network in binary.
- [ ] I can explain IPv6 addresses, MAC addresses, ARP, routing, the default gateway, and NAT.
- [ ] I can explain the four DHCP messages and the information that DHCP gives.
- [ ] I can find DNS records with `dig`, and explain how a name resolves inside Docker.
- [ ] I can find the TCP handshake and a `RST` in a packet capture, and explain "connection refused" and "connection timed out".
- [ ] I can write an HTTP request by hand, and explain methods, status codes, and headers.
- [ ] I can explain what a TLS certificate proves, and read the TLS details with `curl -v`.
- [ ] I can use SSH with keys, a client configuration, `scp`, `rsync`, and port forwarding.
- [ ] I can find the cause of a network failure with the five-step method.

## Next

[Phase 6: API and web test automation](phase-6-api-ui-automation.md)
