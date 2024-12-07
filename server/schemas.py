from pydantic import BaseModel,Field
from datetime import datetime
from typing import List, Optional

# validate data
class PostBase(BaseModel):
    content : str 
    title : str = Field(..., min_length=4)
    user_id : int 

class CreatePost(PostBase):
    pass 

class UpdatePost(BaseModel):
    create_post_at : datetime
    update_post_at : datetime


class UserBase(BaseModel):
    #id : int 
    first_name : str 
    last_name : str 
    age : str 
    username : str 

    class config:
        from_attributes = True
class UpdateUser(BaseModel):
    first_name : Optional[str] = None
    last_name : Optional[str] = None 
    age : str 
    username : str 


# Category Base Model
class BookCategoryBase(BaseModel):
    name: str

    class Config:
        from_attributes = True 


# Book Base Model
class BookBase(BaseModel):
    id : str
    title: str = Field(..., min_length=3)
    author: str
   

    class Config:
        from_attributes = True  




# Create Category Model
class CreateBookCategory(BookCategoryBase):
    pass

# Create Book Model
class CreateBook(BookBase):
    pass


class UpdateBook(BaseModel):
    #id : str
    title: Optional[str] = None
    author: str
    
# Update Category model 
class UpdateCategory(BaseModel):
    # Properly annotated 'name' field
    name: Optional[str] = None  # Optional field, can be None or a string
    
    # Properly annotated 'update_category_at' field
    update_category_at: Optional[datetime] = None  # Optional datetime field



class BookCategoryResponse(BookCategoryBase):
    id: int
    books: List[BookBase] = []

    class Config:
        from_attributes = True


class BookResponse(BookBase):
    id: int
    category: BookCategoryBase  #

    class Config:
        from_attributes = True

# block 
class BlockBase(BaseModel):
    media: str
    content: str
    label: str
    category: str


class BlockCreate(BlockBase):
    pass

class BlockOut(BlockBase):
    id: int
    create_at: datetime
    update_at: datetime


class UpdateBlock(BaseModel):
    lable: Optional[str] = None  # Optional field, can be None or a string
    content : Optional[str] = None
    media : str 
    update_block_at: Optional[datetime] = None  # Optional datetime field


