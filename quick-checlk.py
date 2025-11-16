#!/usr/bin/env python3
"""
Quick LiveKit Server Status Check
"""

import requests
import socket
from livekit import api

LIVEKIT_URL = "wss://app.saadzaheer.com"
LIVEKIT_HOST = "app.saadzaheer.com"
API_KEY = "APIGZJdm2zTMiq6"
API_SECRET = "QbO2uTewtrOwkZJ2PeAVPIHrRoBbQ04xQBebwJZOhYvB"

def check_dns():
    """Check DNS resolution"""
    print("\n[DNS Check]")
    try:
        ip = socket.gethostbyname(LIVEKIT_HOST)
        print(f"✓ DNS resolved: {LIVEKIT_HOST} -> {ip}")
        return True
    except socket.gaierror as e:
        print(f"✗ DNS resolution failed: {e}")
        return False

def check_port():
    """Check if port 443 is open"""
    print("\n[Port Check]")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((LIVEKIT_HOST, 443))
        sock.close()
        
        if result == 0:
            print(f"✓ Port 443 is open")
            return True
        else:
            print(f"✗ Port 443 is closed")
            return False
    except Exception as e:
        print(f"✗ Port check error: {e}")
        return False

def check_https():
    """Check HTTPS connectivity"""
    print("\n[HTTPS Check]")
    try:
        response = requests.head(f"https://{LIVEKIT_HOST}", verify=False, timeout=5)
        print(f"✓ HTTPS is responding (status: {response.status_code})")
        return True
    except requests.exceptions.SSLError:
        print(f"✓ HTTPS is responding (SSL warning - expected)")
        return True
    except requests.exceptions.ConnectionError:
        print(f"✗ Cannot connect via HTTPS")
        return False
    except Exception as e:
        print(f"✗ HTTPS check error: {e}")
        return False

def check_token():
    """Check token generation"""
    print("\n[Token Generation]")
    try:
        at = api.AccessToken(API_KEY, API_SECRET)
        at.identity = "test"
        
        try:
            from livekit.api import VideoGrant
            at.add_grant(VideoGrant(room_join=True, room="test"))
        except:
            pass
        
        token = at.to_jwt()
        print(f"✓ Token generated successfully")
        print(f"  Token length: {len(token)} chars")
        return True
    except Exception as e:
        print(f"✗ Token generation failed: {e}")
        return False

def main():
    print("=" * 60)
    print("LiveKit Server Status Checker")
    print("=" * 60)
    print(f"\nServer: {LIVEKIT_URL}")
    
    # Disable SSL warnings
    import urllib3
    urllib3.disable_warnings()
    
    checks = [
        check_dns(),
        check_port(),
        check_https(),
        check_token()
    ]
    
    print("\n" + "=" * 60)
    if all(checks):
        print("✓ All checks passed! Server is reachable.")
        print("=" * 60)
        print("\nYour server configuration:")
        print(f"  URL: {LIVEKIT_URL}")
        print(f"  Host: {LIVEKIT_HOST}")
        print(f"  API Key: {API_KEY[:10]}...")
        return 0
    else:
        print("✗ Some checks failed. See above for details.")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())