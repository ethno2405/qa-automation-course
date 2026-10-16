# Course Shop: Requirements

This document is the **test basis** for the course shop. Use it to derive test conditions and test cases. When the shop behaves differently from this document, you found a failure. Write a defect report.

The shop sells books. Users register, log in, search the catalog, put books in a cart, and order them. An administrator ships and delivers orders.

All prices are in euros (EUR) with two decimal places.

## R1 Registration

| ID | Requirement |
|---|---|
| R1.1 | A user registers with a user name, a password, an email address, an age, and a membership choice (member or not a member). |
| R1.2 | The user name has 3 to 20 characters. It contains only the letters A–Z and a–z, the digits 0–9, and the underscore (`_`). The first character is a letter. |
| R1.3 | The user name is unique. The check ignores the case: `Anna` and `anna` are the same user name. |
| R1.4 | The password has 8 to 64 characters. It contains at least one letter and at least one digit. |
| R1.5 | The email address has the form `local@domain.tld`: exactly one `@`, no spaces, and at least one `.` in the part after the `@`. |
| R1.6 | The age is a whole number from 16 to 120. |
| R1.7 | If one or more fields are not valid, the shop rejects the registration and gives one error message for each field that is not valid. |
| R1.8 | After a successful registration, the user can log in. A registration does not log the user in. |

## R2 Login

| ID | Requirement |
|---|---|
| R2.1 | A user logs in with the user name and the password. The user name check ignores the case. |
| R2.2 | If the user name or the password is wrong, the shop rejects the login with the same message for both cases. The message does not tell which of the two is wrong. |
| R2.3 | After 3 failed logins in sequence for the same user name, the shop locks the account for 15 minutes. |
| R2.4 | While the account is locked, the shop rejects each login for this account, also with the correct password. The message tells the user that the account is locked. |
| R2.5 | A successful login sets the count of failed logins to zero. |
| R2.6 | When the lock time ends, the count of failed logins is zero. |
| R2.7 | A user can log out. After the logout, the session is not valid. |

## R3 Catalog

| ID | Requirement |
|---|---|
| R3.1 | All visitors can see the catalog. A login is not necessary. |
| R3.2 | The catalog shows 10 books on each page by default. The page size can be 1 to 50. The page number starts at 1. |
| R3.3 | The search finds books where the title or the author contains the search text. The search ignores the case. |
| R3.4 | An empty search text shows all books. |
| R3.5 | Each book has a title, an author, a year, a price, and a stock quantity. |
| R3.6 | If a book does not exist, the shop tells the user that the book was not found. |

## R4 Cart

| ID | Requirement |
|---|---|
| R4.1 | Only a user who is logged in has a cart. |
| R4.2 | The user adds a book to the cart with a quantity from 1 to 10. |
| R4.3 | If the book is already in the cart, the shop adds the new quantity to the old quantity. The total quantity of one book in the cart is not more than 10. |
| R4.4 | The quantity of a book in the cart is not more than the stock of the book. A book with a stock of 0 cannot go into the cart. |
| R4.5 | The user can change the quantity of a book in the cart (1 to 10), or remove the book from the cart. |
| R4.6 | The cart shows each book with its quantity and its line price, and the subtotal, the discount, the shipping cost, and the total (see R5). |
| R4.7 | The cart count in the page header shows the sum of all quantities in the cart. It changes immediately when the cart changes. |
| R4.8 | If the web page cannot add or remove a book (a server error, or no connection to the shop), the page shows an error message. The cart on the page does not change. |

## R5 Prices, discounts, and shipping

| ID | Requirement |
|---|---|
| R5.1 | The subtotal is the sum of (unit price × quantity) for all books in the cart. |
| R5.2 | A member gets a member discount of 5 % of the subtotal. |
| R5.3 | The coupon code `WELCOME10` gives a discount of 10 % of the subtotal. It is valid only for the first order of a user: a user with an earlier order (in any status) cannot use it. |
| R5.4 | The coupon code `BOOKS5` gives a discount of 5.00 EUR. It is valid only when the subtotal is 30.00 EUR or more. |
| R5.5 | The user can enter one coupon code. Coupon codes are case-sensitive. An unknown or a not valid coupon code gives an error message, and the shop does not accept the order with this code. |
| R5.6 | **Only one discount applies.** When more than one discount is possible (the member discount and a valid coupon), the shop applies the discount with the larger amount. When the amounts are equal, the shop applies the coupon. |
| R5.7 | The shop rounds each discount to the nearest cent. A half cent rounds up (0.645 becomes 0.65). |
| R5.8 | The shipping cost depends on the order value. The order value is the subtotal minus the discount: |

| Order value | Shipping cost |
|---|---|
| less than 25.00 EUR | 4.99 EUR |
| 25.00 EUR to 49.99 EUR | 2.99 EUR |
| 50.00 EUR or more | free (0.00 EUR) |

| ID | Requirement |
|---|---|
| R5.9 | The total is the subtotal minus the discount plus the shipping cost. |
| R5.10 | An empty cart has a subtotal, discount, shipping cost, and total of 0.00 EUR. |

## R6 Orders

| ID | Requirement |
|---|---|
| R6.1 | The user places an order from the cart. The cart must not be empty. |
| R6.2 | When the shop accepts an order, it decreases the stock of each book, and it empties the cart. |
| R6.3 | The order keeps the prices, the discount, the shipping cost, and the total from the time of the order. |
| R6.4 | An order has one of these statuses: `NEW`, `PAID`, `SHIPPED`, `DELIVERED`, `CANCELLED`. A new order has the status `NEW`. |
| R6.5 | These status changes are possible. All other status changes are not possible, and the shop rejects them with an error message: |

| From | Action | To | Who |
|---|---|---|---|
| `NEW` | pay | `PAID` | The user who owns the order |
| `NEW` | cancel | `CANCELLED` | The user who owns the order |
| `PAID` | cancel | `CANCELLED` | The user who owns the order |
| `PAID` | ship | `SHIPPED` | An administrator |
| `SHIPPED` | deliver | `DELIVERED` | An administrator |

| ID | Requirement |
|---|---|
| R6.6 | When an order changes to `CANCELLED`, the shop adds the quantities back to the stock. |
| R6.7 | A user sees only their own orders. An administrator sees all orders. |
| R6.8 | The shop records each status change with the time in the order history. |

## R7 Non-functional requirements

| ID | Requirement |
|---|---|
| R7.1 | The API answers 95 % of requests in less than 500 ms on the computer of the learner, when latency simulation is off. |
| R7.2 | The API never returns a server error (HTTP 5xx) for a request from a client. For a request that is not valid, it returns a client error (HTTP 4xx) with a message. |
| R7.3 | The shop writes one log line in JSON format for each HTTP request. |
| R7.4 | The shop does not show passwords in responses or logs. |

## R8 API clients (OAuth 2.0)

Other systems use the API without a user login. They get an access token with the OAuth 2.0 client credentials grant (RFC 6749, section 4.4).

| ID | Requirement |
|---|---|
| R8.1 | An API client gets an access token with `POST /api/oauth/token`. The body is form-encoded (`application/x-www-form-urlencoded`) with `grant_type=client_credentials` and an optional `scope`. |
| R8.2 | The client authenticates with HTTP Basic authentication (client ID and client secret), or with the form fields `client_id` and `client_secret`. |
| R8.3 | The shop has one API client: the shipping service, with the scope `orders:ship`. A request without a scope gets this scope. |
| R8.4 | The response contains `access_token`, `token_type` (`Bearer`), `expires_in` (in seconds), and `scope`. The response has the header `Cache-Control: no-store`. |
| R8.5 | An access token is valid for 300 seconds. After that time, the API rejects it with HTTP 401 and a message that the token has expired. |
| R8.6 | With the scope `orders:ship`, the client can read all orders, and ship and deliver orders. It cannot pay or cancel orders. |
| R8.7 | Errors follow RFC 6749, section 5.2: a missing `grant_type` gives `invalid_request` (400). Wrong client credentials give `invalid_client` (401, with a `WWW-Authenticate` header). A different grant type gives `unsupported_grant_type` (400). A different scope gives `invalid_scope` (400). |

## R9 Order events (WebSocket)

| ID | Requirement |
|---|---|
| R9.1 | A user who is logged in, or an API client, can open a WebSocket connection at `/api/ws/orders`. The token goes in the query parameter `token`, or the browser sends the session cookie. |
| R9.2 | The shop rejects a connection without a valid token. |
| R9.3 | After the connection, the shop sends the message `{"event": "subscribed", "username": ...}`. |
| R9.4 | When the user places an order, the shop sends an `order_placed` event. When the status of an order of the user changes, the shop sends an `order_status_changed` event with the old and the new status. |
| R9.5 | A user gets only the events of their own orders. An administrator and the API client get the events of all orders. |
| R9.6 | The shop sends each event in less than 1 second after the change. |
