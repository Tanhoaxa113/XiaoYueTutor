"""
AI Agent service using Google Gemini 2.0 Flash Experimental.
Handles Chinese tutoring with structured output.
"""

import logging
from typing import Any, Dict, List, Optional
from google import genai
from google.genai import types
from django.conf import settings
from .prompts import SYSTEM_PROMPT_TEMPLATE, MAX_HISTORY_TURNS

logger = logging.getLogger(__name__)


class ChineseTutorAgent:
    """
    AI agent for Chinese language tutoring using Gemini 2.0 Flash.
    Returns structured JSON responses with emotion, content, and actions.
    """
    
    # Define the response schema for structured output
    RESPONSE_SCHEMA = types.Schema(
        type=types.Type.OBJECT,
        properties={
            "thought": types.Schema(
                type=types.Type.STRING,
                description="Internal reasoning about the user's intent. Keep it short."
            ),
            "chinese_content": types.Schema(
                type=types.Type.STRING,
                description="CRITICAL: The response in PURE CHINESE (汉字 only). NO Vietnamese, NO English, NO mixed language. This will be converted to Chinese TTS audio. Example: '师姐好！很高兴见到你。' This field must ONLY contain Chinese characters."
            ),
            "vietnamese_display": types.Schema(
                type=types.Type.STRING,
                description="The response to display to the user in Vietnamese (Wuxia style). KEEP IT CLEAN (No grammar explanation here)."
            ),
            "pinyin": types.Schema(
                type=types.Type.STRING,
                description="Pinyin for the chinese_content."
            ),
            "correction_detail": types.Schema(
                type=types.Type.OBJECT,
                description="Populate this ONLY if user made a mistake. Null if correct.",
                properties={
                    "is_correct": types.Schema(type=types.Type.BOOLEAN),
                    "mistake_highlight": types.Schema(type=types.Type.STRING, description="The specific part user got wrong"),
                    "explanation": types.Schema(type=types.Type.STRING, description="Grammar explanation in Vietnamese")
                }
            ),
            "emotion": types.Schema(
                type=types.Type.STRING,
                enum=[
                    "neutral", "happy", "excited", "cheerful",
                    "strict", "concerned", "sulking", "angry"
                ],
                description="The emotion tag to control the Live2D avatar or TTS expression."
            ),
            "action": types.Schema(
                type=types.Type.STRING,
                enum=["none", "correction", "quiz"],
                description="The type of response."
            ),
            "quiz_list": types.Schema(
                type=types.Type.ARRAY,
                description="List of quiz items if action is 'quiz'. Empty list otherwise.",
                items=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "id": types.Schema(
                            type=types.Type.INTEGER,
                            description="Unique quiz item ID"
                        ),
                        "type": types.Schema(
                            type=types.Type.STRING,
                            enum=["fill_blank", "multiple_choice", "listening"],
                            description="Type of the quiz question"
                        ),
                        "question": types.Schema(
                            type=types.Type.STRING,
                            description="The question content (e.g., 'Fill in the blank: ...')"
                        ),
                        "options": types.Schema(
                            type=types.Type.ARRAY,
                            items=types.Schema(type=types.Type.STRING),
                            description="Options for multiple choice. Empty if not applicable."
                        ),
                        "answer": types.Schema(
                            type=types.Type.STRING,
                            description="The correct answer."
                        )
                    },
                    required=["id", "type", "question", "answer"]
                )
            )
        },
        required=[
            "thought", "chinese_content", "vietnamese_display",
            "pinyin", "emotion", "action", "quiz_list"
        ]
    )
    
    def __init__(self):
        """Initialize the Gemini client."""
        self.api_key = settings.GOOGLE_API_KEY
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.5-pro"#"gemini-2.5-flash"
    
    def _format_conversation_history(
        self, 
        conversation_history: List[Dict[str, Any]]
    ) -> List[types.Content]:
        """
        Convert Redis conversation history to Gemini format.
        
        Args:
            conversation_history: List of dicts with 'role' and 'content' keys
            
        Returns:
            List of Gemini Content objects
        """
        formatted_history = []
        
        for msg in conversation_history[-MAX_HISTORY_TURNS:]:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            # Map roles to Gemini's expected format
            gemini_role = "user" if role == "user" else "model"
            
            formatted_history.append(
                types.Content(
                    role=gemini_role,
                    parts=[types.Part(text=content)]
                )
            )
        
        return formatted_history
    
    async def generate_response(
        self,
        user_text: str,
        user_role: str = "师兄",
        agent_role: str = "小师妹",
        sulking_level: int = 0,
        conversation_history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Generate a structured response from the AI tutor.
        
        Args:
            user_text: The user's input message
            user_role: Role of the user (e.g., "师兄", "师姐")
            agent_role: Role of the AI (e.g., "小师妹")
            sulking_level: Current sulking level (0-3)
            conversation_history: Previous conversation turns
            
        Returns:
            Dict containing the structured AI response
            
        Raises:
            Exception: If API call fails
        """
        try:
            # Format system prompt with user context
            system_instruction = SYSTEM_PROMPT_TEMPLATE.format(
                agent_role=agent_role,
                user_role=user_role,
                sulking_level=sulking_level
            )
            
            # Prepare conversation history
            history = []
            if conversation_history:
                history = self._format_conversation_history(conversation_history)
            
            # Add current user message
            history.append(
                types.Content(
                    role="user",
                    parts=[types.Part(text=user_text)]
                )
            )
            
            # Configure generation parameters
            config = types.GenerateContentConfig(
                temperature=0.9,  # More creative/personality
                top_p=0.95,
                top_k=40,
                max_output_tokens=2048,
                response_mime_type="application/json",
                response_schema=self.RESPONSE_SCHEMA,
                system_instruction=system_instruction
            )
            
            logger.info(f"Calling Gemini API for user message: {user_text[:50]}...")
            
            # Call Gemini API
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=history,
                config=config
            )
            
            # Parse the JSON response
            import json_repair
            result = json_repair.loads(response.text)
            
            logger.info(f"Gemini response received: emotion={result.get('emotion')}, action={result.get('action')}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating AI response: {e}", exc_info=True)
            
            # Return fallback response
            return self._get_fallback_response(user_text, sulking_level)
    
    def _get_fallback_response(
        self, 
        user_text: str, 
        sulking_level: int
    ) -> Dict[str, Any]:
        """
        Generate a fallback response when API fails.
        """
        if sulking_level >= 2:
            return {
                "thought": "API error, using fallback",
                "chinese_content": "哼，现在系统出问题了，师妹暂时不能教你了。",
                "vietnamese_display": "Hừm, hệ thống đang có vấn đề, tiểu sư muội tạm thời không thể dạy anh được.",
                "pinyin": "Hng, xiànzài xìtǒng chū wèntí le, shī mèi zànshí bù néng jiāo nǐ le.",
                "emotion": "sulking",
                "action": "none",
                "quiz_list": []
            }
        else:
            return {
                "thought": "API error, using fallback",
                "chinese_content": "师兄，系统有点小问题，稍等一下好吗？",
                "vietnamese_display": "Sư huynh, hệ thống có chút vấn đề, chờ một chút được không?",
                "pinyin": "Shī xiōng, xìtǒng yǒudiǎn xiǎo wèntí, shāo děng yīxià hǎo ma?",
                "emotion": "concerned",
                "action": "none",
                "quiz_list": []
            }
    
    async def test_connection(self) -> bool:
        """
        Test if the Gemini API connection is working.
        
        Returns:
            True if connection successful
        """
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents="你好",
                config=types.GenerateContentConfig(
                    max_output_tokens=10
                )
            )
            return bool(response.text)
        except Exception as e:
            logger.error(f"API connection test failed: {e}")
            return False

