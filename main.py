from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, status
from typing import Annotated
from server.models import BookCategory,Post, Book, Block,User
from server import models
from server.database import engine, get_db
from server.schemas import PostBase, UserBase, CreateBookCategory, BookCategoryResponse, BookCategoryBase,UpdateCategory,BookBase,CreateBook,BlockCreate,UpdateBlock,UpdateUser,UpdateBook
from sqlalchemy.orm import Session
from server.database import Base 

app = FastAPI()
Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(get_db)]

@app.get('/')
async def say_hello():
    return {'Hello Python FastAPI simple'}
# CRUD
#create post route
@app.post('/post/',status_code=status.HTTP_201_CREATED)
async def create_post(db:db_dependency, post: PostBase):
    db_post = models.Post(**post.dict())
    try:
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
    except Exception as err:
        raise HTTPException(status_code=418, detail=f"Schema error: {err}")
    return db_post

# #get post 
@app.get('/posts/{post_id}/', status_code=status.HTTP_201_CREATED)
async def read_post(post_id : int, db: db_dependency):
    posts = db.query(models.Post).filter(models.Post.id == post_id).first()
    if posts is None:
       HTTPException(status_code=404 , detail='Post is was found ')
    return posts


#put post 
@app.put('/post/{post_id}', status_code=status.HTTP_200_OK)
async def update_post(post_id: int, post_data: PostBase,  db: db_dependency):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    db_post.title = post_data.title
    db_post.content = post_data.content
    db_post.user_id = post_data.user_id

    db.commit()
    db.refresh(db_post)
    return db_post
    
# # # Delete post 
@app.delete('/post/{post_id}',status_code=status.HTTP_200_OK)
async def delete_post(post_id: int, db: db_dependency):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    
    db.delete(db_post)
    print('Delete post complete !!')
    db.commit()

# # Fail
# # User
# # create post users route
@app.post('/users/',status_code=status.HTTP_201_CREATED)
async def create_user(user:UserBase, db:db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# #get users 
@app.get("/users/{user_id}/", status_code=status.HTTP_201_CREATED)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user

# put users 
@app.put('/users/{user_id}/', status_code=status.HTTP_201_CREATED)
async def edit_user(user_id: int, users_update: UpdateUser ,db: db_dependency):
    try:
        users = db.query(User).filter(User.id == user_id).first()
        if users is None :
           raise HTTPException(status_code=404, detail='User not found')
        if users_update.first_name :
           users.first_name = users_update.first_name 
        if users_update.last_name:
           users.last_name = users_update.last_name
        if users_update.age:
           users.age = users_update.age 
        if users_update.username:
           users.username = users_update.username 
        db.commit()
        db.refresh(users)
    except Exception as err :
        raise HTTPException(status_code=404, detail= f'Error edit blocks !!{err}') 
    return users

# Delete categories
@app.delete("/users/{user_id}/")
async def delete_post(user_id: int, db: db_dependency):
    db_find_users = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_find_users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"users with id {db_find_users} not found"
        )
    
    db.delete(db_find_users)
    print('Delete users complete !!')
    db.commit()

# complete!!
# create category 


#Create Book 
@app.post('/book/', status_code=status.HTTP_201_CREATED)
async def create_book(book: BookBase,category_id:int, db: db_dependency):
    book_category_chk = db.query(BookCategory).filter(BookCategory.id == category_id).first()
    if not book_category_chk:
        raise HTTPException(status_code=404, detail='categoryId not found ')
    db_book = Book(id=book.id, title = book.title,author = book.author,category_id = category_id)
    try:
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
    except Exception as err:
        db.rollback() 
        raise HTTPException(status_code=400, detail=f"Error creating category: {err}")
    return db_book

# get book 
@app.get('/book/', status_code=status.HTTP_201_CREATED)
async def get_create_book(book: BookBase, db: db_dependency):
    books = db.query(book).all();
    if not books:
        raise HTTPException(status_code=404, detail='books not found !!')
    return books

# put 
@app.put('/book/{book_id}/',status_code=status.HTTP_201_CREATED)
async def edit_book(book_id: int, update_book: UpdateBook,db: db_dependency):
    db_books_chk = db.query(Book).filter(Book.id == book_id).first()
    if not db_books_chk:
        raise HTTPException(
            status_code=404, 
            detail="Category not found")
    if update_book.title:
        db_books_chk.title = update_book.title
    if update_book.author:
        db_books_chk.author = update_book.author
    db.commit()
    db.refresh(db_books_chk)
    return db_books_chk


# Delete categories
@app.delete("/book_/{book_id}")
async def delete_post(book_id: int, db: db_dependency):
    db_find_books = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_find_books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {db_find_books} not found"
        )
    db.delete(db_find_books)
    print('Delete post complete !!')
    db.commit()

    
    
# post categories
@app.post('/book_category/', status_code=status.HTTP_201_CREATED)
async def create_book_category(book_category: CreateBookCategory, db:db_dependency):
    db_book_category = BookCategory(name=book_category.name)
    try:
        db.add(db_book_category)
        db.commit()
        db.refresh(db_book_category)
    except Exception as err:
        # Customize the error message to fit your case
        raise HTTPException(status_code=400, detail=f"Error creating category: {err}")
    return db_book_category



#get book categories 
@app.get('/book_category/{category_id}',status_code=status.HTTP_201_CREATED)
async def get_categorybook(category_id:int, db: db_dependency):
    db_book_category = db.query(BookCategory).filter(BookCategory.id == category_id).first()
    if not db_book_category :
        raise HTTPException(status_code=404, detail='categoryId not found ')
    return {"category_id": db_book_category.id, "category_name": db_book_category.name }

# Put categries  
@app.put("/book_category/{category_id}")
async def update_category(category_id: int, category: UpdateCategory, db: Session = Depends(get_db)):
    db_category = db.query(BookCategory).filter(BookCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(
            status_code=404, 
            detail="Category not found")
    if category.name:
        db_category.name = category.name
    if category.update_category_at:
        db_category.update_category_at = category.update_category_at or datetime.now()
    db.commit()
    return db_category

# Delete categories
@app.delete("/book_category/{category_id}")
async def delete_post(category_id: int, db: db_dependency):
    db_category = db.query(models.BookCategory).filter(models.BookCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {db_category} not found"
        )
    
    db.delete(db_category)
    print('Delete post complete !!')
    db.commit()


# Create block 
@app.post('/block/',status_code=status.HTTP_201_CREATED)
async def create_block(block: BlockCreate , db:db_dependency):
    db_block = Block(label=block.label, media=block.media, content=block.content, category=block.category)
    try:
        db.add(db_block)
        db.commit()
        db.refresh(db_block)
    except Exception as err:
        # Customize the error message to fit your case
        raise HTTPException(status_code=400, detail=f"Error creating category: {err}")
    return db_block

# get block 
@app.get('/block/{block_id}/',status_code=status.HTTP_201_CREATED)
async def get_block(block_id:int , db:db_dependency):
    get_blocks = db.query(Block).filter(Block.id == block_id).first()
    get_blocks_all = db.query(Block).all()
    if not get_block :
        raise HTTPException(status_code=404, detail='block not found !!')
    return get_blocks

# put block 
@app.put('/block/{block_id}/',status_code=status.HTTP_201_CREATED)
async def edit_block(block_id:int , blocks: UpdateBlock, db: db_dependency):
    db_blocks = db.query(Block).filter(Block.id == block_id).first()
    try:
        if not db_blocks :
           raise HTTPException(status_code=404, detail='id block not found !!')
        if blocks.lable:
           db_blocks.lable = blocks.lable
        if blocks.content:
           db_blocks.content = blocks.content 
        if blocks.media:
           db_blocks.media = blocks.media
        if blocks.update_block_at :
           db_blocks.update_block_at = blocks.update_block_at or datetime.now()
        db.commit()
        db.refresh(db_blocks)
    except Exception as err :
        raise HTTPException(status_code=404, detail= f'Error edit blocks !!{err}')
    
# delete block 
@app.delete('/block/{block_id}/',status_code=status.HTTP_201_CREATED)
async def delete_block(block_id: int, db: db_dependency):
    db_find_block = db.query(models.Block).filter(Block.id == block_id).first()
    if not db_find_block :
       raise HTTPException(status_code=404, detail=f' not blocks !!')
    db.delete(db_find_block)
    print(f'Delete blocks sucess !! {db_find_block}')
    db.commit()
    return db_find_block