from livekit import api, rtc

url = "wss://app.saadzaheer.com"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."  # your generated token

async def main():
    room = rtc.Room()
    await room.connect(url, token)
    print("✅ Connected to LiveKit room!")
    await room.disconnect()

import asyncio
asyncio.run(main())
