
from sqlalchemy import Table, Boolean, Column, Integer, String, ForeignKey,Text,DateTime
from sqlalchemy.orm import relationship
from server.database import Base
from sqlalchemy.sql import func  # Import func for SQL functions

class User(Base):
    __tablename__ = 'users'

    first_name = Column(String(150))
    last_name = Column(String(150))
    age = Column(Integer)
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title =  Column(String(100),nullable=False)
    content = Column(String(255),nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

class Cetegory(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True ,index=True)
    

class BookCategory(Base):
    __tablename__ = 'book_categories'

    id = Column(Integer, primary_key=True ,index=True)
    name = Column(String(100), unique=True)
    books = relationship("Book", back_populates="category")

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(String(200),primary_key=True,index=True)
    title = Column(String(200))
    author = Column(String(200))
    category_id = Column(Integer, ForeignKey('book_categories.id'))
    category = relationship('BookCategory', back_populates='books')
    


class Block(Base):
    __tablename__ = "blocks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String(50), nullable=False)
    media = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(25), nullable=False)
    create_at = Column(DateTime, default=func.now(), nullable=False)
    update_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)