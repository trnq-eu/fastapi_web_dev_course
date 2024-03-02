from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    # estende la classe BaseModel di Pydantic
    
    title: str
    content: str
    # campo con valore di default
    published: bool = True
    # campo opzionale
    rating: Optional[int] = None

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "title of post 2", "content": "content of post 2", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def root():
    return {"message": "welcome to my api!!!!"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} was not found")
    return {"post_detail": post}


@app.delete("/posts/{id}")
def delete_post(id: int, status_code=status.HTTP_204_NO_CONTENT):
    # deleting post
    # find the index in the array
    # my_post.pop(index)
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id:int , post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}