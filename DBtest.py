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

#mycursor.execute("DROP TABLE IF EXISTS Department")

mycursor.execute("""CREATE TABLE IF NOT EXISTS Department (
                 department_id int, 
                 title TEXT,  
                 description TEXT,
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
#departments
mycursor.execute("INSERT INTO Department VALUES (1, 'Home Page', 'Welcome to AltOnline AB, a leader in online sales in Sweden. Here you can find everything from clothes, electronics and skincare.', NULL)")
mycursor.execute("INSERT INTO Department VALUES(2, 'Clothes', 'Clothes for women, men and kids', 1)")
mycursor.execute("INSERT INTO Department VALUES(3, 'Woman', 'Clothes for women', 2)")
mycursor.execute("INSERT INTO Department VALUES(4, 'Men', 'Clothes for men', 2)")
mycursor.execute("INSERT INTO Department VALUES(5, 'Kids', 'Clothes for kids', 2)")

mycursor.execute("INSERT INTO Department VALUES(6, 'Skincare', 'Skincare for all types of skin', 1)")
mycursor.execute("INSERT INTO Department VALUES(7, 'Face', 'Skincare for the face', 6)")
mycursor.execute("INSERT INTO Department VALUES(8, 'Body', 'Skincare for the body', 6)")
mycursor.execute("INSERT INTO Department VALUES(9, 'Sun products', 'Skincare when it is sunny', 6)")

#products
#(id, title, description, product_price, tax, discount, stock, is_featured, department_id)
mycursor.execute("INSERT INTO Product VALUES(1, 'Dress', 'Short blue dress', 100, 10, 20, 1000, 1, 3)")
mycursor.execute("INSERT INTO Product VALUES(2, 'Jeans', 'Stretchy blue jeans', 99.90, 15.99, 0, 500, 1, 3)")
mycursor.execute("INSERT INTO Product VALUES(3, 'Cardigan', 'Soft pink wool cardigan', 200, 19.90, 0, 100, 1, 3)")

mycursor.execute("INSERT INTO Product VALUES(4, 'Jeans', 'Black jeans', 500, 10, 0, 50, 1, 4)")
mycursor.execute("INSERT INTO Product VALUES(5, 'Shirt', 'Red cotton shirt', 1000, 50, 0, 0, 0, 4)")
mycursor.execute("INSERT INTO Product VALUES(6, 'Shorts', 'Green and yellow cotton shorts', 600, 50, 60, 100, 1, 4)")

mycursor.execute("INSERT INTO Product VALUES(7, 'Jeans', 'White jeans', 400, 40, 0, 50, 0, 5)")
mycursor.execute("INSERT INTO Product VALUES(8, 'Skirt', 'Red skirt dotted in white', 300, 30, 0, 100, 0, 5)")

mycursor.execute("INSERT INTO Product VALUES(9, 'Daycream', 'Daycream for oily skin', 150, 15, 0, 100, 1, 7)")
mycursor.execute("INSERT INTO Product VALUES(10, 'Peeling', 'Peeling to help with dry skin', 100, 10, 0, 50, 0, 7)")

mycursor.execute("INSERT INTO Product VALUES(11, 'Shower gel', 'Shower gel with shea butter', 150, 15, 50, 20, 1, 8)")
mycursor.execute("INSERT INTO Product VALUES(12, 'Body lotion', 'Body lotion for everyday use', 400, 40, 0, 60, 0, 8)")

mycursor.execute("INSERT INTO Product VALUES(13, 'Sun screen', 'Sun screen for everyday use', 100, 10, 0, 30, 1, 9)")

# mycursor.execute("SELECT * FROM CUSTOMER")
# records = mycursor.fetchall()
# column_names = [desc[0] for desc in mycursor.description]
# print("Column names", column_names)

# print("Total number of rows in table: ", mycursor.rowcount)
# for row in records: 
#     print(row)



#entities: department, user, order, product, product_in_order, product_keyword, review

mydb.close()