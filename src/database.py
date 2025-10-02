""" Create database and database connection """

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from common import download_object_from_s3, upload_object_to_s3
from constants import ROOT_DIR, DB_FILE_NAME


def download_db():
    if (ROOT_DIR / DB_FILE_NAME).exists():
        return
    print("Downloading database")
    db = download_object_from_s3(DB_FILE_NAME)
    (ROOT_DIR / DB_FILE_NAME).write_bytes(db)


def upload_db():
    print("Uploading database")
    db = (ROOT_DIR / DB_FILE_NAME).read_bytes()
    upload_object_to_s3(db, DB_FILE_NAME)


SQLALCHEMY_DATABASE_URL = f"sqlite:///../{DB_FILE_NAME}"


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
