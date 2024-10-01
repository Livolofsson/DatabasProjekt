import pymysql
from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv
import os

load_dotenv()

password = os.getenv("ssh_password")
password1 = os.getenv("db_password")

tunnel = SSHTunnelForwarder(
    ('fries.it.uu.se', 22),# do not change 22, this is a portal
    ssh_username = 'asol0080', # use your Studium username
    ssh_password = password, # use your Studium password
    remote_bind_address=('127.0.0.1', 3306)
    ) 

tunnel.start()

mydb = pymysql.connect(
    host='127.0.0.1',
    user='ht23_1_group_12',
    password= password1,
    port=tunnel.local_bind_port,
    db = 'ht23_1_project_group_12'
)

mycursor = mydb.cursor ()

mycursor.execute ("SHOW TABLES")

for x in mycursor:
    print (x)

mydb.close()
