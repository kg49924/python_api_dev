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

def find_post(id: int):
    cur.execute(f"SELECT * FROM posts WHERE id = {id};")
    test_post = cur.fetchone()
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return p
    


class Post(BaseModel):
    title: str
    content: str
    published: bool = True



@app.get("/posts")
async def root():
    posts = cur.execute("SELECT * FROM posts;").fetchall()
    return {"posts":posts}


#Using pydantic lib for purpose of data validation.
@app.post("/posts",status_code = status.HTTP_201_CREATED)
async def create_posts(post: Post):
    post_dict = post.model_dump()
    print(post_dict)
    cur.execute(f"""
                INSERT INTO posts (title, content) 
                VALUES
                (%s, %s)
                RETURNING *;
""", (post_dict['title'],post_dict['content']))
    new_post = cur.fetchone()
    conn.commit()
    return {"post":new_post}



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
    post = cur.execute("DELETE FROM posts WHERE id = %s RETURNING *;",(str(id),)).fetchone()
    conn.commit()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"not found"})

 


@app.put("/posts/{id}")
async def update_posts(id: int, post: Post):
  
    updated_post = cur.execute(f"UPDATE posts SET title = '{post.title}', content = '{post.content}' WHERE id = {id} RETURNING *;").fetchone()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail={"message":"not updated"})
    else:
        conn.commit()
        return {"post":updated_post}
        


    
        
