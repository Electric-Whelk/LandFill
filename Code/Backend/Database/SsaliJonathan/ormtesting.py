from sqlalchemy import create_engine
from sqlalchemy import Text

from modelstesting import Base, User, Comment

engine = create_engine("sqlite:///testdb.db")

#Base.metadata.create_all(bind=engine)


with engine.connect() as connection:
    result = connection.execute(Text('SELECT * FROM users'))
    for row in result:
        print(row)
