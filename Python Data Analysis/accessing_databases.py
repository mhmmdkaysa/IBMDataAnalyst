# Writing codes using DB-API
from dmodule import connect

# Create connection object
connection = connect('databasename', 'username', 'pswd')

# Create a cursor object
cursor = connection.cursor()

# Run queries
cursor.execute('select * from mytable')
result = cursor.fetchall()

# Free resources
cursor.close()
connection.close()
