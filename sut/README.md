# Course Shop (the SUT)

The course shop is the system under test (SUT) of the course. It is a small book shop with a web UI, a REST API, and a Linux test host that you connect to with SSH. It runs in Docker on your computer.

- [REQUIREMENTS.md](REQUIREMENTS.md) is the test basis. Read it before you test.
- The shop keeps all data in memory. A restart or a reset loads the seed data again: 24 books and one administrator.
- The shop is for practice only. Do not put it on a public network.

## Start and stop

```sh
cd sut
docker compose up -d --build      # build and start the shop and the test host
docker compose ps                 # show the containers and their state
curl -s http://127.0.0.1:8000/api/health
docker compose logs -f shop       # follow the log of the shop (Ctrl+C to stop)
docker compose down               # stop and remove the containers
```

| Address | Content |
|---|---|
| `http://127.0.0.1:8000` | Web UI |
| `http://127.0.0.1:8000/api` | REST API |
| `http://127.0.0.1:8000/docs` | Interactive API description (OpenAPI) |
| `http://127.0.0.1:8000/openapi.json` | The OpenAPI document |
| `ws://127.0.0.1:8000/api/ws/orders?token=<token>` | Order events (WebSocket) |
| `ssh -p 2222 tester@127.0.0.1` | Test host (password `tester`) |

The ports are open only on your own computer (`127.0.0.1`). Use `127.0.0.1`, not `localhost`, in your tests and tools. On some computers, `localhost` tries IPv6 (`::1`) first, and each request becomes slower (phase 5, topic 5.3).

## Accounts

| User | Password | Role |
|---|---|---|
| `admin` | `Admin12345` (change it with `SUT_ADMIN_PASSWORD`) | Administrator: ships and delivers orders, sees all orders |

| API client (OAuth 2.0) | Client secret | Scope |
|---|---|---|
| `ship-bot` (change it with `SUT_OAUTH_CLIENT_ID`) | `ShipBot-Secret-1` (change it with `SUT_OAUTH_CLIENT_SECRET`) | `orders:ship`: read all orders, ship and deliver orders. See R8 in the requirements. |

Register your own users in the UI or with `POST /api/users`.

## Configuration

Set these environment variables when you start the shop. Example:

```sh
SUT_DEFECTS=all docker compose up -d
```

| Variable | Default | Effect |
|---|---|---|
| `SUT_DEFECTS` | `none` | Seeded defects. `none`: the shop follows the requirements. `all`: all seeded defects are active. A list such as `D01,D04`: only these defects are active. Your mentor tells you which value to use for an exercise. |
| `SUT_LATENCY_MS` | `0` | Adds a random delay from 0 to this number of milliseconds to each API request. Use it to practice waits and timeouts. |
| `SUT_SLOW_UI` | `0` | `1` makes the web UI slow at random: buttons become active later, and the cart count changes later. Use it to practice waits in UI tests. |
| `SUT_TEST_MODE` | `1` | `1` enables the reset endpoint `POST /api/admin/reset`. |
| `SUT_LOCK_MINUTES` | `15` | The lock time after failed logins. Use a small value (for example `0.1`) for faster tests. |
| `SUT_ADMIN_PASSWORD` | `Admin12345` | The password of the administrator |
| `SUT_OAUTH_CLIENT_ID` | `ship-bot` | The client ID of the API client |
| `SUT_OAUTH_CLIENT_SECRET` | `ShipBot-Secret-1` | The client secret of the API client |
| `SUT_OAUTH_TOKEN_SECONDS` | `300` | The lifetime of an access token. Use a small value (for example `5`) to test the expiry. |
| `TESTHOST_PASSWORD` | `tester` | The password of the user `tester` on the test host |

`GET /api/health` shows `"defects": "on"` when at least one seeded defect is active.

**Do not read the code in `app/` before phase 3.** In phases 3 and 4, test the shop as a black box: use only the requirements and the shop itself. In phase 3, topic 3.9 (white-box testing), you read the code.

## Testability features

A good SUT helps the tests. The course shop has these features:

- **Reset:** `POST /api/admin/reset` loads the seed data again. Tests use it to start from a known state.
- **Request ID:** send the header `X-Request-ID` with a request. The shop writes it in the log line and returns it in the response. Use it to find the log line of a failed test.
- **JSON logs:** one log line for each request and each business event (`login_failed`, `account_locked`, `order_placed`, `order_status_changed`).
- **Test IDs:** the elements of the web UI have `data-testid` attributes.
- **OpenAPI:** `/openapi.json` describes all endpoints and response schemas. (The WebSocket endpoint is not in it: OpenAPI does not describe WebSockets. See R9.)
- **Events:** the WebSocket `/api/ws/orders` sends an event for each order change. Tests can wait for the event, in place of polling.

## Network

Docker Compose makes a network `shopnet` with the subnet `172.28.0.0/24`:

| Container | Host name | Address | Ports in the network | Port on your computer |
|---|---|---|---|---|
| `shop` | `shop` | `172.28.0.10` | 8000 | `127.0.0.1:8000` |
| `testhost` | `testhost` | `172.28.0.20` | 22 | `127.0.0.1:2222` |

From the test host, the shop is at `http://shop:8000`. If the subnet overlaps with a network on your computer, change it in `compose.yaml`, and change the two addresses.

## Run without Docker

You can run the shop directly with Python 3.13 or newer. The test host needs Docker.

```sh
cd sut
uv run --with-requirements requirements.txt uvicorn app.main:app --port 8000
```

Set the variables in the same command, for example `SUT_DEFECTS=all uv run ...`.

## Files

| Path | Content |
|---|---|
| `REQUIREMENTS.md` | The test basis |
| `compose.yaml` | The shop and the test host |
| `Dockerfile`, `requirements.txt` | The shop image |
| `app/` | The code of the shop (FastAPI, Jinja2 templates) |
| `testhost/` | The test host image (Ubuntu with an SSH server and network tools) |
| `ssh/` | Put your public key here (`authorized_keys`). Git ignores it. |
| `tests/` | Smoke tests of the shop itself |
