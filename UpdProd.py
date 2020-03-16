from flask import Flask,jsonify
from flask_restful import Resource, Api
from mysql.connector import MySQLConnection, Error
from flask_httpauth import HTTPBasicAuth

from flaskext.mysql import MySQL
from decimal import Decimal
import flask.json
from pymongo import MongoClient
con = MongoClient('localhost', 27017)
db = con.myretaildb

#Access the testdb database and the emp collection.
db = con.myretaildb.prod


app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

USER_DATA = {
    "admin": "SuperSecretPwd"
}

mysql = MySQL()

#MySQL connections
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Seem1Kums'
app.config['MYSQL_DATABASE_DB'] = 'myRetail'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

@app.route("/")
#@app.route("/", methods=['POST'])

#@auth.verify_password
#def verify(username, password):
#    if not (username and password):
#        return False
#    return USER_DATA.get(username) == password

class UpdProd(Resource):
#    @auth.login_required
    def get(self,id,price,desc):
        cnx = mysql.connect()
        cursor = cnx.cursor()

        db.update_one(
        {"id": id},
            {
            "$set": {
            "price":price
            }
            }
        )
        
        cursor.execute("UPDATE store SET description=%s WHERE id = %s", (desc,int(id)))
        cnx.commit()
        return jsonify({'Product Updates:':'Successful'}) #-- working
'''
        try:
            cursor.execute("SELECT id,name,price,curcode FROM store WHERE id = '%d'" %int(id)) 
            row = [dict((cursor.description[i][0], value)
                    for i, value in enumerate(row)) for row in cursor.fetchall()]
            if row:
                for i, s in enumerate(row): getprice = row["price"]
                if getprice == price:
                    return jsonify({'Product details':row}) #-- working
                else:
                    return jsonify({'Product details':'No records found'}) #-- working
        except Error, e:
            try:
                return jsonify({'Error details':e.args[1]})
            except DatabaseError:
                return jsonify({'Error details':str(e)})
            except OperationalError, e:
                return jsonify({'Error details':e})

'''


        
        
        
api.add_resource(UpdProd, '/updprod/<id>/<price>/<desc>') # Route_3
        
if __name__ == '__main__':
    app.run(port='5002')
cursor.close()
cnx.close()
#disconnect from server
#db.close()
