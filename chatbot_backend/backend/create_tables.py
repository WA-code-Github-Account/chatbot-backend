from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# settings ko config se import karo
from config.settings import settings

Base = declarative_base()

DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL, echo=True)

def create_tables():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    create_tables()
