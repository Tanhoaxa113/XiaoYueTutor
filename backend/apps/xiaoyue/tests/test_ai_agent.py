"""
Unit tests for AI Agent service.
"""

import pytest
from apps.xiaoyue.services.ai_agent import ChineseTutorAgent


@pytest.mark.asyncio
async def test_generate_response():
    """Test basic AI response generation."""
    agent = ChineseTutorAgent()
    
    response = await agent.generate_response(
        user_text="你好，小师妹",
        user_role="师兄",
        agent_role="小师妹",
        sulking_level=0,
        conversation_history=[]
    )
    
    # Check response structure
    assert "chinese_content" in response
    assert "vietnamese_display" in response
    assert "pinyin" in response
    assert "emotion" in response
    assert "action" in response
    assert isinstance(response["chinese_content"], str)
    assert len(response["chinese_content"]) > 0


@pytest.mark.asyncio
async def test_sulking_level_affects_response():
    """Test that sulking level affects AI behavior."""
    agent = ChineseTutorAgent()
    
    # Test with sulking level 0 (normal)
    response_normal = await agent.generate_response(
        user_text="教我说早上好",
        user_role="师兄",
        sulking_level=0
    )
    
    # Test with sulking level 3 (angry)
    response_sulking = await agent.generate_response(
        user_text="教我说早上好",
        user_role="师兄",
        sulking_level=3
    )
    
    # Emotions should differ
    assert response_normal["emotion"] != response_sulking["emotion"]
    assert response_sulking["emotion"] in ["sulking", "angry"]


@pytest.mark.asyncio
async def test_conversation_history():
    """Test conversation history handling."""
    agent = ChineseTutorAgent()
    
    history = [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "师兄好~"}
    ]
    
    response = await agent.generate_response(
        user_text="教我一些词汇",
        conversation_history=history
    )
    
    assert "chinese_content" in response


@pytest.mark.asyncio
async def test_api_connection():
    """Test Gemini API connection."""
    agent = ChineseTutorAgent()
    
    is_connected = await agent.test_connection()
    assert is_connected, "Gemini API connection failed"

