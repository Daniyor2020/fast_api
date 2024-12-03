from fastapi import FastAPI
from . import  models
from .database import engine
from .routers import blog, user, crawler, authentication


app = FastAPI()



from fastapi.middleware.cors import CORSMiddleware

origins = [
  "http://localhost",
  "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Specify allowed methods
    allow_headers=["*"],  # Specify allowed headers
)


models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(crawler.router)
 


