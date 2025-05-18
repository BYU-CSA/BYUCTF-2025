# Wembsoncket
Description:
```markdown
WebSockets are relatively new, so they must be secure, right?

https://wembsoncket.chal.cyberjousting.com

[wembsoncket.zip]
```

**Author**: `tm`

## Writeup
The vulnerability in this application is caused by Cross-Site WebSocket Hijacking (CSWSH). In this case, an admin user can request the flag by sending a `/getFlag` message over the WebSocket connection. The application does not properly validate the origin header during the WebSocket handshake (which is the default behavior of WebSockets for some reason) and uses authentication cookies that have the SameSite=None flag, allowing them to be sent cross-origin.

An attacker can exploit this by crafting a malicious webpage that the admin is tricked into visiting. In most browsers, cookies will automatically be sent with the WebSocket handshake if they exist. When the admin visits the malicious page, which establishes a WebSocket connection to the server, the admin's cookie will be sent. Since WebSockets are not bound by the Same-Origin Policy (SOP), the WebSocket connection can come from any origin. WebSockets rely on the developer to check the origin header, which means this vulnerability can actually be found in production quite often. 

The attacker needs to create a malicious page that establishes a WebSocket connection, sends the `/getFlag` message, receives the response, and exfiltrates the flag through a GET request, for example. Since there is no SOP, the malicious page can be hosted anywhere that the admin bot can access (ngrok works great). An example malicious page is included in `solve.html`.

**Flag** - `byuctf{CSWSH_1s_a_b1g_acr0nym}`

## Hosting
This challenge can be run as a Docker container. It contains a Node.js server that listens on port 5003. The challenge should be hosted with a valid certificate or the browser will not automatically send cookies.

To build and run the Docker container, execute the following command from inside the project directory:

```bash
docker compose up -d
```

To stop the challenge:
```bash
docker compose down
```