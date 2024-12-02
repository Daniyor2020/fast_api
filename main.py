from fastapi import FastAPI # type: ignore
from pydantic import BaseModel # type: ignore



app = FastAPI()

class Blog(BaseModel):
    title: str
    body: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

 
@app.post("/blog")
def create_blog(blog:Blog):
    return {"data": f"new blog created:{blog}"}
