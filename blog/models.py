from .database import Base
from sqlalchemy import Column, Integer, String

class Blog(Base):
    __tablename__ = "blog"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    
    def __repr__(self):
        return f"User(name={self.name}, email={self.email}, password={self.password})"
    
class Crawlers(Base):
        __tablename__ = "crawlers"
        id = Column(Integer, primary_key=True, index=True)
        tags = Column(String)
        perspective = Column(String)
        source = Column(String)
        scanned = Column(Integer)
        status = Column(String)
        from_date = Column(String)
        to_date = Column(String)
        
        def __repr__(self):
            return f"Crawler(tags={self.tags}, perspective={self.perspective}, source={self.source}, scanned={self.scanned}, status={self.status}, from_date={self.from_date}, to_date={self.to_date})"
           
class Tags_Table(Base):
    __tablename__ = "tags_table"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    value = Column(String)
            
    def __repr__(self):
        return f"Tags_Table(type={self.type}, value={self.value})"       
        