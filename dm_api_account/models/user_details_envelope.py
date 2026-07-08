from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


class UserRole(str, Enum):
    GUEST = 'Guest'
    PLAYER = 'Player'
    ADMINISTRATOR = 'Administrator'
    NANNYMODERATOR = 'Nannymoderator'
    REGULARMODERATOR = 'Regularmoderator'
    SENIORMODERATOR = 'Seniormoderator'


class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int

class BbParseMode(str, Enum):
    COMMON = 'Common',
    INFO = 'Info',
    POST = 'Post',
    CHAT = 'Chat'

class InfoBbText(BaseModel):
    value: str
    parse_mode: List[BbParseMode]


class PagingSettings(BaseModel):
    posts_per_page: int = Field(None, alias='postsPerPage')
    comments_per_page: int = Field(None, alias='commentsPerPage')
    topics_per_page: int = Field(None, alias='topicsPerPage')
    messages_per_page: int = Field(None, alias='messagesPerPage')
    entities_per_page: int = Field(None, alias='entitiesPerPage')

class ColorSchema(str, Enum):
    Modern = 'Modern',
    Pale = 'Pale',
    Classic = 'Classic',
    ClassicPale = 'ClassicPale',
    Night = 'Night'

class UserSettings(BaseModel):
    color_schema: List[ColorSchema]
    nanny_greetings_message: str = Field(None, alias='nannyGreetingsMessage')
    paging: Paging


class UserDetails(BaseModel):
    login: str
    roles: List[UserRole]
    medium_picture_url: str = Field(None, alias='mediumPictureUrl')
    small_picture_url: str = Field(None, alias='smallPictureUrl')
    status: str = Field(None, alias='status')
    rating: Rating
    online: datetime = Field(None, alias='online')
    name: str = Field(None, alias='name')
    location: str = Field(None, alias='location')
    registration: datetime = Field(None, alias='registration')
    icq: str
    skype: str
    original_picture_url: str = Field(None, alias='originalPictureUrl')
    info: InfoBbText
    settings: Settings


class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(extra='forbid')
    resource: Optional[UserDetails] = None
    metadata: Optional[str] = None