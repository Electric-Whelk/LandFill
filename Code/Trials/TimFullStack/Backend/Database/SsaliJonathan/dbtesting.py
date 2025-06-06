from sqlalchemy import create_engine, text, insert
from sqlalchemy import select

from sqlalchemy.orm import Session
from tablestesting import users_table, comments_table, meta_obj
from modelstesting import Base, User, Comment


engine = create_engine('sqlite:///testdb.db', echo=True)
session = Session(bind=engine)

"""
To create (doesn't need to be in the with statement):
meta_obj.create_all(bind=engine)
"""

"""
To insert:

#rosie = insert(users_table).values(name='Rosie', fullname='Rosie Esther Solomon')
#hils = insert(users_table).values(name='Hils', fullname='Hilary Solomon')

statement = select(users_table)

with engine.connect() as conn:
    result = conn.execute(statement)
    for row in result:
        print(row)

"""

#with Session(engine) as db
#with engine.connect() as db

"""
statement = select(User).where(User.username.in_(['Leah Liddle', 'Rosie Solomon', 'Kwoop']))

with session as ex:
    result = ex.execute(statement)
    for i in result:
        print(i)
    #ex.commit()
"""

#leah = session.query(User).filter_by(username="Leah Liddle").first()

print(leah.email_address)


