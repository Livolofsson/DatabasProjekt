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

# mycursor.execute("DROP TABLE IF EXISTS Review")
# mycursor.execute("DROP TABLE IF EXISTS Product_In_Order")
# mycursor.execute("DROP TABLE IF EXISTS OrderUser")
# mycursor.execute("DROP TABLE IF EXISTS User")

mycursor.execute("""CREATE TABLE IF NOT EXISTS Department (
                 department_id int, 
                 title TEXT NOT NULL,  
                 description TEXT NOT NULL,
                 parent_id int,
                 PRIMARY KEY (department_id),
                 FOREIGN KEY (parent_id) REFERENCES Department(department_id)
                 );""")

mycursor.execute("""CREATE TABLE IF NOT EXISTS User (
                 personnr char(12),
                 name varchar(255), 
                 phone_no varchar(255), 
                 email varchar(255) NOT NULL, 
                 address varchar(255), 
                 password varchar(255) NOT NULL, 
                 consent_to_newsletter BOOLEAN,
                 PRIMARY KEY (personnr)
                 );""")

mycursor.execute("""CREATE TABLE IF NOT EXISTS OrderUser (
                 order_id int, 
                 order_date date, 
                 date_of_last_change date, 
                 pay_ref varchar(255), 
                 tracking_nr int, 
                 status tinyint(1), 
                 user_id char(12) NOT NULL, 
                 PRIMARY KEY (order_id), 
                 FOREIGN KEY (user_id) REFERENCES User(personnr)
                 );""")

mycursor.execute("""CREATE TABLE IF NOT EXISTS Product (
                 product_id int, 
                 title varchar(255) NOT NULL, 
                 description text, 
                 product_price decimal(10,2) NOT NULL,
                 tax decimal(5,2) NOT NULL, 
                 discount decimal(5,2) , 
                 stock int DEFAULT 0, 
                 is_featured BOOLEAN DEFAULT FALSE, 
                 department_id int,
                 PRIMARY KEY (product_id), 
                 FOREIGN KEY (department_id) REFERENCES Department(department_id)
                 );""")

mycursor.execute("""CREATE TABLE IF NOT EXISTS Review (
                 user_id char(12),
                 product_id int, 
                 description text, 
                 stars tinyint, 
                 review_date date,
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
mycursor.execute("INSERT IGNORE INTO Department VALUES (1, 'Home Page', 'Welcome to AltOnline AB, a leader in online sales in Sweden. Here you can find everything from clothes, electronics and skincare.', NULL)")
mycursor.execute("INSERT IGNORE INTO Department VALUES(2, 'Clothes', 'Clothes for women, men and kids', 1)")
mycursor.execute("INSERT IGNORE INTO Department VALUES(3, 'Woman', 'Clothes for women', 2)")
mycursor.execute("INSERT IGNORE INTO Department VALUES(4, 'Men', 'Clothes for men', 2)")
mycursor.execute("INSERT IGNORE INTO Department VALUES(5, 'Kids', 'Clothes for kids', 2)")

mycursor.execute("INSERT IGNORE INTO Department VALUES(6, 'Skincare', 'Skincare for all types of skin', 1)")
mycursor.execute("INSERT IGNORE INTO Department VALUES(7, 'Face', 'Skincare for the face', 6)")
mycursor.execute("INSERT IGNORE INTO Department VALUES(8, 'Body', 'Skincare for the body', 6)")
mycursor.execute("INSERT IGNORE INTO Department VALUES(9, 'Sun products', 'Skincare when it is sunny', 6)")

#products
#(id, title, description, product_price, tax, discount, stock, is_featured, department_id)
mycursor.execute("INSERT IGNORE INTO Product VALUES(1, 'Dress', 'Short blue dress', 100, 10, 20, 1000, TRUE, 3)")
mycursor.execute("INSERT IGNORE INTO Product VALUES(2, 'Jeans', 'Stretchy blue jeans', 99.90, 15.99, 0, 500, TRUE, 3)")
mycursor.execute("INSERT IGNORE INTO Product VALUES(3, 'Cardigan', 'Soft pink wool cardigan', 200, 19.90, 0, 100, TRUE, 3)")

mycursor.execute("INSERT IGNORE INTO Product VALUES(4, 'Jeans', 'Black jeans', 500, 10, 0, 50, TRUE, 4)")
mycursor.execute("INSERT IGNORE INTO Product VALUES(5, 'Shirt', 'Red cotton shirt', 1000, 50, 0, 0, FALSE, 4)")
mycursor.execute("INSERT IGNORE INTO Product VALUES(6, 'Shorts', 'Green and yellow cotton shorts', 600, 50, 60, 100, TRUE, 4)")

mycursor.execute("INSERT IGNORE INTO Product VALUES(7, 'Jeans', 'White jeans', 400, 40, 0, 50, FALSE, 5)")
mycursor.execute("INSERT IGNORE INTO Product VALUES(8, 'Skirt', 'Red skirt dotted in white', 300, 30, 0, 100, FALSE, 5)")

mycursor.execute("INSERT IGNORE INTO Product VALUES(9, 'Daycream', 'Daycream for oily skin', 150, 15, 0, 100, TRUE, 7)")
mycursor.execute("INSERT IGNORE INTO Product VALUES(10, 'Peeling', 'Peeling to help with dry skin', 100, 10, 0, 50, FALSE, 7)")

mycursor.execute("INSERT IGNORE INTO Product VALUES(11, 'Shower gel', 'Shower gel with shea butter', 150, 15, 50, 20, TRUE, 8)")
mycursor.execute("INSERT IGNORE INTO Product VALUES(12, 'Body lotion', 'Body lotion for everyday use', 400, 40, 0, 60, FALSE, 8)")

mycursor.execute("INSERT IGNORE INTO Product VALUES(13, 'Sun screen', 'Sun screen for everyday use', 100, 10, 0, 30, TRUE, 9)")

mycursor.execute("INSERT IGNORE INTO Product VALUES(14, 'Hej', 'Hej', 100, 10, 0, 30, TRUE, 9)")
mycursor.execute("INSERT IGNORE INTO Product VALUES(15, 'Hej', 'Hej', 100, 10, 0, 30, TRUE, 9)")
#users 
mycursor.execute("INSERT IGNORE INTO User VALUES('196501051122', 'Saga Andersson', '0722336776', 'saga_andersson@outlook.com', 'Bergsvägen 3 47887 Uppsala', '4g4s4nd3rsson', TRUE)")
mycursor.execute("INSERT IGNORE INTO User VALUES('197502104444', 'Bert Gustavsson', '0738439988', 'bert_gustavsson@outlook.com', 'Kroksgatan 10 99577 Stockholm', 'b3rtgust4vss0n', FALSE)")

#reviews 
mycursor.execute("INSERT IGNORE INTO Review VALUES ('196501051122', 1, 'I looove this dress. It is so soft and I use it several times a week! Best dress ever!!!', 5, '2024-10-02')")
mycursor.execute("INSERT IGNORE INTO Review VALUES ('197502104444', 1, 'I did not like this dress at all!! It was way too tiny. I had too wide shoulders to fit, not a good dress for a big strong man!', 5, '2024-10-02')")

#order
mycursor.execute("INSERT IGNORE INTO OrderUser VALUES (1, '2024-10-02', '2024-10-02', 'PAY12345', 123456, 1, '196501051122')")
mycursor.execute("INSERT IGNORE INTO Product_In_Order VALUES (1, 1, 2, 90)")
mycursor.execute("INSERT IGNORE INTO Product_In_Order VALUES (2, 1, 1, 115.89)")

#keywords 
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (1, 'dress')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (1, 'blue')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (1, 'short')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (1, 'woman')")

mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (2, 'jeans')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (2, 'slim')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (2, 'stretchy')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (2, 'blue')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (2, 'man')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (2, 'bottom')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (2, 'cotton')")

mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (3, 'cardigan')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (3, 'soft')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (3, 'pink')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (3, 'wool')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (3, 'knit')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (3, 'woman')")

mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (4, 'jeans')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (4, 'black')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (4, 'wide')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (4, 'woman')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (4, 'bottom')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (4, 'cotton')")

mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (5, 'shirt')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (5, 'red')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (5, 'cotton')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (5, 'man')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (5, 'top')")

mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (6, 'shorts')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (6, 'green')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (6, 'wellow')")  # Assuming 'wellow' was meant to be 'yellow'
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (6, 'multicolored')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (6, 'child')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (6, 'bottom')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (6, 'cotton')")

mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (7, 'woman')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (7, 'jeans')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (7, 'white')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (7, 'child')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (7, 'cotton')")

mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (8, 'skirt')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (8, 'bottom')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (8, 'red')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (8, 'white')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (8, 'dotted')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (8, 'woman')")

mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (9, 'daycream')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (9, 'oily skin')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (9, 'day')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (9, 'cream')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (9, 'face')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES (9, 'unisex')")

mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES(13, 'sun care')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES(13, 'body')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES(13, 'face')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES(13, 'unisex')")

mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES(12, 'body')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES(12, 'skincare')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES(12, 'all skintypes')")

mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES(11, 'body')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES(11, 'shower')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES(11, 'all skintypes')")

mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES(10, 'peeling')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES(10, 'dry skin')")

mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES(14, 'hej')")
mycursor.execute("INSERT IGNORE INTO Product_Keyword VALUES(15, 'hej')")


mycursor.execute("SELECT product_id FROM Product_Keyword WHERE keyword = 'all skintypes'")

mydb.commit() 

#home page descripition 
mycursor.execute("SELECT description FROM Department WHERE department_id = 1")
description = mycursor.fetchone() 

if description: 
    print(description[0])

#list of top level departments with field needed for the homepage 
mycursor.execute("SELECT title, description FROM Department WHERE parent_id = 1")
departments = mycursor.fetchall()

#top_level_departments = [f"{department[0]}: {department[1]}" for department in departments]
#print(top_level_departments)

#list of featured products with fields needed for the homepage 
mycursor.execute("SELECT title, description, product_price, tax, discount FROM Product WHERE is_featured = TRUE")
products = mycursor.fetchall() 
featured_products = [f"{product[0]}: {product[1]} for the price of {product[2]} euros including tax {product[3]} and discounting {product[4]} euros due to {product[0]} being on sale." for product in products]
[f"{product[0]}: {product[1]} for the price of {product[2]*(sum(1+product[3]))} euros including tax {product[3]} and discounting {product[4]} euros due to {product[0]} being on sale." for product in products]
#product_id with matching keyword 
mycursor.execute("SELECT DISTINCT product_id FROM Product_Keyword where keyword in (select keyword from Product_Keyword where product_id = 1) and product_id != 1")
products1 = mycursor.fetchall()
product_keyword = [product[0] for product in products1]

#Given a department, list of all its products (title, short description, current retail price) with their average rating
mycursor.execute("SELECT product_price + tax - discount AS retail_price FROM Product WHERE product_id=1")
retail_price = mycursor.fetchall() 
print(retail_price[0])
#mycursor.execute("SELECT title, description, ")


#deleting insertions 
# mycursor.execute("DELETE FROM Review")
# mycursor.execute("DELETE FROM Product_In_Order")
# mycursor.execute("DELETE FROM Product_Keyword")
# mycursor.execute("DELETE FROM Product")
# mycursor.execute("DELETE FROM OrderUser")
# mycursor.execute("DELETE FROM User")

#mycursor.execute("SELECT * FROM User")
#records = mycursor.fetchall()
#column_names = [desc[0] for desc in mycursor.description]
#print("Column names", column_names)

# print("Total number of rows in table: ", mycursor.rowcount)
# for row in records: 
#     print(row)



#entities: department, user, order, product, product_in_order, product_keyword, review

mydb.close()