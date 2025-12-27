"""
Django management command to test Redis connection.

Usage:
    python manage.py test_redis
"""

import asyncio
from django.core.management.base import BaseCommand
from apps.xiaoyue.services.redis_client import RedisClient


class Command(BaseCommand):
    help = 'Test Redis connection and operations'

    def handle(self, *args, **options):
        """Run the Redis test."""
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS("Testing Redis Client"))
        self.stdout.write("=" * 60)
        
        # Run async test
        asyncio.run(self.run_test())
    
    async def run_test(self):
        """Async test execution."""
        client = RedisClient()
        test_user = "test_user_cli"
        
        try:
            # Test 1: Connection
            self.stdout.write("\n📡 Test 1: Connection...")
            redis_conn = await client.get_client()
            await redis_conn.ping()
            self.stdout.write(self.style.SUCCESS("✅ Connection successful!"))
            
            # Test 2: Conversation history
            self.stdout.write("\n💬 Test 2: Conversation History...")
            await client.clear_conversation_history(test_user)
            
            await client.add_to_conversation_history(
                test_user,
                {"role": "user", "content": "你好"}
            )
            await client.add_to_conversation_history(
                test_user,
                {"role": "assistant", "content": "师兄好"}
            )
            
            history = await client.get_conversation_history(test_user)
            self.stdout.write(f"Messages stored: {len(history)}")
            self.stdout.write(self.style.SUCCESS("✅ History operations work!"))
            
            # Test 3: Sulking level
            self.stdout.write("\n😤 Test 3: Sulking Level...")
            await client.set_sulking_level(test_user, 2)
            level = await client.get_sulking_level(test_user)
            self.stdout.write(f"Current level: {level}")
            
            new_level = await client.increment_sulking_level(test_user)
            self.stdout.write(f"After increment: {new_level}")
            
            new_level = await client.decrement_sulking_level(test_user)
            self.stdout.write(f"After decrement: {new_level}")
            self.stdout.write(self.style.SUCCESS("✅ Sulking operations work!"))
            
            # Test 4: User state
            self.stdout.write("\n👤 Test 4: User State...")
            state = await client.get_user_state(test_user)
            self.stdout.write(f"User role: {state.get('user_role')}")
            self.stdout.write(f"Agent role: {state.get('agent_role')}")
            self.stdout.write(self.style.SUCCESS("✅ State operations work!"))
            
            # Cleanup
            await client.clear_conversation_history(test_user)
            
            # Summary
            self.stdout.write("\n" + "=" * 60)
            self.stdout.write(self.style.SUCCESS("✅ All Redis tests passed!"))
            self.stdout.write("=" * 60)
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error: {e}"))
        finally:
            await client.close()

