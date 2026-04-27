---
name: run-flask
description: Start the PureSignage Flask app and verify it boots. Use when the user asks to "run", "start", "launch", "preview", or "open" the app, or when you need to test changes against a live server.
---

# Run the PureSignage Flask app

Single app. Run from the project root.

| Command | URL |
|---|---|
| `python app.py` from `PureSignage/` | http://127.0.0.1:5900 |

## Steps

1. **Check Python is on PATH:** `python --version` (should be 3.x).
2. **Install deps if missing:** if `flask` import fails, run `pip install -r requirements.txt` from the repo root.
3. **Start in background** with `run_in_background: true` so the shell isn't blocked. Capture the bash_id.
4. **Verify boot** by curl'ing the index after ~1s: `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5900/`. Expect `200` or `302`.
5. **Report the URL** to the user. Tell them you left the server running in the background and how to stop it (kill the bash by id).

## Common pitfalls

- **`Address already in use`**: another instance is bound to port 5900. Either stop it or change the port. Don't silently kill processes — ask first.
- **`ModuleNotFoundError: flask_babel`**: `pip install -r requirements.txt` was skipped.
- **`werkzeug` version mismatch**: requirements pin `Werkzeug==2.3.7` against `Flask==2.3.3`. Don't bump only one.
- **Default route is Arabic (RTL)**: that's intentional, not a bug. To preview English, hit `/set-language/en` first.

## After it's running

- Translation changes don't hot-reload — restart the server after editing `.po` files and running `pybabel compile`.
- Template changes DO hot-reload (Flask debug mode is on).
- `app.py` changes auto-restart the dev server.
