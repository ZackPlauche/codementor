from typing import Optional
from pydantic import BaseModel


class ChatUser(BaseModel):
    timezone_str: str
    timezone_offset: int
    timezone_display: str
    timezone: str
    username: str
    name: str
    first_name: str
    level: str
    role: str
    avatar_url: str
    small_avatar_url: str
    uuid: str
    rating: float


class MessageRequest(BaseModel):
    temp_message_id: Optional[str] = None


class MessageResponse(BaseModel):
    request: MessageRequest
    type: str
    created_at: float
    read_at: Optional[float] = None
    id: str
    content: str
    chats_path: str
    sender: ChatUser
    receiver: ChatUser
