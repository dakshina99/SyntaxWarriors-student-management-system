from flask import Flask,render_template,request,redirect
from flask.helpers import url_for
from flask_mysqldb import MySQL
import mysql.connector

app = Flask(__name__)

#Configure db
# db = yaml.load(open('db.yaml'))
# app.config['MYSQL_HOST'] = db['mysql_host']
# app.config['MYSQL_USER'] = db['mysql_user']
# app.config['MYSQL_PASSWORD'] = db['mysql_password']
# app.config['MYSQL_DB'] = db['mysql_db']

# app.config['MYSQL_DATABASE_USER'] = 'check'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'check'
# app.config['MYSQL_DATABASE_DB'] = 'student'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysqll = MySQL(app)

# @app.route('/',methods=['GET','POST'])
# def send():
#     if request.method == "POST":
#         email = request.form['staticEmail']
#         password = request.form['inputPassword']
#         return render_template('show.html',email=email,password=password)
#     return render_template('LoginPage.html')

# @app.route('/show')
# def show():
#     conn = mysql.connect()
#     cursor =conn.cursor()

#     cursor.execute("SELECT * from users")
#     data = cursor.fetchone()
#     return data

# @app.route('/', methods=['POST'])
# def my_form_post():
#     text = request.form['test']
#     processed_text = text.upper()
#     return processed_text

@app.route('/application',methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        cur = mysqll.connection.cursor()
        cur.execute("INSERT INTO users(name,email) VALUES(%s,%s)",(name,email))
        mysqll.connection.commit()
        cur.close()
        return "success"
    return render_template('Application.html')




class MySQLClient:

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = mysql.connector.connect(host = host,
             user = user,
             password = password,
             database = database,
             auth_plugin='mysql_native_password')

    def converByteStringToString(self,byteString):
        return byteString.decode("utf-8")

    # Queries for databases
    def showDatabases(self):
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute("SHOW DATABASES")
        return cursor.fetchall()

    def useDatabase(self,dbName):
        # Enter to database
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute("USE {}".format(dbName))
        print('Database entering is successful')

    def showTables(self,dbName):
        # Show tabales inside the database
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute('USE {}'.format(dbName))
        cursor.execute('SHOW TABLES')
        return cursor.fetchall()

    def readDataFromTable(self,dbName,tableName):
        # Read data from a table
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute('SELECT * FROM {}.{}'.format(dbName,tableName))
        return cursor.fetchall()

dbObj = MySQLClient('localhost','root','','student')

#print(dbObj.readDataFromTable('student','users'))

@app.route('/',methods=['GET','POST'])
def login():
    global loggedIn
    loggedIn = False
    if request.method == "POST":
        if not(loggedIn):
            loggedIn = True
            username = request.form['username']
            password = request.form['password']
            for rows in dbObj.readDataFromTable('student','users'):
                if rows[1]==username and rows[2]==password:
                    if rows[3]==1:
                        return render_template('SDashboard.html')
                    else:
                        return render_template('LDashboard.html')
        else:
            return render_template('Index.html')
        return render_template('show.html',username=username,password=password)
    return render_template('Index.html')

@app.route('/logout')
def logout():
    global loggedIn
    loggedIn = False
    render_template('Index.html')


if __name__ == "__main__":
    app.run(debug=True)