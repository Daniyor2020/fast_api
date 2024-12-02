from fastapi import FastAPI, Depends,status, HTTPException # type: ignore
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .hashing import Hash


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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create_blog(blog:schemas.Blog, db: Session = Depends(get_db)):
  new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
  db.add(new_blog)
  db.commit()
  db.refresh(new_blog)
  return new_blog

@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id)
  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
  blog.delete(synchronize_session=False)
  db.commit()
  return "deleted"

@app.put("/blog/{id}")
def update_blog(id: int, blog: schemas.Blog, db: Session = Depends(get_db)):
  blog_to_update = db.query(models.Blog).filter(models.Blog.id == id)
  if not blog_to_update.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
  blog_to_update.update(blog.dict())
  db.commit()
  return "updated"

@app.get("/blog", response_model=list[schemas.Blog], status_code=status.HTTP_201_CREATED)
def get_all_blogs(db: Session = Depends(get_db)):
  return db.query(models.Blog).all()

@app.get("/blog/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.showBlog)
def get_blog(id: int, db: Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id).first()
  if not blog:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
  return blog
  
  
  # user 
@app.post("/user", status_code=status.HTTP_201_CREATED, tags = ["User"])
def create_user(user:schemas.User, db: Session = Depends(get_db)):
  hashed_password = Hash.bcrypt(user.password)
  new_user = models.User(name=user.name, email=user.email, password=hashed_password)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user
@app.get("/user/{id}", status_code=status.HTTP_201_CREATED, tags = ["User"], response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
  return user
@app.post("/crawler/create", status_code=status.HTTP_201_CREATED, tags = ["Crawler"])
def create_crawler(crawler: schemas.Crawler, db: Session = Depends(get_db)):
    data = {
        "perspective": crawler.perspective,
        "tags": "",
        "status": "In Progress",
        "scanned": 0,
    }
    if crawler.tiktok:
        data["source"] = "tiktok"
    if crawler.news:
        data["source"] = crawler.source + "-news"


    new_crawler = models.Crawlers(
        tags=add_tags_table(crawler.tags, db),
        perspective=crawler.perspective,
        source=data["source"],
        scanned=0,
        status='In Progress',
        from_date=crawler.fromDate,
        to_date=crawler.toDate
    )
    db.add(new_crawler)
    db.commit()
    db.refresh(new_crawler)
    return new_crawler

@app.get("/crawler/history", status_code=status.HTTP_201_CREATED, tags = ["Crawler"], response_model=list[schemas.ShowCrawler])
def get_crawler(db: Session = Depends(get_db)):
    list_crawlers = db.query(models.Crawlers).all()
    clawlers = []
    
    for crawler in list_crawlers:
      tag_list = []
      for tag in get_tags_table(crawler.tags, db):
        tag_list.append(tag)
      crawler.tags = tag_list
      clawlers.append(crawler)
    return clawlers
  
@app.post("/crawler/update", status_code=status.HTTP_201_CREATED, tags = ["Crawler"], response_model=schemas.ShowCrawler)
def update_crawler(crawler: schemas.Crawler, db: Session = Depends(get_db)):
    update_crawler = db.query(models.Crawlers).filter(models.Crawlers.id == crawler.id)
    if not update_crawler.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Crawler with id {crawler.id} not found")
    update_crawler.update(crawler.dict())
    db.commit()
    return update_crawler
@app.post("/crawler/update_statusById", status_code=status.HTTP_201_CREATED, tags=["Crawler"], response_model=schemas.ShowCrawler)
def update_crawler(crawler: schemas.ScannedValue, db: Session = Depends(get_db)):
    update_crawler_query = db.query(models.Crawlers).filter(models.Crawlers.id == crawler.id)
    crawler_instance = update_crawler_query.first()

    if not crawler_instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Crawler with id {crawler.id} not found")

    try:
        update_crawler_query.update({"scanned": crawler.value})
        db.commit()
        db.refresh(crawler_instance)
        return 'updated'
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    


def add_tags_table(tags:list[schemas.TagsTable], db: Session = Depends(get_db)):
  tag_ids_str =''
  for tag in tags:
    new_tag = models.Tags_Table(type=tag.type, value=tag.value)
    db.add(new_tag)
    db.commit()
    tag_ids_str += str(new_tag.id) + ","
  return tag_ids_str

def get_tags_table(tags:str, db: Session = Depends(get_db)):
    tag_ids = tags.split(",") 
    return db.query(models.Tags_Table).filter(models.Tags_Table.id.in_(tag_ids)).all()
    
  