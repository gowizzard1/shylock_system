from bottle import Bottle,route, run, template,static_file,request,get,post,abort,redirect
import jwt
import datetime
import json
from functools import wraps
from sqlalchemy import create_engine
app=Bottle()


#connect to a local database


db = create_engine('postgresql://postgres@localhost:5432/auth')
connection = db.connect()



if __name__=='__main__':
    app.run(host='localhost', port=8080,debug = True)
    
#run(debug = True, reloader = True, host='localhost', port=8080)
#run(host='localhost', port=8080, debug='True', reloader='True')
