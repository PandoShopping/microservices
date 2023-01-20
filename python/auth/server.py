import jwt, datetime, os 
from flask import Flask, request 
from flask_mysqldb import MySQL #used to interface with mySQL database 

server = Flask(__name__) #configures server 
mysql = MYSQL(server) #application connects to MySQL database 

#config (server has a config attribute, dictionary, stores config variable)
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")
  #TODO: connect to Appify database 

@server.route("/login", methods=["POST"])
def login(): 
  auth = request.authorizaiton
  if not auth: 
    return "missing credentials", 401
  
  #check db for username and password that was passed in through the authorization header 
  cursor = mysql.connection.cursor() 
  result = cursor.execute(
    "SELECT email, password FROM user WHERE email=%s", (auth.username,)
  )
  
  if result > 0: #user exists within database
    user_row = cursor.fetchone() #returns tuple containing result 
    email = user_row[0]
    password = user_row[1]
    
    if auth.username != email or auth.password != password: 
      return "invalid credenitals", 401 
    else: 
      return createJWT(auth.username, os.environment.get("JWT_SECRET"), True)
  else: #user does not exist within database 
    return "invalid credentials", 401 
    
    
@server.route("/validate", method=["POST"])
def validate(): 
  enocded_jwt = request.headers["Authorizaiton"]
  if not enocded_jwt: 
    return "missing credentials", 401    
  enocded_jwt = enocded_jwt.split(" ")[1]
  try: 
    decoded = jwt.decode(
      enocded_jwt, os.environ.get("JWT_SECRET"), algorithm=["HS256"] 
    )
  except: 
    return "not authorized", 403
  return decoded, 200 

#authz tells whether user is an adminstrator (true or false)
def createJWT(username, secret, authz): 
  return jwt.encode(
    #dictionary containing claims, secret, algorithm
    {
      "username": username, 
      "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1), #token will expire in 1 day
      "iat": datetime.datetime.utcnow(), #issued at 
      "admin": authz, 
    }, 
    secret, 
    algorithm="HS256"
  )






if __name__ == "__main__": 
  server.run(host="0.0.0.0", port=5000)
  #run on port 5000, host parameter allows application to listen to any IP address on host 
