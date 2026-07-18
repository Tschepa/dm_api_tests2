from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    GUEST = 'Guest'
    PLAYER = 'Player'
    ADMINISTRATOR = 'Administrator'
    NANNYMODERATOR = 'Nannymoderator'
    REGULARMODERATOR = 'Regularmoderator'
    SENIORMODERATOR = 'Seniormoderator'

class BbParseMode(str, Enum):
    COMMON = 'Common'
    INFO = 'Info'
    POST = 'Post'
    CHAT = 'Chat'

class ColorSchema(str, Enum):
    MODERN = 'Modern'
    PALE = 'Pale'
    CLASSIC = 'Classic'
    CLASSIC_PALE = 'ClassicPale'
    NIGHT = 'Night'

class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int

class InfoBbText(BaseModel):
    value: str
    parse_mode: BbParseMode = Field(..., alias='parseMode')

class PagingSettings(BaseModel):
    posts_per_page: int = Field(..., alias='postsPerPage')
    comments_per_page: int = Field(..., alias='commentsPerPage')
    topics_per_page: int = Field(..., alias='topicsPerPage')
    messages_per_page: int = Field(..., alias='messagesPerPage')
    entities_per_page: int = Field(..., alias='entitiesPerPage')

class UserSettings(BaseModel):
    color_schema: ColorSchema = Field(..., alias='colorSchema')
    nanny_greetings_message: Optional[str] = Field(None, alias='nannyGreetingsMessage')
    paging: PagingSettings

class UserDetails(BaseModel):
    login: str
    roles: List[UserRole]
    medium_picture_url: Optional[str] = Field(None, alias='mediumPictureUrl')
    small_picture_url: Optional[str] = Field(None, alias='smallPictureUrl')
    status: Optional[str] = None
    rating: Rating
    online: Optional[datetime] = Field(None, alias='online')
    name: Optional[str] = None
    location: Optional[str] = None
    registration: Optional[datetime] = None
    icq: Optional[str] = None
    skype: Optional[str] = None
    original_picture_url: Optional[str] = Field(None, alias='originalPictureUrl')
    info: Optional[str] = None
    settings: UserSettings

class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(extra='forbid')
    resource: Optional[UserDetails] = None
    metadata: Optional[str] = None