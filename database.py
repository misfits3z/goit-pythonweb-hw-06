from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:goit@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)