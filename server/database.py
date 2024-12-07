from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
# from dotenv import load_dotenv
# load_dotenv()
DATABASE_URL="mysql+mysqlconnector://root:@localhost:3306/ntcms"
engine = create_engine(DATABASE_URL)
meta= MetaData()
conection=engine.connect()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
#connect database 
try:
    conection=engine.connect()  
    print('Connect database complelte!!')
    conection.close()
except Exception as e:
    print(f"Error connecting to database: {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()
        