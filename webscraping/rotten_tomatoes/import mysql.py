import mysql.connector
import dataframe_series
from sqlalchemy import create_engine

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="jogodefutebol1",
  database="rotten_tomatoes"
)

engine = create_engine('mysql+mysqlconnector://root:jogodefutebol1@localhost/rotten_tomatoes', echo=False)


dataframe_to_sql = dataframe.df6.to_sql(name='tb_rotten', con=engine, if_exists='replace', index=False)

dataframe.df6.tail()