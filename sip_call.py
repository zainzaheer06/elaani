import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0LXVzZXItMDAxIiwiaXNzIjoiQVBJR1pKZG0yelRNaXE2IiwibmJmIjoxNzYxMjk2MDEzLCJleHAiOjE3NjEzMTc2MTMsInZpZGVvIjp7InJvb21Kb2luIjp0cnVlLCJyb29tIjoiZGVtby1yb29tIiwiY2FuUHVibGlzaCI6dHJ1ZSwiY2FuU3Vic2NyaWJlIjp0cnVlLCJjYW5QdWJsaXNoRGF0YSI6dHJ1ZX19.7rm8hlqR0oZgNIkrYaiQkl0WBkDtWLyl3IcPW7yEJFE"
resp = requests.post(
    "http://46.62.217.240:7880/sip/call",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "to": "sip:+16505551212@nevoxai.pstn.twilio.com",
        "from": "sip:nevox_user@46.62.217.240",
        "trunk": "Twilio"
    }
)


print(resp.text)
