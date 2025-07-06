from sqlalchemy import create_engine

def get_engine():
    DB_USER = "admin"
    DB_PASSWORD = "admin123"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "keisan_trading"

    return create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
