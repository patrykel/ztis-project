import sqlalchemy
from sqlalchemy.orm import sessionmaker

USERNAME = 'postgres'
PASSWORD = 'postgres'
DB_NAME = 'ztis_fxa'
HOST = 'localhost'
PORT = 5432

__session = None


def db_connect():
    """
    Returns a connection and a metadata object for PostgreSQL database
    """
    url = "postgres://{}:{}@{}:{}/{}"
    url = url.format(USERNAME, PASSWORD, HOST, PORT, DB_NAME)

    con = sqlalchemy.create_engine(url, client_encoding='utf-8')
    meta = sqlalchemy.MetaData(bind=con, reflect=True)

    return con, meta


def get_session():
    global __session
    if __session is None:
        con, meta = db_connect()
        Session = sessionmaker(bind=con)
        __session = Session()
    return __session
