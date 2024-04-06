from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
import time
from psycopg.rows import dict_row
from dotenv import load_dotenv, find_dotenv
import os
import time
from database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
import models

models.Base.metadata.create_all(bind=engine)


load_dotenv()

db_password = os.getenv('DB_PASS')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')

app = FastAPI()



class Post(BaseModel):
    # estende la classe BaseModel di Pydantic
    title: str
    content: str
    # campo con valore di default
    published: bool = True
    # campo opzionale


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
    with psycopg.connect(f'host=localhost dbname={db_name}_db user={db_user} password={db_password}') as conn:
    # Apre un cursore per fare le operazioni sul db
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""SELECT * FROM posts""")
            posts = cur.fetchall()
            print(posts)
            return {"data": posts}



@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    try:
        new_post = models.Post(title=post.title, content=post.content, published=post.published)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating post")
    
# def create_posts(post: Post):
#     with psycopg.connect(f'host=localhost dbname={db_name}_db user={db_user} password={db_password}') as conn:
#     # Apre un cursore per fare le operazioni sul db
#         with conn.cursor(row_factory=dict_row) as cur:
#             cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) 
#                         RETURNING * """, 
#                         (post.title, post.content, post.published))
#             new_post = cur.fetchone()
#     return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int):
    with psycopg.connect(f'host=localhost dbname={db_name}_db user={db_user} password={db_password}') as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
            post = cur.fetchone()
            if not post:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                    detail = f"post with id: {id} was not found")
            return {"post_detail": post}


@app.delete("/posts/{id}")
def delete_post(id: int, status_code=status.HTTP_204_NO_CONTENT):
    with psycopg.connect(f'host=localhost dbname={db_name}_db user={db_user} password={db_password}') as conn:
    # Apre un cursore per fare le operazioni sul db
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
            deleted_post = cur.fetchone()
            if deleted_post == None:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')

            return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id:int , post: Post):
    with psycopg.connect(f'host=localhost dbname={db_name}_db user={db_user} password={db_password}') as conn:
    # Apre un cursore per fare le operazioni sul db
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""UPDATE posts SET title = %s, content = %s, published=%s WHERE id = %s RETURNING *""", 
                        (post.title, post.content, post.published, str(id)))
            updated_post = cur.fetchone()
            
            if updated_post == None:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')


            return {"data": updated_post}
        
# Function to test the database connection and print all tables
def test_db_connection():
    try:
        with engine.connect() as connection:
            # Query to get all table names
            result = connection.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
            """))
            tables = result.fetchall()
            print("Database connection successful!")
            print("Tables in the database:")
            for table in tables:
                print(table[0])
    except Exception as e:
        print(f"Database connection failed! ERROR: {e}")
# Call the function to test the connection
