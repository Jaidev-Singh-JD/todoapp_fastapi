from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

  #for sqlite connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread": False}) # Create engine with proper configuration

  #for postgres connection
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Jaidev@localhost/TodoApplicationDatabase"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Create SessionLocal class for creating database sessions 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()