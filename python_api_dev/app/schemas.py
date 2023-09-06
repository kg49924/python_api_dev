from datetime import datetime 
from pydantic import BaseModel, EmailStr
from pydantic.utils import GetterDict




class PostBase(BaseModel):
    title: str
    content: str 
    published: bool = True
    

    class Config:
        from_attributes = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    published: bool 


class Post(PostBase):
    title: str
    content: str
    publshed: bool


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
    


if __name__ == "__main__":
    t = PostUpdate(title="nejrgnr",
                   content="nefjkvnrf",
                published=False)
    print(t)

    t1 = PostCreate(title="efnjkve",content="fnjvnef")
    print(t1)
    print("ran just fine.")


