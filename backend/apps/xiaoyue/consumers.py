"""
WebSocket Consumer for real-time Chinese tutoring chat.
Handles connection, message processing, AI response generation, and TTS.
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional
from channels.generic.websocket import AsyncWebsocketConsumer
from .services.ai_agent import ChineseTutorAgent
from .services.tts_handler import generate_tts_with_emotion
from .services.redis_client import RedisClient
from .services.role_mapper import get_agent_role, validate_user_role, is_sulking_enabled

logger = logging.getLogger(__name__)


class ChineseTutorConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id: Optional[str] = None
        self.ai_agent = ChineseTutorAgent()
        self.redis_client = RedisClient()
        self.user_state: Dict[str, Any] = {}
    
    async def connect(self):
        self.user_id = self.scope.get("url_route", {}).get("kwargs", {}).get("user_id")
        if not self.user_id:
            self.user_id = self.scope.get("session", {}).get("session_key", "anonymous")
        
        logger.info(f"WebSocket connection attempt for user: {self.user_id}")

        await self.accept()
        try:
            self.user_state = await self.redis_client.get_user_state(self.user_id)
            logger.info(f"User state loaded: {self.user_state}")

            await self.send_json({
                "status": "connected",
                "message": "欢迎回来！小师妹准备好教你中文了~",
                "user_state": self.user_state
            })
        except Exception as e:
            logger.error(f"Error loading user state: {e}")
            await self.send_error("连接失败，请重试")
    
    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnected for user: {self.user_id}, code: {close_code}")

        await self.redis_client.close()
    
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            action = data.get("action", "chat")

            logger.info(f"Received message from {self.user_id}: action={action}")

            if action == "chat":
                await self.handle_chat_message(data)
            elif action == "reset":
                await self.handle_reset_conversation()
            elif action == "get_state":
                await self.handle_get_state()
            elif action == "set_sulking":
                await self.handle_set_sulking(data)
            else:
                await self.send_error(f"Unknown action: {action}")
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
            await self.send_error("消息格式错误")
        except Exception as e:
            logger.error(f"Error handling message: {e}", exc_info=True)
            await self.send_error("处理消息时出错")
    
    async def handle_chat_message(self, data: Dict[str, Any]):
        user_message = data.get("message", "").strip()
        
        if not user_message:
            await self.send_error("消息不能为空")
            return
        
        try:
            if "user_role" in data:
                user_role = validate_user_role(data["user_role"])
                self.user_state["user_role"] = user_role
                agent_role = get_agent_role(user_role)
                self.user_state["agent_role"] = agent_role
                await self.redis_client.set_user_state(self.user_id, self.user_state)
                
                logger.info(f"Roles updated: user={user_role}, agent={agent_role}")
            if "agent_role" not in self.user_state or not self.user_state["agent_role"]:
                user_role = self.user_state.get("user_role", "Sư huynh")
                self.user_state["agent_role"] = get_agent_role(user_role)

            user_role = self.user_state.get("user_role", "Sư huynh")
            if is_sulking_enabled(user_role):
                sulking_level = await self.redis_client.get_sulking_level(self.user_id)
            else:
                sulking_level = 0
            
            self.user_state["sulking_level"] = sulking_level
            conversation_history = await self.redis_client.get_conversation_history(
                self.user_id,
                limit=20
            )
            
            logger.info(f"Processing message with sulking_level={sulking_level}, history_length={len(conversation_history)}")

            await self.send_json({
                "status": "typing",
                "message": "小师妹正在思考..."
            })

            user_role = self.user_state.get("user_role", "Sư huynh")
            agent_role = self.user_state.get("agent_role", "Muội muội")
            
            logger.info(f"Generating response with roles: user={user_role}, agent={agent_role}, sulking={sulking_level}")
            
            ai_response = await self.ai_agent.generate_response(
                user_text=user_message,
                user_role=user_role,
                agent_role=agent_role,
                sulking_level=sulking_level,
                conversation_history=conversation_history
            )

            chinese_content = ai_response.get("chinese_content", "")
            emotion = ai_response.get("emotion", "neutral")

            if chinese_content:

                has_chinese = any('\u4e00' <= char <= '\u9fff' for char in chinese_content)

                has_latin = any('a' <= char.lower() <= 'z' for char in chinese_content)
                has_vietnamese = any(char in 'áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ' for char in chinese_content)
                
                if not has_chinese or has_latin or has_vietnamese:
                    logger.error(f"   AI RETURNED WRONG LANGUAGE in chinese_content!")
                    logger.error(f"   Content: {chinese_content[:100]}")
                    logger.error(f"   has_chinese={has_chinese}, has_latin={has_latin}, has_vietnamese={has_vietnamese}")
                    logger.error(f"   User role: {user_role}, Agent role: {agent_role}")
                    logger.error("   This MUST be fixed! TTS will sound wrong!")
            
            audio_base64 = await generate_tts_with_emotion(
                text=chinese_content,
                emotion=emotion,
                custom_voice=self.user_state.get("preferred_voice")
            )
            
            if audio_base64:
                ai_response["audio_base64"] = audio_base64
            else:
                logger.warning("TTS generation failed, sending response without audio")
                ai_response["audio_base64"] = None

            ai_response["sulking_level"] = sulking_level
            ai_response["timestamp"] = datetime.utcnow().isoformat() + "Z"

            await self.redis_client.add_to_conversation_history(
                self.user_id,
                {
                    "role": "user",
                    "content": user_message,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
            await self.redis_client.add_to_conversation_history(
                self.user_id,
                {
                    "role": "assistant",
                    "content": chinese_content,
                    "emotion": emotion,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )

            await self.send_json({
                "status": "success",
                "data": ai_response
            })
            
            logger.info(f"Response sent successfully to {self.user_id}")
            
        except Exception as e:
            logger.error(f"Error in handle_chat_message: {e}", exc_info=True)
            await self.send_error("处理消息时出错，请稍后重试")
    
    async def handle_reset_conversation(self):
        try:
            await self.redis_client.clear_conversation_history(self.user_id)
            await self.redis_client.set_sulking_level(self.user_id, 0)
            
            await self.send_json({
                "status": "success",
                "message": "对话已重置",
                "data": {
                    "sulking_level": 0
                }
            })
            
            logger.info(f"Conversation reset for user {self.user_id}")
            
        except Exception as e:
            logger.error(f"Error resetting conversation: {e}")
            await self.send_error("重置失败")
    
    async def handle_get_state(self):
        try:
            sulking_level = await self.redis_client.get_sulking_level(self.user_id)
            self.user_state["sulking_level"] = sulking_level
            
            await self.send_json({
                "status": "success",
                "data": self.user_state
            })
            
        except Exception as e:
            logger.error(f"Error getting state: {e}")
            await self.send_error("获取状态失败")
    
    async def handle_set_sulking(self, data: Dict[str, Any]):
        try:
            level = data.get("level", 0)
            await self.redis_client.set_sulking_level(self.user_id, level)
            
            await self.send_json({
                "status": "success",
                "message": f"Sulking level set to {level}",
                "data": {
                    "sulking_level": level
                }
            })
            
            logger.info(f"Sulking level set to {level} for user {self.user_id}")
            
        except Exception as e:
            logger.error(f"Error setting sulking level: {e}")
            await self.send_error("设置失败")
    
    async def send_json(self, content: Dict[str, Any]):
        await self.send(text_data=json.dumps(content, ensure_ascii=False))
    
    async def send_error(self, error_message: str):
        await self.send_json({
            "status": "error",
            "message": error_message
        })

