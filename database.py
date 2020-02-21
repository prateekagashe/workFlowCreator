import mysql.connector

credentials = {}

# Retrieving database credentials from dbCredentials.txt
with open("dbCredentials.txt") as file:
    for line in file:
        if not line.isspace():
            newLine = line.replace(" ", "")
            newLine = newLine.rstrip('\n')
            key = newLine.find('=')
            if key != -1:
                credentials[newLine[0:key]] = newLine[key+1:]
print(credentials)
# MySQL Connection
db = mysql.connector.connect(
    host=credentials['host'],
    database=credentials['database'],
    user=credentials['user'],
    passwd=credentials['password']
)
