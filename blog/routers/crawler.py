from fastapi import APIRouter, Depends, status, HTTPException, Response, status
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..hashing import Hash
from ..database import get_db


router = APIRouter(
     tags = ["Crawlers"],
)

@router.post("/crawler/create", status_code=status.HTTP_201_CREATED)
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

@router.get("/crawler/history", status_code=status.HTTP_201_CREATED, response_model=list[schemas.ShowCrawler])
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
  
@router.post("/crawler/update", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowCrawler)
def update_crawler(crawler: schemas.Crawler, db: Session = Depends(get_db)):
    update_crawler = db.query(models.Crawlers).filter(models.Crawlers.id == crawler.id)
    if not update_crawler.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Crawler with id {crawler.id} not found")
    update_crawler.update(crawler.dict())
    db.commit()
    return update_crawler
@router.post("/crawler/update_statusById", status_code=status.HTTP_201_CREATED,  response_model=schemas.ShowCrawler)
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
    
  