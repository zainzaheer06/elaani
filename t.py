import base64
import json
from livekit import api

API_KEY = "APIGZJdm2zTMiq6"
API_SECRET = "QbO2uTewtrOwkZJ2PeAVPIHrRoBbQ04xQBebwJZOhYvB"

# Generate token
at = api.AccessToken(API_KEY, API_SECRET)
at.identity = "test-user"

try:
    from livekit.api import VideoGrant
    grant = VideoGrant(room_join=True, room="demo-room")
    at.add_grant(grant)
    print("✓ VideoGrant added")
except Exception as e:
    print(f"✗ Failed to add VideoGrant: {e}")

token = at.to_jwt()

# Decode and display
parts = token.split('.')
payload = parts[1]

# Add padding
payload += '=' * (4 - len(payload) % 4)

decoded = base64.urlsafe_b64decode(payload)
claims = json.loads(decoded)

print("\n" + "="*70)
print("TOKEN CLAIMS:")
print("="*70)
print(json.dumps(claims, indent=2))
print("="*70)

# Check for grants
if 'video' in claims:
    print("✓ Video grant found in token")
else:
    print("✗ NO video grant in token!")

print(f"\nFull token:\n{token}")