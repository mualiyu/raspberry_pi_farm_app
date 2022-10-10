import sqlite3
#connect to database file
dbconnect = sqlite3.connect("smartFarmDB");
#If we want to access columns by name we need to set
#row_factory to sqlite3.Row class
dbconnect.row_factory = sqlite3.Row;
#now we create a cursor to work with db
cursor = dbconnect.cursor();
#execute insetr statement
#cursor.execute('''insert into sensor values (1, 34.5, 10.2, 123)''');
#dbconnect.commit();
#execute simple select statement
cursor.execute('SELECT * FROM sensor');
#print data
for row in cursor:
    print(row['nodeId'],row['temperature'],row['humidity'],row['moisture'] );
#close the connection
dbconnect.close();
