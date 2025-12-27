"""
Unit tests for Redis client.
"""

import pytest
from apps.xiaoyue.services.redis_client import RedisClient


@pytest.fixture
async def redis_client():
    """Create Redis client for testing."""
    client = RedisClient()
    yield client
    await client.close()


@pytest.mark.asyncio
async def test_conversation_history(redis_client):
    """Test conversation history operations."""
    user_id = "test_user_123"
    
    # Clear existing history
    await redis_client.clear_conversation_history(user_id)
    
    # Add messages
    message1 = {"role": "user", "content": "你好"}
    message2 = {"role": "assistant", "content": "师兄好"}
    
    await redis_client.add_to_conversation_history(user_id, message1)
    await redis_client.add_to_conversation_history(user_id, message2)
    
    # Retrieve history
    history = await redis_client.get_conversation_history(user_id)
    
    assert len(history) == 2
    assert history[0]["content"] == "你好"
    assert history[1]["content"] == "师兄好"
    
    # Cleanup
    await redis_client.clear_conversation_history(user_id)


@pytest.mark.asyncio
async def test_sulking_level(redis_client):
    """Test sulking level operations."""
    user_id = "test_user_456"
    
    # Get default level
    level = await redis_client.get_sulking_level(user_id)
    assert level == 0
    
    # Set level
    await redis_client.set_sulking_level(user_id, 2)
    level = await redis_client.get_sulking_level(user_id)
    assert level == 2
    
    # Increment
    new_level = await redis_client.increment_sulking_level(user_id)
    assert new_level == 3
    
    # Cannot exceed 3
    new_level = await redis_client.increment_sulking_level(user_id)
    assert new_level == 3
    
    # Decrement
    new_level = await redis_client.decrement_sulking_level(user_id)
    assert new_level == 2


@pytest.mark.asyncio
async def test_user_state(redis_client):
    """Test user state operations."""
    user_id = "test_user_789"
    
    # Get default state
    state = await redis_client.get_user_state(user_id)
    assert state["user_role"] == "师兄"
    assert state["agent_role"] == "小师妹"
    
    # Update state
    new_state = {
        "user_role": "师姐",
        "agent_role": "小师妹",
        "sulking_level": 1,
        "preferred_voice": "zh-CN-YunxiNeural"
    }
    
    await redis_client.set_user_state(user_id, new_state)
    
    # Retrieve updated state
    retrieved_state = await redis_client.get_user_state(user_id)
    assert retrieved_state["user_role"] == "师姐"
    assert retrieved_state["preferred_voice"] == "zh-CN-YunxiNeural"


@pytest.mark.asyncio
async def test_history_limit(redis_client):
    """Test conversation history limit."""
    user_id = "test_user_limit"
    
    await redis_client.clear_conversation_history(user_id)
    
    # Add 25 messages
    for i in range(25):
        await redis_client.add_to_conversation_history(
            user_id,
            {"role": "user", "content": f"Message {i}"}
        )
    
    # Should only keep last 20 by default
    history = await redis_client.get_conversation_history(user_id, limit=20)
    assert len(history) <= 20
    
    # Cleanup
    await redis_client.clear_conversation_history(user_id)

