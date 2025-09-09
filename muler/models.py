#!/usr/bin/python3
"""Maps models to existing muler.db tables

Classes
------
Pharm
Name
Synonym
Product
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import muler.config as config

# Create engine with appropriate parameters based on database type
db_url = config.db_config['local_mysql_db']
if 'sqlite' in db_url:
    engine = create_engine(db_url, echo=False, connect_args={'check_same_thread': False})
elif 'mysql' in db_url:
    engine = create_engine(db_url, echo=False, pool_recycle=280, pool_pre_ping=True)
else:
    engine = create_engine(db_url, echo=False)

Base = declarative_base()

class Pharm(Base):
    __tablename__ = 'pharm'

    drugbank_id = Column(String, primary_key=True)
    pd = Column(String)
    mech = Column(String)
    ind = Column(String)
    d_class = Column(String)

class Name(Base):
    __tablename__ = 'name'

    drugbank_id = Column(String, primary_key=True)
    name = Column(String)

class Synonym(Base):
    __tablename__ = 'synonym'

    drugbank_id = Column(String, ForeignKey(Name.drugbank_id), primary_key=True)
    synonym = Column(String)
    name = relationship('Name', backref = 'synonym')

class Product(Base):
    __tablename__ = 'product'

    drugbank_id = Column(String, ForeignKey(Name.drugbank_id), primary_key=True)
    product = Column(String)
    name = relationship('Name', backref = 'product')

if __name__ == '__main__':
    print('models.py executed.')

