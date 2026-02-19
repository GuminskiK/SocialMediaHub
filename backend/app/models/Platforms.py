from sqlmodel import SQLModel, Field, Relationship 
from typing import Optional, List, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from .posts import Post

class PlatformType(str, Enum):
    YouTube = "youtube"
    Instagram = "instagram"
    TikTok = "tiktok"
    X = "x"

class PlatformBase(SQLModel):
    name: str = Field(index=True, unique=True)

    PlatformType = Field(default = None)

class Platform(PlatformBase):
    id: int | None = Field(default= None, primary_key=True)
    posts: List["Post"] = Relationship(back_populates=True)

    creator_id: int = Field(foreign_key="creator.id")

class PlatformCreate(PlatformBase):
    pass

class PlatformRead(PlatformBase):
    pass

class PlatformUpdate(SQLModel):
    name: Optional[str] = None