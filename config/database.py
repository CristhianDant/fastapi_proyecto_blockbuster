import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database file 
sqlite_file_name = '../database.sqlite'

# Database connection
base_dir = os.path.dirname(os.path.realpath(__file__))
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"
engine = create_engine(database_url, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


# # Database file 
# mysql_user = 'your_username'
# mysql_password = 'your_password'
# mysql_host = 'your_host'
# mysql_db = 'your_database'

# # Database connection
# database_url = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"
# engine = create_engine(database_url, echo=True)
# Session = sessionmaker(bind=engine)
# Base = declarative_base()