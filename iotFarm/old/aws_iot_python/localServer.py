from flask import Flask
import json
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    #connect to database file
    dbconnect = sqlite3.connect("smartFarmDB");
    #If we want to access columns by name we need to set
    #row_factory to sqlite3.Row class
    dbconnect.row_factory = sqlite3.Row;
    #now we create a cursor to work with db
    cursor = dbconnect.cursor();
    cursor.execute('SELECT * FROM sensor LIMIT 10');
    #print data
    dataset=""
    for row in cursor:
        dataset = """
        <tr>
           <td>"""+row['nodeId']+"""</td>
           <td>"""+row['temperature']+"""</td>
           <td>"""+row['humidity']+"""</td>
           <td>"""+row['moisture']+"""</td>
        </tr>"""
        print(row['nodeId'],row['temperature'],row['humidity'],row['moisture'] );
    dbconnect.close()
    return """<h1>Sensor Data</h1>
<table>
    <tr>
       <th>Node ID</th>
       <th>Temperature</th>
       <th>Humidity</th>
       <th>Moisture</th>
    </tr>"""+dataset+"""
    
</table>"""
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
    
        
