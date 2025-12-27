"""
Simple WebSocket test client for testing the Chinese Tutor chatbot.

Usage:
    python test_websocket_client.py
"""

import asyncio
import json
import websockets


async def test_chat():
    """Test the WebSocket chat functionality."""
    uri = "ws://localhost:8000/ws/chat/test_user_123/"
    
    print(f"🔌 Connecting to {uri}...")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected!")
            
            # Receive welcome message
            welcome = await websocket.recv()
            print(f"📩 Welcome: {welcome}\n")
            
            # Test messages
            test_messages = [
                {
                    "action": "chat",
                    "message": "你好，小师妹",
                    "user_role": "师兄"
                },
                {
                    "action": "chat",
                    "message": "教我说'早上好'",
                },
                {
                    "action": "chat",
                    "message": "我今天很高心",  # Intentional error
                },
                {
                    "action": "get_state"
                }
            ]
            
            for msg in test_messages:
                print(f"\n📤 Sending: {msg}")
                await websocket.send(json.dumps(msg))
                
                # Receive response
                response = await websocket.recv()
                response_data = json.loads(response)
                
                print(f"📥 Response Status: {response_data.get('status')}")
                
                if response_data.get('status') == 'typing':
                    # Wait for actual response
                    response = await websocket.recv()
                    response_data = json.loads(response)
                
                if 'data' in response_data:
                    data = response_data['data']
                    print(f"   Chinese: {data.get('chinese_content', 'N/A')}")
                    print(f"   Vietnamese: {data.get('vietnamese_display', 'N/A')}")
                    print(f"   Pinyin: {data.get('pinyin', 'N/A')}")
                    print(f"   Emotion: {data.get('emotion', 'N/A')}")
                    print(f"   Action: {data.get('action', 'N/A')}")
                    print(f"   Sulking Level: {data.get('sulking_level', 'N/A')}")
                    
                    if data.get('audio_base64'):
                        audio_len = len(data['audio_base64'])
                        print(f"   Audio: ✅ ({audio_len} chars)")
                    else:
                        print(f"   Audio: ❌ None")
                
                # Wait a bit between messages
                await asyncio.sleep(2)
            
            # Test reset
            print("\n🔄 Testing conversation reset...")
            await websocket.send(json.dumps({"action": "reset"}))
            response = await websocket.recv()
            print(f"📥 Reset response: {response}")
            
            print("\n✅ All tests completed!")
            
    except websockets.exceptions.WebSocketException as e:
        print(f"❌ WebSocket error: {e}")
    except ConnectionRefusedError:
        print("❌ Connection refused. Is the server running?")
        print("   Start with: daphne -b 127.0.0.1 -p 8000 config.asgi:application")
    except Exception as e:
        print(f"❌ Error: {e}")


async def test_connection_only():
    """Just test if we can connect."""
    uri = "ws://localhost:8000/ws/chat/"
    
    print(f"Testing connection to {uri}...")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connection successful!")
            response = await websocket.recv()
            print(f"Welcome message: {response}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("XiaoYue WebSocket Test Client")
    print("=" * 60)
    
    # Choose test mode
    print("\n1. Full chat test")
    print("2. Connection test only")
    choice = input("\nChoose test mode (1/2): ").strip()
    
    if choice == "2":
        asyncio.run(test_connection_only())
    else:
        asyncio.run(test_chat())

