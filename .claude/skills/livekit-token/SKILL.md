---
name: livekit-token
description: Generate or debug LiveKit access tokens / test the LiveKit server. Use when the user asks about video calls, room tokens, "livekit", JWT for video, SIP calling, or wants to verify the LiveKit backend at app.saadzaheer.com is reachable.
---

# LiveKit utilities

LiveKit is **not wired into Flask routes**. The integration is utility scripts only — used for generating tokens manually or smoke-testing the server.

## Server

- WebSocket: `wss://app.saadzaheer.com`
- REST: `https://app.saadzaheer.com`
- Self-hosted on `46.62.217.240` (Docker Compose)

## Scripts

| Script | Purpose |
|---|---|
| `generate_token.py` | Mint a JWT with video grants using PyJWT directly. Run standalone: `python generate_token.py`. |
| `livekit-code.py` | Mint a token via the official `livekit-server-sdk-python` AccessToken builder, then hit the REST API to list rooms. Smoke test for "is the server up?". |
| `test-livekit.py` | Lightweight livekit smoke check. |
| `sip_call.py` | Helper to place an outbound SIP call through LiveKit's SIP gateway. |

## Generating a token

```bash
python generate_token.py
# prints token, claims, and the wss:// + room + identity to use
```

To customize identity / room, edit the bottom of `generate_token.py`:

```python
identity = "test-user-001"
room = "demo-room"
```

The token grants `roomJoin`, `canPublish`, `canSubscribe`, `canPublishData` for 6 hours.

## Smoke-testing the server

```bash
python livekit-code.py
# 1. Mints a token
# 2. Calls /twirp/livekit.RoomService/ListRooms
# 3. Reports server up/down
```

If it fails, the script prints SSH/firewall troubleshooting steps for the host.

## ⚠️ SECURITY — hardcoded credentials

Both `generate_token.py` and `livekit-code.py` contain **plaintext** `API_KEY` and `API_SECRET`:

```python
API_KEY = "APIGZJdm2zTMiq6"
API_SECRET = "QbO2uTewtrOwkZJ2PeAVPIHrRoBbQ04xQBebwJZOhYvB"
```

**Before committing to a public repo or sharing the project:**
1. Move them to environment variables (`os.environ['LIVEKIT_API_KEY']`).
2. Add a `.env` to `.gitignore` (already ignored) and load via `python-dotenv`.
3. Rotate the secret on the LiveKit server — assume the current one is leaked since it's been in plaintext.

If the user asks to deploy, share, or push this repo, **flag this first** before doing anything else.

## Wiring LiveKit into Flask (when asked)

Currently no Flask route exposes a `/livekit/token` endpoint. To add one:

```python
from generate_token import create_access_token

@app.route('/api/livekit/token')
def livekit_token():
    identity = request.args.get('identity', f'user-{session.get("user_id")}')
    room = request.args.get('room', 'default-room')
    token, _claims = create_access_token(identity, room)
    return jsonify({'token': token, 'url': 'wss://app.saadzaheer.com'})
```

Add real auth before exposing this — currently any visitor could mint a token.
