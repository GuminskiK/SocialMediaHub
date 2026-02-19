from sqlmodel import SQLModel, Field, Relationship 
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .platforms import Platform

class CreatorBase(SQLModel):
    name: str = Field(index=True, unique=True)
    
class Creator(CreatorBase, table=True):
    id: int | None = Field(default= None, primary_key=True)
    platforms: List["Platform"] = Relationship(back_populates="creator")

    user_id: int = Field(foreign_key="user.id")
    
class CreatorRead(CreatorBase):
    pass

class CreatorUpdate(CreatorBase):
    name: Optional[str] = None