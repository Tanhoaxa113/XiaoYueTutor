"""
Text-to-Speech handler using edge-tts.
Generates audio in-memory and returns Base64 encoded string.
"""

import base64
import logging
from io import BytesIO
from typing import Optional
import edge_tts
import re

logger = logging.getLogger(__name__)

def _sanitize_text_for_audio(text: str) -> str:
    """
    Hàm độc lập (Helper function) để xử lý text.
    Không có 'self' vì không nằm trong class.
    """
    if not text:
        return ""
    
    # 1. Thay thế dấu ba chấm (...) hoặc (……) bằng dấu phẩy (，) để ngắt giọng
    cleaned_text = re.sub(r'(\.{2,}|…+)', '，', text)
    
    # 2. Xử lý các ký tự lạ khác nếu cần
    return cleaned_text


async def generate_tts_audio(
    text: str,
    voice: str = "zh-CN-XiaoxiaoNeural",
    rate: str = "+0%",
    volume: str = "+0%",
) -> Optional[str]:
    """
    Generate Text-to-Speech audio and return as Base64 string.
    
    Args:
        text: Chinese text to convert to speech
        voice: Edge TTS voice name (default: zh-CN-XiaoxiaoNeural - young female)
               Other options:
               - zh-CN-YunxiNeural (male)
               - zh-CN-XiaoyiNeural (female)
               - zh-CN-YunjianNeural (male)
        rate: Speech rate (e.g., "+10%", "-10%")
        volume: Speech volume (e.g., "+10%", "-10%")
    
    Returns:
        Base64 encoded audio string (MP3 format), or None if failed
    """
    try:
        tts_text = _sanitize_text_for_audio(text)
        logger.info(f"Generating TTS for text: {text[:50]}... with voice: {voice}")
        
        # Create TTS communicator
        communicate = edge_tts.Communicate(
            text=tts_text,
            voice=voice,
            rate=rate,
            volume=volume
        )
        
        # Use BytesIO to store audio in memory
        audio_buffer = BytesIO()
        
        # Stream audio chunks into buffer
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_buffer.write(chunk["data"])
        
        # Get audio bytes
        audio_bytes = audio_buffer.getvalue()
        
        if not audio_bytes:
            logger.warning("TTS generated empty audio")
            return None
        
        # Convert to Base64
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        
        logger.info(f"TTS generated successfully, size: {len(audio_bytes)} bytes")
        
        return audio_base64
        
    except Exception as e:
        logger.error(f"Error generating TTS audio: {e}", exc_info=True)
        return None


async def get_available_voices() -> list:
    """
    Get list of available Chinese voices from edge-tts.
    
    Returns:
        List of voice dictionaries with 'Name', 'Gender', 'Locale' keys
    """
    try:
        voices = await edge_tts.list_voices()
        
        # Filter for Chinese voices only
        chinese_voices = [
            {
                "name": v["Name"],
                "gender": v["Gender"],
                "locale": v["Locale"],
                "description": v.get("FriendlyName", v["Name"])
            }
            for v in voices
            if v["Locale"].startswith("zh-")
        ]
        
        return chinese_voices
        
    except Exception as e:
        logger.error(f"Error fetching available voices: {e}")
        return []


# Voice presets for different character emotions
VOICE_PRESETS = {
    "neutral": {
        "voice": "zh-CN-XiaoxiaoNeural",
        "rate": "+0%",
        "volume": "+0%"
    },
    "happy": {
        "voice": "zh-CN-XiaoxiaoNeural",
        "rate": "+10%",
        "volume": "+10%"
    },
    "excited": {
        "voice": "zh-CN-XiaoxiaoNeural",
        "rate": "+15%",
        "volume": "+20%"
    },
    "cheerful": {
        "voice": "zh-CN-XiaoxiaoNeural",
        "rate": "+10%",
        "volume": "+10%"
    },
    "strict": {
        "voice": "zh-CN-XiaoxiaoNeural",
        "rate": "-5%",
        "volume": "+10%"
    },
    "concerned": {
        "voice": "zh-CN-XiaoxiaoNeural",
        "rate": "-5%",
        "volume": "-15%"
    },
    "sulking": {
        "voice": "zh-CN-XiaoxiaoNeural",
        "rate": "-10%",
        "volume": "-10%"
    },
    "angry": {
        "voice": "zh-CN-XiaoxiaoNeural",
        "rate": "+20%",
        "volume": "+25%"
    }
}


async def generate_tts_with_emotion(
    text: str,
    emotion: str = "neutral",
    custom_voice: Optional[str] = None
) -> Optional[str]:
    """
    Generate TTS with emotion-based voice modulation.
    
    Args:
        text: Chinese text to convert
        emotion: Emotion type (happy, excited, sulking, angry, etc.)
        custom_voice: Override default voice
        
    Returns:
        Base64 encoded audio string
    """
    preset = VOICE_PRESETS.get(emotion, VOICE_PRESETS["neutral"])
    
    if custom_voice:
        preset["voice"] = custom_voice
    
    return await generate_tts_audio(
        text=text,
        voice=preset["voice"],
        rate=preset["rate"],
        volume=preset["volume"]
    )

