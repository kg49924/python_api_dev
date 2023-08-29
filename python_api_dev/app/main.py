#Importing modules

from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time


# Connecting DB

while True:
    try:
        conn = psycopg.connect(host='localhost',
                                dbname='python_api_dev_prod_db', 
                                user='postgres', 
                            password='Kara@123',
                                port=5432,
                                row_factory=dict_row)
        
        cur = conn.cursor()
        print("DB connection successfull.")
        break

    except Exception as error:
        print("db not working")
        print("Error:",error)
        time.sleep(2)




# Server APIs


app = FastAPI()
my_posts = [{'title':"title of post 1","content":"simple thing here na","id":1},
            {'title':"title of post 2","content":"simple thing here too.","id":2}]

def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p
    


class Post(BaseModel):
    title: str
    content: str
    published: bool = True



@app.get("/posts")
async def root():
    posts = cur.execute("SELECT * FROM posts").fetchall()
    return {"posts":posts}


#Using pydantic lib for purpose of data validation.
@app.post("/posts",status_code = status.HTTP_201_CREATED)
async def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0,100000)
    my_posts.append(post_dict)
    return {"post":post_dict}

@app.get("/posts/{id}")
async def get_posts(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = {"message":"not found"})
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"message":"not found"}

    return ({"post":post})

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_posts(id:int):
    flag=0
    for p in my_posts:
        if p['id']==id:
            my_posts.remove(p)
            flag = 1


@app.put("/posts/{id}")
async def update_posts(id: int, post: Post):
    post_dict = post.model_dump()
    post_dict['id']=id
    flag =0

    for i,p in enumerate(my_posts):
        if p['id']==id:
            flag=1 
            my_posts[i]=post_dict
    if flag==0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail={"something":"else"})
    else:
        return {"post":post_dict}
        


    
        
