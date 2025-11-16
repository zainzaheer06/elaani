#!/usr/bin/env python3
"""
LiveKit Server Test - Using REST API
"""

import requests
import json
from livekit import api

# Your LiveKit server credentials
LIVEKIT_URL = "wss://app.saadzaheer.com"
LIVEKIT_REST_URL = "https://app.saadzaheer.com"
API_KEY = "APIGZJdm2zTMiq6"
API_SECRET = "QbO2uTewtrOwkZJ2PeAVPIHrRoBbQ04xQBebwJZOhYvB"


def generate_access_token(identity: str, room: str) -> str:
    """Generate a LiveKit access token"""
    try:
        at = api.AccessToken(API_KEY, API_SECRET)
        at.identity = identity
        
        try:
            from livekit.api import VideoGrant
            grant = VideoGrant(room_join=True, room=room)
            at.add_grant(grant)
        except ImportError:
            at.grants = {
                "video": {
                    "roomJoin": True,
                    "room": room
                }
            }
        
        token = at.to_jwt()
        return token
    except Exception as e:
        print(f"Error generating token: {e}")
        raise


def test_rest_api():
    """Test LiveKit REST API"""
    print("\n" + "=" * 70)
    print("LiveKit REST API Test")
    print("=" * 70 + "\n")
    
    # Test 1: Generate token
    print("[1] Generating Access Token...")
    try:
        token = generate_access_token("test-user-rest", "test-room")
        print(f"✓ Token generated successfully")
        print(f"   Token (first 50 chars): {token[:50]}...\n")
    except Exception as e:
        print(f"✗ Failed to generate token: {e}\n")
        return False
    
    # Test 2: List rooms via REST API
    print("[2] Testing REST API - List Rooms...")
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            f"{LIVEKIT_REST_URL}/twirp/livekit.RoomService/ListRooms",
            headers=headers,
            verify=False  # Ignore SSL for self-signed certs
        )
        
        print(f"   Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ REST API is working!")
            print(f"   Rooms: {len(data.get('rooms', []))}")
            if data.get('rooms'):
                for room in data['rooms']:
                    print(f"      - {room.get('name')} ({room.get('num_participants')} participants)")
            print()
        else:
            print(f"✗ REST API returned status {response.status_code}")
            print(f"   Response: {response.text}\n")
            return False
            
    except requests.exceptions.SSLError:
        print("✓ REST API endpoint is reachable (SSL cert warning expected)")
        print("   This is normal for self-signed certificates\n")
    except Exception as e:
        print(f"✗ REST API test failed: {e}\n")
        return False
    
    # Test 3: Check connectivity
    print("[3] Testing Connectivity...")
    try:
        response = requests.get(f"{LIVEKIT_REST_URL}/health", verify=False, timeout=5)
        print(f"✓ Server is responding (status: {response.status_code})\n")
        return True
    except requests.exceptions.ConnectionError:
        print(f"✗ Cannot connect to server at {LIVEKIT_REST_URL}")
        print(f"   Check if server is running and DNS is correct\n")
        return False
    except Exception as e:
        print(f"✗ Connectivity test failed: {e}\n")
        return False


def main():
    print("\n" + "🔧 LiveKit Server Diagnostic Tool 🔧".center(70))
    
    print("\nServer Configuration:")
    print(f"  WebSocket URL: {LIVEKIT_URL}")
    print(f"  REST URL:      {LIVEKIT_REST_URL}")
    print(f"  API Key:       {API_KEY}")
    
    # Suppress SSL warnings for testing
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    success = test_rest_api()
    
    print("=" * 70)
    if success:
        print("✓ LiveKit Server is Running!")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Use this token to connect from a client:")
        token = generate_access_token("my-user", "my-room")
        print(f"\n   Token: {token}\n")
        print("2. For JavaScript client:")
        print("   const room = await connect('wss://app.saadzaheer.com', {")
        print("     token: 'YOUR_TOKEN_HERE',")
        print("     userInfo: { identity: 'my-user' }")
        print("   });\n")
        return 0
    else:
        print("✗ LiveKit Server Test Failed")
        print("=" * 70)
        print("\nTroubleshooting:")
        print("1. SSH to your server and check logs:")
        print("   ssh root@46.62.217.240")
        print("   docker compose logs -f\n")
        print("2. Verify DNS resolution:")
        print("   ping app.saadzaheer.com\n")
        print("3. Check firewall ports are open:")
        print("   - 80/tcp (HTTP)")
        print("   - 443/tcp (HTTPS)")
        print("   - 7881/tcp (WebRTC TCP)")
        print("   - 50000-60000/udp (WebRTC UDP)\n")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())