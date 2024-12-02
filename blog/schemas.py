from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str
    


        
class User(BaseModel):
    name: str
    email: str
    password: str
    
    
class ShowUser(BaseModel):
    name: str
    email: str
    blogs: list[Blog]
    
    class Config:
        orm_mode = True
        
class showBlog(Blog):
    title: str
    body: str
    creator: ShowUser
    class Config:
        orm_mode = True
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
