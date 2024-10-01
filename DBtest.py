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
    user='ht24_1_group_12',
    password= password1,
    port=tunnel.local_bind_port,
    db = 'ht24_1_project_group_12'
)

mycursor = mydb.cursor()

mycursor.execute("""CREATE TABLE IF NOT EXISTS Department (
                 department_id int, 
                 title varchar(255),  
                 description varchar(255),
                 parent_id int,
                 PRIMARY KEY (department_id),
                 FOREIGN KEY (parent_id) REFERENCES Department(department_id)
                 );""")

mycursor.execute("""CREATE TABLE IF NOT EXISTS User (
                 personnr int,
                 name varchar(255), 
                 phone_no int(10), 
                 email varchar(255), 
                 address varchar(255), 
                 password varchar(255), 
                 consent_to_newsletter tinyint(1),
                 PRIMARY KEY (personnr)
                 );""")

#mycursor.execute("DROP TABLE IF EXISTS User")

mycursor.execute("""CREATE TABLE IF NOT EXISTS OrderUser (
                 order_id int, 
                 order_date varchar(255), 
                 date_of_last_change varchar(255), 
                 pay_ref varchar(255), 
                 tracking_nr int, 
                 status tinyint(1), 
                 user_id int, 
                 PRIMARY KEY (order_id), 
                 FOREIGN KEY (user_id) REFERENCES User(personnr)
                 );""")

mycursor.execute("""CREATE TABLE IF NOT EXISTS Product (
                 product_id int, 
                 title varchar(255), 
                 description text, 
                 product_price decimal(10,2),
                 tax decimal(5,2), 
                 discount decimal(5,2), 
                 stock int, 
                 is_featured varchar(255), 
                 department_id int,
                 PRIMARY KEY (product_id), 
                 FOREIGN KEY (department_id) REFERENCES Department(department_id)
                 );""")

mycursor.execute("""CREATE TABLE IF NOT EXISTS Review (
                 user_id int,
                 product_id int, 
                 description text, 
                 stars tinyint, 
                 review_date varchar(255),
                 FOREIGN KEY (user_id) REFERENCES User(personnr), 
                 FOREIGN KEY (product_id) REFERENCES Product(product_id),
                 PRIMARY KEY (user_id, product_id),
                 CHECK (0 <= stars <= 5)
                 );""")

mycursor.execute("""CREATE TABLE IF NOT EXISTS Product_In_Order (
                 product_id int,
                 order_id int,
                 quantity int, 
                 price_at_order decimal(10,2), 
                 FOREIGN KEY (product_id) REFERENCES Product(product_id), 
                 FOREIGN KEY (order_id) REFERENCES OrderUser(order_id),
                 PRIMARY KEY (product_id, order_id)
                 );""")

mycursor.execute("""CREATE TABLE IF NOT EXISTS Product_Keyword (
                 product_id int, 
                 keyword varchar(255),
                 FOREIGN KEY (product_id) REFERENCES Product(product_id), 
                 PRIMARY KEY (product_id, keyword)
                 );""")

# mycursor.execute("SELECT * FROM CUSTOMER")
# records = mycursor.fetchall()
# column_names = [desc[0] for desc in mycursor.description]
# print("Column names", column_names)

# print("Total number of rows in table: ", mycursor.rowcount)
# for row in records: 
#     print(row)



#entities: department, user, order, product, product_in_order, product_keyword, review


#('CUSTOMER',)
#('DEPARTMENT',)
#('KEYWORD',)
#('ORDER_CONTAINS',)
#('ORDER_INFO',)
#('PRODUCT',)
#('REVIEW',)

mydb.close()