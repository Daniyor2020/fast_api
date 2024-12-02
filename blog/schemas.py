from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str

class showBlog(Blog):
    class Config:
        orm_mode = True
        
        
        
        
"""
    class Crawler(Base):
        __tablename__ = "crawler"
        id = Column(Integer, primary_key=True, index=True)
        tags = Column(list(String))
        perspective = Column(String)
        source = Column(list(String))
        scanned = Column(Integer)
        status = Column(String)
        
"""
class User(BaseModel):
    name: str
    email: str
    password: str

class TagsTable(BaseModel):
    type: str
    value: str
    
class Crawler(BaseModel):
    tags: list[TagsTable]
    perspective: str
    toDate: str
    fromDate: str
    tiktok: bool
    news: bool
 
class ShowCrawler(BaseModel):
    tags: list[TagsTable]
    source: str
    scanned: int
    status: str
    from_date: str
    to_date: str
    perspective: str
    class Config:
        orm_mode = True     
        
    
class ScannedValue(BaseModel):
    id: int
    value: int
    class Config:
        orm_mode = True
