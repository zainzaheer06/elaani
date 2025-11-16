#!/usr/bin/env python3
"""
LiveKit Token Generator - Using PyJWT directly
Manually creates tokens with video grant claims
"""

import jwt
import time
from datetime import datetime, timedelta

API_KEY = "APIGZJdm2zTMiq6"
API_SECRET = "QbO2uTewtrOwkZJ2PeAVPIHrRoBbQ04xQBebwJZOhYvB"

def create_access_token(identity: str, room: str, duration_hours: int = 6):
    """Create a LiveKit access token with proper video grants"""
    
    now = datetime.utcnow()
    expires = now + timedelta(hours=duration_hours)
    
    # Build the claims with video grant
    claims = {
        "sub": identity,
        "iss": API_KEY,
        "nbf": int(now.timestamp()),
        "exp": int(expires.timestamp()),
        "video": {
            "roomJoin": True,
            "room": room,
            "canPublish": True,
            "canSubscribe": True,
            "canPublishData": True
        }
    }
    
    # Sign the token
    token = jwt.encode(claims, API_SECRET, algorithm="HS256")
    
    return token, claims

if __name__ == "__main__":
    identity = "test-user-001"
    room = "demo-room"
    
    print("Generating token with PyJWT...")
    token, claims = create_access_token(identity, room)
    
    print("\n" + "="*70)
    print("LIVEKIT ACCESS TOKEN (WITH VIDEO GRANT)")
    print("="*70)
    print(f"\nServer:   wss://app.saadzaheer.com")
    print(f"Room:     {room}")
    print(f"Identity: {identity}")
    print(f"\nToken Claims:")
    import json
    print(json.dumps(claims, indent=2))
    print(f"\nFull Token:\n{token}\n")
    print("="*70)
    
    # Verify
    if 'video' in claims and claims['video']['roomJoin']:
        print("✓ Token has video grant with roomJoin=true")
        print("✓ Ready to use in browser or API calls")
    else:
        print("✗ Video grant missing!")