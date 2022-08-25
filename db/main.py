from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, engine, desc, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd


#change this to your postgres db
engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/postgres', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, bind= engine))

#change this to your schema of choice.
cschema = "ocorrencia_aerea"
Base = declarative_base(metadata=MetaData(schema=cschema))
Base.query = db_session.query_property()

valores_ausentes = ['**','##!','###!','***','####','****','*****','NULL']

#checks to see if the database already exists, if it dosent it will create it, if it does it will atempt to update it.
try:
    sdf = pd.read_sql_table('ocorrencia', engine, schema=cschema)
    pass
except ValueError:
    print("Banco de dados não encontrado, criando banco de dados")
    ocorrencia = pd.read_csv("http://sistema.cenipa.aer.mil.br/cenipa/media/opendata/ocorrencia.csv", sep=";", encoding='utf8', parse_dates=['ocorrencia_dia'], dayfirst=True)
    aeronave = pd.read_csv("http://sistema.cenipa.aer.mil.br/cenipa/media/opendata/aeronave.csv", sep=";", encoding='utf8')
    ocorrencia_tipo = pd.read_csv("http://sistema.cenipa.aer.mil.br/cenipa/media/opendata/ocorrencia_tipo.csv", sep=";", encoding='utf8')
    recomendacao = pd.read_csv("http://sistema.cenipa.aer.mil.br/cenipa/media/opendata/recomendacao.csv", sep=";", encoding='utf8')
    fator_contribuinte = pd.read_csv("http://sistema.cenipa.aer.mil.br/cenipa/media/opendata/fator_contribuinte.csv", sep=";", encoding='utf8')
    print(ocorrencia['codigo_ocorrencia'].value_counts())
    dfs = [ocorrencia, aeronave, ocorrencia_tipo, recomendacao, fator_contribuinte]
    # i am creating the list with the names as strings manually as i was afraid of the order being different when getting them automatically
    dfname = ["ocorrencia", "aeronave", "ocorrencia_tipo", "recomendacao", "fator_contribuinte"]
    for df in dfs:
        df.replace(valores_ausentes, "Não Informado", inplace=True)
        df.fillna("Não Informado", inplace =True)
    print(ocorrencia['ocorrencia_aerodromo'].value_counts())
    ocorrencia["ocorrencia_mes"] = (ocorrencia["ocorrencia_dia"].dt.month).apply(str)
    ocorrencia.replace({"1": "Janeiro", "2": "Fevereiro", "3": "Março", "4": "Abril", "5": "Maio", "6": "Junho", "7": "Julho", "8": "Agosto", "9": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro"}, inplace=True)
    print(ocorrencia)
    for x in range(len(dfs)):
        dfs[x].to_sql(dfname[x], engine, if_exists='append', index=False, schema=cschema)
else:
    ocorrencia = pd.read_csv("http://sistema.cenipa.aer.mil.br/cenipa/media/opendata/ocorrencia.csv", sep=";", encoding='utf8', parse_dates=['ocorrencia_dia'], dayfirst=True)
    aeronave = pd.read_csv("http://sistema.cenipa.aer.mil.br/cenipa/media/opendata/aeronave.csv", sep=";", encoding='utf8')
    ocorrencia_tipo = pd.read_csv("http://sistema.cenipa.aer.mil.br/cenipa/media/opendata/ocorrencia_tipo.csv", sep=";", encoding='utf8')
    recomendacao = pd.read_csv("http://sistema.cenipa.aer.mil.br/cenipa/media/opendata/recomendacao.csv", sep=";", encoding='utf8')
    fator_contribuinte = pd.read_csv("http://sistema.cenipa.aer.mil.br/cenipa/media/opendata/fator_contribuinte.csv", sep=";", encoding='utf8')
    print(ocorrencia['ocorrencia_aerodromo'].value_counts())
    dfs = [ocorrencia, aeronave, ocorrencia_tipo, recomendacao, fator_contribuinte]
    # i am creating the list with the names as strings manually as i was afraid of the order being different when getting them automaticly
    dfname = ["ocorrencia", "aeronave", "ocorrencia_tipo", "recomendacao", "fator_contribuinte"]
    for df in dfs:
        df.replace(valores_ausentes, "Não Informado", inplace=True)
        df.fillna("Não Informado", inplace =True)
    print(ocorrencia['codigo_ocorrencia'].value_counts())
    ocorrencia["ocorrencia_mes"] = (ocorrencia["ocorrencia_dia"].dt.month).apply(str)
    ocorrencia.replace({"1": "Janeiro", "2": "Fevereiro", "3": "Março", "4": "Abril", "5": "Maio", "6": "Junho", "7": "Julho", "8": "Agosto", "9": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro"}, inplace=True)
    print(dfs[0]['ocorrencia_mes'])

    #reads the already existing database.
    db_ocorrencia = pd.read_sql_table('ocorrencia', engine, schema=cschema)
    db_aeronave = pd.read_sql_table('aeronave', engine, schema=cschema)
    db_ocorrencia_tipo = pd.read_sql_table('ocorrencia_tipo', engine, schema=cschema)
    db_recomendacao = pd.read_sql_table('recomendacao', engine, schema=cschema)
    db_fator_contribuinte = pd.read_sql_table('fator_contribuinte', engine, schema=cschema)

    #i am setting the index here as this will be used to remove duplicates later on.
    db_ocorrencia = db_ocorrencia.set_index('codigo_ocorrencia1',drop=False)
    db_ocorrencia_tipo = db_ocorrencia_tipo.set_index('codigo_ocorrencia1',drop=False)
    db_aeronave = db_aeronave.set_index('codigo_ocorrencia2',drop=False)
    db_fator_contribuinte = db_fator_contribuinte.set_index('codigo_ocorrencia3',drop=False)
    db_recomendacao = db_recomendacao.set_index('codigo_ocorrencia4',drop=False)

    ocorrencia = ocorrencia.set_index('codigo_ocorrencia1',drop=False)
    ocorrencia_tipo = ocorrencia_tipo.set_index('codigo_ocorrencia1',drop=False)
    aeronave = aeronave.set_index('codigo_ocorrencia2',drop=False)
    fator_contribuinte = fator_contribuinte.set_index('codigo_ocorrencia3',drop=False)
    recomendacao = recomendacao.set_index('codigo_ocorrencia4',drop=False)

    db_dfs = [db_ocorrencia, db_aeronave, db_ocorrencia_tipo, db_recomendacao, db_fator_contribuinte]
    db_dfname = ["db_ocorrencia", "db_aeronave", "db_ocorrencia_tipo", "db_recomendacao", "db_fator_contribuinte"]

    #the changes on the index only seem to apply on the list if i create the list again, so i am doing this here.
    dfs = [ocorrencia, aeronave, ocorrencia_tipo, recomendacao, fator_contribuinte]


    #by removing the index this way i am removing all the entrys that already exist in the database and are also present in the csv
    for x in range(len(dfs)):
        #the changes that drop makes can only be acessed if you see the specifc dataframe inside of the list, outside of the list the changes dosent seems to apply, which is not a problem here since the list will also be used to update the sql.
        dfs[x].drop(db_dfs[x].index, axis=0, errors='ignore', inplace=True)


    #this will write all the dfs to the database.
    for x in range(len(dfs)):
       dfs[x].to_sql(dfname[x], engine, if_exists='append', index=False, schema=cschema)
