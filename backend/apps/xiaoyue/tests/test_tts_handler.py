"""
Unit tests for TTS handler.
"""

import pytest
import base64
from apps.xiaoyue.services.tts_handler import (
    generate_tts_audio,
    generate_tts_with_emotion,
    get_available_voices
)


@pytest.mark.asyncio
async def test_generate_tts_audio():
    """Test basic TTS generation."""
    text = "你好，师兄"
    audio_base64 = await generate_tts_audio(text)
    
    assert audio_base64 is not None
    assert isinstance(audio_base64, str)
    assert len(audio_base64) > 0
    
    # Verify it's valid Base64
    try:
        audio_bytes = base64.b64decode(audio_base64)
        assert len(audio_bytes) > 0
    except Exception as e:
        pytest.fail(f"Invalid Base64 encoding: {e}")


@pytest.mark.asyncio
async def test_generate_tts_with_emotion():
    """Test TTS with emotion modulation."""
    text = "师兄，你真厉害！"
    
    emotions = ["happy", "excited", "sulking", "neutral"]
    
    for emotion in emotions:
        audio_base64 = await generate_tts_with_emotion(text, emotion)
        assert audio_base64 is not None
        assert len(audio_base64) > 0


@pytest.mark.asyncio
async def test_get_available_voices():
    """Test fetching available Chinese voices."""
    voices = await get_available_voices()
    
    assert isinstance(voices, list)
    assert len(voices) > 0
    
    # Check voice structure
    for voice in voices:
        assert "name" in voice
        assert "locale" in voice
        assert voice["locale"].startswith("zh-")


@pytest.mark.asyncio
async def test_empty_text():
    """Test TTS with empty text."""
    audio_base64 = await generate_tts_audio("")
    
    # Should return None or empty string
    assert audio_base64 is None or audio_base64 == ""


@pytest.mark.asyncio
async def test_long_text():
    """Test TTS with long Chinese text."""
    long_text = "师兄好！" * 50  # 150 characters
    audio_base64 = await generate_tts_audio(long_text)
    
    assert audio_base64 is not None
    assert len(audio_base64) > 0

