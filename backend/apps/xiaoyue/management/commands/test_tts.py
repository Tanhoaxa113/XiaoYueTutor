"""
Django management command to test TTS functionality.

Usage:
    python manage.py test_tts
"""

import asyncio
import base64
from django.core.management.base import BaseCommand
from apps.xiaoyue.services.tts_handler import (
    generate_tts_audio,
    generate_tts_with_emotion,
    get_available_voices
)


class Command(BaseCommand):
    help = 'Test Edge-TTS functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--save',
            action='store_true',
            help='Save audio to file for testing',
        )

    def handle(self, *args, **options):
        """Run the TTS test."""
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS("Testing Edge-TTS Handler"))
        self.stdout.write("=" * 60)
        
        # Run async test
        asyncio.run(self.run_test(options['save']))
    
    async def run_test(self, save_audio=False):
        """Async test execution."""
        
        # Test 1: List available voices
        self.stdout.write("\n🎤 Test 1: Available Chinese Voices...")
        voices = await get_available_voices()
        
        if voices:
            self.stdout.write(f"Found {len(voices)} Chinese voices:")
            for voice in voices[:5]:  # Show first 5
                self.stdout.write(f"  - {voice['name']} ({voice['gender']})")
        else:
            self.stdout.write(self.style.ERROR("❌ No voices found!"))
            return
        
        # Test 2: Basic TTS
        self.stdout.write("\n🔊 Test 2: Basic TTS Generation...")
        text = "师兄好，很高兴见到你！"
        audio_base64 = await generate_tts_audio(text)
        
        if audio_base64:
            audio_size = len(base64.b64decode(audio_base64))
            self.stdout.write(self.style.SUCCESS(f"✅ Audio generated: {audio_size} bytes"))
            
            if save_audio:
                with open("test_output.mp3", "wb") as f:
                    f.write(base64.b64decode(audio_base64))
                self.stdout.write("💾 Saved to test_output.mp3")
        else:
            self.stdout.write(self.style.ERROR("❌ TTS generation failed!"))
        
        # Test 3: Emotion-based TTS
        self.stdout.write("\n😊 Test 3: Emotion-based TTS...")
        emotions = ["happy", "sulking", "excited"]
        
        for emotion in emotions:
            audio = await generate_tts_with_emotion(
                "这是测试",
                emotion=emotion
            )
            
            if audio:
                size = len(base64.b64decode(audio))
                self.stdout.write(f"  {emotion}: ✅ ({size} bytes)")
            else:
                self.stdout.write(f"  {emotion}: ❌ Failed")
        
        # Test 4: Long text
        self.stdout.write("\n📖 Test 4: Long Text...")
        long_text = "师兄好！" * 30
        audio = await generate_tts_audio(long_text)
        
        if audio:
            size = len(base64.b64decode(audio))
            self.stdout.write(self.style.SUCCESS(f"✅ Long text generated: {size} bytes"))
        else:
            self.stdout.write(self.style.ERROR("❌ Long text failed!"))
        
        # Summary
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("✅ All TTS tests completed!"))
        self.stdout.write("=" * 60)

