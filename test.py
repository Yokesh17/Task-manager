import pymysql

# Database configuration
#generally its not a good practise to config db config like this, I have done as it is my local d
db_config = {
    'user': 'root',
    'password': 'yokesh2002',
    'host': 'localhost',
    'database': 'task_management',
    'port': '3306',
    'connection_timeout': 10  # Set a timeout for the connection
}

connection = pymysql.connect(user = 'root',host = 'localhost',passwd = 'yokesh2002',database = 'task_management')
print(connection)
print("Starting the database connection test...")

cursor = connection.cursor()

cursor.execute("SELECT VERSION()")
version = cursor.fetchone()
print("Database version:", version) 

cursor.close()
connection.close()


