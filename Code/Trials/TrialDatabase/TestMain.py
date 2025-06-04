from Configure_DB import Base
from Configure_DB import engine
from Configure_DB import session
from Format import Format
from sqlalchemy import select

#create all tables
"""Base.metadata.create_all(bind=engine)"""

#Creating Formats
"""
#already created: 
standard = Format(name='Standard', singleton=False, min=60)
modern = Format(name='Modern', singleton=False, min=60)
legacy = Format(name='Legacy', singleton=False, min=60)
vintage = Format(name='Vintage', singleton=False, min=60)
edh = Format(name='EDH', singleton=True, min=100, max=100)

all_formats = [standard, modern, legacy, vintage, edh]

session.add_all(all_formats)
session.commit()"""

#select something
with session as sesh:
    #select by criteria; returns an iteratable object
    statement = select(Format).where(Format.name.in_(['Modern', 'EDH']))
    result = sesh.scalars(statement)
    critformats = []
    for format in result:
        critformats.append(format)

    #get everything; this time as an array
    querformats = sesh.query(Format).all()


    #below code toggles whether standard is singleton
    standard = querformats[0]
    print(standard)
    sesh.commit()