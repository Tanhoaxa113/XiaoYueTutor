"""
Django management command to test Gemini API connection.

Usage:
    python manage.py test_gemini
"""

import asyncio
from django.core.management.base import BaseCommand
from apps.xiaoyue.services.ai_agent import ChineseTutorAgent


class Command(BaseCommand):
    help = 'Test Google Gemini API connection and AI agent'

    def handle(self, *args, **options):
        """Run the Gemini test."""
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS("Testing Gemini AI Agent"))
        self.stdout.write("=" * 60)
        
        # Run async test
        asyncio.run(self.run_test())
    
    async def run_test(self):
        """Async test execution."""
        agent = ChineseTutorAgent()
        
        # Test 1: Connection test
        self.stdout.write("\n📡 Test 1: API Connection...")
        is_connected = await agent.test_connection()
        
        if is_connected:
            self.stdout.write(self.style.SUCCESS("✅ Connection successful!"))
        else:
            self.stdout.write(self.style.ERROR("❌ Connection failed!"))
            return
        
        # Test 2: Simple greeting
        self.stdout.write("\n💬 Test 2: Simple Greeting...")
        response = await agent.generate_response(
            user_text="你好，小师妹",
            user_role="师兄",
            agent_role="小师妹",
            sulking_level=0
        )
        
        self.stdout.write(f"Chinese: {response.get('chinese_content')}")
        self.stdout.write(f"Vietnamese: {response.get('vietnamese_display')}")
        self.stdout.write(f"Pinyin: {response.get('pinyin')}")
        self.stdout.write(f"Emotion: {response.get('emotion')}")
        
        # Test 3: Teaching request
        self.stdout.write("\n📚 Test 3: Teaching Request...")
        response = await agent.generate_response(
            user_text="教我说'早上好'",
            user_role="师兄",
            sulking_level=0
        )
        
        self.stdout.write(f"Chinese: {response.get('chinese_content')}")
        self.stdout.write(f"Action: {response.get('action')}")
        
        # Test 4: Error correction
        self.stdout.write("\n✏️ Test 4: Error Correction...")
        response = await agent.generate_response(
            user_text="我今天很高心",  # Wrong character
            user_role="师兄",
            sulking_level=0
        )
        
        self.stdout.write(f"Chinese: {response.get('chinese_content')}")
        self.stdout.write(f"Action: {response.get('action')}")
        
        # Test 5: Sulking mode
        self.stdout.write("\n😤 Test 5: Sulking Mode (Level 3)...")
        response = await agent.generate_response(
            user_text="教我中文",
            user_role="师兄",
            sulking_level=3
        )
        
        self.stdout.write(f"Chinese: {response.get('chinese_content')}")
        self.stdout.write(f"Emotion: {response.get('emotion')}")
        
        # Summary
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("✅ All tests completed successfully!"))
        self.stdout.write("=" * 60)

