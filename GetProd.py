from flask import Flask,jsonify
from flask_restful import Resource, Api
from mysql.connector import MySQLConnection, Error
from flask_httpauth import HTTPBasicAuth

from flaskext.mysql import MySQL
from decimal import Decimal
import flask.json
import json

from pymongo import MongoClient
con = MongoClient('localhost', 27017)
db = con.myretaildb

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

@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password

#def userauth(username,pass):
    

class GetProd(Resource):
    @auth.login_required
    def get(self,id):
        #cursor = mysql.connect().cursor()

            #Access the testdb database and the emp collection.
            db = con.myretaildb.prod

            doc=db.find_one({'id':id})

            #Read data from NoSQL
            if not doc:
                data = [{'Error' : 'Price not found'}]
                return jsonify({'Error':data})
            else:
                price_data = doc.get('price')
                       
                cnx = mysql.connect()
                
                cursor = cnx.cursor()
                
                try:
                    sql = "SELECT id,name, '" + price_data + "' as price,description, curcode FROM store WHERE id = " + id
                    #sql = "SELECT id,name,price,curcode FROM store WHERE id = %s"
                    print(sql)
                    cursor.execute(sql)
                    row = [dict((cursor.description[i][0], value)
                            for i, value in enumerate(row)) for row in cursor.fetchall()]
                    if row:
                        return jsonify({'Product':row}) #-- working
                    else:
                        data = [{'Error' : 'No records found'}]
                        return jsonify({'Error':data}) #-- working
                except Error, e:
                    try:
                        return jsonify({'Error':e.args[1]})
                    except DatabaseError:
                        return jsonify({'Error':str(e)})
                    except OperationalError, e:
                        return jsonify({'Error':e})
              
    
api.add_resource(GetProd, '/getprod/<id>') # Route_1

if __name__ == '__main__':
    app.run()
cursor.close()
#disconnect from server
db.close()
