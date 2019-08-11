
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


@app.route('/login', method=['GET','POST'])
def index():
    if request.POST.get('save','').strip():
        #get logins credentials
        username=request.POST.get('uname')
        password=request.POST.get('psw')
        #print(username)
        #print(password)
        #check if the user exist in the database
        result = db.execute("SELECT * FROM userlogin WHERE email= %s AND password =%s",(username,password))
       #if result is None:
        data =result.fetchall()
        if(len(data)==0):
            return "no user found"
        else:
            result = db.execute("SELECT * FROM userlogin WHERE email= %s AND password =%s",(username,password))
            for row in result:
                secretkey='tobereplaced'
                payload={'email':row['email'],'status':row['status'],'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}
                access_token = jwt.encode(payload,secretkey).decode('UTF-8')
                #return access_token
                
                #add and view users
                redirect("/listcustomers?token="+access_token)
                        
    else:
        return template('fontPageDesign')
    
   
def tokenrequired(f):
    #@wraps(f)
    def decorated(*args, **kwargs):
        token = request.query.token
        #token = request.headers.get("Authorization")
        
        if not token:
            abort(400, 'fail to get token')
        
        try:
            jwtsecret='tobereplaced'
            token_decoded = jwt.decode(token, jwtsecret)    # throw away value
        except jwt.ExpiredSignature:
            abort(401, "toke has expired")
        except jwt.DecodeError:
            abort(402, {'decoder error'})
       
        return f(*args, **kwargs)
    return decorated
        

@app.route('./static/<filename>')
def server_static():
    return static_file(filename,root='./')


@app.route('/listcustomers') 
#@tokenrequired
def listcustomers():
    
    return 'here is the list of customers'

@app.route('/registercustomers') 
@tokenrequired
def listcustomers():
    
    return 'register customer here'

@app.route('/registeruser', method=['POST']) 
def register():
    
    username = request.POST.get('username')
    password = request.POST.get('password')
    first_name = request.POST.get('fname')

    regPayload={
    "username":username,
    "password":password,
    "first_name":first_name
    }

    return regPayload




if __name__=='__main__':
    app.run(host='localhost', port=8080,debug = True)
    
#run(debug = True, reloader = True, host='localhost', port=8080)
#run(host='localhost', port=8080, debug='True', reloader='True')
