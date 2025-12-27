import logging
from typing import Optional
from functools import wraps
import asyncio

logger = logging.getLogger(__name__)


def async_retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_attempts} failed for {func.__name__}: {e}"
                    )
                    
                    if attempt < max_attempts - 1:
                        await asyncio.sleep(delay * (attempt + 1))
            
            logger.error(f"All {max_attempts} attempts failed for {func.__name__}")
            raise last_exception
        
        return wrapper
    return decorator


def sanitize_user_input(text: str, max_length: int = 500) -> str:
    if not text:
        return ""
    text = text.strip()
    if len(text) > max_length:
        text = text[:max_length]
    dangerous_patterns = ["<script", "</script", "javascript:", "onerror="]
    for pattern in dangerous_patterns:
        text = text.replace(pattern, "")
    
    return text


def extract_user_id_from_scope(scope: dict) -> Optional[str]:
    user_id = scope.get("url_route", {}).get("kwargs", {}).get("user_id")
    if user_id:
        return user_id

    query_string = scope.get("query_string", b"").decode("utf-8")
    if "user_id=" in query_string:
        parts = query_string.split("user_id=")
        if len(parts) > 1:
            user_id = parts[1].split("&")[0]
            if user_id:
                return user_id

    session = scope.get("session", {})
    if session and hasattr(session, "session_key"):
        return session.session_key

    user = scope.get("user")
    if user and hasattr(user, "id") and user.id:
        return str(user.id)
    
    return None

