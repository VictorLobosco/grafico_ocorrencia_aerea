from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from sqlalchemy import create_engine, MetaData, Column, Integer, Table, BigInteger
from sqlalchemy import event, inspect, table
from dataclasses import dataclass
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)






#change this to your postgres db.
engine = create_engine('postgresql+psycopg2://airflow:airflow@postgres:5432/airflow', convert_unicode=True)
# engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/postgres', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,bind= engine))

#change this to the schema of your choice.
cschema = "ocorrencia"
metadata = MetaData(schema=cschema)

metadata.reflect(engine, schema=cschema)
Base = automap_base(metadata=metadata)
Base.query = db_session.query_property()

#Because of how the database is created it dosent have an primary key, this part of the code helps create one inside of sql alchemy
@event.listens_for(Base.metadata, "column_reflect")
def column_reflect(inspector, table, column_info):
    # set column.key = "attr_<lower_case_name>"
    column_info['key'] = "attr_%s" % column_info['name'].lower()

@dataclass
class ocorrencia(Base):
    __tablename__ = 'ocorrencia'
    __table__ = Table(__tablename__, Base.metadata, schema=cschema, autoload=True, autoload_with=engine)
    __mapper_args__ = {'primary_key': [__table__.c.codigo_ocorrencia]}

@dataclass
class ocorrencia_tipo(Base):
    __tablename__ = 'ocorrencia_tipo'
    __table__ = Table(__tablename__, Base.metadata, schema=cschema, autoload=True, autoload_with=engine)   
    __mapper_args__ = {'primary_key': [__table__.c.codigo_ocorrencia1]} 

@dataclass
class aeronave(Base):
    __tablename__ = 'aeronave'
    __table__ = Table(__tablename__, Base.metadata, schema=cschema, autoload=True, autoload_with=engine)   
    __mapper_args__ = {'primary_key': [__table__.c.codigo_ocorrencia2]} 

@dataclass
class fator_contribuinte(Base):
    __tablename__ = 'fator_contribuinte'
    __table__ = Table(__tablename__, Base.metadata, schema=cschema, autoload=True, autoload_with=engine)
    __mapper_args__ = {'primary_key': [__table__.c.codigo_ocorrencia3]}

@dataclass
class recomendacao(Base):
    __tablename__ = 'recomendacao'
    __table__ = Table(__tablename__, Base.metadata, schema=cschema, autoload=True, autoload_with=engine)
    __mapper_args__ = {'primary_key': [__table__.c.codigo_ocorrencia4]}
    
       
 
Base.prepare()


mapper = inspect(ocorrencia)



def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()