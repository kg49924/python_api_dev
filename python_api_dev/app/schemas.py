from pydantic import BaseModel



class Post(BaseModel):
    title: str
    content: str 
    published: bool = True


class PostBase(BaseModel):
    title: str
    content: str 
    published: bool = True



class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    published: bool 




class Post(PostBase):
    title: str
    content: str
    publshed: bool

    class Config:
        orm_mode = True



if __name__ == "__main__":
    t = PostUpdate(title="nejrgnr",
                   content="nefjkvnrf",
                published=False)
    print(t)

    t1 = PostCreate(title="efnjkve",content="fnjvnef")
    print(t1)
    print("ran just fine.")


